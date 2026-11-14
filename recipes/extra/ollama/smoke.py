#!/usr/bin/env python3
"""Opt-in installed-package Vulkan inference test. Downloads a small test model.

Uses only a temporary loopback server, HOME, and model directory; it does not
register a service or use the user's Ollama configuration/model store.
Requires Python, Mesa RADV, vulkan-loader, ca-certs, and access to /dev/dri.
"""
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request


def main():
    subprocess.run(["/usr/bin/ollama", "--version"], check=True)
    subprocess.run(["/usr/lib/ollama/llama-server", "--version"], check=True)
    assert Path("/usr/lib/ollama/vulkan/libggml-vulkan.so").is_file()
    icd = "/usr/share/vulkan/icd.d/radeon_icd.x86_64.json"
    assert Path(icd).is_file(), "RADV ICD missing"
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix="ollama-smoke-") as work:
        env = dict(os.environ, HOME=work, OLLAMA_MODELS=work + "/models",
                   OLLAMA_HOST=f"127.0.0.1:{port}", OLLAMA_DEBUG="1",
                   OLLAMA_VULKAN="1", VK_DRIVER_FILES=icd,
                   GGML_VK_VISIBLE_DEVICES="0", OLLAMA_NUM_PARALLEL="1",
                   OLLAMA_MAX_LOADED_MODELS="1", OLLAMA_CONTEXT_LENGTH="512")
        logpath = Path(work, "server.log")
        with logpath.open("w") as log:
            server = subprocess.Popen(["/usr/bin/ollama", "serve"], env=env,
                                      stdout=log, stderr=subprocess.STDOUT,
                                      start_new_session=True)
            base = f"http://127.0.0.1:{port}"
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

            def api(path, payload=None, timeout=300):
                body = None if payload is None else json.dumps(payload).encode()
                request = urllib.request.Request(base + path, data=body,
                                                  headers={"Content-Type": "application/json"})
                with opener.open(request, timeout=timeout) as response:
                    return json.load(response)

            try:
                for _ in range(120):
                    if server.poll() is not None:
                        raise RuntimeError("Ollama server exited during startup")
                    try:
                        api("/api/version", timeout=1)
                        break
                    except (urllib.error.URLError, TimeoutError):
                        time.sleep(0.5)
                else:
                    raise RuntimeError("Ollama startup timed out")
                model = "smollm2:135m"
                pulled = api("/api/pull", {"model": model, "stream": False}, timeout=600)
                assert pulled.get("status") == "success", pulled
                result = api("/api/generate", {
                    "model": model, "prompt": "Reply with one word: hello",
                    "stream": False, "keep_alive": "2m",
                    "options": {"num_predict": 16, "num_ctx": 512,
                                "num_gpu": 999, "seed": 1, "temperature": 0},
                })
                assert result.get("done") and result.get("eval_count", 0) > 0, result
                assert result.get("response", "").strip(), result
                models = api("/api/ps").get("models", [])
                assert len(models) == 1, models
                loaded = models[0]
                assert loaded.get("size_vram", 0) > 0, "CPU fallback: " + repr(loaded)
                assert "vulkan" in logpath.read_text().lower(), "No Vulkan backend evidence"
                seconds = result.get("eval_duration", 0) / 1e9
                print(json.dumps({
                    "model": model, "digest": loaded.get("digest"),
                    "size": loaded.get("size"), "size_vram": loaded.get("size_vram"),
                    "tokens": result["eval_count"],
                    "tokens_per_second": result["eval_count"] / seconds if seconds else None,
                    "response": result["response"],
                }, indent=2), flush=True)
                print("PASS: Vulkan GPU inference", flush=True)
            except BaseException:
                print(logpath.read_text()[-24000:], flush=True)
                raise
            finally:
                if server.poll() is None:
                    os.killpg(server.pid, signal.SIGTERM)
                    try:
                        server.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        os.killpg(server.pid, signal.SIGKILL)
                        server.wait(timeout=15)


if __name__ == "__main__":
    main()

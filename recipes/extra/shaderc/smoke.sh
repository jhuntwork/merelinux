#!/bin/sh
# Installed-package test: no GPU, network, or host modifications required.
set -eu
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT HUP INT TERM

glslc --version
pkg-config --modversion shaderc
glslc --target-env=vulkan1.2 -O -fshader-stage=compute \
    /usr/share/shaderc/tests/compute.comp -o "$work/compute.spv"
spirv-val --target-env vulkan1.2 "$work/compute.spv"
spirv-dis "$work/compute.spv" -o "$work/compute.spvasm"
grep -q 'OpEntryPoint GLCompute' "$work/compute.spvasm"
grep -q 'OpStore' "$work/compute.spvasm"
printf 'not a shader\n' > "$work/invalid.comp"
if glslc "$work/invalid.comp" -o "$work/invalid.spv" > "$work/invalid.log" 2>&1; then
    printf 'ERROR: glslc accepted invalid GLSL\n' >&2
    exit 1
fi

# Also check the installed headers, shared API, and its transitive linkage.
cat > "$work/consumer.cc" <<'EOF'
#include <shaderc/shaderc.h>
#include <cstring>
int main() {
    const char* source = "#version 450\nlayout(local_size_x=1) in; void main() {}\n";
    shaderc_compiler_t compiler = shaderc_compiler_initialize();
    if (!compiler) return 1;
    shaderc_compilation_result_t result = shaderc_compile_into_spv(
        compiler, source, std::strlen(source), shaderc_compute_shader,
        "consumer.comp", "main", nullptr);
    int failed = !result ||
        shaderc_result_get_compilation_status(result) != shaderc_compilation_status_success ||
        shaderc_result_get_length(result) < 20;
    if (result) shaderc_result_release(result);
    shaderc_compiler_release(compiler);
    return failed;
}
EOF
clang++ "$work/consumer.cc" $(pkg-config --cflags --libs shaderc) -o "$work/consumer"
"$work/consumer"
printf 'PASS: optimized compute SPIR-V validated; invalid GLSL rejected; shared API consumer compiled and ran\n'

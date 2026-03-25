FROM alpine AS init

ARG VERSION
ARG TARGETARCH

RUN ARCH=$(case "${TARGETARCH}" in amd64) echo x86_64;; arm64) echo aarch64;; *) echo "${TARGETARCH}";; esac) && \
    wget https://codeberg.org/merelinux/mere/releases/download/v${VERSION}/mere-${VERSION}-linux-${ARCH} -O /usr/local/bin/mere && \
    chmod +x /usr/local/bin/mere
RUN mere init
RUN wget http://pkgs.merelinux.org/mere.pub -O /mere/keys/mere.pub
RUN printf 'repo "core" {\n    url "http://pkgs.merelinux.org/core/new"\n    priority 100\n    trusted-fingerprints "eb3877e48560eaa832db2901e6b6ed36798d49831c76ffb66a2eb20010611265"\n}\n' > /mere/config.kdl
RUN mere install busybox ca-certs

FROM scratch

COPY --from=init /mere /mere
COPY --from=init /usr/local/bin/mere /usr/local/bin/mere
COPY --from=init /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

RUN ["/usr/local/bin/mere", "init", "--system"]
RUN ["/mere/profiles/system/current/bin/rm", "-rf", "/mere/cache/packages", "/mere/cache/repos"]

CMD ["/bin/sh"]

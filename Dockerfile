FROM alpine AS init

ARG VERSION
ARG TARGETARCH

RUN ARCH="$(case "${TARGETARCH}" in amd64) echo x86_64;; arm64) echo aarch64;; *) echo "${TARGETARCH}";; esac)" && \
    wget https://codeberg.org/merelinux/mere/releases/download/v${VERSION}/mere-${VERSION}-linux-${ARCH} -O /usr/local/bin/mere && \
    chmod +x /usr/local/bin/mere
RUN mere store init
RUN wget https://pkgs.merelinux.org/mere.pub -O /mere/keys/mere.pub
RUN wget https://pkgs.merelinux.org/config.kdl -O /mere/config.kdl
RUN mere install busybox ca-certs

FROM scratch

COPY --from=init /mere /mere
COPY --from=init /usr/local/bin/mere /usr/local/bin/mere
COPY --from=init /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

RUN ["/usr/local/bin/mere", "store", "init", "--system"]
RUN ["/mere/profiles/system/current/bin/rm", "-rf", "/mere/cache/packages", "/mere/cache/repos"]

CMD ["/bin/sh"]

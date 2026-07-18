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

# Create system layout: directories and symlinks exposing the active
# system profile at standard paths (replaces the removed --system flag).
RUN ["/mere/profiles/system/current/bin/busybox", "sh", "-c", "\
  BB=/mere/profiles/system/current/bin/busybox && \
  $BB mkdir -p /etc /tmp /usr && $BB chmod 1777 /tmp && \
  $BB ln -s /mere/profiles/system/current/bin /bin && \
  $BB ln -s /mere/profiles/system/current/lib /lib && \
  $BB ln -s /mere/profiles/system/current/sbin /sbin && \
  $BB ln -s /mere/profiles/system/current/usr/bin /usr/bin && \
  $BB ln -s /mere/profiles/system/current/usr/include /usr/include && \
  $BB ln -s /mere/profiles/system/current/usr/lib /usr/lib && \
  $BB ln -s /mere/profiles/system/current/usr/libexec /usr/libexec && \
  $BB ln -s /mere/profiles/system/current/usr/sbin /usr/sbin && \
  $BB ln -s /mere/profiles/system/current/usr/share /usr/share && \
  $BB rm -rf /mere/cache/packages /mere/cache/repos"]

CMD ["/bin/sh"]

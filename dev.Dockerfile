FROM mere/base

COPY packages/pacman/pacman-dev.conf /etc/pacman.conf
COPY scripts/build-in-docker.sh /local/bin

RUN install -d /mere/pkgs && \
    touch /mere/pkgs/buildlocal.db && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm build-essential && \
    chmod +x /local/bin/build-in-docker.sh && \
    find /var/cache/pacman -not -type d -delete

WORKDIR /src

CMD ["/bin/sh"]

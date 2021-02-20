FROM mere/base

COPY packages/pacman/pacman-dev.conf /etc/pacman.conf

RUN install -d /mere/pkgs && \
    touch /mere/pkgs/buildlocal.db && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm build-essential && \
    find /var/cache/pacman -not -type d -delete

WORKDIR /src

CMD ["/bin/sh"]

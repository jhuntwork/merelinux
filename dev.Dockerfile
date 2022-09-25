FROM mere/base

COPY packages/pacman/pacman-dev.conf /etc/pacman.conf

RUN install -d /mere/pkgs && \
    touch /mere/pkgs/buildlocal.db && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm build-base pacman-build perl && \
    rm -rf /var/lib/pacman/sync && \
    find /var/cache/pacman -not -type d -delete

CMD ["/bin/sh"]

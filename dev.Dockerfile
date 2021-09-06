FROM mere/base

RUN rm -f /usr/local && chmod 755 /usr

COPY packages/pacman/pacman-dev.conf /etc/pacman.conf

RUN install -d /mere/pkgs && \
    touch /mere/pkgs/buildlocal.db && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm base-layout busybox build-base pacman-build sudo && \
    rm -rf /var/lib/pacman/sync && \
    printf 'merebuild ALL=(ALL) NOPASSWD: ALL\n' >>/etc/sudoers && \
    find /var/cache/pacman -not -type d -delete

WORKDIR /src

CMD ["/bin/sh"]

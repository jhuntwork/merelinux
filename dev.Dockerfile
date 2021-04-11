FROM mere/base

RUN rm -f /usr/local && chmod 755 /usr

COPY packages/pacman/pacman-dev.conf /etc/pacman.conf
COPY scripts/build-in-docker.sh /usr/local/bin/build-in-docker.sh

RUN install -d /mere/pkgs && \
    touch /mere/pkgs/buildlocal.db && \
    pacman -Syu --noconfirm && \
    pacman -Sy --noconfirm build-essential sudo && \
    chmod +x /usr/local/bin/build-in-docker.sh && \
    rm -rf /var/lib/pacman/sync && \
    printf 'merebuild ALL=(ALL) NOPASSWD: ALL\n' >>/etc/sudoers && \
    find /var/cache/pacman -not -type d -delete

WORKDIR /src

CMD ["/bin/sh"]

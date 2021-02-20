FROM mere/base

RUN pacman -Syu --noconfirm && \
    find /var/cache/pacman -not -type d -delete

CMD ["/bin/sh"]

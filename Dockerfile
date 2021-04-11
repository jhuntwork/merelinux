FROM scratch as build

ADD busybox-1.32.1-4-x86_64.pkg.tar.xz \
    pacman-5.2.2-2-x86_64.pkg.tar.xz \
    /

RUN install -d /tmp/system/var/lib/pacman && \
    pacman -r /tmp/system -Sy base-layout busybox pacman --noconfirm && \
    rm -rf /tmp/system/var/cache/pacman/pkg/*

FROM scratch

COPY --from=build /tmp/system /

CMD ["/bin/sh"]

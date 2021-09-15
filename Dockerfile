FROM mere/base as build

RUN install -d /tmp/system/var/lib/pacman
RUN pacman -r /tmp/system -Sy base-layout busybox pacman --noconfirm
RUN rm /tmp/system/etc/services \
       /tmp/system/etc/protocols \
       /tmp/system/etc/pacman.conf.example \
       /tmp/system/usr/bin/pacman-conf

FROM scratch

COPY --from=build /tmp/system /

CMD ["/bin/sh"]

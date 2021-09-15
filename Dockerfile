FROM mere/base as build

ENV BL_VRS=2.0.5-1
ENV BB_VRS=1.33.1-5
ENV PM_VRS=6.0.1-3

RUN install -d /tmp/system/var/lib/pacman
RUN pacman -r /tmp/system -Sy \
        base-layout=${BL_VRS} busybox=${BB_VRS} pacman=${PM_VRS} --noconfirm
RUN rm /tmp/system/etc/services \
       /tmp/system/etc/protocols \
       /tmp/system/etc/pacman.conf.example \
       /tmp/system/usr/bin/pacman-conf

FROM scratch

COPY --from=build /tmp/system /

CMD ["/bin/sh"]

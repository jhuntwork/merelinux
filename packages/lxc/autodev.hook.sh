#!/bin/sh +xe
ln -sf /proc/self/fd/0 "${LXC_ROOTFS_MOUNT}/dev/tty"

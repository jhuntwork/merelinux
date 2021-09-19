# Installing Mere Linux

The process for installing Mere Linux to a machine is still fairly manual, but
we've tried to make it simple. There are three main methods for installation.

- [Installing Mere Linux](#installing-mere-linux)
  - [Using the Mere Linux ISO Image](#using-the-mere-linux-iso-image)
    - [Set up a disk for legacy booting](#set-up-a-disk-for-legacy-booting)
    - [Set up a disk for EFI booting](#set-up-a-disk-for-efi-booting)
    - [Installing the base system](#installing-the-base-system)
    - [Configure the boot loader for a legacy boot](#configure-the-boot-loader-for-a-legacy-boot)
    - [Configure the boot loader for an EFI boot](#configure-the-boot-loader-for-an-efi-boot)
  - [Using an existing Linux system](#using-an-existing-linux-system)
  - [Using the Mere Linux raw disk image](#using-the-mere-linux-raw-disk-image)

## Using the Mere Linux ISO Image

Current images can be found at
[https://pkgs.merelinux.org/images/](https://pkgs.merelinux.org/images/).

The Mere Linux ISO runs in a `tmpfs`, meaning you can change its contents like a
real system during your session, including adding or upgrading packages.
However, since it is all happening in memory, those changes will not persist
through a reboot.

The ISO will by default attempt to start a network device and retrieve an IP
address via DHCP. You can check that it has by running `ifconfig eth0`. A
working internet connection will be necessary in order to install any packages.

If you don't see your network device, probably the kernel module for your device
has not been built and included. Although we intend to support more hardware,
we are currently adding those in slowly. In this case, please run `lspci` and
add the output to a
[new Github issue](https://github.com/jhuntwork/merelinux/issues).

The ISO also includes the `dropbear` package to provide ssh access to the
`tmpfs` system, if you should wish. To use it, set a root password, and start
the service.

```sh
passwd
service start dropbear
```

### Set up a disk for legacy booting

Here is a _sample_ way to install Mere Linux from the running ISO. We'll assume
that the physical disk is called `/dev/sda`. Alternatively, if you want to use
EFI booting, skip to
[Set up a disk for EFI booting](#set-up-a-disk-for-efi-booting).

First, create a single partition, filling the entire disk. *Note: This will
erase the contents of the disk*

```sh
sgdisk -Z /dev/sda
sgdisk -N=1 -A 1:set:2 /dev/sda
```

Inspect the details of the created partition, and note the Partition unique
GUID.

```sh
sgdisk -i=1
# Grab the unique GUID - we'll need this later
partuuid=$(sgdisk -i=1 /dev/sda 2>&1 | grep unique | awk '{print $NF}')
```

Now format the new partition. Because we are using a single partition in this
example, we have to turn off ext4's 64bit support. You can avoid this by using
a separate boot partition.

```sh
mkfs.ext4 -O ^64bit /dev/sda1
```

Mount the new file system:

```sh
mount /dev/sda1 /mnt
```

Now skip ahead to [Installing the base system](#installing-the-base-system).

### Set up a disk for EFI booting

Assuming our disk is called `/dev/sda`, set up two partitions, one for for the
EFI boot partition, and one for the root partition. *Note: This will erase the
contents of the disk*

```sh
sgdisk -Z /dev/sda
sgdisk -n=1:0:100M /dev/sda
sgdisk -N=2 /dev/sda
```

Inspect the details of the created root partition, and note the Partition unique
GUID.

```sh
sgdisk -i=2
# Grab the unique GUID - we'll need this later
partuuid=$(sgdisk -i=2 /dev/sda 2>&1 | grep unique | awk '{print $NF}')
```

Format the partitions.

```sh
mkfs.vfat /dev/sda1
mkfs.ext4 /dev/sda2
```

Mount the partitions.

```sh
mount /dev/sda2 /mnt
mkdir /mnt/boot
mount /dev/sda1 /mnt/boot
```

### Installing the base system

First create the database directory `pacman` needs to run, then install the
base-layout and `busybox` packages. Although base-layout and `busybox` are both
part of the base group, we install them first separately because the other
packages need those to be present to correctly run some of their install hook
scripts.

```sh
mkdir -p /mnt/var/lib/pacman
pacman -Sy -r /mnt -b /mnt/var/lib/pacman base-layout busybox
```

Now install the rest of the packages in the base group. When prompted, choose
the default selection of 'all'.

```sh
pacman -Sy -r /mnt -b /mnt/var/lib/pacman --needed base
```

Change the root password in the installed system.

```sh
chroot /mnt passwd
```

Set the hostname for the system.

```sh
echo 'myhostname' >/mnt/etc/hostname
```

Tell the initial tty screen to clear itself:

```sh
clear >/mnt/etc/issue
```

Install a basic networking configuration.

```sh
cat >/mnt/etc/network/interfaces << EOF
auto lo eth0

iface lo inet loopback

iface eth0 inet dhcp
EOF

echo '127.0.0.1 localhost' >/mnt/etc/hosts
```

Add an initial `/etc/fstab` file.

```sh
cat > /mnt/etc/fstab << EOF
devpts /dev/pts devpts defaults 0 0
tmpfs  /dev/shm tmpfs  defaults 0 0
EOF
```

### Configure the boot loader for a legacy boot

If you set up your disks for EFI boot, skip to
[Configure the boot loader for an EFI boot](#configure-the-boot-loader-for-a-legacy-boot).

Create the configuration. *Make sure the `partuuid` variable is set to the GUID
of the filesystem we created earlier*.

```sh
mkdir -p /mnt/boot/extlinux
cat >/mnt/boot/extlinux/extlinux.conf <<EOF
DEFAULT mere
PROMPT 1
TIMEOUT 30

LABEL mere
  LINUX /boot/vmlinux
  APPEND root=PARTUUID=${partuuid} quiet
EOF
```

Install the bootloader and prepare the MBR.

```sh
extlinux -i /mnt/boot/extlinux
cat /usr/share/syslinux/gptmbr.bin >/dev/sda
```

At this point you should be able to unmount the volume and restart the machine.

```sh
umount /mnt
reboot
```

### Configure the boot loader for an EFI boot

Create the EFI directory and install `syslinux` to it

```sh
mkdir -p /mnt/boot/EFI/BOOT
cp /usr/share/syslinux/efi64/syslinux.efi /mnt/boot/EFI/BOOT/bootx64.efi
cp /usr/share/syslinux/efi64/ldlinux.e64 /mnt/boot/EFI/BOOT/
```

Create the `syslinux` configuration. *Make sure the `partuuid` variable is set
to the GUID of the filesystem we created earlier*.

```sh
cat >/mnt/boot/EFI/BOOT/syslinux.cfg << EOF
DEFAULT mere
PROMPT 1
TIMEOUT 30

LABEL mere
  LINUX ../../vmlinux
  APPEND root=PARTUUID=${partuuid} quiet
EOF
```

At this point you should be able to unmount the volume and restart the machine.

```sh
umount /mnt/boot
umount /mnt
reboot
```

## Using an existing Linux system

Assuming you already have a running Linux system with a spare disk or partition,
you can easily grab Mere's `pacman` package and install Mere to it. Setting up
the partitions and boot loader is left as an exercise to the reader, but you can
use the section
[Using the Mere Linux ISO Image](#using-the-mere-linux-iso-image) as a generic
guide. Note that Mere's kernel currently only supports ext2,3,4 filesystems, but
we are open to adding support for more as we mature. If you would like to use a
different file system, please create a
[new Github issue](https://github.com/jhuntwork/merelinux/issues).

First, download `pacman`.

```sh
curl -LO https://pkgs.merelinux.org/core/pacman-latest-x86_64.pkg.tar.xz
```

You can validate the file using the `pacman-latest.SHA512SUM` file.

```sh
curl -LO https://pkgs.merelinux.org/core/pacman-latest.SHA512SUM
sha512sum -c pacman-latest.SHA512SUM
```

Extract it to a temporary location.

```sh
mkdir -p /tmp/pacman
tar -C /tmp/pacman -xf pacman-latest-x86_64.pkg.tar.xz
```

Now you can use
`/tmp/pacman/usr/bin/pacman --config /tmp/pacman/etc/pacman.conf` to install the
system in the same way that is described under
[Installing the base system](#installing-the-base-system). Simply replace every
usage of `pacman` with
`/tmp/pacman/usr/bin/pacman --config /tmp/pacman/etc/pacman.conf`.

If you want to use Mere's `syslinux` package to boot the system, install that
package as well, either to a temporary location on the host system, or into the
destination system, and use one of the boot methods described in
[Configure the boot loader for a legacy boot](#configure-the-boot-loader-for-a-legacy-boot)
or
[Configure the boot-loader for an EFI boot](#configure-the-boot-loader-for-an-efi-boot).

## Using the Mere Linux raw disk image

There is a raw disk image created in essentially the same manner as described
above located at
[https://pkgs.merelinux.org/images/](https://pkgs.merelinux.org/images/).

There are a lot of ways that this image could be used, but it works really well
as a starting point for a virtual machine. It has been successfully used as a
Digital Ocean droplet and an Oracle Cloud instance. It should be usable in any
cloud provider that supports MBR booting and the `VIRTIO` kernel drivers.

To use it as a VirtualBox disk, you could do the following, resizing the disk
to the size you wish to use.

```sh
VBoxManage convertfromraw meredisk.raw meredisk.vdi
VBoxManage modifymedium disk meredisk.vdi --resize <megabytes>
```

Then simply attach it to a new Linux virtual machine. In the machine settings,
under Network->Advanced, be sure to set the Adapter Type to
`Paravirtualized Network (virtio-net)`. When the image boots, it will attempt to
resize the root file system to fill the entire disk space available.

Unlike the ISO, the disk image has a default password set to `merepass`. Be sure
to change it if you deploy it anywhere.

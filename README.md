# Gnome-Software-Snap-RPM
Make snap into gnome-software on RHEL

# Support
aarch64 - arm64
x86_64 - x64
x86_64_v2 - x64 (Support x86-64-v2)

# Setup
1 \
install epel 

if your system is Red Hat Enterprise Linux \
run:

subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms && dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm

if your system is centOS Stream / Rocky Linux / AlmaLinux \
run:

dnf config-manager --set-enabled crb && dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm

2 \
install snapd
run:

sudo yum install snapd && sudo systemctl enable --now snapd.socket && sudo ln -s /var/lib/snapd/snap /snap

3 \
install gnome-software and gnome-software-fedora-langpacks

4 \
open Flathub
run:

flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

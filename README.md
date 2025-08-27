# Gnome-Software-Snap-RHEL
Make snap into gnome-software on RHEL

![473796292-93fe3577-03be-440c-83f5-7c865c01743](https://github.com/user-attachments/assets/fd42d8a5-19be-4a02-9d1e-4b0bab742acb)

# Support
- aarch64 → arm64
- x86_64 → x64 (Required x86-64-v3 and above)
- x86_64_v2 → x64 (Support x86-64-v2)

# Setup

### 1. Install EPEL

**If your system is Red Hat Enterprise Linux**
```bash
subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms && \
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
```

**If your system is CentOS Stream / Rocky Linux / AlmaLinux**
```bash
dnf config-manager --set-enabled crb && \
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
```

---

### 2. Install Snapd
```bash
sudo yum install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
```

---

### 3. Install GNOME Software and language packs
```bash
sudo dnf install gnome-software gnome-software-fedora-langpacks
```

---

### 4. Open Flathub
```bash
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

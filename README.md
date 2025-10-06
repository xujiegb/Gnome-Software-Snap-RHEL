# Gnome-Software-Snap-RHEL
Make snap into Gnome Software on RHEL\
令 RHEL 的 Gnome Software 支援 Snap

![473796292-93fe3577-03be-440c-83f5-7c865c01743](https://github.com/user-attachments/assets/fd42d8a5-19be-4a02-9d1e-4b0bab742acb)

# Branch 分支
- aarch64 → arm64
- x86_64 → x64 (Required x86-64-v3 and above)
- x86_64_v2 → x64 (Support x86-64-v2)

# Setup 安裝

### 1. Install EPEL
安装 EPEL

**If your system is Red Hat Enterprise Linux**
如果你的系統是 紅帽企業Linux
```bash
subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms && \
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
```

**If your system is CentOS Stream / Rocky Linux / AlmaLinux**
如果你的系統是 CentOS Stream / Rocky Linux / AlmaLinux
```bash
dnf config-manager --set-enabled crb && \
dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
```

---

### 2. Install Snapd
安裝 Snapd
```bash
sudo yum install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
```

---

### 3. Install GNOME Software and language packs
安装 GNOME Softwareand language packs
```bash
sudo dnf install gnome-software gnome-software-fedora-langpacks
```

---

### 4. Add Flathub
新增 Flathub
```bash
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

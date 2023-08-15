#!/bin/bash

set -eux

# Nouveau 絶対入れさせないマン
sudo sh -c "echo 'blacklist nouveau\noptions nouveau modeset=0' > /etc/modprobe.d/blacklist-nouveau.conf";
sudo update-initramfs -u;

# 確認した環境をこのスクリプトの前提条件として書いておく

if ! lspci | grep -i nvidia | grep -q 'rev a1'; then
    echo "Different GPU" > /dev/stderr;
    exit 1;
fi

# nvidia 何も入ってない
if dpkg -l | grep -q nvidia; then
    echo "Already installed nvidia's something" > /dev/stderr;
    exit 1;
fi

# cuda 何も入ってない
if dpkg -l | grep -q cuda; then
    echo "Already installed cuda's something" > /dev/stderr;
    exit 1;
fi

# driver を調べる
sudo apt install ubuntu-drivers-common -y;

# 535 で行ってみる
if ! ubuntu-drivers devices | grep -q nvidia-driver-535; then
    echo "Can't use nvidia-driver-535"  > /dev/stderr;
    exit 1
fi

sudo apt install nvidia-driver-535 -y

sudo reboot


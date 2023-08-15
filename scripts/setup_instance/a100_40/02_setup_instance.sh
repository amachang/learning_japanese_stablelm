#!/bin/bash

set -eux

# repo の設定
sudo wget -O /etc/apt/preferences.d/cuda-repository-pin-600 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin;
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub;
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /";
sudo apt update

# ここで依存関係を組み立て直す。 cuda の repo が増えて依存関係の再構築をしなければならないところがあるので　
sudo apt --fix-broken install -y

# 念の為
sudo apt upgrade -y

# cuda のインストール
sudo apt install cuda-11-8 -y

# パスをちゃんと通しておかないと pip とかで入れられたやつとかとぐちゃぐちゃになるイメージがあるのでちゃんと書いておく
echo 'export CUDA_PATH=/usr/local/cuda-11.8' >> ~/.bashrc;
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc;
echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc;

sudo update-initramfs -u
sudo reboot


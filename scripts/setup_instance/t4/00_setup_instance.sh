#!/bin/bash

set -eu

if ! lsb_release -r | grep -q "22.04"; then
    echo "Error: This script requires Ubuntu 22.04. Please use Ubuntu 22.04 and try again."
    exit 1
fi

# 諸々のアップグレード
sudo apt update
sudo apt upgrade -y

# 朝 6 時に起動してたら必ず終了する（お金がもったいないので）
sudo timedatectl set-timezone Asia/Tokyo
sudo sh -c 'crontab -l > /tmp/current_cron' || : # ignore error
sudo sh -c 'echo "0 6 * * * /sbin/shutdown -h now" >> /tmp/current_cron'
sudo crontab /tmp/current_cron
sudo systemctl restart cron
sudo rm /tmp/current_cron

# 再起動
sudo reboot

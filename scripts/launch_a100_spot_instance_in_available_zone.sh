#!/bin/bash

set -eux

launch_instance() {
    zone="$1"

    # 長いコマンドなので wrap した
    gcloud compute instances create stablelm \
        --zone="$zone" \
        --machine-type=a2-highgpu-1g \
        --accelerator=count=1,type=nvidia-tesla-a100 \
        --provisioning-model=SPOT \
        --create-disk=auto-delete=yes,boot=yes,device-name=stablelm,image=projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20230727,mode=rw,size=100,type=pd-ssd
}

launch_instance_in_available_zone() {
    zones="$1"

    for zone in $zones; do
        echo "Trying to launch instance in zone $zone..."
        
        # 起動できたら 0 を返して終了
        if launch_instance "$zone"; then
            echo "Instance launched successfully in zone $zone."
            return 0
        fi
    done

    # 失敗なら 1 を返す
    return 1
}

# 日本のインスタンスを確認
japan_zones="$(gcloud compute accelerator-types list --filter="name=nvidia-tesla-a100" --format="value(zone)" | grep "asia-northeast")"
if launch_instance_in_available_zone "$japan_zones"; then
    echo "Successfully launched instance in Japan zone."
    exit 0
fi

# アジアのインスタンスを確認
asia_zones="$(gcloud compute accelerator-types list --filter="name=nvidia-tesla-a100" --format="value(zone)" | grep "asia" | grep -v "asia-northeast")"
if launch_instance_in_available_zone "$asia_zones"; then
    echo "Successfully launched instance in Asia zone."
    exit 0
fi

# 他のインスタンスを確認
other_zones="$(gcloud compute accelerator-types list --filter="name=nvidia-tesla-a100" --format="value(zone)" | grep -v "asia")"
if launch_instance_in_available_zone "$other_zones"; then
    echo "Successfully launched instance in non-Asia zone."
    exit 0
fi

echo "Failed to create instance in all zones."
exit 1


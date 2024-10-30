#!/bin/bash

DEVICE=$(getprop ro.product.vendor.device)

if [[ "$DEVICE" == "r8s" || "$DEVICE" == "c1s" ]]; then
    sleep 0.5
    if [ -e /sys/devices/virtual/camera/flash/rear_flash ]; then
        sudo chown phablet /sys/devices/virtual/camera/flash/rear_flash
    fi
fi

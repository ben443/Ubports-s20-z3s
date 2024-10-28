#!/bin/bash

DEVICE=$(getprop ro.product.vendor.device)

if [ "$DEVICE" == "r8s" ]; then
    sleep 0.5
    if [ -e /sys/class/camera/rear_flash ]; then
        sudo chown phablet /sys/class/camera/rear_flash
    fi
elif [ "$DEVICE" == "c1s" ]; then
    sleep 0.5
    if [ -e /sys/class/camera/rear_flash ]; then
        sudo chown phablet /sys/class/camera/rear_flash
    fi
fi

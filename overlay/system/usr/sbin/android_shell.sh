#!/bin/bash

if [ -z "$1" ]; then
    exit 1
fi

CMD="$@"

sudo bash -c "LD_PRELOAD='' LD_LIBRARY_PATH='/system/lib64:/vendor/lib64' lxc-attach -n android -- $CMD"

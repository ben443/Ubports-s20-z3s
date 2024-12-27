### Power saving

Currently when the screen is on, aidl powerhal on the halium vendor is instructed to enable `SUSTAINED_PERFORMANCE` + `EXPENSIVE_RENDERING`, while it enables `LOW_POWER` when the screen is off. Clock speeds are raised during that combo to improve responsiveness, and the scheduler will have access to all 4 big cores during instead of 2 in `LOW_POWER` mode.

To always stay in `LOW_POWER` mode, create an empty file at `/home/phablet/.config/power_saving`, one can do that in terminal with `touch /home/phablet/.config/power_saving`. The change is applied the next screen wake.

Slightly dangerous, but advanced users can also adjust power hints at `/home/phablet/.config/config_hyper_permission.json`, `config_chipset.json`, `config_vendor.json` then reboot.

Optionally network power saving can be enabled, which only allows internet to be on for 30 seconds every 9 and a half minutes when screen is off. With https://gitlab.com/ubports/development/core/repowerd/-/merge_requests/74 merged it can detect whether any app or the system is instructing the device to stay awake and not disable networking during that.

To enable network power saving, create an empty file at `/home/phablet/.config/network_power_saving`, one can do that in terminal with `touch /home/phablet/.config/network_power_saving`. The change is applied the next screen off.

### Enable swap file

Currently zswap is enabled by default. If a swap file is also needed to have even more applications in the background, swapfile at `/userdata/SWAP.img` is auto mounted during boot.

This will never be the default since the usage of swap file could rapidly degrade flash storage lifespan. Do that at your own risk.

```
# allocating 2GiB of swap
sudo fallocate /userdata/SWAP.img -l 2G
sudo chmod 600 /userdata/SWAP.img
sudo mkswap /userdata/SWAP.img
sudo reboot
```

https://gitlab.com/ubports/porting/community-ports/android11/samsung-galaxy-s7/samsung-exynos8890/-/blob/focal/tinker.md

# allow users to override aidl power config if they wish to
if ! ls /home/phablet/.config/config* >/dev/null 2>&1; then
    cp /vendor/etc/hyper/config_* /home/phablet/.config/
fi

chmod 644 /home/phablet/.config/config_*
chown root: /home/phablet/.config/config_*

for file in /home/phablet/.config/config_*; do
    filename=$(basename "$file")
    mount -o bind,ro "$file" "/vendor/etc/hyper/$filename"
done

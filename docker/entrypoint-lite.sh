#!/bin/sh
set -eu
# This image deliberately has no browser binaries or browser login modules.
export WEBUI_TWITCH_LOGIN=cookie-only
if [ "$(id -u)" -eq 0 ]; then
    case "$USER_ID:$GROUP_ID" in *[!0-9:]*|:*|*:) echo "USER_ID and GROUP_ID must be numeric" >&2; exit 1;; esac
    if [ "$USER_ID" -eq 0 ]; then echo "USER_ID must be nonzero" >&2; exit 1; fi
    mkdir -p config cache
    chown "$USER_ID:$GROUP_ID" /TwitchDropsMiner
    chown -R "$USER_ID:$GROUP_ID" config cache
    exec su-exec "$USER_ID:$GROUP_ID" /TwitchDropsMiner/TwitchDropsMiner --stdlog "$@"
fi
exec /TwitchDropsMiner/TwitchDropsMiner --stdlog "$@"

#!/usr/bin/env bash
set -euo pipefail

raw_base="${DOTFILES_SKILLS_RAW_BASE:-https://raw.githubusercontent.com/TarasPriadka/dotfiles/main}"
user_home="${DOTFILES_SKILLS_HOME:-$HOME}"
local_bin_dir="$user_home/.local/bin"
user_units_dir="$user_home/.config/systemd/user"
mkdir -p "$local_bin_dir" "$user_units_dir"

download_dir="$(mktemp -d)"
trap 'rm -rf -- "$download_dir"' EXIT
for file in sync.sh systemd/dotfiles-skills-sync.service systemd/dotfiles-skills-sync.timer; do
    curl -fsSL --retry 2 "$raw_base/skills/$file" -o "$download_dir/$(basename "$file")"
done
bash -n "$download_dir/sync.sh"

sync_command="$local_bin_dir/dotfiles-skills-sync"
if [ -L "$sync_command" ]; then
    if [ "$(readlink "$sync_command")" != "$user_home/code/dotfiles/skills/sync.sh" ]; then
        echo "Refusing to replace $sync_command: it points elsewhere" >&2
        exit 1
    fi
    rm -- "$sync_command"
fi
install -m 755 "$download_dir/sync.sh" "$sync_command"
install -m 644 "$download_dir/dotfiles-skills-sync.service" "$user_units_dir/"
install -m 644 "$download_dir/dotfiles-skills-sync.timer" "$user_units_dir/"

"$sync_command"
if command -v systemctl >/dev/null 2>&1; then
    if systemctl --user daemon-reload; then
        systemctl --user enable --now dotfiles-skills-sync.timer
        echo "Hourly personal skill updates enabled"
    else
        echo "Skills installed; user systemd is unavailable, so the timer was not enabled" >&2
    fi
else
    echo "Skills installed; systemd is unavailable, so the timer was not enabled" >&2
fi

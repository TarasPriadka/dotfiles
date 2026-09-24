#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="$HOME/.agents/skills"
user_units_dir="$HOME/.config/systemd/user"
local_bin_dir="$HOME/.local/bin"

mkdir -p "$skills_dir" "$user_units_dir" "$local_bin_dir"

for skill_dir in "$repo_root"/skills/*; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_link="$skills_dir/$(basename "$skill_dir")"
    if [ -L "$skill_link" ] && [ "$(readlink "$skill_link")" = "$skill_dir" ]; then
        continue
    fi
    if [ -e "$skill_link" ] || [ -L "$skill_link" ]; then
        echo "Skipping $skill_link: it already exists" >&2
        continue
    fi
    ln -s "$skill_dir" "$skill_link"
done

sync_link="$local_bin_dir/dotfiles-skills-sync"
if [ ! -e "$sync_link" ] && [ ! -L "$sync_link" ]; then
    ln -s "$repo_root/skills/sync.sh" "$sync_link"
elif [ ! -L "$sync_link" ] || [ "$(readlink "$sync_link")" != "$repo_root/skills/sync.sh" ]; then
    echo "Skipping $sync_link: it already exists" >&2
fi

cp "$repo_root/skills/systemd/dotfiles-skills-sync.service" "$user_units_dir/"
cp "$repo_root/skills/systemd/dotfiles-skills-sync.timer" "$user_units_dir/"

if command -v systemctl >/dev/null 2>&1; then
    if systemctl --user daemon-reload; then
        systemctl --user enable --now dotfiles-skills-sync.timer
        echo "Skill links and hourly update timer installed"
    else
        echo "Skill links installed; user systemd is unavailable, so the timer was not enabled" >&2
    fi
else
    echo "Skill links installed; systemd is unavailable, so the timer was not enabled" >&2
fi

#!/usr/bin/env bash
set -euo pipefail

archive_url="${DOTFILES_SKILLS_ARCHIVE_URL:-https://github.com/TarasPriadka/dotfiles/archive/refs/heads/main.tar.gz}"
user_home="${DOTFILES_SKILLS_HOME:-$HOME}"
cache_dir="$user_home/.local/share/dotfiles-skills"
skills_dir="$user_home/.agents/skills"
mkdir -p "$cache_dir/releases" "$skills_dir"

if [ -e "$cache_dir/current" ] && [ ! -L "$cache_dir/current" ]; then
    echo "Refusing to replace $cache_dir/current: it is not a symlink" >&2
    exit 1
fi

download_dir="$(mktemp -d)"
pending_release="$(mktemp -d "$cache_dir/releases/skillset.XXXXXXXX")"
next_link="$cache_dir/.current.next.$$"
cleanup() {
    rm -rf -- "$download_dir"
    if [ -n "$pending_release" ]; then
        rm -rf -- "$pending_release"
    fi
    rm -f -- "$next_link"
}
trap cleanup EXIT

curl -fsSL --retry 2 "$archive_url" -o "$download_dir/dotfiles.tar.gz"
tar -xzf "$download_dir/dotfiles.tar.gz" -C "$download_dir"
source_dir="$download_dir/dotfiles-main/skills"
if [ ! -d "$source_dir" ]; then
    echo "The downloaded archive has no skills directory" >&2
    exit 1
fi

skill_count=0
for skill_dir in "$source_dir"/*; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    cp -R "$skill_dir" "$pending_release/"
    skill_count=$((skill_count + 1))
done
if [ "$skill_count" -eq 0 ]; then
    echo "The downloaded archive has no skills" >&2
    exit 1
fi

old_release="$(readlink "$cache_dir/current" 2>/dev/null || true)"
ln -s "$pending_release" "$next_link"
mv -Tf -- "$next_link" "$cache_dir/current"
pending_release=""

for skill_dir in "$cache_dir/current"/*; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name="$(basename "$skill_dir")"
    skill_link="$skills_dir/$skill_name"
    managed_target="$cache_dir/current/$skill_name"
    old_checkout_target="$user_home/code/dotfiles/skills/$skill_name"
    if [ -L "$skill_link" ]; then
        existing_target="$(readlink "$skill_link")"
        if [ "$existing_target" = "$managed_target" ]; then
            continue
        fi
        if [ "$existing_target" = "$old_checkout_target" ]; then
            ln -sfn "$managed_target" "$skill_link"
            continue
        fi
    fi
    if [ -e "$skill_link" ] || [ -L "$skill_link" ]; then
        echo "Skipping $skill_link: it already exists" >&2
        continue
    fi
    ln -s "$managed_target" "$skill_link"
done

case "$old_release" in
    "$cache_dir"/releases/*)
        for old_skill_dir in "$old_release"/*; do
            [ -f "$old_skill_dir/SKILL.md" ] || continue
            skill_name="$(basename "$old_skill_dir")"
            if [ ! -e "$cache_dir/current/$skill_name/SKILL.md" ]; then
                skill_link="$skills_dir/$skill_name"
                if [ -L "$skill_link" ] &&
                    [ "$(readlink "$skill_link")" = "$cache_dir/current/$skill_name" ]; then
                    rm -- "$skill_link"
                fi
            fi
        done
        rm -rf -- "$old_release"
        ;;
esac

echo "Updated $skill_count personal Codex skill(s)"

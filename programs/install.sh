#!/usr/bin/env bash
set -euo pipefail

raw_base="${DOTFILES_PROGRAMS_RAW_BASE:-https://raw.githubusercontent.com/TarasPriadka/dotfiles/main}"
user_home="${DOTFILES_PROGRAMS_HOME:-$HOME}"
bin_dir="$user_home/.local/bin"

download_dir="$(mktemp -d)"
trap 'rm -rf -- "$download_dir"' EXIT

for program in night coin beach git-uncommit; do
    curl -fsSL --retry 2 "$raw_base/programs/$program" -o "$download_dir/$program"
    python3 -m py_compile "$download_dir/$program"
done

mkdir -p "$bin_dir"
for program in night coin beach git-uncommit; do
    install -m 755 "$download_dir/$program" "$bin_dir/$program"
done

# Resolve HOME when the alias runs, rather than embedding the installer's environment.
# shellcheck disable=SC2016
git config --file "$user_home/.gitconfig" alias.uncommit '!"$HOME/.local/bin/git-uncommit"'

echo "Installed night, coin, beach, and git-uncommit in $bin_dir"
echo "Updated git uncommit in $user_home/.gitconfig; other Git settings preserved."

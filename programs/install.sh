#!/usr/bin/env bash
set -euo pipefail

raw_base="${DOTFILES_PROGRAMS_RAW_BASE:-https://raw.githubusercontent.com/TarasPriadka/dotfiles/main}"
user_home="${DOTFILES_PROGRAMS_HOME:-$HOME}"
bin_dir="$user_home/.local/bin"

download_dir="$(mktemp -d)"
trap 'rm -rf -- "$download_dir"' EXIT

for program in night coin; do
    curl -fsSL --retry 2 "$raw_base/programs/$program" -o "$download_dir/$program"
    python3 -m py_compile "$download_dir/$program"
done

mkdir -p "$bin_dir"
for program in night coin; do
    install -m 755 "$download_dir/$program" "$bin_dir/$program"
done

echo "Installed night and coin in $bin_dir"

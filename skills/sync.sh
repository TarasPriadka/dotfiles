#!/usr/bin/env bash
set -euo pipefail

user_home="${DOTFILES_SKILLS_HOME:-$HOME}"
cache_dir="$user_home/.local/share/dotfiles-skills"
skills_dir="$user_home/.agents/skills"
mkdir -p "$cache_dir/releases" "$skills_dir"
archive_url="${DOTFILES_SKILLS_ARCHIVE_URL:-}"
if [ -z "$archive_url" ] && [ -f "$cache_dir/archive-url" ]; then
    IFS= read -r archive_url < "$cache_dir/archive-url"
fi
archive_url="${archive_url:-https://github.com/TarasPriadka/dotfiles/archive/refs/heads/main.tar.gz}"

# Serialize the timer and a manual installation against the same release pointer.
exec 9> "$cache_dir/sync.lock"
flock 9

if [ -n "${DOTFILES_CODEX_HOME:-}" ]; then
    codex_home="$DOTFILES_CODEX_HOME"
elif [ -f "$cache_dir/codex-home" ]; then
    IFS= read -r codex_home < "$cache_dir/codex-home"
elif [ -n "${CODEX_HOME:-}" ] && [ -z "${DOTFILES_SKILLS_HOME:-}" ]; then
    codex_home="$CODEX_HOME"
else
    codex_home="$user_home/.codex"
fi
case "$codex_home" in
    /*) ;;
    *) echo "Codex home must be an absolute path: $codex_home" >&2; exit 1 ;;
esac

if [ -e "$cache_dir/current" ] && [ ! -L "$cache_dir/current" ]; then
    echo "Refusing to replace $cache_dir/current: it is not a symlink" >&2
    exit 1
fi
old_release="$(readlink "$cache_dir/current" 2>/dev/null || true)"
if [ -n "$old_release" ]; then
    if [ "$(dirname -- "$old_release")" != "$cache_dir/releases" ] ||
        [[ "$(basename -- "$old_release")" != skillset.* ]] ||
        [ -L "$old_release" ]; then
        echo "Refusing to replace an unmanaged cache pointer: $cache_dir/current" >&2
        exit 1
    fi
fi

# Both parts of the framework must be installable before advancing the cache.
for destination in "$codex_home/AGENTS.md" "$skills_dir/engineering-work"; do
    if [ "$destination" = "$codex_home/AGENTS.md" ]; then
        managed_target="$cache_dir/current/AGENTS.md"
        checkout_target="$user_home/code/dotfiles/agents/AGENTS.md"
    else
        managed_target="$cache_dir/current/engineering-work"
        checkout_target="$user_home/code/dotfiles/skills/engineering-work"
    fi
    if [ -e "$destination" ] || [ -L "$destination" ]; then
        existing_target="$(readlink "$destination" 2>/dev/null || true)"
        if [ "$existing_target" != "$managed_target" ] && [ "$existing_target" != "$checkout_target" ]; then
            echo "Refusing to replace $destination: it is not managed by dotfiles. Review it before installing." >&2
            exit 1
        fi
    fi
done
if [ -e "$codex_home/AGENTS.override.md" ] || [ -L "$codex_home/AGENTS.override.md" ]; then
    echo "Refusing to install beneath $codex_home/AGENTS.override.md: it may shadow the default guide." >&2
    exit 1
fi
mkdir -p "$codex_home"

download_dir="$(mktemp -d)"
pending_release="$(mktemp -d "$cache_dir/releases/skillset.XXXXXXXX")"
next_link="$cache_dir/.current.next.$$"
next_config="$cache_dir/.codex-home.next.$$"
next_updater="$user_home/.local/bin/.dotfiles-skills-sync.next.$$"
cleanup() {
    rm -rf -- "$download_dir"
    if [ -n "$pending_release" ]; then
        rm -rf -- "$pending_release"
    fi
    rm -f -- "$next_link" "$next_config" "$next_updater"
}
trap cleanup EXIT

curl -fsSL --retry 2 "$archive_url" -o "$download_dir/dotfiles.tar.gz"
tar -xzf "$download_dir/dotfiles.tar.gz" -C "$download_dir"
source_roots=("$download_dir"/dotfiles-*)
if [ "${#source_roots[@]}" -ne 1 ] || [ ! -d "${source_roots[0]}" ]; then
    echo "Expected one dotfiles source directory in the archive." >&2
    exit 1
fi
source_root="${source_roots[0]}"
for required in agents/AGENTS.md agents/refinement.py agents/dotfiles-refinement skills/sync.sh skills/engineering-work/SKILL.md skills/engineering-work/references/work-record.md skills/engineering-work/references/steering.md; do
    if [ ! -s "$source_root/$required" ]; then
        echo "The downloaded framework is incomplete: missing or empty $required" >&2
        exit 1
    fi
done
cp "$source_root/agents/AGENTS.md" "$pending_release/AGENTS.md"
command -v python3 >/dev/null || { echo "Python 3 is required for the handoff hook." >&2; exit 1; }
python3 -c 'import ast, pathlib, sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())' "$source_root/agents/refinement.py"
bash -n "$source_root/agents/dotfiles-refinement"
bash -n "$source_root/skills/sync.sh"
cp "$source_root/agents/refinement.py" "$pending_release/refinement.py"
cp "$source_root/agents/dotfiles-refinement" "$pending_release/dotfiles-refinement"
chmod +x "$pending_release/dotfiles-refinement"
refinement_command="$user_home/.local/bin/dotfiles-refinement"
if [ -e "$refinement_command" ] || [ -L "$refinement_command" ]; then
    if [ ! -L "$refinement_command" ] || [ "$(readlink "$refinement_command")" != "$cache_dir/current/dotfiles-refinement" ]; then
        echo "Preserving existing command: $refinement_command" >&2
        exit 1
    fi
fi
hook_action=enable
[ ! -f "$cache_dir/refinement-disabled" ] || hook_action=disable
hook_args=("$hook_action" --codex-home "$codex_home" --script-path "$cache_dir/current/refinement.py")
python3 "$pending_release/refinement.py" "${hook_args[@]}" --check

skill_count=0
for skill_dir in "$source_root/skills"/*; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    cp -R "$skill_dir" "$pending_release/"
    skill_count=$((skill_count + 1))
done

# Configuration is checked before the guide, skills and hook implementation switch.
python3 "$pending_release/refinement.py" "${hook_args[@]}"
ln -s "$pending_release" "$next_link"
mv -Tf -- "$next_link" "$cache_dir/current"
pending_release=""
mkdir -p "$user_home/.local/bin"
ln -sfn "$cache_dir/current/dotfiles-refinement" "$refinement_command"
printf '%s\n' "$archive_url" > "$cache_dir/archive-url"
# Refresh the installed updater too, so future code changes reach timer runs.
install -m 755 "$source_root/skills/sync.sh" "$next_updater"
mv -f -- "$next_updater" "$user_home/.local/bin/dotfiles-skills-sync"
ln -sfn "$cache_dir/current/AGENTS.md" "$codex_home/AGENTS.md"
printf '%s\n' "$codex_home" > "$next_config"
mv -f -- "$next_config" "$cache_dir/codex-home"

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

if [ -d "$old_release" ]; then
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
fi

echo "Updated the default Codex guide, $skill_count personal skill(s), and engineering handoff hook. Review /hooks in a fresh Codex session."

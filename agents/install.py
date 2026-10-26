#!/usr/bin/env python3
"""Install a local development framework from this checkout, without downloads."""

import argparse
import os
from pathlib import Path
import sys


PREREQUISITES = (
    "work-ownership",
    "design-collaboration",
    "design-challenge",
    "technical-writing",
    "pr-comprehension",
    "publish-reviewable-work",
)


def exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def owned_link(destination: Path, source: Path) -> bool:
    # Compare the literal target: a link through a managed cache is not ours.
    return destination.is_symlink() and os.readlink(destination) == str(source)


def parent_error(destination: Path) -> str | None:
    for parent in destination.parents:
        if exists(parent) and not parent.is_dir():
            return f"Cannot create {destination}: parent {parent} is not a directory."
    return None


def install(checkout: Path, home: Path, codex_home: Path, uninstall: bool) -> int:
    skills = home / ".agents" / "skills"
    links = (
        (codex_home / "AGENTS.md", checkout / "agents" / "AGENTS.md"),
        (skills / "engineering-work", checkout / "skills" / "engineering-work"),
    )
    if uninstall:
        for destination, source in links:
            if owned_link(destination, source):
                destination.unlink()
                print(f"Removed {destination}")
            elif exists(destination):
                print(f"Preserved {destination}: it is not an installer-owned link.")
        return 0

    errors = []
    required = (
        checkout / "agents" / "AGENTS.md",
        checkout / "skills" / "engineering-work" / "SKILL.md",
        checkout / "skills" / "engineering-work" / "references" / "work-record.md",
    )
    for source in required:
        if not source.is_file():
            errors.append(f"Missing source file {source}; restore it in this checkout.")

    override = codex_home / "AGENTS.override.md"
    if exists(override):
        errors.append(
            f"{override} exists and may shadow AGENTS.md. Review it and move it "
            "aside yourself before installing (dangling links also require review)."
        )
    for destination, source in links:
        if exists(destination) and not owned_link(destination, source):
            errors.append(
                f"Refusing to replace {destination}: it is not this checkout's link. "
                "Back it up or move it aside yourself, then rerun."
            )
        error = parent_error(destination)
        if error:
            errors.append(error)
    if errors:
        print("Installation stopped before making changes:\n" + "\n".join(errors), file=sys.stderr)
        return 1

    created = []
    try:
        for destination, source in links:
            if owned_link(destination, source):
                print(f"Already installed {destination}")
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source, target_is_directory=source.is_dir())
            created.append((destination, source))
            print(f"Installed {destination} -> {source}")
    except OSError:
        for destination, source in reversed(created):
            if owned_link(destination, source):
                destination.unlink()
        raise

    missing = [name for name in PREREQUISITES if not (skills / name / "SKILL.md").is_file()]
    if missing:
        print(
            "Warning: prerequisite personal skills are missing: " + ", ".join(missing)
            + ". Install them with the existing dotfiles skills installer before using "
            "workflows that reference them. This pilot does not download or replace them.",
            file=sys.stderr,
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--home", type=Path,
        help="Use this home for skill links and default .codex; ignores CODEX_HOME unless --codex-home is given.",
    )
    parser.add_argument("--codex-home", type=Path, help="Override the global guide destination.")
    parser.add_argument("--uninstall", action="store_true", help="Remove only this checkout's exact symlinks.")
    args = parser.parse_args()
    home = (args.home if args.home is not None else Path.home()).expanduser().absolute()
    if args.codex_home is not None:
        codex_home = args.codex_home
    elif args.home is None and os.environ.get("CODEX_HOME"):
        codex_home = Path(os.environ["CODEX_HOME"])
    else:
        codex_home = home / ".codex"
    codex_home = codex_home.expanduser().absolute()
    checkout = Path(__file__).resolve().parent.parent
    try:
        return install(checkout, home, codex_home, args.uninstall)
    except OSError as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

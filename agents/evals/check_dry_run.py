#!/usr/bin/env python3
"""Check the implemented task independently: python3 check_dry_run.py FIXTURE_DIR."""

import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def check(fixture: Path) -> None:
    sys.path.insert(0, str(fixture))
    cleanup_cache = importlib.import_module("cleanup").cleanup_cache
    scenarios = {
        "mixed": {
            "z-old": {"value": {"nested": [1, 2]}, "expires_at": 99},
            "a-boundary": {"value": "due", "expires_at": 100},
            "fresh": {"value": "keep", "expires_at": 100.5},
            "permanent": {"value": None, "expires_at": None},
        },
        "empty": {},
        "nonexpiring": {"permanent": {"value": "keep", "expires_at": None}},
        "all-expired": {"zero": {"value": 0, "expires_at": 0}},
    }
    with tempfile.TemporaryDirectory() as temporary:
        cache = Path(temporary) / "cache with spaces.json"
        for name, entries in scenarios.items():
            expected = sorted(
                key for key, entry in entries.items()
                if entry["expires_at"] is not None and entry["expires_at"] <= 100
            )
            remaining = {key: value for key, value in entries.items() if key not in expected}
            original = ("  " + json.dumps(entries, indent=3) + "\n\n").encode()
            for interface in ("library", "cli"):
                for dry_run in (True, False):
                    label = f"{name}, {interface}, dry_run={dry_run}"
                    cache.write_bytes(original)
                    if interface == "library":
                        if dry_run:
                            actual = cleanup_cache(cache, now=100, dry_run=True)
                        else:
                            actual = cleanup_cache(cache, now=100)
                    else:
                        command = [sys.executable, str(fixture / "cli.py"), str(cache), "--now", "100"]
                        if dry_run:
                            command.append("--dry-run")
                        result = subprocess.run(command, text=True, capture_output=True, check=False)
                        assert result.returncode == 0, f"{label}: CLI failed: {result.stderr}"
                        actual = result.stdout.splitlines()
                    assert actual == expected, f"{label}: expected keys {expected!r}, got {actual!r}"
                    if dry_run or not expected:
                        assert cache.read_bytes() == original, f"{label}: file bytes changed"
                    else:
                        actual_entries = json.loads(cache.read_bytes())
                        assert actual_entries == remaining, f"{label}: wrong remaining entries: {actual_entries!r}"
                    print(f"PASS {label}")
            # Explicit False is part of the Python option's contract as well.
            cache.write_bytes(original)
            assert cleanup_cache(cache, now=100, dry_run=False) == expected, name
            assert json.loads(cache.read_bytes()) == remaining, name
    print("PASS: dry-run and normal cleanup satisfy library and CLI behavior")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 check_dry_run.py FIXTURE_DIR")
    check(Path(sys.argv[1]).resolve())

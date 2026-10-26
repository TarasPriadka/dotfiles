"""Remove expired entries from a cache file."""

from pathlib import Path
import time

from storage import load_cache, save_cache


def cleanup_cache(path: Path, *, now: float | None = None) -> list[str]:
    """Remove entries expiring at or before now and return their sorted keys."""
    cutoff = time.time() if now is None else now
    entries = load_cache(path)
    removed = sorted(
        key
        for key, entry in entries.items()
        if entry["expires_at"] is not None and entry["expires_at"] <= cutoff
    )
    for key in removed:
        del entries[key]
    if removed:
        save_cache(path, entries)
    return removed

"""JSON storage for the local cache."""

import json
from pathlib import Path
from typing import Any


def load_cache(path: Path) -> dict[str, dict[str, Any]]:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def save_cache(path: Path, entries: dict[str, dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as destination:
        json.dump(entries, destination, indent=2, sort_keys=True)
        destination.write("\n")

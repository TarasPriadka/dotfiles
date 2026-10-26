"""Command-line cache cleanup."""

import argparse
from pathlib import Path

from cleanup import cleanup_cache


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove expired cache entries.")
    parser.add_argument("cache", type=Path, help="Path to the JSON cache")
    parser.add_argument("--now", type=float, help="Expiration cutoff; defaults to current time")
    args = parser.parse_args()
    for key in cleanup_cache(args.cache, now=args.now):
        print(key)


if __name__ == "__main__":
    main()

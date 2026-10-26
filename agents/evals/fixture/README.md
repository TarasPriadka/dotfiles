# Cache cleanup

This small Python 3.10+ tool removes expired entries from a local JSON cache.
It has no third-party dependencies.

The cache is an object keyed by entry name. Each entry contains `value` and
`expires_at`. Expiration is a numeric Unix timestamp, or `null` for entries
that never expire. An entry is expired **at or before** the cutoff.

```json
{
  "old": {"value": "cached result", "expires_at": 100},
  "permanent": {"value": "configuration", "expires_at": null}
}
```

Run `python3 cli.py cache.json --now 100` to remove expired entries and print
their keys in sorted order, one key per line. Without `--now`, cleanup uses
the current time. No output means no entries were removed.

Python callers use `cleanup.cleanup_cache(Path("cache.json"), now=100)`.
It updates the file and returns the sorted list of removed keys. Remaining
entries retain their contents. A cleanup with nothing to remove leaves the
file untouched.

Run the baseline tests from this directory:

```sh
python3 -m unittest discover -s tests -v
```

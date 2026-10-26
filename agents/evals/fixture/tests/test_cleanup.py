import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from cleanup import cleanup_cache


class CleanupTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "cache.json"
        self.entries = {
            "expired": {"value": "old", "expires_at": 90},
            "boundary": {"value": "due", "expires_at": 100},
            "fresh": {"value": "new", "expires_at": 101},
            "permanent": {"value": "keep", "expires_at": None},
        }
        self.path.write_text(json.dumps(self.entries), encoding="utf-8")

    def test_cleanup_removes_entries_at_or_before_cutoff(self):
        self.assertEqual(cleanup_cache(self.path, now=100), ["boundary", "expired"])
        self.assertEqual(
            json.loads(self.path.read_text(encoding="utf-8")),
            {key: self.entries[key] for key in ("fresh", "permanent")},
        )

    def test_cli_prints_removed_keys(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "cli.py"),
             str(self.path), "--now", "100"],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["boundary", "expired"])
        self.assertEqual(set(json.loads(self.path.read_text(encoding="utf-8"))), {"fresh", "permanent"})


if __name__ == "__main__":
    unittest.main()

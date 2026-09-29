"""Exercise the command against real Git histories, without network access."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest

PROGRAM = Path(__file__).resolve().parents[1] / "git-uncommit"


class UncommitTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "alias.uncommit", "!python3 " + shlex.quote(str(PROGRAM)))
        self.commit("base", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.git("checkout", "-b", "feature")
        self.commit("one", "one")
        self.commit("two", "two")
        self.original = self.git("rev-parse", "HEAD")

    def git(self, *args, check=True):
        result = subprocess.run(
            ["git", *args], cwd=self.repo, env=self.env, text=True, capture_output=True
        )
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout.strip()
        return result

    def commit(self, filename, content):
        (self.repo / filename).write_text(content)
        self.git("add", filename)
        self.git("commit", "-m", filename)

    def state(self):
        return Path(self.git("rev-parse", "--absolute-git-dir")) / "uncommit-state.json"

    def fake_github(self, base="main", fail=False):
        remote = self.root / "remote.git"
        self.git("clone", "--bare", str(self.repo), str(remote))
        self.git("remote", "add", "origin", str(remote))
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        gh = fake_bin / "gh"
        payload = json.dumps({"baseRefName": base, "url": remote.as_uri() + "/pull/1"})
        gh.write_text(
            "#!/bin/sh\n"
            + ("exit 1\n" if fail else "printf '%s\\n' " + shlex.quote(payload) + "\n")
        )
        gh.chmod(0o755)
        self.env["PATH"] = str(fake_bin) + os.pathsep + self.env["PATH"]

    def test_multiple_commits_and_restore_preserve_history(self):
        self.git("uncommit", "--base", "main")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "one\ntwo")
        self.git("uncommit", "--restore")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertFalse(self.state().exists())
        self.assertEqual(self.git("for-each-ref", "--format=%(refname)", "refs/uncommit/"), "")

    def test_main_merge_and_newer_remote_main_are_excluded(self):
        self.git("checkout", "main")
        self.commit("upstream", "upstream")
        merged_base = self.git("rev-parse", "HEAD")
        self.git("checkout", "feature")
        self.git("merge", "--no-ff", "main", "-m", "merge main")
        merged_head = self.git("rev-parse", "HEAD")
        self.git("checkout", "main")
        self.commit("later-upstream", "later")
        self.git("checkout", "feature")
        self.fake_github()
        self.git("uncommit")
        self.assertEqual(self.git("rev-parse", "HEAD"), merged_base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "one\ntwo")
        self.git("uncommit", "--restore")
        self.assertEqual(self.git("rev-parse", "HEAD"), merged_head)

    def test_stacked_pr_uses_its_actual_target(self):
        self.git("branch", "stack-parent", "HEAD~1")
        self.fake_github("stack-parent")
        self.git("uncommit")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.git("rev-parse", "stack-parent"))
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "two")

    def test_repeated_call_keeps_restore_point_without_network(self):
        self.git("uncommit", "--base", "main")
        saved = self.state().read_bytes()
        self.git("uncommit")
        self.assertEqual(self.state().read_bytes(), saved)
        self.git("uncommit", "--restore")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)

    def test_staged_unstaged_and_untracked_work_survive_round_trip(self):
        (self.repo / "one").write_text("staged")
        self.git("add", "one")
        (self.repo / "one").write_text("unstaged")
        (self.repo / "untracked").write_text("untracked")
        index = self.git("write-tree")
        status = self.git("status", "--porcelain")
        self.git("uncommit", "--base", "main")
        self.git("uncommit", "--restore")
        self.assertEqual(self.git("write-tree"), index)
        self.assertEqual(self.git("status", "--porcelain"), status)
        self.assertEqual((self.repo / "one").read_text(), "unstaged")
        self.assertEqual((self.repo / "untracked").read_text(), "untracked")

    def test_new_commits_are_not_overwritten_by_restore(self):
        self.git("uncommit", "--base", "main")
        self.git("commit", "-m", "new history")
        head = self.git("rev-parse", "HEAD")
        result = self.git("uncommit", "--restore", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        saved = json.loads(self.state().read_text())
        self.assertEqual(self.git("rev-parse", saved["backup_ref"]), self.original)

    def test_one_retains_legacy_behavior(self):
        expected = self.git("rev-parse", "HEAD~1")
        self.git("uncommit", "--one")
        self.assertEqual(self.git("rev-parse", "HEAD"), expected)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "two")
        self.assertFalse(self.state().exists())

    def test_dry_run_does_not_reset_or_create_restore_point(self):
        result = self.git("uncommit", "--base", "main", "--dry-run")
        self.assertIn("Would soft-reset", result)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertFalse(self.state().exists())

    def test_failed_detection_does_not_guess_main(self):
        self.fake_github(fail=True)
        result = self.git("uncommit", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--base", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertFalse(self.state().exists())

    def test_fetch_failure_preserves_head(self):
        self.fake_github()
        self.git("push", "origin", "--delete", "main")
        result = self.git("uncommit", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertFalse(self.state().exists())

    def test_active_merge_is_rejected(self):
        self.git("checkout", "main")
        self.commit("main-change", "main")
        self.git("checkout", "feature")
        self.git("merge", "--no-commit", "--no-ff", "main")
        result = self.git("uncommit", "--base", "main", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)

    def test_worktree_has_its_own_restore_state(self):
        other = self.root / "other"
        self.git("worktree", "add", "-b", "other", str(other), "feature")
        self.git("uncommit", "--base", "main")
        first_state = self.state()
        self.repo = other
        self.git("uncommit", "--base", "main")
        self.assertNotEqual(first_state, self.state())
        self.git("uncommit", "--restore")
        self.assertTrue(first_state.exists())


if __name__ == "__main__":
    unittest.main()

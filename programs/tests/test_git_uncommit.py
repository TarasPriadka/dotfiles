"""Exercise the command against real Git histories, without network access."""

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
        # Git prefers an installed git-uncommit over the alias below.
        self.env["PATH"] = str(PROGRAM.parent) + os.pathsep + self.env["PATH"]
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
        self.git("update-ref", "refs/remotes/origin/" + base, base)
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        gh = fake_bin / "gh"
        gh.write_text(
            "#!/bin/sh\n"
            + ("exit 1\n" if fail else "printf '%s\\n' " + shlex.quote(base) + "\n")
        )
        gh.chmod(0o755)
        self.env["PATH"] = str(fake_bin) + os.pathsep + self.env["PATH"]

    def test_uncommits_all_branch_commits_without_saving_state(self):
        self.fake_github()
        self.git("uncommit")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "one\ntwo")
        self.assertFalse(self.state().exists())
        self.assertEqual(self.git("for-each-ref", "--format=%(refname)", "refs/uncommit/"), "")

    def test_one_uncommits_only_latest_commit_without_github(self):
        self.fake_github(fail=True)
        parent = self.git("rev-parse", "HEAD^1")
        self.git("uncommit", "--one")
        self.assertEqual(self.git("rev-parse", "HEAD"), parent)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "two")
        self.assertEqual(self.git("rev-parse", "ORIG_HEAD"), self.original)
        self.git("uncommit", "--one")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "one\ntwo")

    def test_one_preserves_local_edits(self):
        (self.repo / "one").write_text("staged")
        self.git("add", "one")
        (self.repo / "one").write_text("unstaged")
        (self.repo / "untracked").write_text("untracked")
        (self.repo / ".gitignore").write_text("ignored\n")
        (self.repo / "ignored").write_text("ignored")
        index = self.git("write-tree")
        parent = self.git("rev-parse", "HEAD^1")
        self.git("uncommit", "--one")
        self.assertEqual(self.git("rev-parse", "HEAD"), parent)
        self.assertEqual(self.git("write-tree"), index)
        self.assertEqual((self.repo / "one").read_text(), "unstaged")
        self.assertEqual((self.repo / "untracked").read_text(), "untracked")
        self.assertEqual((self.repo / "ignored").read_text(), "ignored")

    def test_one_uses_first_parent_of_merge(self):
        self.git("checkout", "main")
        self.commit("upstream", "upstream")
        self.git("checkout", "feature")
        self.git("merge", "--no-ff", "main", "-m", "merge main")
        self.git("uncommit", "--one")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "upstream")

    def test_one_rejects_base_without_changing_history(self):
        result = self.git("uncommit", "--one", "--base", "main", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not allowed with argument", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_one_at_root_leaves_history_unchanged(self):
        self.git("checkout", "main")
        result = self.git("uncommit", "--one", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("--base", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_stacked_pr_uses_its_parent(self):
        self.git("branch", "stack-parent", "HEAD~1")
        self.fake_github("stack-parent")
        self.git("uncommit")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.git("rev-parse", "stack-parent"))
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "two")

    def test_new_parent_commits_are_excluded(self):
        self.git("checkout", "main")
        self.commit("upstream", "upstream")
        self.git("checkout", "feature")
        self.git("merge", "--no-ff", "main", "-m", "merge main")
        merged_base = self.git("rev-parse", "main")
        self.git("checkout", "main")
        self.commit("later-upstream", "later")
        self.git("checkout", "feature")
        self.fake_github()
        self.git("uncommit")
        self.assertEqual(self.git("rev-parse", "HEAD"), merged_base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "one\ntwo")

    def test_local_edits_are_preserved_with_explicit_base(self):
        (self.repo / "one").write_text("staged")
        self.git("add", "one")
        (self.repo / "one").write_text("unstaged")
        (self.repo / "untracked").write_text("untracked")
        (self.repo / ".gitignore").write_text("ignored\n")
        (self.repo / "ignored").write_text("ignored")
        index = self.git("write-tree")
        self.git("uncommit", "--base", "main")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("write-tree"), index)
        self.assertEqual((self.repo / "one").read_text(), "unstaged")
        self.assertEqual((self.repo / "untracked").read_text(), "untracked")
        self.assertEqual((self.repo / "ignored").read_text(), "ignored")

    def test_old_state_and_moved_head_do_not_block_uncommit(self):
        self.state().write_text("obsolete review metadata")
        self.commit("three", "three")
        self.git("uncommit", "--base", "main")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "one\nthree\ntwo")

    def test_repeated_calls_preserve_diff_and_original_head(self):
        self.git("uncommit", "--base", "main")
        index = self.git("write-tree")
        self.git("uncommit", "--base", "main")
        self.assertEqual(self.git("rev-parse", "HEAD"), self.base)
        self.assertEqual(self.git("write-tree"), index)
        self.assertEqual(self.git("rev-parse", "ORIG_HEAD"), self.original)

    def test_failed_parent_lookup_leaves_history_unchanged(self):
        self.fake_github(fail=True)
        result = self.git("uncommit", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--base", result.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_invalid_base_leaves_history_unchanged(self):
        result = self.git("uncommit", "--base", "missing", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_git_rejects_soft_reset_during_merge(self):
        self.git("checkout", "main")
        self.commit("main-change", "main")
        self.git("checkout", "feature")
        self.git("merge", "--no-commit", "--no-ff", "main")
        result = self.git("uncommit", "--base", "main", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.original)


if __name__ == "__main__":
    unittest.main()

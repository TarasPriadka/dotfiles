"""Exercise review cleanup and branch refresh against real, local Git remotes."""

import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest

PROGRAM = Path(__file__).resolve().parents[1] / "git-review"


class ReviewTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.remote = self.root / "remote.git"
        self.author = self.root / "author"
        self.repo = self.root / "reviewer"
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", LC_ALL="C")
        self.env["PATH"] = str(PROGRAM.parent) + os.pathsep + self.env["PATH"]
        self.git("init", "--bare", "-b", "main", str(self.remote), cwd=self.root)
        self.git("clone", str(self.remote), str(self.author), cwd=self.root)
        self.git("config", "user.name", "Test", cwd=self.author)
        self.git("config", "user.email", "test@example.com", cwd=self.author)
        for name in ("shared", "removed"):
            (self.author / name).write_text("base\n")
        self.commit("base")
        self.base = self.git("rev-parse", "HEAD", cwd=self.author)
        self.git("push", "origin", "main", cwd=self.author)
        self.git("switch", "-c", "feature", cwd=self.author)
        (self.author / "shared").write_text("feature\n")
        (self.author / "feature").write_text("feature\n")
        (self.author / "removed").unlink()
        self.commit("feature")
        self.head = self.git("rev-parse", "HEAD", cwd=self.author)
        self.git("push", "origin", "feature", cwd=self.author)
        self.git("clone", str(self.remote), str(self.repo), cwd=self.root)
        self.git("switch", "feature")

    def git(self, *args, cwd=None, check=True):
        result = subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, text=True, capture_output=True
        )
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout.strip()
        return result

    def commit(self, message, cwd=None):
        self.git("add", "--all", cwd=cwd or self.author)
        self.git("commit", "-m", message, cwd=cwd or self.author)

    def review(self, *args, check=True):
        return self.git("review", *args, check=check)

    def snapshot(self):
        return (
            self.git("symbolic-ref", "HEAD"),
            self.git("rev-parse", "HEAD"),
            self.git("write-tree"),
            self.git("status", "--porcelain", "--untracked-files=all"),
            {str(path.relative_to(self.repo)): path.read_bytes()
             for path in self.repo.rglob("*") if path.is_file() and ".git" not in path.relative_to(self.repo).parts},
        )

    def assert_failure_preserves_review(self, *args, message):
        before = self.snapshot()
        result = self.review(*args, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def assert_review(self, ancestor=None, head=None):
        self.assertEqual(self.git("rev-parse", "HEAD"), ancestor or self.base)
        self.assertEqual(self.git("write-tree"), self.git("rev-parse", (head or self.head) + "^{tree}"))
        self.assertEqual(self.git("diff", "--name-only"), "")
        self.assertEqual(self.git("rev-parse", "ORIG_HEAD"), head or self.head)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "@{upstream}"), "origin/feature")

    def fake_github(self, base="main", fail=False, cross_repository=False, wait_for_fetch=False):
        fake_bin = self.root / "bin"
        fake_bin.mkdir()
        real_git = shutil.which("git", path=self.env["PATH"])
        git_wrapper = fake_bin / "git"
        fetch_signal = shlex.quote(str(self.root / "fetch-started"))
        git_wrapper.write_text(
            '#!/bin/sh\nif [ "$1" = remote ] && [ "$2" = get-url ]; then\n'
            "  printf '%s\\n' git@github.com:example/project.git\nelse\n"
            f'  if [ "$1" = fetch ]; then touch {fetch_signal}; fi\n'
            f"  exec {shlex.quote(real_git)} \"$@\"\nfi\n"
        )
        git_wrapper.chmod(0o755)
        response = json.dumps({"baseRefName": base, "headRefName": "feature", "isCrossRepository": cross_repository})
        gh = fake_bin / "gh"
        wait = ""
        if wait_for_fetch:
            wait = "python3 -c " + shlex.quote(
                "from pathlib import Path\nimport time\n"
                f"signal = Path({str(self.root / 'fetch-started')!r})\n"
                "deadline = time.monotonic() + 5\n"
                "while not signal.exists() and time.monotonic() < deadline:\n"
                "    time.sleep(0.01)\n"
                "assert signal.exists(), 'PR lookup and fetch did not overlap'\n"
            ) + " || exit 1\n"
        gh.write_text(
            "#!/bin/sh\nprintf '%s\\n' \"$@\" > " + shlex.quote(str(self.root / "gh-args")) + "\n"
            + wait
            + ("echo 'PR lookup failed' >&2\nexit 1\n" if fail else "printf '%s\\n' " + shlex.quote(response) + "\n")
        )
        gh.chmod(0o755)
        self.env["PATH"] = str(fake_bin) + os.pathsep + self.env["PATH"]
        self.env["GIT_EXEC_PATH"] = str(fake_bin)

    def test_stages_fetched_branch_with_additions_and_deletions(self):
        self.review("--base", "main")
        self.assert_review()
        self.assertEqual(self.git("diff", "--cached", "--name-status"), "A\tfeature\nD\tremoved\nM\tshared")

    def test_repeated_review_discards_staged_edits_and_refreshes(self):
        self.review("--base", "main")
        (self.repo / "shared").write_text("disposable review\n")
        (self.repo / "scratch").write_text("staged scratch\n")
        self.git("add", "shared", "scratch")
        self.review("--base", "main")
        self.assert_review()
        self.assertFalse((self.repo / "scratch").exists())
        self.assertEqual((self.repo / "shared").read_text(), "feature\n")

    def test_switches_from_previous_staged_review(self):
        self.git("switch", "main")
        (self.repo / "shared").write_text("previous review\n")
        self.git("add", "shared")
        self.review("feature", "--base", "main")
        self.assert_review()
        self.assertEqual(self.git("branch", "--show-current"), "feature")
        self.assertEqual(self.git("rev-parse", "main"), self.base)

    def test_fetches_new_commits(self):
        self.review("--base", "main")
        (self.author / "later").write_text("new commit\n")
        self.commit("later")
        self.git("push", "origin", "feature", cwd=self.author)
        head = self.git("rev-parse", "HEAD", cwd=self.author)
        self.review("--base", "main")
        self.assert_review(head=head)

    def test_replaces_force_pushed_history_instead_of_merging(self):
        self.review("--base", "main")
        self.git("reset", "--hard", "main", cwd=self.author)
        (self.author / "replacement").write_text("rebased\n")
        self.commit("replacement")
        self.git("push", "--force", "origin", "feature", cwd=self.author)
        head = self.git("rev-parse", "HEAD", cwd=self.author)
        self.review("--base", "main")
        self.assert_review(head=head)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "replacement")
        self.assertFalse((self.repo / "feature").exists())

    def test_stacked_pr_uses_fetched_parent(self):
        self.git("branch", "parent", self.head, cwd=self.author)
        self.git("push", "origin", "parent", cwd=self.author)
        (self.author / "child").write_text("child\n")
        self.commit("child")
        self.git("push", "origin", "feature", cwd=self.author)
        head = self.git("rev-parse", "HEAD", cwd=self.author)
        self.fake_github(base="parent")
        self.review()
        self.assert_review(ancestor=self.head, head=head)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "child")
        self.assertIn("example/project", (self.root / "gh-args").read_text())

    def test_reports_fresh_base_without_rebasing(self):
        self.git("switch", "main", cwd=self.author)
        (self.author / "upstream").write_text("upstream\n")
        self.commit("upstream")
        self.git("push", "origin", "main", cwd=self.author)
        output = self.review("--base", "main")
        self.assert_review()
        self.assertIn("behind its base by 1", output)
        self.assertFalse((self.repo / "upstream").exists())

    def test_repeated_review_overlaps_lookup_and_fetch(self):
        self.review("--base", "main")
        self.fake_github(wait_for_fetch=True)
        self.review()
        self.assert_review()

    def test_retargeted_pr_fetches_new_base(self):
        self.review("--base", "main")
        self.git("branch", "parent", self.head, cwd=self.author)
        self.git("push", "origin", "parent", cwd=self.author)
        (self.author / "child").write_text("child\n")
        self.commit("child")
        self.git("push", "origin", "feature", cwd=self.author)
        head = self.git("rev-parse", "HEAD", cwd=self.author)
        self.fake_github(base="parent")
        self.review()
        self.assert_review(ancestor=self.head, head=head)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "child")
        self.assertEqual(self.git("config", "branch.feature.reviewBase"), "parent")

    def test_deleted_base_hint_does_not_block_retargeted_pr(self):
        self.review("--base", "main")
        self.git("config", "branch.feature.reviewBase", "deleted-parent")
        self.fake_github()
        self.review()
        self.assert_review()

    def test_failed_speculative_fetch_preserves_review(self):
        self.review("--base", "main")
        self.git("push", "origin", ":feature", cwd=self.author)
        self.fake_github()
        self.assert_failure_preserves_review(message="couldn't find remote ref")

    def test_preserves_untracked_and_ignored_files(self):
        (self.repo / "notes").write_text("keep\n")
        (self.repo / "ignored").write_text("keep ignored\n")
        with (self.repo / ".git/info/exclude").open("a") as exclude:
            exclude.write("ignored\n")
        self.review("--base", "main")
        self.assert_review()
        self.assertEqual((self.repo / "notes").read_text(), "keep\n")
        self.assertEqual((self.repo / "ignored").read_text(), "keep ignored\n")

    def test_unstaged_edits_stop_before_cleanup(self):
        self.review("--base", "main")
        (self.repo / "shared").write_text("unstaged\n")
        self.assert_failure_preserves_review("--base", "main", message="Unstaged edits")

    def test_failed_fetch_preserves_staged_review(self):
        self.review("--base", "main")
        self.assert_failure_preserves_review("missing", "--base", "main", message="couldn't find remote ref")

    def test_failed_base_fetch_preserves_staged_review(self):
        self.review("--base", "main")
        self.assert_failure_preserves_review("--base", "missing", message="couldn't find remote ref")

    def test_failed_pr_lookup_preserves_staged_review(self):
        self.review("--base", "main")
        self.fake_github(fail=True)
        self.assert_failure_preserves_review(message="PR lookup failed")

    def test_cross_repository_pr_stops_before_cleanup(self):
        self.review("--base", "main")
        self.fake_github(cross_repository=True)
        self.assert_failure_preserves_review(message="PR head does not match")

    def test_other_worktree_stops_before_cleanup(self):
        self.git("worktree", "add", str(self.root / "other"), "main")
        self.review("--base", "main")
        self.assert_failure_preserves_review("main", "--base", "feature", message="another worktree")

    def test_untracked_file_collision_stops_before_cleanup(self):
        self.git("switch", "main")
        (self.repo / "feature").write_text("keep untracked\n")
        self.assert_failure_preserves_review("feature", "--base", "main", message="would be overwritten")

    def test_ignored_file_collision_stops_before_cleanup(self):
        self.git("switch", "main")
        (self.repo / "feature").write_text("keep ignored\n")
        with (self.repo / ".git/info/exclude").open("a") as exclude:
            exclude.write("feature\n")
        self.assert_failure_preserves_review("feature", "--base", "main", message="would be overwritten")

    def test_staged_deletion_with_untracked_replacement_is_preserved(self):
        self.git("rm", "shared")
        (self.repo / "shared").write_text("untracked replacement\n")
        self.assert_failure_preserves_review("--base", "main", message="would be overwritten")

    def test_untracked_directory_conflicting_with_file_is_preserved(self):
        self.git("switch", "main")
        (self.repo / "feature").mkdir()
        (self.repo / "feature/notes").write_text("keep\n")
        self.assert_failure_preserves_review("feature", "--base", "main", message="would be overwritten")

    def test_untracked_file_conflicting_with_directory_is_preserved(self):
        (self.author / "folder").mkdir()
        (self.author / "folder/file").write_text("remote\n")
        self.commit("folder")
        self.git("push", "origin", "feature", cwd=self.author)
        (self.repo / "folder").write_text("keep\n")
        self.assert_failure_preserves_review("--base", "main", message="would be overwritten")

    def test_disjoint_untracked_file_in_new_remote_directory_is_preserved(self):
        (self.author / "folder").mkdir()
        (self.author / "folder/file").write_text("remote\n")
        self.commit("folder")
        self.git("push", "origin", "feature", cwd=self.author)
        head = self.git("rev-parse", "HEAD", cwd=self.author)
        (self.repo / "folder").mkdir()
        (self.repo / "folder/notes").write_text("keep\n")
        self.review("--base", "main")
        self.assert_review(head=head)
        self.assertEqual((self.repo / "folder/notes").read_text(), "keep\n")

    def test_ignored_collision_inside_untracked_directory_is_preserved(self):
        (self.author / "folder").mkdir()
        (self.author / "folder/file").write_text("remote\n")
        self.commit("folder")
        self.git("push", "origin", "feature", cwd=self.author)
        (self.repo / "folder").mkdir()
        (self.repo / "folder/file").write_text("keep ignored\n")
        with (self.repo / ".git/info/exclude").open("a") as exclude:
            exclude.write("folder/\n")
        self.assert_failure_preserves_review("--base", "main", message="would be overwritten")

    def test_same_base_is_rejected_without_cleanup(self):
        self.review("--base", "main")
        self.assert_failure_preserves_review("--base", "feature", message="must differ")

    def test_active_merge_is_rejected_without_cleanup(self):
        (self.repo / ".git/MERGE_HEAD").write_text(self.base + "\n")
        self.assert_failure_preserves_review("--base", "main", message="current Git operation")

    def test_uses_configured_upstream_branch_name(self):
        self.git("branch", "-m", "local-review")
        self.review("--base", "main")
        self.assert_review()
        self.assertEqual(self.git("branch", "--show-current"), "local-review")

    def test_runs_from_subdirectory(self):
        folder = self.repo / "local-folder"
        folder.mkdir()
        self.git("review", "--base", "main", cwd=folder)
        self.assert_review()

    def test_installer_registers_helper_and_preserves_other_git_settings(self):
        install_home = self.root / "install-home"
        install_home.mkdir()
        config = install_home / ".gitconfig"
        config.write_text('[alias]\n  keep = status\n[user]\n  name = Existing User\n')
        env = self.env.copy()
        env.update(
            DOTFILES_PROGRAMS_HOME=str(install_home),
            DOTFILES_PROGRAMS_RAW_BASE=PROGRAM.parent.parent.as_uri(),
        )
        result = subprocess.run(
            ["bash", str(PROGRAM.parent / "install.sh")], env=env,
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        installed = install_home / ".local/bin/git-review"
        self.assertEqual(installed.read_bytes(), PROGRAM.read_bytes())
        self.assertTrue(os.access(installed, os.X_OK))
        self.assertEqual(self.git("config", "--file", str(config), "alias.keep"), "status")
        self.assertEqual(self.git("config", "--file", str(config), "user.name"), "Existing User")
        self.assertEqual(
            self.git("config", "--file", str(config), "alias.review"),
            '!"$HOME/.local/bin/git-review"',
        )
        self.env["PATH"] = str(installed.parent) + os.pathsep + self.env["PATH"]
        self.review("--base", "main")
        self.assert_review()


if __name__ == "__main__":
    unittest.main()

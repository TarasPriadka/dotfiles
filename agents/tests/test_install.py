"""Exercise the installer in disposable checkouts and homes, without network access."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / "install.py"
PREREQUISITES = (
    "work-ownership", "design-collaboration", "design-challenge",
    "technical-writing", "pr-comprehension", "publish-reviewable-work",
)


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.checkout = self.root / "checkout with spaces"
        self.home = self.root / "home"
        self.home.mkdir()
        self.guide = self.checkout / "agents" / "AGENTS.md"
        self.guide.parent.mkdir(parents=True)
        self.guide.write_text("Global framework guide\n")
        self.script = self.guide.parent / "install.py"
        shutil.copyfile(INSTALLER, self.script)
        self.skill = self.checkout / "skills" / "engineering-work"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Engineering workflow\n")
        (self.skill / "references" / "work-record.md").write_text("Work record\n")
        self.guide_link = self.home / ".codex" / "AGENTS.md"
        self.skill_link = self.home / ".agents" / "skills" / "engineering-work"

    def run_installer(self, *args, expected=0, home=None, env=None):
        environment = dict(os.environ)
        environment.pop("CODEX_HOME", None)
        # No shell or downloader is needed, even when prerequisites are absent.
        environment["PATH"] = ""
        if env:
            environment.update(env)
        result = subprocess.run(
            [sys.executable, str(self.script), "--home", str(home or self.home), *args],
            cwd=self.root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_install_is_usable_from_other_directory_and_idempotent(self):
        result = self.run_installer()
        self.assertIn("prerequisite personal skills are missing", result.stderr)
        self.assertEqual(os.readlink(self.guide_link), str(self.guide))
        self.assertEqual(os.readlink(self.skill_link), str(self.skill))
        self.assertEqual(self.guide_link.read_text(), "Global framework guide\n")
        self.assertEqual((self.skill_link / "references" / "work-record.md").read_text(), "Work record\n")
        initial_inode = self.guide_link.lstat().st_ino
        self.guide.write_text("Updated guide\n")
        self.run_installer()
        self.assertEqual(self.guide_link.lstat().st_ino, initial_inode)
        self.assertEqual(self.guide_link.read_text(), "Updated guide\n")

    def test_existing_cached_prerequisites_are_preserved(self):
        for name in PREREQUISITES:
            cached = self.home / ".local" / "share" / "dotfiles-skills" / "current" / name
            cached.mkdir(parents=True)
            (cached / "SKILL.md").write_text(name)
            link = self.home / ".agents" / "skills" / name
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(cached)
        result = self.run_installer()
        self.assertEqual(result.stderr, "")
        for name in PREREQUISITES:
            link = self.home / ".agents" / "skills" / name
            self.assertTrue(link.is_symlink())
            self.assertEqual((link / "SKILL.md").read_text(), name)

    def test_skill_conflict_blocks_guide_install(self):
        self.skill_link.mkdir(parents=True)
        (self.skill_link / "personal.txt").write_text("Keep me")
        result = self.run_installer(expected=1)
        self.assertIn("Refusing to replace", result.stderr)
        self.assertFalse(self.guide_link.parent.exists())
        self.assertEqual((self.skill_link / "personal.txt").read_text(), "Keep me")

    def test_guide_conflicts_preserve_content_and_do_not_install_skill(self):
        for kind in ("file", "directory", "other_link", "dangling_link"):
            with self.subTest(kind=kind):
                home = self.root / kind
                guide = home / ".codex" / "AGENTS.md"
                guide.parent.mkdir(parents=True)
                if kind == "file":
                    guide.write_text("Personal guide")
                elif kind == "directory":
                    guide.mkdir()
                else:
                    guide.symlink_to(self.guide if kind == "other_link" else self.root / "missing")
                    if kind == "other_link":
                        # A differently spelled target must not be adopted.
                        guide.unlink()
                        guide.symlink_to(str(self.guide.parent) + "/../agents/AGENTS.md")
                before = guide.lstat()
                self.run_installer(home=home, expected=1)
                self.assertEqual(guide.lstat().st_ino, before.st_ino)
                self.assertFalse((home / ".agents").exists())

    def test_override_even_dangling_blocks_install(self):
        for dangling in (False, True):
            with self.subTest(dangling=dangling):
                home = self.root / f"override-{dangling}"
                override = home / ".codex" / "AGENTS.override.md"
                override.parent.mkdir(parents=True)
                if dangling:
                    override.symlink_to(self.root / "missing-override")
                else:
                    override.write_text("")
                result = self.run_installer(home=home, expected=1)
                self.assertIn("may shadow", result.stderr)
                self.assertFalse((override.parent / "AGENTS.md").is_symlink())
                self.assertFalse((home / ".agents").exists())

    def test_missing_reference_blocks_all_changes(self):
        (self.skill / "references" / "work-record.md").unlink()
        result = self.run_installer(expected=1)
        self.assertIn("Missing source file", result.stderr)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_non_directory_parent_blocks_all_changes(self):
        (self.home / ".agents").write_text("Personal data")
        self.run_installer(expected=1)
        self.assertFalse(self.guide_link.parent.exists())
        self.assertEqual((self.home / ".agents").read_text(), "Personal data")

    def test_home_override_ignores_environment_codex_home(self):
        elsewhere = self.root / "environment-codex"
        self.run_installer(env={"CODEX_HOME": str(elsewhere)})
        self.assertTrue(self.guide_link.is_symlink())
        self.assertFalse(elsewhere.exists())

    def test_default_home_honors_codex_home_environment(self):
        custom = self.root / "environment-codex"
        environment = dict(os.environ, HOME=str(self.home), CODEX_HOME=str(custom), PATH="")
        result = subprocess.run(
            [sys.executable, str(self.script)], cwd=self.root, env=environment,
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((custom / "AGENTS.md").is_symlink())
        self.assertTrue(self.skill_link.is_symlink())
        self.assertFalse(self.guide_link.parent.exists())

    def test_explicit_codex_home_controls_install_and_uninstall(self):
        custom = self.root / "custom codex"
        self.run_installer("--codex-home", str(custom))
        self.assertTrue((custom / "AGENTS.md").is_symlink())
        self.assertTrue(self.skill_link.is_symlink())
        self.assertFalse(self.guide_link.parent.exists())
        self.run_installer("--codex-home", str(custom), "--uninstall")
        self.assertFalse((custom / "AGENTS.md").is_symlink())
        self.assertFalse(self.skill_link.is_symlink())

    def test_uninstall_removes_only_owned_links_even_without_sources(self):
        self.run_installer()
        unrelated = self.guide_link.parent / "personal.txt"
        unrelated.write_text("Preserve")
        # Uninstall must remain available even when an override or broken source appears.
        (self.guide_link.parent / "AGENTS.override.md").write_text("Override")
        self.guide.unlink()
        shutil.rmtree(self.skill)
        self.run_installer("--uninstall")
        self.assertFalse(self.guide_link.is_symlink())
        self.assertFalse(self.skill_link.is_symlink())
        self.assertEqual(unrelated.read_text(), "Preserve")
        self.run_installer("--uninstall")

    def test_uninstall_preserves_replaced_file_and_changed_link(self):
        self.run_installer()
        self.guide_link.unlink()
        self.guide_link.write_text("New user guide")
        self.skill_link.unlink()
        other = self.root / "other skill"
        other.mkdir()
        self.skill_link.symlink_to(other)
        result = self.run_installer("--uninstall")
        self.assertIn("Preserved", result.stdout)
        self.assertEqual(self.guide_link.read_text(), "New user guide")
        self.assertEqual(os.readlink(self.skill_link), str(other))


if __name__ == "__main__":
    unittest.main()

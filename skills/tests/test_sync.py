"""Exercise the published installer and updater using local archives and fake homes."""

import io
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest


SKILLS_ROOT = Path(__file__).resolve().parents[1]
SYNC = SKILLS_ROOT / "sync.sh"


class SyncTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.home = self.root / "home with spaces"
        self.cache = self.home / ".local/share/dotfiles-skills"
        self.guide = self.home / ".codex/AGENTS.md"
        self.skill = self.home / ".agents/skills/engineering-work"
        self.archive = self.root / "release.tar.gz"
        self.make_archive("v1")

    def make_archive(self, version, omit=None, extras=()):
        files = {
            "agents/AGENTS.md": f"Guide {version}\n",
            "agents/refinement.py": (SKILLS_ROOT.parent / "agents/refinement.py").read_text(),
            "agents/dotfiles-refinement": (SKILLS_ROOT.parent / "agents/dotfiles-refinement").read_text(),
            "skills/sync.sh": SYNC.read_text(),
            "skills/engineering-work/SKILL.md": f"Workflow {version}\n",
            "skills/engineering-work/references/work-record.md": f"Record {version}\n",
            "skills/engineering-work/references/steering.md": f"Steering {version}\n",
        }
        for name in extras:
            files[f"skills/{name}/SKILL.md"] = f"{name} {version}\n"
        if omit:
            del files[omit]
        with tarfile.open(self.archive, "w:gz") as archive:
            for name, content in files.items():
                data = content.encode()
                info = tarfile.TarInfo("dotfiles-main/" + name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))

    def run_sync(self, expected=0, extra_env=None, script=SYNC):
        env = dict(os.environ)
        for key in ("CODEX_HOME", "DOTFILES_CODEX_HOME", "DOTFILES_SKILLS_RAW_BASE"):
            env.pop(key, None)
        env.update(DOTFILES_SKILLS_HOME=str(self.home),
                   DOTFILES_SKILLS_ARCHIVE_URL=self.archive.as_uri())
        if extra_env:
            env.update(extra_env)
        result = subprocess.run(["bash", str(script)], env=env, text=True,
                                capture_output=True, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_fresh_install_and_update_use_one_release(self):
        self.run_sync()
        first = (self.cache / "current").resolve()
        self.assertEqual(self.guide.read_text(), "Guide v1\n")
        self.assertEqual((self.skill / "SKILL.md").read_text(), "Workflow v1\n")
        self.assertEqual(self.guide.resolve().parent, self.skill.resolve().parent)
        self.make_archive("v2")
        self.run_sync()
        self.assertEqual(self.guide.read_text(), "Guide v2\n")
        self.assertEqual((self.skill / "SKILL.md").read_text(), "Workflow v2\n")
        self.assertEqual(self.guide.resolve().parent, self.skill.resolve().parent)
        self.assertFalse(first.exists())

    def test_legacy_local_pilot_migrates_both_links(self):
        self.guide.parent.mkdir(parents=True)
        self.skill.parent.mkdir(parents=True)
        self.guide.symlink_to(self.home / "code/dotfiles/agents/AGENTS.md")
        self.skill.symlink_to(self.home / "code/dotfiles/skills/engineering-work")
        self.run_sync()
        self.assertEqual(os.readlink(self.guide), str(self.cache / "current/AGENTS.md"))
        self.assertEqual(os.readlink(self.skill), str(self.cache / "current/engineering-work"))

    def test_unrelated_guide_is_preserved_and_update_does_not_advance(self):
        self.run_sync()
        previous = (self.cache / "current").resolve()
        self.guide.unlink()
        self.guide.write_text("My personal instructions")
        self.make_archive("v2")
        self.run_sync(expected=1)
        self.assertEqual(self.guide.read_text(), "My personal instructions")
        self.assertEqual((self.cache / "current").resolve(), previous)
        self.assertEqual((self.skill / "SKILL.md").read_text(), "Workflow v1\n")

    def test_override_prevents_shadowed_install(self):
        self.guide.parent.mkdir(parents=True)
        override = self.guide.parent / "AGENTS.override.md"
        override.symlink_to(self.root / "missing-override")
        self.run_sync(expected=1)
        self.assertTrue(override.is_symlink())
        self.assertFalse((self.cache / "current").exists())
        self.assertFalse(self.guide.is_symlink())

    def test_conflicting_core_skill_stops_before_install(self):
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("Custom workflow")
        self.run_sync(expected=1)
        self.assertEqual((self.skill / "SKILL.md").read_text(), "Custom workflow")
        self.assertFalse(self.guide.is_symlink())

    def test_incomplete_archives_preserve_the_previous_release(self):
        self.run_sync()
        previous = (self.cache / "current").resolve()
        for missing in ("agents/AGENTS.md", "skills/engineering-work/SKILL.md",
                        "skills/engineering-work/references/work-record.md",
                        "skills/engineering-work/references/steering.md", "agents/refinement.py",
                        "agents/dotfiles-refinement", "skills/sync.sh"):
            with self.subTest(missing=missing):
                self.make_archive("v2", omit=missing)
                self.run_sync(expected=1)
                self.assertEqual((self.cache / "current").resolve(), previous)
                self.assertEqual(self.guide.read_text(), "Guide v1\n")
                self.assertEqual(len(list((self.cache / "releases").iterdir())), 1)

    def test_download_failure_preserves_existing_install(self):
        self.run_sync()
        previous = (self.cache / "current").resolve()
        self.run_sync(expected=37, extra_env={
            "DOTFILES_SKILLS_ARCHIVE_URL": (self.root / "missing.tar.gz").as_uri(),
        })
        self.assertEqual((self.cache / "current").resolve(), previous)
        self.assertEqual(self.guide.read_text(), "Guide v1\n")

    def test_custom_codex_home_survives_timer_environment(self):
        custom = self.root / "custom codex"
        self.run_sync(extra_env={"DOTFILES_CODEX_HOME": str(custom)})
        self.make_archive("v2")
        self.run_sync()
        self.assertEqual((custom / "AGENTS.md").read_text(), "Guide v2\n")
        self.assertFalse(self.guide.exists())
        self.assertEqual((self.cache / "codex-home").read_text(), str(custom) + "\n")

    def test_removed_skills_are_pruned_only_when_still_owned(self):
        self.make_archive("v1", extras=("removed", "customized"))
        self.run_sync()
        custom = self.skill.parent / "customized"
        custom.unlink()
        custom.mkdir()
        (custom / "SKILL.md").write_text("My version")
        self.make_archive("v2")
        self.run_sync()
        self.assertFalse((self.skill.parent / "removed").is_symlink())
        self.assertEqual((custom / "SKILL.md").read_text(), "My version")

    def test_unmanaged_cache_pointer_is_not_deleted_or_replaced(self):
        other = self.root / "personal-files"
        other.mkdir()
        (other / "keep.txt").write_text("keep")
        self.cache.mkdir(parents=True)
        (self.cache / "current").symlink_to(other)
        self.run_sync(expected=1)
        self.assertEqual((self.cache / "current").resolve(), other)
        self.assertEqual((other / "keep.txt").read_text(), "keep")

    def test_supporting_skill_conflict_is_preserved(self):
        self.make_archive("v1", extras=("technical-writing",))
        custom = self.skill.parent / "technical-writing"
        custom.mkdir(parents=True)
        (custom / "SKILL.md").write_text("Personal writing")
        result = self.run_sync()
        self.assertIn("Skipping", result.stderr)
        self.assertEqual((custom / "SKILL.md").read_text(), "Personal writing")
        self.assertEqual(self.guide.read_text(), "Guide v1\n")

    def test_handoff_hook_installs_and_disable_survives_updates(self):
        self.run_sync()
        launcher = self.home / ".local/bin/dotfiles-refinement"
        self.assertTrue(launcher.is_symlink())
        hooks = self.home / ".codex/hooks.json"
        import json
        configured = json.loads(hooks.read_text())["hooks"]
        self.assertEqual(set(configured), {"UserPromptSubmit", "Stop"})
        env = dict(os.environ, DOTFILES_SKILLS_HOME=str(self.home),
                   CODEX_THREAD_ID="dotfiles-port-test", TMPDIR=str(self.root))
        def event(name):
            command = configured[name][0]["hooks"][0]["command"]
            result = subprocess.run(command, shell=True, env=env, text=True,
                                    input=json.dumps({"hook_event_name": name,
                                                      "session_id":"dotfiles-port-test", "turn_id":"request-a",
                                                      "stop_hook_active":False}),
                                    capture_output=True, check=True)
            return json.loads(result.stdout)
        event("UserPromptSubmit")
        lock = self.cache / "sync.lock"
        lock.chmod(0o400)
        try:
            result = subprocess.run([str(launcher), "handoff", "--task", "Finish verified implementation"],
                                    env=env, text=True, capture_output=True, check=True)
            self.assertIn("armed", result.stdout)
        finally:
            lock.chmod(0o600)
        self.assertEqual(event("Stop")["decision"], "block")
        self.assertEqual(event("Stop"), {})
        subprocess.run([str(launcher), "disable"], env=env, capture_output=True, check=True)
        self.make_archive("v2")
        self.run_sync()
        self.assertEqual(json.loads(hooks.read_text())["hooks"], {})
        self.assertEqual(self.guide.read_text(), "Guide v2\n")
        self.assertEqual((self.cache / "archive-url").read_text().strip(), self.archive.as_uri())

    def test_published_installer_bootstraps_framework_and_timer(self):
        raw = self.root / "raw/skills"
        (raw / "systemd").mkdir(parents=True)
        for name in ("sync.sh", "systemd/dotfiles-skills-sync.service",
                     "systemd/dotfiles-skills-sync.timer"):
            shutil.copyfile(SKILLS_ROOT / name, raw / name)
        binaries = self.root / "bin"
        binaries.mkdir()
        systemctl = binaries / "systemctl"
        systemctl.write_text("#!/bin/sh\nexit 0\n")
        systemctl.chmod(0o755)
        self.run_sync(script=SKILLS_ROOT / "install.sh", extra_env={
            "DOTFILES_SKILLS_RAW_BASE": (self.root / "raw").as_uri(),
            "PATH": str(binaries) + os.pathsep + os.environ["PATH"],
        })
        self.assertEqual(self.guide.read_text(), "Guide v1\n")
        helper = self.home / ".local/bin/dotfiles-skills-sync"
        self.assertEqual(helper.read_bytes(), SYNC.read_bytes())
        unit = self.home / ".config/systemd/user/dotfiles-skills-sync.timer"
        self.assertTrue(unit.is_file())
        self.make_archive("v2")
        self.run_sync(script=helper)
        self.assertEqual(self.guide.read_text(), "Guide v2\n")
        self.assertEqual((self.skill / "SKILL.md").read_text(), "Workflow v2\n")


if __name__ == "__main__":
    unittest.main()

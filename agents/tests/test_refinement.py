"""Exercise hook registration, task state and Codex's JSON event protocol."""

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "agents/refinement.py"


class RefinementTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="refinement test ")
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.codex = self.home / "custom codex"
        self.state = self.home / "state"
        self.env = dict(os.environ, CODEX_THREAD_ID="session-a")
        self.call("enable")
        self.submit()

    def call(self, *args, event=None, check=True, raw=None):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                *args,
                "--codex-home",
                str(self.codex),
                "--state-dir",
                str(self.state),
            ],
            input=(
                raw
                if raw is not None
                else json.dumps(event) if event is not None else None
            ),
            env=self.env,
            text=True,
            capture_output=True,
            timeout=10,
        )
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def event(self, active=False, **extra):
        return self.call(
            "event",
            event={
                "hook_event_name": "Stop",
                "session_id": "session-a",
                "turn_id": "turn-a",
                "stop_hook_active": active,
                **extra,
            },
        )

    def submit(self, prompt="Implement the requested feature", turn="turn-a"):
        return self.call(
            "event",
            event={
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-a",
                "turn_id": turn,
                "prompt": prompt,
            },
        )

    def status(self):
        return json.loads(self.call("status").stdout)

    def handoff(self, *args):
        self.call("handoff", "--task", "Preserve local work without publishing", *args)

    def test_once_per_task_survives_duplicate_events_and_new_processes(self):
        self.assertEqual(json.loads(self.event().stdout), {})
        self.handoff()
        result = json.loads(self.event().stdout)
        self.assertEqual(result["decision"], "block")
        self.assertIn("Preserve local work without publishing", result["reason"])
        self.assertEqual(self.status()["task"]["status"], "consumed")
        for active in (True, False):
            self.assertEqual(json.loads(self.event(active).stdout), {})
        self.handoff()
        self.assertEqual(json.loads(self.event().stdout), {})
        self.handoff("--new-task")
        self.assertEqual(json.loads(self.event().stdout)["decision"], "block")

    def test_concurrent_stops_claim_only_one_nudge(self):
        self.handoff()
        with ThreadPoolExecutor(max_workers=6) as pool:
            outputs = list(
                pool.map(lambda _: json.loads(self.event().stdout), range(6))
            )
        self.assertEqual(
            sum(result.get("decision") == "block" for result in outputs), 1
        )

    def test_cancelled_task_and_active_hook_do_not_restart(self):
        self.handoff()
        self.call("skip")
        self.assertEqual(json.loads(self.event().stdout), {})
        self.handoff()
        self.assertEqual(json.loads(self.event(True).stdout), {})
        self.assertEqual(self.status()["task"]["status"], "cancelled")
        self.assertEqual(json.loads(self.event().stdout), {})

    def test_session_isolation_and_compaction_does_not_rearm(self):
        self.handoff()
        self.assertEqual(json.loads(self.event(session_id="other-session").stdout), {})
        self.event()
        response = json.loads(
            self.call(
                "event", event={"hook_event_name": "SessionStart", "source": "compact"}
            ).stdout
        )
        self.assertEqual(response, {})
        self.assertEqual(self.status()["task"]["status"], "consumed")
        self.assertEqual(json.loads(self.event().stdout), {})

    def test_reviews_direct_requests_and_other_flows_do_not_inherit_handoffs(self):
        for number, prompt in enumerate(
            (
                "Review this PR",
                "Explain this function",
                "Push this now",
                "Rebase this stack",
                "Investigate the failure",
                "Discuss the design",
            )
        ):
            with self.subTest(prompt=prompt):
                self.handoff("--new-task")
                turn = f"request-{number}"
                self.submit(prompt, turn)
                self.assertEqual(json.loads(self.event(turn_id=turn).stdout), {})
                self.assertEqual(self.status()["task"]["status"], "cancelled")
        # Even if a prompt callback is missing, a different turn cannot inherit it.
        self.handoff()
        self.assertEqual(
            json.loads(self.event(turn_id="unobserved-new-turn").stdout), {}
        )

    def test_handoff_requires_prompt_receipt_and_ignores_legacy_arming(self):
        self.env["CODEX_THREAD_ID"] = "session-without-prompt-hook"
        self.handoff()
        self.assertIsNone(self.status()["task"])
        self.env["CODEX_THREAD_ID"] = "session-a"
        path = self.state / (hashlib.sha256(b"session-a").hexdigest() + ".json")
        path.write_text(
            json.dumps(
                {"status": "armed", "task": "old broad task", "turn_id": "turn-a"}
            )
        )
        self.assertEqual(json.loads(self.event().stdout), {})

    def test_old_startup_hook_is_replaced_without_changing_stop_definition(self):
        path = self.codex / "hooks.json"
        data = json.loads(path.read_text())
        stop = data["hooks"]["Stop"]
        data["hooks"]["SessionStart"] = stop
        del data["hooks"]["UserPromptSubmit"]
        path.write_text(json.dumps(data))
        self.call("enable")
        updated = json.loads(path.read_text())
        self.assertNotIn("SessionStart", updated["hooks"])
        self.assertEqual(updated["hooks"]["Stop"], stop)
        self.assertTrue(self.status()["enabled"])

    def test_malformed_events_and_state_allow_completion(self):
        self.handoff()
        for raw in (
            "invalid JSON",
            "[]",
            "{}",
            '{"hook_event_name":"Stop","session_id":"session-a"}',
            '{"hook_event_name":"Stop","session_id":"session-a","stop_hook_active":"false"}',
        ):
            with self.subTest(raw=raw):
                self.assertEqual(json.loads(self.call("event", raw=raw).stdout), {})
        path = self.state / (hashlib.sha256(b"session-a").hexdigest() + ".json")
        path.write_text("broken state")
        self.assertEqual(json.loads(self.event().stdout), {})
        self.assertEqual(path.read_text(), "broken state")

    def test_disabled_hook_does_not_arm_or_continue(self):
        self.handoff()
        self.call("disable")
        self.assertEqual(json.loads(self.event().stdout), {})
        self.assertEqual(
            json.loads(
                self.call("event", event={"hook_event_name": "SessionStart"}).stdout
            ),
            {},
        )
        self.call("handoff", "--task", "Different work", "--new-task")
        self.assertFalse(self.status()["enabled"])
        self.assertEqual(
            self.status()["task"]["task"], "Preserve local work without publishing"
        )

    def test_registration_is_idempotent_and_preserves_other_hooks(self):
        self.call("disable")
        path = self.codex / "hooks.json"
        custom = {
            "description": "mine",
            "hooks": {
                "Stop": [{"hooks": [{"type": "command", "command": "my-check"}]}],
                "OtherEvent": [{"custom": True}],
            },
        }
        path.write_text(json.dumps(custom))
        toml = self.codex / "config.toml"
        toml.write_text("[hooks]\n# Other inline hooks remain untouched.\n")
        self.call("enable")
        first = path.read_text()
        self.call("enable")
        self.assertEqual(path.read_text(), first)
        self.assertTrue(self.status()["enabled"])
        self.call("disable")
        self.assertEqual(json.loads(path.read_text()), custom)
        self.assertEqual(
            toml.read_text(), "[hooks]\n# Other inline hooks remain untouched.\n"
        )

    def test_customized_or_invalid_configuration_is_preserved(self):
        path = self.codex / "hooks.json"
        data = json.loads(path.read_text())
        data["hooks"]["Stop"][0]["hooks"][0]["timeout"] = 7
        path.write_text(json.dumps(data))
        for action in ("enable", "disable"):
            before = path.read_bytes()
            self.assertNotEqual(self.call(action, check=False).returncode, 0)
            self.assertEqual(path.read_bytes(), before)
        for content in (
            "not JSON",
            '{"hooks":{"Stop":{}}}',
            '{"hooks":{"Stop":[{"hooks":null}]}}',
        ):
            path.write_text(content)
            self.assertNotEqual(self.call("enable", check=False).returncode, 0)
            self.assertEqual(path.read_text(), content)
        target = self.home / "external.json"
        target.write_text("{}")
        path.unlink()
        path.symlink_to(target)
        self.assertNotEqual(self.call("enable", check=False).returncode, 0)
        self.assertEqual(target.read_text(), "{}")

    def test_registration_command_executes_with_spaces_and_current_symlink(self):
        package = self.home / "managed package"
        (package / "hooks").mkdir(parents=True)
        (package / "hooks/refinement.py").write_bytes(SCRIPT.read_bytes())
        current = self.home / "current"
        current.symlink_to(package)
        helper = current / "hooks/refinement.py"
        codex = self.home / "separate codex"
        subprocess.run(
            [sys.executable, str(helper), "enable", "--codex-home", str(codex)],
            check=True,
            capture_output=True,
        )
        command = json.loads((codex / "hooks.json").read_text())["hooks"][
            "UserPromptSubmit"
        ][0]["hooks"][0]["command"]
        self.assertIn(str(current), command)
        env = dict(self.env, CODEX_HOME=str(codex), TMPDIR=str(self.home))
        result = subprocess.run(
            command,
            shell=True,
            input='{"hook_event_name":"UserPromptSubmit","session_id":"fixture","turn_id":"first"}',
            env=env,
            text=True,
            capture_output=True,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {})


if __name__ == "__main__":
    unittest.main()

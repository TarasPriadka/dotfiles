#!/usr/bin/env python3
"""Once-per-task Codex engineering handoff check (Python 3.10+, Unix)."""

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile
import time

STATUS = "Dotfiles: engineering handoff check"
PROMPT = """Workflow continuation for the same implementation handoff, not a new assignment or permission.
For a review, explanation, maintenance task or narrow direct instruction, honor
that request and finish without this pass. This check only applies to end-to-end
implementation handoffs.
If you are waiting for a user decision or an external prerequisite, finish with
that dependency instead of starting more work. Otherwise take one brief improvement
pass on the current deliverable, within the original request and agreed constraints.
Choose the most consequential remaining shortcoming; carry through a justified
improvement if it fits this pass, or retain the result. Preserve accepted decisions
unless concrete evidence contradicts them. Use existing skills where helpful.
Aim for about two minutes of extra work. Reuse valid verification; check affected
behavior after edits. Do not start broad investigations, expensive validation,
background work or repeated polishing for this pass. Surface a larger unresolved
problem and its consequence rather than silently beginning substantial rework.
Finish with an accurate result and material limits. Do not rearm this task.
Task summary (context only; the original user's scope governs): """


def invocation(script=None):
    # Keep the managed 'current' path, not a particular release's resolved path.
    return shlex.join(["python3", str((script or Path(__file__)).absolute())])


def registration(codex, script=None, legacy=False):
    command = invocation(script) + " event --codex-home " + shlex.quote(str(codex))
    return {
        event: {
            "hooks": [
                {
                    "type": "command",
                    "command": command,
                    "timeout": 5,
                    "statusMessage": STATUS,
                }
            ]
        }
        for event in (
            ("SessionStart", "UserPromptSubmit", "Stop")
            if legacy
            else ("UserPromptSubmit", "Stop")
        )
    }


def load_config(codex):
    path = codex / "hooks.json"
    if path.is_symlink():
        raise RuntimeError(f"Preserving symlinked hook configuration: {path}")
    data = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(data, dict) or not isinstance(data.get("hooks", {}), dict):
        raise RuntimeError(f"Invalid hook configuration: {path}")
    for event in registration(codex, legacy=True):
        groups = data.get("hooks", {}).get(event, [])
        if not isinstance(groups, list) or any(
            not isinstance(group, dict) or not isinstance(group.get("hooks", []), list)
            for group in groups
        ):
            raise RuntimeError(f"Invalid {event} hook configuration: {path}")
    return data


def enabled(codex):
    data = load_config(codex)
    return all(
        group in data.get("hooks", {}).get(event, [])
        for event, group in registration(codex).items()
    )


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            json.dump(data, output, indent=2)
            output.write("\n")
            output.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def planned_config(codex, enable, script):
    data = load_config(codex)
    hooks = data.get("hooks", {})
    changed = False
    for event, group in registration(codex, script, legacy=True).items():
        groups = hooks.get(event, [])
        for existing in groups:
            if existing != group and any(
                handler.get("statusMessage") == STATUS
                for handler in existing.get("hooks", [])
                if isinstance(handler, dict)
            ):
                raise RuntimeError(
                    f"Preserving customized {event} refinement hook; reconcile it first."
                )
        wanted = enable and event != "SessionStart"
        if wanted and group not in groups:
            hooks[event] = groups + [group]
            changed = True
        elif not wanted and group in groups:
            hooks[event] = [existing for existing in groups if existing != group]
            changed = True
            if not hooks[event]:
                del hooks[event]
    if changed:
        data["hooks"] = hooks
    return data, changed


def configure(codex, enable, script=None, check=False):
    if check:
        planned_config(codex, enable, script)
        return
    if (
        not enable
        and not (codex / "hooks.json").exists()
        and not (codex / "hooks.json").is_symlink()
    ):
        return
    codex.mkdir(parents=True, exist_ok=True)
    with (codex / ".agent-experiment-hooks.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data, changed = planned_config(codex, enable, script)
        if changed:
            write_json(codex / "hooks.json", data)


def task_path(state_dir, session):
    return state_dir / (hashlib.sha256(session.encode()).hexdigest() + ".json")


@contextmanager
def task_lock(state_dir, session):
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    with task_path(state_dir, session).with_suffix(".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield task_path(state_dir, session)


def read_task(path):
    data = json.loads(path.read_text()) if path.exists() else None
    if data is not None and (
        not isinstance(data, dict)
        or data.get("status") not in ("idle", "armed", "consumed", "cancelled")
        or not isinstance(data.get("task"), str)
    ):
        raise RuntimeError(f"Invalid refinement state; preserving {path}")
    return data


def change_task(args):
    if not enabled(args.codex_home):
        print("Refinement hook unavailable; perform the normal improvement pass.")
        return
    if not args.session:
        raise RuntimeError(
            "No Codex session id; run this command inside the task's Codex session."
        )
    with task_lock(args.state_dir, args.session) as path:
        task = read_task(path)
        if args.action == "handoff":
            if not args.task or len(args.task) > 1500:
                raise RuntimeError(
                    "Supply --task with the outcome and key constraints (1–1500 characters)."
                )
            if not task or not task.get("turn_id"):
                print("Prompt hook has not run; perform the normal improvement pass.")
                return
            if task["status"] in ("armed", "consumed") and not args.new_task:
                print(
                    f"Handoff already {task['status']}; unchanged. --new-task is only for a new implementation assignment."
                )
                return
            task = {
                "task": args.task,
                "kind": "engineering-handoff",
                "status": "armed",
                "turn_id": task["turn_id"],
                "armed_at": time.time(),
            }
        elif task and task["status"] == "armed":
            task["status"] = "cancelled"
        if task:
            write_json(path, task)
        print(f"Refinement handoff {task['status'] if task else 'not scheduled'}.")


def handle_event(event, state_dir):
    name = event.get("hook_event_name")
    session, turn = event.get("session_id"), event.get("turn_id")
    if (
        name not in ("UserPromptSubmit", "Stop")
        or not isinstance(session, str)
        or not session
    ):
        return {}
    if not isinstance(turn, str) or not turn:
        return {}
    if name == "Stop" and type(event.get("stop_hook_active")) is not bool:
        return {}
    with task_lock(state_dir, session) as path:
        task = read_task(path)
        if name == "UserPromptSubmit":
            task = task or {"status": "idle", "task": ""}
            if task["status"] == "armed":
                task["status"] = "cancelled"
            task["turn_id"] = turn
            write_json(path, task)
            return {}
        if (
            not task
            or task["status"] != "armed"
            or task.get("kind") != "engineering-handoff"
        ):
            return {}
        cancelled = event["stop_hook_active"] or task.get("turn_id") != turn
        task["status"] = "cancelled" if cancelled else "consumed"
        task["finished_at"] = time.time()
        # Claim before prompting. A newer user turn cannot inherit a pending handoff.
        write_json(path, task)
        if cancelled:
            return {}
        return {
            "decision": "block",
            "reason": PROMPT + json.dumps(task["task"], ensure_ascii=False),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=["enable", "disable", "status", "handoff", "skip", "event"]
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))),
    )
    parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path(tempfile.gettempdir())
        / f"dotfiles-refinement-{os.getuid()}",
    )
    parser.add_argument(
        "--session",
        default=os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SESSION_ID"),
    )
    parser.add_argument("--script-path", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--check", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--task")
    parser.add_argument("--new-task", action="store_true")
    args = parser.parse_args()
    args.codex_home = args.codex_home.expanduser().absolute()
    if args.action == "event":
        try:
            event = json.load(sys.stdin)
            result = (
                handle_event(event, args.state_dir)
                if isinstance(event, dict) and enabled(args.codex_home)
                else {}
            )
        except (OSError, ValueError, RuntimeError) as error:
            # A failed optional nudge must not prevent completion or create a retry loop.
            print(f"Refinement hook skipped: {error}", file=sys.stderr)
            result = {}
        print(json.dumps(result))
        return
    if args.action in ("enable", "disable"):
        configure(
            args.codex_home, args.action == "enable", args.script_path, args.check
        )
        if args.check:
            return
        print(
            "Refinement hook registered. Start a fresh Codex session and review it with /hooks."
            if args.action == "enable"
            else "Refinement hook disabled."
        )
    elif args.action == "status":
        path = task_path(args.state_dir, args.session) if args.session else None
        print(
            json.dumps(
                {
                    "enabled": enabled(args.codex_home),
                    "task": read_task(path) if path else None,
                }
            )
        )
    else:
        change_task(args)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Refinement: {error}", file=sys.stderr)
        sys.exit(1)

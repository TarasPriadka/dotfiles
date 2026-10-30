#!/usr/bin/env python3
"""Read-only matching of a prepared review to staged or committed Git contents."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


REQUIRED_CHECKS = {"code-review", "design", "scope", "verification"}
FINISHED = {"complete", "limited", "not-applicable"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )


def commit(repo, ref):
    result = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}")
    return result.stdout.strip() if result.returncode == 0 else None


def check(entry, repo, base, head):
    result = {"status": "incomplete", "reasons": [], "edited_reports": []}
    try:
        state = json.loads((entry / "state.json").read_text())
    except (OSError, ValueError):
        result["reasons"].append("No readable completion record; keep existing reports.")
        return result
    if not isinstance(state, dict):
        result["reasons"].append("Completion record is not an object.")
        return result
    checks, files, rules = (
        state.get("checks"), state.get("files"), state.get("review_rules")
    )
    if (
        not isinstance(checks, dict)
        or not REQUIRED_CHECKS.issubset(checks)
        or any(not isinstance(value, str) or value not in FINISHED for value in checks.values())
        or checks.get("code-review") != "complete"
        or not isinstance(files, dict)
        or "review.md" not in files
        or not isinstance(rules, dict)
        or not rules
        or not isinstance(state.get("base"), str)
        or not isinstance(state.get("head"), str)
    ):
        result["reasons"].append("Review preparation is incomplete or uses explanation-only metadata.")
        return result

    required_reports = {"review.md"} | {f"checks/{name}.md" for name in checks}
    if not required_reports.issubset(files):
        result["reasons"].append("Completion record does not include all check reports.")
        return result
    for name, expected in files.items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            result["reasons"].append("Report path must stay within the entry.")
            return result
        try:
            if sha256(entry / relative) != expected:
                result["edited_reports"].append(name)
        except OSError:
            result["reasons"].append(f"Missing report: {name}")
            return result

    result["status"] = "unverified"
    refs = [state["base"], state["head"], base]
    resolved = [commit(repo, ref) for ref in refs]
    if any(ref is None for ref in resolved):
        result["reasons"].append("Reviewed or current Git objects are unavailable.")
        return result
    reviewed_base, reviewed_head, current_base = resolved
    diff_options = ["--no-ext-diff", "--no-textconv", "--quiet"]
    comparisons = [("base context", [*diff_options, reviewed_base, current_base, "--"])]
    if head == "index":
        unmerged = git(repo, "ls-files", "--unmerged")
        if unmerged.returncode or unmerged.stdout:
            result["reasons"].append("Cannot match an unavailable or unmerged index.")
            return result
        comparisons.append(("staged content", ["--cached", *diff_options, reviewed_head, "--"]))
    else:
        current_head = commit(repo, head)
        if current_head is None:
            result["reasons"].append("Current head is unavailable.")
            return result
        comparisons.append(("target content", [*diff_options, reviewed_head, current_head, "--"]))

    differences = []
    for label, args in comparisons:
        compared = git(repo, "diff", *args)
        if compared.returncode not in (0, 1):
            result["reasons"].append(f"Could not compare {label}.")
            return result
        if compared.returncode == 1:
            differences.append(f"Changed {label}; assess its impact on saved conclusions.")
    for name, expected in rules.items():
        path = Path(name)
        try:
            actual = sha256(path if path.is_absolute() else repo / path)
        except OSError:
            result["reasons"].append(f"Review instructions unavailable: {name}")
            return result
        if actual != expected:
            differences.append(f"Changed review instructions: {name}; assess the resulting gaps.")
    result["status"] = "changed" if differences else "reusable"
    result["reasons"] = differences
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True, help="Git commit reference or 'index'")
    args = parser.parse_args()
    print(json.dumps(check(args.entry, args.repo, args.base, args.head), indent=2))


if __name__ == "__main__":
    main()

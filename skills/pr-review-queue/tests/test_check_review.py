import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_review.py"


class ReviewComparisonTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Queue test")
        self.git("config", "user.email", "queue@example.invalid")
        self.git("config", "core.filemode", "true")
        self.git("config", "core.autocrlf", "false")
        (self.repo / "REVIEW.md").write_text("Review the actual behavior.\n")
        (self.repo / "app.py").write_text("answer = 1\n")
        self.git("add", "REVIEW.md", "app.py")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD").strip()
        (self.repo / "app.py").write_text("answer = 2\n")
        self.git("add", "app.py")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "reviewed head")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.git("reset", "--soft", self.base)
        self.entry = self.root / "entry"
        (self.entry / "checks").mkdir(parents=True)
        self.state = {
            "base": self.base,
            "head": self.head,
            "checks": {
                "code-review": "complete", "design": "complete",
                "scope": "not-applicable", "verification": "limited",
            },
            "review_rules": {"REVIEW.md": self.digest(self.repo / "REVIEW.md")},
            "files": {},
        }
        for name in ["review.md", *(f"checks/{key}.md" for key in self.state["checks"])]:
            path = self.entry / name
            path.write_text("Saved result with its limits.\n")
            self.state["files"][name] = self.digest(path)
        self.save()

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-C", str(self.repo), *args], text=True, stderr=subprocess.PIPE
        )

    @staticmethod
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def save(self):
        (self.entry / "state.json").write_text(json.dumps(self.state))

    def check(self, head="index"):
        result = subprocess.check_output(
            [sys.executable, str(SCRIPT), "--entry", str(self.entry),
             "--repo", str(self.repo), "--base", "HEAD", "--head", head], text=True
        )
        return json.loads(result)

    def test_soft_reset_reuses_review_without_writes(self):
        before = self.git("status", "--porcelain=v1")
        self.assertEqual("reusable", self.check()["status"])
        self.assertEqual(before, self.git("status", "--porcelain=v1"))

    def test_unstaged_edits_are_excluded(self):
        (self.repo / "app.py").write_text("answer = 3\n")
        self.assertEqual("reusable", self.check()["status"])
        self.git("add", "app.py")
        self.assertEqual("changed", self.check()["status"])

    def test_different_commit_with_same_tree_reuses_review(self):
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "new commit identity")
        self.assertNotEqual(self.head, self.git("rev-parse", "HEAD").strip())
        # The caller resolves the actual base for a committed comparison.
        result = subprocess.check_output(
            [sys.executable, str(SCRIPT), "--entry", str(self.entry),
             "--repo", str(self.repo), "--base", self.base, "--head", "HEAD"], text=True
        )
        self.assertEqual("reusable", json.loads(result)["status"])

    def test_changed_base_context_is_detected(self):
        self.git("restore", "--staged", "app.py")
        (self.repo / "dependency.py").write_text("changed dependency\n")
        self.git("add", "dependency.py")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "base context changed")
        self.git("add", "app.py")
        result = self.check()
        self.assertEqual("changed", result["status"])
        self.assertTrue(any("base context" in reason for reason in result["reasons"]))

    def test_missing_and_edited_reports_are_distinct(self):
        report = self.entry / "review.md"
        report.write_text("User edited the explanation.\n")
        result = self.check()
        self.assertEqual("reusable", result["status"])
        self.assertEqual(["review.md"], result["edited_reports"])
        report.unlink()
        self.assertEqual("incomplete", self.check()["status"])

    def test_rules_change_requires_impact_assessment(self):
        (self.repo / "REVIEW.md").write_text("A newly required review check.\n")
        self.assertEqual("changed", self.check()["status"])

    def test_legacy_explanation_is_not_a_completed_review(self):
        self.state = {"progress": "ready", "head_sha": self.head}
        self.save()
        self.assertEqual("incomplete", self.check()["status"])

    def test_missing_objects_leave_freshness_unverified(self):
        self.state["head"] = "0" * 40
        self.save()
        self.assertEqual("unverified", self.check()["status"])

    def test_missing_check_does_not_claim_ready(self):
        self.state["checks"]["code-review"] = "incomplete"
        self.save()
        self.assertEqual("incomplete", self.check()["status"])

    def test_malformed_check_does_not_crash(self):
        self.state["checks"]["design"] = {}
        self.save()
        self.assertEqual("incomplete", self.check()["status"])

    def test_mode_changes_are_detected(self):
        self.git("update-index", "--chmod=+x", "app.py")
        self.assertEqual("changed", self.check()["status"])


if __name__ == "__main__":
    unittest.main()

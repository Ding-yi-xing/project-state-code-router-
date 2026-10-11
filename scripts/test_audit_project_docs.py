import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_project_docs as audit


class AuditTests(unittest.TestCase):
    def make_project(self, root: Path) -> None:
        docs = root / "docs"
        (docs / "shared" / "current").mkdir(parents=True)
        (docs / "navigation.md").write_text("# Navigation\n", encoding="utf-8")
        (docs / "process").mkdir()
        (docs / "process" / "000-init.md").write_text("# Init\n", encoding="utf-8")
        (docs / "units" / "sample" / "requirements").mkdir(parents=True)
        for folder in ("blockers", "issues", "sync", "archive"):
            (docs / "units" / "sample" / folder).mkdir(parents=True, exist_ok=True)
        manifest = {
            "schema_version": 1,
            "structure_version": 1,
            "initialized_by": "test",
            "initialized_at": "2026-10-05",
            "responsibility_lookup": {"primary_source": "docs/.project-docs-manifest.yaml", "fallback_action": "ask-user"},
            "roles": {"pm": {"entry": "docs/navigation.md"}},
            "work_units": [{"key": "sample", "label": "Sample", "owner": "test", "entry": "docs/units/sample/manifest.md"}],
            "active_core_files": ["docs/shared/current/scope.md"],
        }
        (docs / ".project-docs-manifest.yaml").write_text(audit.yaml.safe_dump(manifest), encoding="utf-8")
        (docs / "shared" / "current" / "scope.md").write_text(
            "---\nstatus: active\nauthority: current\nowner: pm\nlast_verified: 2026-10-05\n---\n# Scope\n", encoding="utf-8"
        )
        unit = docs / "units" / "sample"
        (unit / "README.md").write_text("# Sample\n", encoding="utf-8")
        (unit / "manifest.md").write_text("# Manifest\n", encoding="utf-8")
        (unit / "status.md").write_text("# Status\n", encoding="utf-8")
        for path in ("requirements/index.md", "blockers/index.md", "issues/index.md", "sync/outward-needs.md", "archive/index.md"):
            (unit / path).write_text("# Index\n", encoding="utf-8")

    def test_valid_minimal_project_has_no_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root)
            findings = audit.audit(root, 30)
            self.assertEqual([], findings)

    def test_invalid_manifest_is_reported_without_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            manifest = docs / ".project-docs-manifest.yaml"
            original = "schema_version: [broken\n"
            manifest.write_text(original, encoding="utf-8")
            findings = audit.audit(root, 30)
            self.assertIn("MANIFEST_INVALID_YAML", {item.code for item in findings})
            self.assertEqual(original, manifest.read_text(encoding="utf-8"))

    def test_terminal_plan_in_active_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root)
            plan = root / "docs" / "shared" / "exec-plans" / "active" / "done.md"
            plan.parent.mkdir(parents=True)
            plan.write_text("---\nstatus: done\n---\n# Done\n", encoding="utf-8")
            findings = audit.audit(root, 30)
            self.assertIn("TERMINAL_PLAN_IN_ACTIVE", {item.code for item in findings})

    def test_broken_markdown_link_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_project(root)
            nav = root / "docs" / "navigation.md"
            nav.write_text("[missing](no-such-file.md)\n", encoding="utf-8")
            findings = audit.audit(root, 30)
            self.assertIn("BROKEN_MARKDOWN_LINK", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Read-only audit for project-state-code-router collaboration docs.

Usage: python scripts/audit_project_docs.py <project-root> [--stale-days 30] [--json]
Requires PyYAML. This script never edits the audited project.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

STANDARD_FIELDS = (
    "schema_version", "structure_version", "initialized_by", "initialized_at",
    "responsibility_lookup", "roles", "work_units", "active_core_files",
)
UNIT_FILES = (
    "README.md", "manifest.md", "status.md", "requirements/index.md",
    "blockers/index.md", "issues/index.md", "sync/outward-needs.md", "archive/index.md",
)
TERMINAL_PLAN_STATUSES = {"completed", "cancelled"}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str = ""
    evidence: str = ""
    remediation: str = ""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def add(items: list[Finding], severity: str, code: str, message: str,
        path: Path | None = None, evidence: str = "", remediation: str = "") -> None:
    items.append(Finding(severity, code, message, str(path) if path else "", evidence, remediation))


def frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in content[3:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("'\"")
    return result


def parse_manifest(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    if not path.exists():
        add(findings, "P0", "MANIFEST_MISSING", "Standard manifest is missing", path,
            remediation="Use bootstrap or patch mode; do not guess project responsibility.")
        return None
    try:
        value = yaml.safe_load(read(path))
    except yaml.YAMLError as exc:
        add(findings, "P0", "MANIFEST_INVALID_YAML", "Manifest YAML cannot be parsed", path, str(exc),
            "Preserve the original; repair manually or create a confirmed backup before migration.")
        return None
    if not isinstance(value, dict):
        add(findings, "P0", "MANIFEST_NOT_MAPPING", "Manifest top level must be a mapping", path,
            remediation="Preserve the original and migrate manually; do not overwrite it automatically.")
        return None
    missing = [key for key in STANDARD_FIELDS if key not in value]
    if missing:
        legacy = any(key in value for key in ("docs_root", "navigation_file", "units_root", "default_read_order"))
        add(findings, "M1" if legacy else "P0", "MANIFEST_SCHEMA_INCOMPLETE",
            "Manifest is missing standard fields", path, ", ".join(missing),
            "Map legacy fields compatibly; never replace a legacy manifest wholesale in patch mode.")
    if "schema_version" in value and value["schema_version"] != 1:
        add(findings, "P1", "MANIFEST_SCHEMA_VERSION", "Manifest schema version is unsupported", path,
            str(value.get("schema_version")), "Report the migration need; do not upgrade an unknown schema automatically.")
    return value


def check_manifest(root: Path, docs: Path, manifest: dict[str, Any] | None,
                   findings: list[Finding]) -> None:
    if not manifest:
        return
    manifest_path = docs / ".project-docs-manifest.yaml"
    active = manifest.get("active_core_files")
    if isinstance(active, list):
        for item in active:
            if not isinstance(item, str):
                add(findings, "P1", "ACTIVE_CORE_NOT_PATH", "active_core_files contains a non-string", manifest_path, str(item))
                continue
            if not (root / item).exists():
                add(findings, "P0", "ACTIVE_CORE_MISSING", "active_core_files points to a missing path", manifest_path,
                    item, "Remove the stale reference or restore the confirmed file.")
            if "/archive/" in item or "/process/" in item:
                add(findings, "P1", "ACTIVE_CORE_DIRTY", "Historical material is included in active_core_files",
                    manifest_path, item, "Remove it from the default read set; retrieve it only when needed.")
    roles = manifest.get("roles")
    if isinstance(roles, dict):
        for role, config in roles.items():
            entry = config.get("entry") if isinstance(config, dict) else None
            if entry and not (root / entry).exists():
                add(findings, "P1", "ROLE_ENTRY_MISSING", "Manifest role entry does not exist", manifest_path,
                    f"{role}: {entry}", "Fix the path or restore the actual entry file.")
    units = manifest.get("work_units")
    if units is None:
        return
    if not isinstance(units, list):
        add(findings, "P0", "WORK_UNITS_NOT_LIST", "work_units must be a list", manifest_path)
        return
    for unit in units:
        if not isinstance(unit, dict):
            add(findings, "P0", "WORK_UNIT_INVALID", "work_units contains a non-object entry", manifest_path, str(unit))
            continue
        missing = [key for key in ("key", "label", "owner", "entry") if not unit.get(key)]
        if missing:
            add(findings, "P0", "WORK_UNIT_FIELDS_MISSING", "Work-unit route entry is incomplete", manifest_path,
                ", ".join(missing), "Fill confirmed route facts; ask rather than inventing an owner.")
        entry = unit.get("entry")
        if entry and not (root / entry).exists():
            add(findings, "P0", "WORK_UNIT_ENTRY_MISSING", "Work-unit entry does not exist", manifest_path,
                str(entry), "Repair the reference or restore the unit entry; do not silently reroute.")


def check_active_headers(docs: Path, stale_days: int, findings: list[Finding]) -> None:
    current = docs / "shared" / "current"
    for path in sorted(current.glob("*.md")) if current.exists() else []:
        meta = frontmatter(read(path))
        missing = sorted({"status", "authority", "owner", "last_verified"} - set(meta))
        if missing:
            add(findings, "M1", "ACTIVE_HEADER_MISSING", "Active current file lacks standard metadata", path,
                ", ".join(missing), "Add fields to new files; patch existing files narrowly, not by rewriting them.")
        value = meta.get("last_verified")
        if value:
            try:
                age = (dt.date.today() - dt.date.fromisoformat(value)).days
                if age > stale_days:
                    add(findings, "P1", "ACTIVE_STALE", "Active file verification date is stale", path,
                        f"{value} ({age} days)", "Re-verify the facts before updating the date.")
            except ValueError:
                add(findings, "P1", "ACTIVE_DATE_INVALID", "last_verified is not an ISO date", path, value)


def check_units(docs: Path, findings: list[Finding]) -> None:
    units_dir = docs / "units"
    if not units_dir.exists():
        return
    active_material = "\n".join(read(p) for base in (docs / "shared" / "current", docs / "shared" / "exec-plans" / "active")
                                  if base.exists() for p in base.rglob("*.md"))
    for unit in sorted(p for p in units_dir.iterdir() if p.is_dir() and p.name != ".template"):
        missing = [name for name in UNIT_FILES if not (unit / name).exists()]
        if missing:
            severity = "P1" if unit.name in active_material else "M1"
            add(findings, severity, "UNIT_FILES_MISSING", "Work unit lacks minimum entry files", unit,
                ", ".join(missing), "Complete only units needed for current routing; do not bulk-rebuild legacy docs.")


def check_plans(docs: Path, findings: list[Finding]) -> None:
    plans = docs / "shared" / "exec-plans"
    active, completed = plans / "active", plans / "completed"
    if active.exists():
        for path in sorted(active.iterdir()):
            if not path.is_file():
                continue
            content = read(path)
            status = frontmatter(content).get("status")
            if not status:
                match = re.search(r"(?mi)^status:\s*(\S+)", content)
                status = match.group(1) if match else ""
            status = status.lower()
            if status in TERMINAL_PLAN_STATUSES | {"done", "finished", "closed"}:
                add(findings, "P1", "TERMINAL_PLAN_IN_ACTIVE", "Terminal plan remains in active/", path, status,
                    "Record completion/cancellation date and move it to completed/.")
            has_checked = re.search(r"(?m)^- \[[xX]\]", content) is not None
            has_open = re.search(r"(?m)^- \[ \]", content) is not None
            if status == "active" and has_checked and not has_open:
                add(findings, "P1", "PLAN_COMPLETION_DRIFT", "All checklist steps are checked but plan remains active", path,
                    "Checked steps exist; no unchecked steps", "Verify acceptance and docs write-back before archiving.")
            if not any(h in content for h in ("Docs write-back", "Docs write-back targets", "Docs \u5199\u56de\u76ee\u6807")):
                add(findings, "P1", "PLAN_WRITEBACK_MISSING", "Active plan lacks docs write-back targets", path,
                    remediation="List authoritative docs to update, or state none and why.")
            if not any(h in content for h in ("Resume Point", "Interruption recovery", "\u4e2d\u65ad\u6062\u590d\u70b9")):
                add(findings, "P1", "PLAN_RESUME_MISSING", "Active plan lacks an interruption recovery point", path,
                    remediation="Record next action, known blockers, and history that should remain unread.")
    if completed.exists():
        for path in sorted(completed.iterdir()):
            if path.is_file() and re.search(r"(?mi)^status:\s*(active|in-progress)\s*$", read(path)):
                add(findings, "P1", "ACTIVE_PLAN_IN_COMPLETED", "Plan in completed/ still has an active status", path)


def check_git(root: Path, docs: Path, findings: list[Finding]) -> None:
    if not (root / ".git").exists():
        return
    ignored_target = docs / ".project-docs-manifest.yaml"
    try:
        ignored = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", str(ignored_target)],
                                 capture_output=True).returncode == 0
        if ignored:
            add(findings, "P1", "DOCS_IGNORED", "docs manifest is ignored by Git", root / ".gitignore",
                str(ignored_target), "Confirm the authoritative persistence location; do not edit ignore rules automatically.")
        tracked = subprocess.run(["git", "-C", str(root), "ls-files", "docs"], capture_output=True,
                                 text=True, encoding="utf-8", errors="replace").stdout.strip()
        if not tracked:
            add(findings, "P1", "DOCS_UNTRACKED", "No docs files are tracked by Git", docs,
                "git ls-files docs returned no paths", "Confirm where durable project state is stored.")
    except OSError as exc:
        add(findings, "I", "GIT_CHECK_UNAVAILABLE", "Git check could not run", root, str(exc))


def check_links(docs: Path, findings: list[Finding]) -> None:
    link_re = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for source in docs.rglob("*.md"):
        for raw in link_re.findall(read(source)):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if target and not (source.parent / target).resolve().exists():
                add(findings, "P1", "BROKEN_MARKDOWN_LINK", "Markdown link target does not exist", source,
                    raw, "Fix the link or mark it as an external / pending reference.")


def check_heuristics(docs: Path, findings: list[Finding]) -> None:
    current = docs / "shared" / "current"
    if not current.exists():
        return
    phrases = ["\u5f53\u524d\u65e0\u6d3b\u8dc3\u5de5\u5355", "\u65e0\u6d3b\u8dc3\u5de5\u5355",
               "\u8fdb\u884c\u4e2d", "\u5f53\u524d\u8fdb\u884c\u4e2d", "\u672a\u5b8c\u6210"]
    claims: list[str] = []
    for path in current.glob("*.md"):
        content = read(path)
        claims.extend(f"{path.name}:{phrase}" for phrase in phrases if phrase in content)
    if len({item.split(":", 1)[0] for item in claims}) >= 2:
        add(findings, "I", "CURRENT_REVIEW_REQUIRED", "Several current files contain status claims; manually verify current truth",
            current, "; ".join(claims[:12]),
            "Compare user direction, current code/tests, active docs, references, then history; never resolve by keywords alone.")


def audit(root: Path, stale_days: int) -> list[Finding]:
    findings: list[Finding] = []
    docs = root / "docs"
    if not docs.exists():
        add(findings, "P0", "DOCS_MISSING", "Project has no docs directory", docs,
            remediation="Use bootstrap mode to create only the minimum structure.")
        return findings
    manifest = parse_manifest(docs / ".project-docs-manifest.yaml", findings)
    check_manifest(root, docs, manifest, findings)
    check_active_headers(docs, stale_days, findings)
    process_dir = docs / "process"
    if not process_dir.exists() or not any(path.is_file() for path in process_dir.iterdir()):
        add(findings, "M1", "PROCESS_RECORD_MISSING", "No initialization or patch process record was found", process_dir,
            remediation="If docs were bootstrapped/patched, record date, reason, files added/preserved, and unresolved inputs; do not invent history.")
    check_units(docs, findings)
    check_plans(docs, findings)
    check_git(root, docs, findings)
    check_links(docs, findings)
    check_heuristics(docs, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only audit of project collaboration docs")
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--stale-days", type=int, default=30)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    root = args.project_root.resolve()
    findings = audit(root, args.stale_days)
    if args.as_json:
        print(json.dumps({"project_root": str(root), "findings": [asdict(x) for x in findings]}, ensure_ascii=False, indent=2))
    else:
        print(f"Project: {root}\nMode: audit (read-only)\nFindings: {len(findings)}")
        for item in findings:
            print(f"[{item.severity}] {item.code} [{item.path}]: {item.message}")
            if item.evidence:
                print(f"  evidence: {item.evidence}")
            if item.remediation:
                print(f"  remediation: {item.remediation}")
        print("Changed project files: none")
    return 1 if any(item.severity == "P0" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

# Project-state audit and repair protocol

**Scope:** `audit` and `repair` modes for existing project collaboration docs.

## Purpose

Use this reference when the user asks whether a project follows this skill, asks to clean up project docs, or asks to repair findings from a prior audit. Audit is not normal implementation work: it may inspect the whole docs tree, but it must not silently modify project files.

## Modes

### `audit`

- Read the manifest, root collaboration entry, navigation, active current docs, work-unit entries, active plans, and relevant Git metadata.
- Scan the whole docs tree only for checks that require it: missing routes, stale lifecycle items, broken references, duplicate current claims, and ignored/untracked docs.
- Do not create, move, rename, or edit project files.
- Report each finding with severity, file path, evidence, and a bounded remediation.

### `repair`

- Enter only when the user explicitly asks to fix the audit findings.
- Repair only the confirmed findings, using append/field/block edits where possible.
- Never migrate an entire historical docs tree for cleanliness alone.
- Re-run the audit after edits and report unresolved migration debt separately.

## Severity and finding classes

- **P0 rule violation:** Can cause wrong routing, wrong current truth, unsafe implementation, lost collaboration state, or an invalid manifest entry.
- **P1 rule violation:** Breaks lifecycle, write-back, freshness, or recovery behavior but has a bounded workaround.
- **M1 migration debt:** Legacy shape or missing optional structure that does not by itself invalidate current routing. Report it; do not rewrite it automatically in patch mode.
- **I informational:** Useful context or cleanup opportunity with no current correctness impact.

Do not infer that every missing template file is P0. A legacy unit becomes urgent only when it is the current responsibility area, is referenced by an active plan, or is needed to record a current fact.

## Required audit checks

1. Parse `docs/.project-docs-manifest.yaml`; report invalid YAML without replacing it.
2. Check standard manifest fields and resolve every declared path.
3. Check `active_core_files` for existence and accidental inclusion of archive/process material.
4. Check current active files for `status`, `authority`, `owner`, and `last_verified`. A stale date is a finding, not permission to invent a new verification result.
5. Check each declared work unit's routing entry. For new units, require the minimal unit files; for legacy units, classify missing files as migration debt unless the unit is active or referenced.
6. Check active plans for canonical status, required recovery/write-back sections, completed steps left in `active/`, and missing `completed_at` on terminal plans.
7. Check REQ/ISS/BLK/SYNC/PLAN lifecycle metadata and index-to-entry references when formal entries are used.
8. Check current docs for likely contradictory claims. Heuristics must be reported as “manual current-truth review required”; never auto-resolve semantic conflicts.
9. Check Markdown path references that look like repository paths.
10. Check whether `docs/` is ignored or absent from Git tracking when the project is a Git repository. Report the condition; do not change `.gitignore` automatically.

## Current-truth review

When audit finds conflicting active claims:

1. Compare the user request, current code and tests, active docs, reference docs, and process/archive history in that order.
2. Identify the stale source; do not choose based only on file name or modification time.
3. Repair the smallest authoritative active source and add `last_verified` only after actual verification.
4. If code and tests cannot establish the fact, report a user decision or verification blocker instead of guessing.

## Audit output

The report must include:

- detected mode and project root;
- files and scopes inspected;
- P0/P1/M1/I findings, grouped by severity;
- evidence paths and concise excerpts where useful;
- whether any project files were changed (audit must say “none”);
- a repair order;
- facts that require user confirmation.

After a repair run, include the post-repair audit result and any remaining findings. Do not claim compliance merely because the directory shape exists.

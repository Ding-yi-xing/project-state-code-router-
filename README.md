# project-state-code-router

A Claude Code skill for **repo-as-system-of-record project work**: it routes agents through current project state before implementation, prevents dirty reads from stale docs, and only then loads fallback coding constraints when project/ECC/language rules do not already cover the work.

It helps Claude (or any other coding agent) decide **what is current truth, what to read, what to skip, where to write facts back, and which rules apply** before changing code or docs.

---

## What this skill does

When invoked, it guides the agent to:

1. Detect whether the project is in `bootstrap`, `patch`, or `normal` mode
2. Identify the narrowest responsibility area: a work unit, `pm`, or `cross-area`
3. Read only the smallest active fact set required for that scope
4. Avoid leaking archive, old plans, process logs, or completed work into current context
5. Persist lightweight plans or active execution plans before non-trivial work
6. Write changed facts back to their authoritative docs locations before finishing
7. Apply layered fallback coding rules only after project state has been scoped

It is opinionated: current truth is small, archive is opt-in, responsibility-aware reading beats whole-repo scanning, plans live in the repo, and implementation rules load **late**, not early.

---

## Why this exists

Most AI coding workflows fail in two ways:

1. **They read too much.** Old plans, archive notes, and stale process logs leak into context and cause dirty reads.
2. **They apply coding guidance too early.** The agent enforces style and abstraction before knowing which part of the project it is responsible for.

This skill splits the workflow into two layers and routes through state first, rules second.

---

## The two layers

### 1. Project-state layer

- Identifies the current responsibility area
- Decides what is current truth
- Restricts default reading to the smallest useful active set
- Bootstraps or patches collaboration docs only when needed
- Enforces veto-first decisions, prohibition granularity, and dirty-read prevention
- Defines write-back routing for requirements, issues, blockers, sync, plans, archive, and process notes

Main reference: `references/project-state.md`

### 2. Coding-constraints layer

- Loads targeted implementation rules from `references/` only after project state is scoped
- Always loads `references/overrides.md` before task-specific fallback references
- Uses `references/warning-signs.md` as a cross-cutting red-flag list
- Applies Code Complete 2-inspired constraints that have been modernized or narrowed by overrides
- Does **not** replace project `CLAUDE.md`, ECC rules, language/framework rules, hooks, security rules, testing rules, or performance rules

Routing table lives in `SKILL.md`.

---

## Compatibility with project and ECC rules

This skill is not a universal style guide that overrides local practice.

If a project already has `CLAUDE.md`, ECC rules, language-specific rules, framework rules, or hook-based checks, those rules own implementation quality. This skill owns:

- project-state routing
- work-unit scope
- active / reference / archive separation
- dirty-read prevention
- documentation-first planning
- authoritative docs write-back
- fallback coding constraints only when no more specific rule exists

The practical order is:

```text
user request + system/developer instructions
> project CLAUDE.md / ECC / language / framework rules
> project-state-code-router project-state layer
> project-state-code-router fallback coding references
```

---

## Influences from OpenAI's Harness Engineering post

This skill incorporates several practices from OpenAI's [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/):

| Practice | Where in this skill |
|---|---|
| AGENTS.md as a short map, not an encyclopedia | `SKILL.md` (map layer: routing + safety rules; detailed rules live under `references/`) |
| Repo as system of record | `docs/` collaboration structure and write-back routing |
| Doc-gardening agent + code-rot GC | `references/gc-rules.md` |
| Strict architecture layers + custom lint | `references/architecture-layers.md` |
| Plans as first-class artifacts | `docs/shared/exec-plans/{active,completed}/` |
| Project-level Golden Rules | `references/gc-rules.md` and downstream `docs/GOLDEN_RULES.md` |
| Lint error message = fix instruction | `references/architecture-layers.md` + `references/gc-rules.md` |
| Top-level principle files | Optional downstream `docs/{DESIGN,FRONTEND,RELIABILITY,SECURITY,PRODUCT_SENSE,GOLDEN_RULES,ARCHITECTURE}.md` |
| `references/<lib>-llms.txt` for stable external context | Downstream `docs/references/` in the bootstrap template |

---

## Repository structure

```text
project-state-code-router/
├── SKILL.md                          # Map layer: two layers, modes,
│                                     # safety rules, routing table
├── README.md / README.zh-CN.md
├── LICENSE
└── references/
    ├── overrides.md                  # Modern fallback-rule overrides; load first
    ├── warning-signs.md              # Cross-cutting red flags
    ├── project-state.md              # Project-state layer rules
    ├── bootstrap-templates.md        # Minimal docs skeleton, manifest schema,
    │                                 # work units, plans, principle files, llms.txt
    ├── architecture-layers.md        # Layered architecture + boundary lint
    ├── gc-rules.md                   # Doc-gardening + code GC, golden rules
    ├── design.md                     # Class / module / interface design
    ├── naming.md                     # Variable, function, type naming
    ├── layout.md                     # Code formatting, comments
    ├── control.md                    # Control flow, conditionals, loops
    ├── defense.md                    # Input validation, assertions, errors
    ├── debugging.md                  # Reproduce, isolate, verify
    ├── quality.md                    # Test design, testability, review
    ├── performance.md                # Optimization strategy
    ├── git-workflow.md               # Commits, branches, PRs
    ├── templates.md                  # File / function templates
    └── downstream-samples/
        └── gc-lint.example.mjs       # Reference implementation for downstream
                                      # doc-gardening (copy & adapt)
```

---

## Suggested downstream project structure

When bootstrapping a project that uses this skill, the recommended layout is intentionally minimal and lives at the project root:

```text
<project-root>/
├── CLAUDE.md                         # Routing entry contract
├── docs/
│   ├── .project-docs-manifest.yaml   # Responsibility lookup, roles,
│   │                                 # work_units, active_core_files
│   ├── DESIGN.md / FRONTEND.md / RELIABILITY.md / …  # Optional long-term principles
│   ├── GOLDEN_RULES.md               # Optional project-level mechanical rules
│   ├── ARCHITECTURE.md               # Optional top-level layer map
│   ├── navigation/
│   ├── shared/
│   │   ├── current/                  # Active facts: scope, priorities,
│   │   │                             # blockers, acceptance, locked ranges
│   │   ├── contracts/
│   │   ├── decisions/
│   │   ├── milestones/
│   │   ├── exec-plans/
│   │   │   ├── active/               # In-flight execution plans
│   │   │   ├── completed/            # Historical decisions, never deleted
│   │   │   └── tech-debt-tracker.md
│   │   ├── generated/                # Auto-generated contracts; do not hand-edit
│   │   └── archive/
│   ├── units/                        # Confirmed work units only
│   │   └── .template/
│   ├── references/                   # Downstream llms.txt files for dependencies
│   └── process/
└── <code-dirs>/
```

Names can be localized (Chinese names work too); structure semantics matter, not the literal filenames. Do not pre-create speculative work units. Ask the project manager or current user for the units that are actually needed.

---

## Project states

| Mode | When | Behavior |
|---|---|---|
| `bootstrap` | No `docs/`, no manifest, no active layer | Create the minimal skeleton only; do not invent business units or items |
| `patch` | `docs/` exists but manifest / active layer / unit entry is missing | Fill only what is missing; never overwrite non-empty files |
| `normal` | Manifest, active layer, and current unit entry all exist | Read the smallest necessary set; edit only inside the current scope |

Manifest recovery is conservative: parsing errors, missing fields, stale `active_core_files`, or incomplete `work_units` are reported and repaired only in the smallest safe way.

---

## Document model

Documents are split into three layers:

- **Active** — current truth, the only layer loaded by default
- **Reference** — long-lived design material, read only when the task needs it
- **Archive** — historical, never default-loaded; reactivate as a new active entry, do not edit in place

If active conflicts with reference or archive, **active wins**. If active conflicts with current code or test behavior, verify the current fact first and then update either the code or the authoritative active document.

---

## Documentation-first planning

Before non-trivial coding, architecture work, cross-file edits, cross-unit coordination, risky fixes, or plan advancement, create or update a lightweight plan / active exec plan in the repo.

A plan must state:

- goal
- scope and non-scope
- steps
- verification method
- docs write-back targets
- interruption recovery point

Small 1-3 step, single-file, low-risk edits may skip a persisted plan, but the agent should say why.

---

## Write-back routing before finishing

Every project-work session ends with a docs sync check. `status.md` is only a dashboard/index; it must not become the only source of truth for requirements, bugs, blockers, sync needs, process notes, or archive state.

| Fact change | Authoritative destination |
|---|---|
| Requirement change | `docs/units/<unit>/requirements/` |
| Bug, defect, failed acceptance | `docs/units/<unit>/issues/` |
| Blocker or external dependency | `docs/units/<unit>/blockers/` or `docs/shared/current/当前阻塞与待修复问题清单.md` |
| Cross-unit request | `docs/units/<unit>/sync/outward-needs.md` |
| Project-level scope / priority / acceptance / lock change | `docs/shared/current/*.md` |
| Completed or cancelled item | `docs/units/<unit>/archive/` and `archive/index.md` |
| Investigation or handoff narrative | `docs/process/` or active exec-plan progress log |
| Active multi-step plan | `docs/shared/exec-plans/active/` |
| Long-term architecture or principle | `docs/ARCHITECTURE.md`, `docs/DESIGN.md`, `docs/GOLDEN_RULES.md`, etc. |

---

## Lightweight fast path

For a task that is all of the following:

- single-file
- non-structural
- not the first setup task
- not security-critical

…the agent may skip the full project-state route and load only the core warning signs. If the work expands beyond that shape, it falls back to the full routing protocol.

---

## How to use

Use this skill when Claude is asked to:

- continue or resume work from project docs
- advance an active execution plan
- bootstrap or patch collaboration docs
- decide current truth, scope, blockers, requirements, or acceptance criteria
- review, debug, refactor, or test code without dragging in irrelevant history
- install doc-gardening or code-GC on a downstream project
- establish architecture layers and boundary enforcement
- perform implementation work that may change project facts

The skill activates automatically when its trigger keywords appear in your request (see `SKILL.md` frontmatter).

### Recommended flow

1. Read root `CLAUDE.md` if it exists
2. Read `docs/.project-docs-manifest.yaml`
3. Determine the narrowest responsibility area
4. Determine project mode (`bootstrap` / `patch` / `normal`)
5. Read only the minimum active-layer documents for that scope
6. Use archive only when historical traceability is genuinely required
7. Persist a lightweight plan / active exec plan before non-trivial work
8. Load fallback implementation references only after the task is scoped
9. Before finishing, run the write-back checklist and update authoritative docs

---

## Garbage collection for downstream projects

The skill repo itself does **not** run GC on itself (single maintainer, low edit frequency). But it ships a complete GC playbook for downstream projects that use it:

- **Doc-gardening** — invariants for `docs/` structure, semantic checks for stale status / blockers / archive references
- **Code GC** — drift detection on architecture layers, naming conventions, file size, banned dependencies, golden-rule violations
- **Reference implementation** — `references/downstream-samples/gc-lint.example.mjs` (Node.js, zero-dep) as a starting point

See `references/gc-rules.md` for the full playbook.

---

## Customization

You'll likely want to adapt:

- responsibility area names and work-unit taxonomy
- collaboration doc filenames (English / Chinese / your team's terms)
- manifest `roles`, `work_units`, and `active_core_files`
- which top-level principle files to keep
- the layer model in `architecture-layers.md`
- your project's Golden Rules

The right places to customize:

- root `CLAUDE.md` — routing contract
- `docs/.project-docs-manifest.yaml` — responsibility lookup and active-file discovery
- `docs/GOLDEN_RULES.md` — project-level mechanical rules
- `docs/ARCHITECTURE.md` — your layer model
- `docs/shared/exec-plans/` — active and completed plans
- `references/overrides.md` — only when a fallback CC2-derived rule conflicts with modern practice

---

## Who this is for

Especially useful when your project has:

- multiple work units or teams
- a mix of active work and substantial historical documentation
- shared collaboration docs at the project root
- a need to prevent AI dirty reads and accidental rollback to old designs
- a desire for fallback coding standards without forcing heavyweight legacy ceremony
- multiple agents (Claude, Codex, others) reading the same repo

If your project prefers exhaustive documentation-by-default, monolithic process logs, or global style enforcement before scoping, this skill will feel intentionally restrictive.

---

## Attribution

Created and curated by `DingYiXing`.

Coding guidance distilled from *Code Complete 2*, then filtered through a modern override layer to reduce ceremony and stale-process drag.

Harness-engineering practices (AGENTS.md as map, doc-gardening, code GC, architecture layers, plans as artifacts, lint-as-fix-instruction) adapted from OpenAI's [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/).

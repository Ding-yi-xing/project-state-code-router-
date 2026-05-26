# project-state-code-router

A Claude Code skill that fuses **project-state collaboration routing** with **Code Complete 2 coding constraints**, modernized through an override layer and **OpenAI Harness-Engineering–style** entry/GC discipline.

It helps Claude (or any other coding agent) decide **what is current truth, what to read, what to skip, and what rules apply** before writing a single line of code.

---

## What this skill does

When invoked, it makes the agent:

1. Detect whether the project is in `bootstrap`, `patch`, or `normal` mode
2. Identify the narrowest responsibility area (a work unit, `pm`, or `cross-area`)
3. Read only the smallest active fact set required for that scope
4. Avoid leaking archive, old plans, or process logs into context
5. Apply layered coding rules — modern overrides first, then domain-specific references

It is opinionated: current truth is small, archive is opt-in, responsibility-aware reading beats whole-repo scanning, and coding rules load **late**, not early.

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

Main reference: `references/project-state.md`

### 2. Coding-constraints layer
- Loads targeted implementation rules from `references/`
- Always loads `references/overrides.md` and `references/warning-signs.md` first
- Applies Code Complete 2–inspired constraints, modernized via overrides
- Routes to specific files based on the task (naming, design, defense, debugging, etc.)

Routing table lives in `SKILL.md`.

---

## Influences from OpenAI's Harness Engineering post

This skill incorporates several practices from OpenAI's [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/):

| Practice | Where in this skill |
|---|---|
| AGENTS.md as a ~100-line map, not encyclopedia | `SKILL.md` (≤ 150 lines, pure routing + safety rules) |
| Repo as system of record | The whole `docs/` structure described below |
| Doc-gardening agent + code-rot GC | `references/gc-rules.md` |
| Strict architecture layers + custom lint | `references/architecture-layers.md` |
| Plans as first-class artifacts | `docs/shared/exec-plans/{active,completed}/` |
| Project-level Golden Rules | `references/gc-rules.md` (Golden Rules section) |
| Lint error message = fix instruction | `references/architecture-layers.md` + `references/gc-rules.md` |
| Top-level principle files | `docs/{DESIGN,FRONTEND,RELIABILITY,SECURITY,…}.md` |
| `references/<lib>-llms.txt` for stable external context | `docs/references/` in the bootstrap template |

---

## Repository structure

```text
project-state-code-router/
├── SKILL.md                          # Map (~130 lines): two layers, modes,
│                                     # safety rules, routing table
├── README.md / README.zh-CN.md
├── LICENSE
└── references/
    ├── overrides.md                  # Modern default overrides — always loaded first
    ├── warning-signs.md              # Cross-cutting red flags — always loaded
    ├── project-state.md              # Project-state layer rules (full version)
    ├── bootstrap-templates.md        # Doc skeleton, manifest, unit templates,
    │                                 # plans-as-artifacts, principle files, llms.txt
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

When bootstrapping a project that uses this skill, the recommended layout is:

```text
<project-root>/
├── CLAUDE.md                         # Routing entry contract
├── docs/
│   ├── .project-docs-manifest.yaml   # Responsibility lookup, active_core_files
│   ├── DESIGN.md / FRONTEND.md / RELIABILITY.md / …  # Long-term principles
│   ├── GOLDEN_RULES.md               # Project-level mechanical rules
│   ├── ARCHITECTURE.md               # Top-level layer map
│   ├── navigation/
│   ├── shared/
│   │   ├── current/                  # Active facts (what we're doing now)
│   │   ├── contracts/
│   │   ├── decisions/
│   │   ├── milestones/
│   │   ├── exec-plans/
│   │   │   ├── active/               # In-flight execution plans
│   │   │   ├── completed/            # Historical decisions, never deleted
│   │   │   └── tech-debt-tracker.md
│   │   ├── generated/                # Auto-generated contracts (don't hand-edit)
│   │   └── archive/
│   ├── units/                        # Work units (per responsibility area)
│   │   └── .template/
│   ├── references/                   # llms.txt for libraries you depend on
│   └── process/
└── <code-dirs>/
```

Names can be localized (Chinese names work too); structure semantics matter, not the literal filenames.

---

## Project states

| Mode | When | Behavior |
|---|---|---|
| `bootstrap` | No `docs/`, no manifest, no active layer | Create minimal skeleton, do not invent business units or items |
| `patch` | `docs/` exists but manifest / active layer / unit entry is missing | Fill only what's missing, never overwrite non-empty files |
| `normal` | Manifest, active layer, current unit entry all present | Read smallest necessary set, edit only inside current unit |

---

## Document model

Documents are split into three layers:

- **Active** — current truth, the only layer loaded by default
- **Reference** — long-lived design material, read only when the task needs it
- **Archive** — historical, never default-loaded; reactivate as a new entry, do not edit in place

If active conflicts with reference or archive, **active wins**.

---

## How to use

Use this skill when Claude is asked to:

- continue work in a specific work unit
- write or modify code in an existing project
- bootstrap collaboration docs for a new repo
- patch missing collaboration docs
- review, debug, refactor, or test code without dragging in irrelevant history
- install doc-gardening or code-GC on a project
- establish architecture layers and boundary enforcement

The skill activates automatically when its trigger keywords appear in your request (see SKILL.md frontmatter).

### Recommended flow

1. Read root `CLAUDE.md` if it exists
2. Determine the narrowest responsibility area
3. Determine the project mode (`bootstrap` / `patch` / `normal`)
4. Read only the minimum active-layer documents for that scope
5. Use archive only when historical traceability is genuinely required
6. Load implementation rules from `references/` only after the task is scoped
7. Always load `overrides.md` and `warning-signs.md` first; let modern overrides win

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
- the active-core file list in the manifest
- which top-level principle files to keep
- the layer model in `architecture-layers.md`
- your project's Golden Rules

The right places to customize:

- root `CLAUDE.md` — routing contract
- `docs/.project-docs-manifest.yaml` — responsibility lookup
- `docs/GOLDEN_RULES.md` — project-level mechanical rules
- `docs/ARCHITECTURE.md` — your layer model
- the override layer in `references/overrides.md` if a CC2 default conflicts with your modern practice

---

## Who this is for

Especially useful when your project has:

- multiple work units or teams
- a mix of active work and substantial historical documentation
- shared collaboration docs at the project root
- a need to prevent AI dirty reads and accidental rollback to old designs
- a desire for coding standards without forcing heavyweight legacy ceremony
- multiple agents (Claude, Codex, others) reading the same repo

If your project prefers exhaustive documentation-by-default, monolithic process logs, or global style enforcement before scoping, this skill will feel intentionally restrictive.

---

## Attribution

Created and curated by `DingYiXing`.

Coding guidance distilled from *Code Complete 2*, then filtered through a modern override layer to reduce ceremony and stale-process drag.

Harness-engineering practices (AGENTS.md as map, doc-gardening, code GC, architecture layers, plans as artifacts, lint-as-fix-instruction) adapted from OpenAI's [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/).

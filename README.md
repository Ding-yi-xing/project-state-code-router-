# project-state-code-router

A Claude Code skill for **routing coding work through the current project state first**, then applying implementation constraints with a **minimal-reading, low-staleness workflow**.

This skill is designed for repositories where AI coding should not blindly scan everything, trust old plans, or overfit to broad style rules. It helps Claude decide:

- what the current source of truth is
- which responsibility area the task belongs to
- whether the project is in `normal`, `bootstrap`, or `patch` mode
- which documents should be read now
- which documents should stay out of context unless explicitly needed
- which coding rules should apply after the task is scoped correctly

## Why this exists

Most AI coding workflows fail in one of two ways:

1. **They read too much.**
   Old plans, archive notes, and stale process logs leak into the context and cause dirty reads.

2. **They apply coding guidance too early.**
   The agent starts enforcing style, abstraction, comments, or structure before it knows which part of the project it is actually responsible for.

This skill fixes that by splitting the workflow into two layers:

1. **Project-state layer**
   - identifies the current responsibility area
   - decides what is current truth
   - restricts default reading to the smallest useful active set
   - bootstraps or patches collaboration docs only when needed

2. **Coding-constraints layer**
   - loads targeted implementation rules from `references/`
   - applies Code Complete 2–inspired constraints after the task is scoped
   - uses a modern override layer to suppress overly ceremonial or outdated defaults

## Core ideas

### 1. Active facts first
Only the smallest current fact set should enter context by default.

### 2. CLAUDE.md before routing
If a root-level `CLAUDE.md` exists, Claude should read it first and use it as the collaboration entry contract.

### 3. Archive is opt-in
Archived plans, process notes, and old designs are not current execution guides.

### 4. Patch, don't rebuild
If collaboration docs are incomplete, create only what is missing.

### 5. Responsibility-aware reading
The skill routes tasks into the narrowest responsibility area that fits:

- work unit (`<unit-name>`)
- `pm`
- `cross-area`

### 6. Modern default behavior overrides
The skill preserves safety and correctness rules, but suppresses heavy legacy defaults such as:

- mandatory comment-heavy workflows
- file header ceremony by default
- unnecessary abstraction scaffolding
- defensive validation on already-trusted internal flows
- historical process rituals that add noise without improving correctness

## Project states

Every invocation begins by classifying the project into one of three states:

### `normal`
Use when the repository already has an active collaboration structure.

### `bootstrap`
Use when the repository is effectively uninitialized and needs a minimal collaboration docs structure.

### `patch`
Use when the repository has some collaboration docs, but required active files or responsibility-area entry points are missing.

## Document model

The skill organizes project documents into three layers:

### Active
Current truth. These are the only documents that should be loaded by default.

Typical examples:
- current scope
- current priorities
- current acceptance criteria
- current implementation boundaries
- locked/no-redesign zones
- responsibility-area entry files

### Reference
Long-lived design material.

Typical examples:
- API design
- architecture design
- data design
- UI/visual design
- module design

### Archive
Historical material.

Typical examples:
- old plans
- completed phase notes
- deprecated constraints
- old handoff records

**Rule:** if active facts conflict with reference or archive, active facts win.

## Suggested collaboration docs structure

When bootstrapping, the skill expects a minimal shared documentation layout like this:

```text
<project-root-directory>/
├── CLAUDE.md
├── docs/
│   ├── .project-docs-manifest.yaml
│   ├── navigation/
│   │   └── 项目导航.md
│   ├── shared/
│   │   ├── README.md
│   │   ├── current/
│   │   │   ├── 当前阶段目标与范围.md
│   │   │   ├── 当前任务优先级清单.md
│   │   │   ├── 当前阻塞与待修复问题清单.md
│   │   │   ├── 当前验收标准清单.md
│   │   │   ├── 当前实现边界对照.md
│   │   │   └── 当前锁定范围与禁止主动重构清单.md
│   │   ├── contracts/
│   │   ├── decisions/
│   │   ├── milestones/
│   │   └── archive/
│   ├── units/
│   │   ├── .template/
│   │   └── <unit-name>/
│   └── process/
│       └── 000-项目初始化.md
```

The file names can be localized or adapted, but the structure should preserve the same semantics:

- one root collaboration entry
- one manifest for responsibility lookup
- a small active layer for current truth
- explicit archive separation

## Repository structure

```text
project-state-code-router/
├── SKILL.md
└── references/
    ├── bootstrap-templates.md
    ├── comments.md
    ├── control.md
    ├── debugging.md
    ├── defense.md
    ├── design.md
    ├── git-workflow.md
    ├── layout.md
    ├── naming.md
    ├── performance.md
    ├── process.md
    ├── project-state.md
    ├── quality.md
    ├── refactoring.md
    ├── overrides.md
    ├── templates.md
    ├── warning-signs.md
    └── writing.md
```

### Key files

- `SKILL.md`
  - main router and policy entry
  - defines project states, document layers, routing, minimal reading, and coding rule loading

- `references/project-state.md`
  - collaboration-doc governance
  - responsibility lookup
  - active/reference/archive handling
  - bootstrap/patch safety

- `references/overrides.md`
  - modern default behavior overrides — downgrades or disables legacy CC2 rules that conflict with modern practice
  - loaded before all other reference files; overrides always win

- `references/bootstrap-templates.md`
  - minimal content expectations for collaboration docs

- `references/comments.md`, `references/writing.md`, `references/defense.md`, etc.
  - implementation guidance loaded only after task scope is clear

## How to use this skill

Use this skill when Claude is asked to:

- continue work in a specific work unit
- write or modify code in an existing project
- bootstrap collaboration docs for a new repository
- patch missing collaboration docs in a partially structured repository
- review, debug, refactor, or test code without dragging in irrelevant project history

### Recommended workflow

1. Read root `CLAUDE.md` if it exists.
2. Determine the narrowest responsibility area.
3. Determine whether the project is in `normal`, `bootstrap`, or `patch` mode.
4. Read only the minimum active-layer documents for that scope.
5. Use archive only when the task explicitly needs historical traceability.
6. Load implementation rules from `references/` only after the task is scoped.
7. Apply the modern override layer when generic legacy guidance conflicts with clarity.

## Responsibility routing examples

### Example: work unit task
Read only the current work unit's manifest.md and status.md, plus boundaries, acceptance criteria, and locked zones for that unit.

### Example: API bug fix
Read only the relevant work unit's manifest.md and status.md, interface/data contract if needed, and blocker list only if the task is truly blocked.

### Example: PM coordination
Read scope, priorities, acceptance, and lock decisions — not all engineering detail.

### Example: cross-unit integration issue
Read only the directly involved work unit entries plus shared blockers and task-specific contracts.

## Comment philosophy in this skill

This skill includes a detailed comment ruleset, but its default behavior is intentionally modernized.

In practice, the effective default is:

- prefer self-documenting code
- comment intent and constraints, not obvious mechanics
- do not use comments to compensate for unclear code
- do not add file-header or author-block ceremony by default
- keep comments for non-obvious behavior, invariants, workarounds, and boundary assumptions

## Who this is for

This skill is especially useful if you want Claude to work well in repositories that have:

- multiple work units
- active work plus a lot of historical documentation
- shared collaboration docs at the project root
- a need to prevent AI dirty reads and accidental rollback to old designs
- a desire for coding standards without forcing heavyweight legacy ceremony

## Customization

You will probably want to adapt:

- responsibility area names
- collaboration docs file names
- active-core file list
- work unit taxonomy
- project-language-specific references
- comment and documentation expectations

The best place to customize behavior is:

- root `CLAUDE.md` for routing contract
- `docs/.project-docs-manifest.yaml` for responsibility lookup
- `references/` files for coding guidance
- the modern override section in `SKILL.md` for default behavior tuning

## Notes for open-source users

This skill is opinionated.

It assumes that:

- current truth should be small and explicit
- archived material should not silently steer implementation
- responsibility routing is better than broad repository scanning
- code guidance should be loaded late, not early
- modern clarity should outrank ritual unless safety or correctness requires otherwise

If your project prefers exhaustive documentation-by-default, monolithic process logs, or global style enforcement before scoping, this skill may feel intentionally restrictive.

## Attribution

Created and curated by `DingYiXing`.

Part of the coding guidance is distilled from principles inspired by *Code Complete 2*, then filtered through a modern default-behavior override layer to reduce ceremony and stale-process drag.

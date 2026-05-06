---
name: project-state-code-router
description: >
  This skill should be used whenever the user asks to write, modify, refactor,
  review, debug, or continue software work in an existing or new project.
  Provides a project-state router plus actionable coding constraints distilled
  from Code Complete 2. Trigger on: continuing work in a delivery surface or
  service domain, project-management coordination, initializing project docs,
  patching missing collaboration docs, writing functions, designing classes,
  naming variables, handling errors, writing comments/documentation, testing,
  debugging, refactoring, optimizing performance, setting up projects, and code
  review. Use when the user says "write code", "implement", "refactor", "fix
  bug", "continue web", "continue ios", "continue api", "set up project docs",
  "initialize project", "create project structure", "write test", "review
  code", or any code-related request that would benefit from minimal, current,
  responsibility-specific context.
---

# Code Constraints

anthor=DingYiXing

This skill is a project-state router and coding-governance workflow.

Use it to:
- determine the current responsibility area (`delivery-surface`, `service-domain`, `pm`, or `cross-area`)
- initialize or patch the minimum project-collaboration document structure
- load only the smallest active fact set needed for the current task
- prevent dirty reads from outdated plans, process logs, or historical designs
- retrieve archived context only when the current task explicitly requires historical traceability
- apply actionable coding constraints distilled from Code Complete 2 once the active project state is clear
- follow a root-level `CLAUDE.md` first when it exists, using it as the collaboration entry contract for routing and responsibility lookup

The skill has two layers:
1. **Project-state layer** — decides what is current, what to read, what to create, and what must stay untouched.
2. **Coding-constraints layer** — applies implementation rules from `references/` after the task has been scoped correctly.

## Core principles

1. **Active facts first.** Default to the smallest current fact set, not the largest available documentation set.
2. **CLAUDE.md before routing.** If a root-level `CLAUDE.md` exists, read it first and use it to determine routing rules, responsibility lookup, and when to ask the user.
3. **Archive is opt-in.** Historical materials are only for explicit backtracking, redesign, migration, or root-cause tracing.
4. **Never overwrite existing user content.** If a file already exists and is non-empty, preserve it.
5. **Locked means no proactive redesign.** If a page, module, interface, or requirement is marked completed/locked, do not restyle, restructure, or re-architect it unless the user explicitly asks.
6. **One current truth, many historical references.** Current truth belongs in a tiny active layer; detailed history belongs in archive.
7. **Patch missing structure, do not rebuild the whole project.** Create only what is missing.
8. **Code does not outrank current facts by default, and old docs never outrank current facts.** Resolve conflicts deliberately.

## Document layers

Treat project documents as belonging to one of three layers.

### 1. Active
Current truth. These are the only documents that should enter context by default.

Typical examples:
- current phase goals and scope
- current priorities
- current acceptance criteria
- current implementation boundaries
- current locked/no-redesign zones
- responsibility-area entry files for delivery surfaces, service domains, and pm

### 2. Reference
Long-lived design material. Load only when the current task truly needs it.

Typical examples:
- API design
- architecture design
- data design
- visual design
- module design

### 3. Archive
Historical material. Default to not reading it.

Typical examples:
- completed requirement details
- closed phase progress notes
- old plans
- deprecated constraints
- historical handoff notes

If active facts conflict with reference or archive materials, **active facts win**.
Archive content must never be used as the default basis for current implementation.

## Responsibility routing

Choose the narrowest responsibility area that matches the current task.

### delivery-surface
Use for user-facing delivery work such as web, ios, android, miniapp, admin, or other client surfaces. Typical tasks include page implementation, interactions, client state, API integration, surface-specific acceptance, and UI fixes.
Default active reading is: the current delivery-surface entry file, the delivery-surface execution view when actively推进任务, current boundaries, current acceptance, current locked zones, blocker list only when the task is actually blocked, and task-specific API contracts only if required.

### service-domain
Use for service-side or shared service work such as api, jobs, data, auth, or other service domains. Typical tasks include domain logic, APIs, data access, permissions, security, jobs, service testing, and service-side fixes.
Default active reading is: the current service-domain entry file, the service-domain execution view when actively推进任务, current boundaries, current acceptance, current locked zones, blocker list only when the task is actually blocked, and task-specific interface or data contracts only if required.

### pm
Use for project goals, scope, priorities, acceptance criteria, risk tracking, task splitting, lock decisions, and current delivery state.

### cross-area
Use only when the task truly spans boundaries: integration, migration, boundary disputes, shared acceptance, or project-wide coordination.

Do not load cross-area material unless the task genuinely crosses responsibility boundaries.

## Project state machine

Every invocation must begin by deciding whether the project is in `normal`, `bootstrap`, or `patch` mode.

### normal
Use when the project already has an active collaboration structure.

Behavior:
- do not create new structure
- if a root-level `CLAUDE.md` exists, read it first as the routing and responsibility entry contract
- use `docs/.project-docs-manifest.yaml` as the sentinel for default active files and responsibility-area entry files
- read only the minimum active set for the chosen responsibility area
- read reference files only when the task needs them
- read archive only through the archive retrieval protocol

### bootstrap
Use when the project is effectively uninitialized.

Behavior:
- create the minimum docs structure
- create a root-level `CLAUDE.md` that tells Claude where to look for responsibility and active docs
- create the minimum active-layer files
- create a manifest file that records the structure version and responsibility lookup
- create an initialization record
- do not create extra long-form design docs unless the user asks

### patch
Use when the project has some docs, but is missing required active-layer or responsibility-area entry files.

Behavior:
- create only missing directories/files
- never overwrite existing non-empty files
- prefer adding a companion file or migration note over rewriting user-authored docs
- patch the active layer first before adding deeper design structure

## Initialization detection

Use these heuristics to decide which mode applies.

### Enter bootstrap mode when:
- the `docs/` directory does not exist at the project root directory, or
- the project has no manifest and no recognizable active-core files, or
- the user explicitly says this is a new project, project setup, initialization, or first-time documentation task

### Enter patch mode when:
- the `docs/` directory exists at the project root directory but the manifest is missing, or
- active-core files are incomplete, or
- the current responsibility-area entry file is missing, or
- the project only has old long-form docs and lacks a compact active layer

### Enter normal mode when:
- the manifest exists, and
- the active-core files exist, and
- the current responsibility-area entry file exists

## Minimum structure to create

When bootstrapping, create only the minimum collaboration structure.
These docs are project-level shared facts and should live at the project root directory, alongside the project's top-level code or app directories, not inside one side's source tree.
Here, “project root directory” means the root of the current project scope the skill is operating on, not a literal folder named `project-root`.

```text
<project-root-directory>/
├── CLAUDE.md
├── docs/
│   ├── .project-docs-manifest.yaml
│   ├── 00-导航/
│   │   └── 项目经理导航文档.md
│   ├── 10-共享状态/
│   │   ├── 当前阶段目标与范围.md
│   │   ├── 当前任务优先级清单.md
│   │   ├── 当前阻塞与待修复问题清单.md
│   │   ├── 当前验收标准清单.md
│   │   ├── 当前实现边界对照.md
│   │   └── 当前锁定范围与禁止主动重构清单.md
│   ├── 20-交付面/
│   ├── 30-服务域/
│   ├── 40-项目治理/
│   │   ├── 项目协作与开发原则.md
│   │   └── AI防脏读与防回滚规则.md
│   ├── 90-过程记录/
│   │   └── 000-项目初始化.md
│   └── 99-归档/
├── <top-level-code-dir-a>/
└── <top-level-code-dir-b>/
```

Read `references/bootstrap-templates.md` when you need the minimal content expectations for these files.

## Idempotency and safety rules

- Create a directory only if it does not exist.
- Create a file only if it does not exist.
- If a file exists and is non-empty, do not overwrite it.
- If a template evolves, do not rewrite old files automatically; create a migration note or missing companion file instead.
- Never rebuild the entire docs tree when only one or two active files are missing.
- Never auto-delete archive content.
- When in doubt, preserve user-authored content and create a missing companion file instead of editing aggressively.

## Minimal reading protocol

The whole point is to minimize token use and avoid stale context.

### For delivery-surface work, default to:
1. the current delivery-surface entry file
2. the current delivery-surface task execution view when the task is in active progress
3. current implementation boundaries
4. current acceptance criteria
5. current locked/no-redesign zones
6. shared blocker list only when there is an active API/bug/integration blocker
7. task-specific API contract only if required

### For service-domain work, default to:
1. the current service-domain entry file
2. the current service-domain task execution view when the task is in active progress
3. current implementation boundaries
4. current acceptance criteria
5. current locked/no-redesign zones
6. shared blocker list only when there is an active API/bug/integration blocker
7. task-specific interface or data contract only if required

### For PM work, default to:
1. current phase goals and scope
2. current priorities
3. current acceptance criteria
4. current locked zones
5. shared blocker list only when tracking progress, risk, or acceptance blockers

### For cross-area work, default to:
1. current implementation boundaries
2. current acceptance criteria
3. current locked zones
4. only the responsibility-area entry files directly involved
5. shared blocker list only when the task is truly blocked across areas
6. reference docs only if the active layer is insufficient

Do **not** default to long process logs, archived plans, old redesign notes, or project-wide omnibus documents.

## Archive retrieval protocol

Archived requirements, old plans, and historical process notes are not current execution guides.

Only retrieve archive material when one of the following is true:
- the user explicitly asks to review old design, old progress, or a previous phase
- the current task is revisiting, migrating, or repairing a previously completed area
- an active-layer doc explicitly points to an archived source
- you need to explain why a current constraint exists or why an old one was dropped
- there is a real conflict that requires historical traceability

When archive access is necessary:
1. read the smallest possible archive index/summary first
2. retrieve only the 1-2 most relevant archived files
3. do not scan the whole archive tree by default

Do not use archived requirements, historical plans, or old process notes as the default basis for current implementation.

## Locked-state protection

If a page, module, interface, or requirement is marked completed, locked, or no-redesign:
- do not proactively restyle it
- do not proactively re-architect it
- do not proactively rename or normalize it just because an older doc suggests another direction
- do not treat old design ideals as permission to rewrite working code

If the current implementation is locked and the task is not explicitly a redesign or migration task, preserve the implementation and update facts instead of reworking the code.

## Conflict resolution

When sources disagree, use this priority order:

1. active canonical facts
2. current responsibility-area entry file
3. task-specific referenced docs
4. reference design docs
5. process records
6. archived docs

Apply these rules:
- active vs archive → active wins
- active vs reference → active wins
- code vs old archive → do not revert code because of archive
- code vs active facts → determine which one is stale before changing anything
- if docs are stale, prefer updating the active fact source over dragging code backward

## Modern default behavior overrides

Before applying the coding rules in `references/`, normalize them to modern repository defaults.
This layer exists to prevent historically useful but overly heavy rules from turning into default agent behavior.

1. **Core safety and correctness still win.** Any `[核心]` or security-relevant rule about correctness, data loss, privilege boundaries, injection, undefined behavior, or real runtime hazards remains in force.
2. **Project instructions outrank generic ceremony.** A root-level `CLAUDE.md`, active-layer project docs, and established repository conventions take priority over generic `[扩展]` or `[历史]` guidance.
3. **Prefer the minimum sufficient change.** Do not add abstractions, helper layers, validation paths, comments, headers, or scaffolding unless they improve the current code materially.
4. **Do not add ceremony by default.** Skip heavyweight practices unless the project already uses them or the task explicitly asks for them: file header metadata, author/contact blocks, version-control tags in source files, UDF/SDF-style design traces, mandatory pseudocode-as-comments workflows, or comments on every control structure.
5. **Validate at boundaries, not everywhere.** Validate external, cross-process, persistence, network, filesystem, user-input, and other untrusted boundary data. Do not duplicate defensive validation on already-trusted internal flows unless the current architecture explicitly requires it.
6. **Prefer native language and ecosystem mechanisms.** When a language or framework already provides the modern, idiomatic solution, prefer it over older manual patterns. Examples: type systems over comment-only contracts, linters/static analysis over manual checklists, structured exceptions/results over ad hoc status plumbing, and standard library/container abstractions over custom low-level workarounds.
7. **Comments are exceptional, not automatic.** Prefer self-explanatory code. Add comments only for non-obvious intent, invariants, workarounds, surprising behavior, or important constraints that the code alone cannot express.
8. **Abstraction must pay for itself now.** Extract functions, layers, and reusable helpers only when they reduce present complexity, duplication, or boundary confusion. Do not fragment obvious local logic just to satisfy a generic rule about small routines.
9. **When a generic rule conflicts with modern clarity, choose clarity.** If an `[扩展]` or `[历史]` rule would make the result noisier, more ceremonial, or less idiomatic without improving safety or correctness, prefer the simpler modern implementation and briefly document the choice when needed.

## Coding constraints layer

Once the project state is clear, route to the Code Complete rule files below.

## Priority

1. correctness
2. readability
3. maintainability
4. simplicity
5. consistency
6. performance

Lower priority never overrides higher. On same-level conflict, choose the safer, more intuitive option for callers and future maintainers. Document the reasoning.

### Conflict Resolution

When two `[必须]` rules conflict in a specific context:

1. **Narrower scope wins.** A rule about the specific function you're writing beats a rule about "all functions in general."
2. **Same scope: climb the priority ladder.** Correctness > readability > maintainability > simplicity > consistency > performance.
3. **Same scope, same priority: choose the safer option** — the one less likely to cause bugs, data loss, or confusion for future maintainers.
4. **Document the choice.** Add a one-line comment explaining why rule X was preferred over rule Y.
   Example: `# CH07.S01 over CH07.S04: extracting this 3-line validator would fragment the validation logic`

## Format

- `[必须]` = required. Must follow unless there is a documented reason not to.
- `[禁止]` = prohibited. Must not do this.
- `[核心]` = core rule. Applies universally — correctness, safety, fundamentals.
- `[扩展]` = extended rule. Situational — optimization, conventions, process.
- `[语言特定]` = language-specific. Only applies to named languages.
- `[历史]` = legacy. Rarely applicable to modern code.
- `anchor=CC2.CHxx.Syy` traces rule to its source section in Code Complete 2.

### Core Criteria

A rule should be marked `[核心]` only if all three hold:

1. **Default-must-read**: reading these rules alone is sufficient to avoid common, severe, or hidden bugs in this domain.
2. **Language-independent**: the rule applies regardless of programming language.
3. **Minimal-execution**: the rule states a concrete, immediately actionable constraint, not a methodology choice, architectural strategy, or optimization technique.

Rules that fail criterion 3 belong in `[扩展]`. Rules tied to a specific language belong in `[语言特定]`. Legacy conventions belong in `[历史]`.

For quick tasks, filter to `[核心]` only. For thorough work, include `[扩展]`. Skip `[语言特定]` and `[历史]` unless the language/context matches.

## Reading protocol for coding rules

1. **First, scan `[核心]` rules** in the target file(s) — these cover ~10-30% of rules, are the minimal safe working surface, and always apply.
2. **Then, read `[扩展]` rules** only when:
   - the task is complex (multi-file, multi-class, or architectural)
   - you're writing public API surfaces
   - the code handles money, security, or safety-critical operations
3. **Skip `[语言特定]` rules** unless the language matches the current file.
4. **Skip `[历史]` rules** unless the project explicitly uses those patterns.
5. **Templates** in `references/templates.md` — load only when creating new files or new public functions. Skip for small edits and bug fixes.

Each reference file's header tells you what `[核心]` and `[扩展]` cover in that domain.

## Routing

| When you are | Load |
|---|---|
| planning project collaboration, project state, current truth, archive policy, or active-layer governance | references/project-state.md |
| bootstrapping a new project or patching missing collaboration docs | references/project-state.md, references/bootstrap-templates.md |
| handling task boards, blocker lists, handoff status, or execution views | references/project-state.md, references/bootstrap-templates.md |
| preparing commits / branches / merges / rebases / PR workflow | references/git-workflow.md, references/process.md |
| writing functions / methods | references/writing.md, references/naming.md, references/layout.md, references/defense.md |
| naming anything | references/naming.md |
| designing classes / modules / interfaces | references/design.md, references/naming.md |
| writing control flow / conditions / loops | references/control.md |
| handling errors / exceptions / edge cases | references/defense.md |
| formatting / laying out code | references/layout.md |
| writing or editing comments / docs | references/comments.md |
| creating a new source file / writing file headers | references/layout.md, references/comments.md, references/templates.md |
| writing tests / test cases | references/quality.md, references/templates.md |
| debugging / fixing a bug | references/debugging.md |
| refactoring existing code | references/refactoring.md, references/design.md |
| optimizing performance / tuning code | references/performance.md |
| new project / module setup / planning | references/process.md, references/project-state.md |
| code review / PR review / merge readiness check | references/process.md, references/git-workflow.md, references/project-state.md |

`references/warning-signs.md` applies to all coding activities — load it when uncertain.

## Git workflow quick entry

For commit / PR / MR / merge-readiness tasks, `references/git-workflow.md` is the execution file.

### Author-side entry

Use this path when deciding whether a change is ready to submit:
- `Submission timing`
- `Do not submit yet when`
- `Commit message templates`
- `Pre-commit checklist template`
- `PR / MR description templates`

### Reviewer-side entry

Use this path when deciding whether a submitted change is ready to approve or merge:
- `Review / merge gate`
- `Reviewer checklist template`
- `Reviewer guidance`

### Fast-path usage

- “can I commit this now?” → `Pre-commit checklist template`
- “how should I write this commit or PR?” → use the templates
- “is this ready to approve or merge?” → use the reviewer-side checks and verify claims against active facts

## Usage

1. Determine the task responsibility area.
2. Determine whether the project is in `normal`, `bootstrap`, or `patch` mode.
3. If a root-level `CLAUDE.md` exists, read it first.
4. Read only the minimum active-layer material needed for the current responsibility area.
5. Create or patch the minimum structure only if required.
6. Use archive only through the archive retrieval protocol.
7. Once the active project state is clear, follow the routing table above and apply all `[必须]` rules while avoiding all `[禁止]` rules.
8. For commit / PR / MR / merge-readiness tasks, switch to the Git workflow quick entry and apply the matching author-side or reviewer-side sections in `references/git-workflow.md`.
9. When in doubt, default to correctness, readability, and the smallest current fact set.

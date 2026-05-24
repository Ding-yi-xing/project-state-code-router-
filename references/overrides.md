# Modern Override Layer

**Scope:** Rules from the Code Complete 2 reference files that are downgraded or replaced by modern defaults.
**Load:** Always read `[核心]` overrides before applying rules from any other reference file. When an override conflicts with a rule in another reference file, the override wins.

## Override precedence

```
modern_override > active_layer > user_config > reference_defaults > legacy_archive
```

When a rule is listed here with `action: downgrade` or `action: replace`, the referenced file's original rule is superseded. Do not apply both.

---

## Core overrides (always apply)

### Comment philosophy

| Original | Reference | Action | Modern replacement |
|----------|-----------|--------|--------------------|
| `[扩展][必须]` Comment liberally on design decisions, file headers, and routine mechanics | comments.md §Design Documentation | **downgrade** to `[扩展][可选]` | Prefer self-documenting code. Comment intent and constraints, not obvious mechanics. File headers are unnecessary — use `git blame`. |
| `[扩展][必须]` Use UDF/SDF folders to record design decision trails | comments.md line 11 | **replace** | The project-state layer's `docs/units/<unit>/` structure is the modern UDF/SDF. Use `status.md`, `requirements/`, `blockers/`, and `issues/` instead of paper-trail folders. |

### Naming conventions

| Original | Reference | Action | Modern replacement |
|----------|-----------|--------|--------------------|
| `[扩展][必须]` Variable names 8-20 chars, average 10-16 | naming.md §11.1 | **downgrade** to `[扩展][可选]` | Use meaningful names at any reasonable length. Modern IDEs autocomplete. `customerEmailAddress` is better than `custEmlAddr`. |
| Hungarian notation (implied by type-prefix rules) | naming.md (various) | **disable** | Not applicable in modern typed languages with IDE type hints. |

### Design & architecture

| Original | Reference | Action | Modern replacement |
|----------|-----------|--------|--------------------|
| `[扩展][必须]` Full class design before coding (PPP) | writing.md §Pseudocode Programming Process | **downgrade** to `[扩展][可选]` | For routine classes, design the interface contract and write the implementation iteratively. Full PPP is reserved for complex algorithms with non-obvious logic. |
| `[扩展][必须]` Create inline subroutines for even trivially simple operations | writing.md line 14 | **downgrade** to `[扩展][可选]` | Extract only when the extraction reduces duplication or clarifies intent. A 2-line helper used once is noise. |

### Defensive programming

| Original | Reference | Action | Modern replacement |
|----------|-----------|--------|--------------------|
| `[扩展][必须]` Check ALL subroutine input parameters as if from external sources | defense.md §Input Validation line 19 | **narrow** to public APIs only | Validate at system boundaries (public APIs, user input, external data). Internal/private methods may trust callers within the same module. Assertions are preferred for internal invariants. |
| `[扩展][必须]` Check return values of ALL functions, even ones you think cannot fail | defense.md line 53 | **narrow** to I/O and external calls | Trust the language runtime and standard library for pure operations. Always check I/O, network, and FFI calls. |

### Process & methodology

| Original | Reference | Action | Modern replacement |
|----------|-----------|--------|--------------------|
| `[扩展][必须]` Formal change control board for requirements | process.md §Requirements | **downgrade** to `[扩展][可选]` | For small-medium projects: use PR reviews and issue tracking. Formal CCB is for life-critical or regulated systems. |
| `[扩展][必须]` 80% requirements detailed upfront | process.md §Requirements | **downgrade** to `[扩展][可选]` | For modern iterative projects: detail only the current sprint/milestone. Keep a lightweight backlog for the rest. |

### Legacy language features

| Original | Reference | Action | Modern replacement |
|----------|-----------|--------|--------------------|
| `[扩展][必须]` Rules about macros, inline, `#define` | writing.md §Macros | **disable** for languages without a preprocessor | These rules apply only to C/C++. Skip entirely for Python, TypeScript, Go, Rust, Java, etc. |
| `[扩展][禁止]` Freeing pointers without nulling | warning-signs.md line 18 | **disable** for GC languages | Not applicable to garbage-collected or ownership-managed languages. |
| `[扩展][必须]` Isolate non-portable code in subroutines | writing.md line 17 | **keep** as `[核心]` | This rule ages well. Still applies: isolate platform-specific code. |

---

## How to use overrides

1. When loading a reference file for a task, scan this overrides list first for matching entries.
2. If an override matches a rule you're about to apply, use the modern replacement.
3. If no override matches, apply the original rule as-is.
4. The `action` field tells you what to do:
   - `downgrade`: the rule is still valid but no longer mandatory. Treat as optional guidance.
   - `replace`: use the modern replacement instead. The original rule does not apply.
   - `narrow`: the rule still applies but only in a restricted scope.
   - `disable`: the rule does not apply in modern contexts. Skip it.
   - `keep`: the rule is re-affirmed at its original level.

## When to add new overrides

Add an override when:
- A CC2 rule consistently produces noise without improving correctness for modern projects
- The project's CLI, IDE, or language features make a rule redundant
- The project's collaboration model (project-state layer) provides a lighter equivalent

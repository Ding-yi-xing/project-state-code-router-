---
name: project-state-code-router
description: >
  This skill should be used when the user asks to write, modify, refactor, review,
  debug, or continue code and project work. It fuses two layers: a project-state /
  collaboration router plus actionable coding constraints distilled from Code
  Complete 2 and OpenAI's harness-engineering practices. Trigger on: initializing
  or patching project collaboration docs, routing work through project-defined
  units, avoiding dirty reads in multi-person documentation workflows, writing
  functions, designing classes, naming variables, handling errors, writing
  comments/documentation, testing, debugging, refactoring, optimizing performance,
  setting up projects, code review, establishing architecture layers or boundary
  enforcement, installing doc-gardening or code garbage collection on a project,
  defining project-level golden rules, and preventing documentation or code rot.
  Use when the user mentions docs setup, project collaboration, current status,
  requirements, blockers, archive, implementation, refactor, fix bug, add function,
  create class, write test, add comment, review code, architecture boundaries,
  layer rules, doc-gardening, garbage collection, code rot, golden rules, lint
  drift, or any code-related request that benefits from minimal current context
  plus coding-governance guidance.
compatibility:
  tools:
    - Read
    - Write
    - Edit
    - Glob
    - Grep
---

# Project State Router and Code Constraints

Skill 入口（地图层）。详细规则全部下沉到 `references/`，按需加载。

**维护者自律**：本文件目标 ≤ 150 行。详细行为规则不放在这里，全部到对应 reference。新增内容前先问"这是路由决策还是详细规则"，详细规则一律下沉。这是给 skill 维护者的自律提示，不靠脚本强制。

## 两层模型

| 层 | 解决什么 | 主入口 |
|---|---|---|
| 项目状态层 | 当前任务属于哪个工作单元、可信事实集是什么、是否需要补结构、跨单元如何避免脏读 | `references/project-state.md` |
| 代码约束层 | 命名、设计、防御、调试、布局、性能等具体编码规范 | `references/overrides.md` 先加载，再按路由表 |

使用顺序：先项目状态层缩小可信上下文，再代码约束层执行规范。如果是纯代码任务且不涉及协作文档，直接进代码约束层。

## 模式判定（项目状态层）

| 模式 | 进入条件 | 行为 |
|---|---|---|
| `bootstrap` | 无 `docs/`、无 manifest、无活动层文档 | 只创建最小骨架，不预创建业务单元和条目 |
| `patch` | 有 `docs/` 但 manifest / 活动层 / 单元入口缺失 | 只补缺失文件，不覆盖已有非空文件 |
| `normal` | manifest、活动层、当前单元入口都存在 | 不新建结构，只读最小必要文档，只在当前单元内做最小更新 |

详细规则、各模式具体行为、骨架结构 → `references/project-state.md` 和 `references/bootstrap-templates.md`。

## 默认读取顺序（项目状态层）

1. 根 `CLAUDE.md`（若存在）
2. `docs/.project-docs-manifest.yaml`
3. 定位当前工作单元
4. 只读当前单元最小集（manifest.md、status.md，按需 requirements / blockers / issues / sync）
5. 只在跨单元 / 共享事实 / 共享验收时才读 `shared/current/`
6. archive 仅在显式需要历史时读

## 绝对安全规则（标题清单）

详细规则在 `references/project-state.md`：
- 永远不要覆盖已有非空文件
- 永远不要在初始化时捏造业务事实
- 永远不要把归档当当前执行面
- 永远不要默认跨单元写入
- 否决条件优先（先读锁定范围 → 否决 → 才评估）
- 禁止事项必须具体点名（字段、接口路径、文件名、包名）

**强制深读触发条件**：以下任务**必须**完整加载 `references/project-state.md`，不得仅依赖本文件的标题清单：
- PM / 范围决策 / 是否纳入新需求
- 跨单元写入或评估
- 任何"是否批准"的判断（必须输出读了哪些否决条件、哪条规则被触发）
- 重新激活归档事项

## 轻量任务快速通道

任务同时满足：单文件、非结构性、非首次、非安全关键 → 跳过项目状态层和完整路由，只加载 `references/warning-signs.md` 的 `[核心]` 部分。典型场景：代码 typo 修复、变量重命名、单行 bug 修复、注释修正、文档 typo 修正、单段措辞调整。如果执行中范围超出（如发现牵连其他文件、动到接口签名、发现要新建测试），回退完整流程。

## 代码约束层加载协议

0. **先加载** `references/overrides.md` 的 `[核心]` overrides — override 永远胜过它指向的原规则。
1. 然后扫描目标 reference 的 `[核心]` 规则（约 10–30%，最小安全工作面，永远适用）。
2. 仅在以下情况读 `[扩展]` 规则：任务复杂（多文件 / 多类 / 架构）、写公开 API、涉及金钱 / 安全 / 安全关键。
3. `[语言特定]` 跳过，除非语言匹配。
4. `[历史]` 跳过，除非项目显式使用对应过时模式。
5. `references/templates.md` 仅在创建新文件 / 新公开函数时读。

每个 reference 文件的头部都有 `Scope` / `Core` / `Extended` 说明，告诉你它覆盖什么。

## 优先级与冲突解决

优先级：correctness > readability > maintainability > simplicity > consistency > performance。

两条 `[必须]` 规则在具体场景冲突时：(1) 范围更窄的规则胜出；(2) 同范围按上面的优先级阶梯；(3) 同范围同优先级选更安全的；(4) 用一行注释记录选择理由（如 `# CH07.S01 over CH07.S04: 抽出会割裂校验逻辑`）。

## 规则标签

- `[必须]` / `[禁止]` — 必须遵守 / 必须不做
- `[核心]` — 通用、语言无关、立即可执行的安全底线
- `[扩展]` — 情境化（优化、约定、流程）
- `[语言特定]` — 仅适用于命名语言
- `[历史]` — 过时模式，现代代码很少用
- `anchor=CC2.CHxx.Syy` — 追溯到 Code Complete 2 章节

`[核心]` 资格三条件全部成立才能打：默认必读、语言无关、最小可执行约束。失之第三条进 `[扩展]`，绑语言进 `[语言特定]`，过时进 `[历史]`。

## Routing

| When you are | Load |
|---|---|
| planning project collaboration / project state / current truth / archive policy | references/project-state.md |
| bootstrapping or patching collaboration docs | references/project-state.md, references/bootstrap-templates.md |
| handling task boards / blocker lists / handoff status | references/project-state.md, references/bootstrap-templates.md |
| preparing commits / branches / merges / rebases / PR workflow | references/git-workflow.md |
| writing functions / methods | references/naming.md, references/layout.md, references/defense.md |
| naming anything | references/naming.md |
| designing classes / modules / interfaces | references/design.md, references/naming.md |
| establishing architecture layers / enforcing layer boundaries / preventing dependency drift | references/architecture-layers.md, references/design.md |
| writing control flow / conditions / loops | references/control.md |
| handling errors / exceptions / edge cases | references/defense.md |
| formatting / laying out code / writing comments | references/layout.md |
| creating a new source file / writing file headers | references/layout.md, references/templates.md |
| writing tests / test cases | references/quality.md, references/templates.md |
| debugging / fixing a bug | references/debugging.md |
| refactoring existing code | references/design.md, references/architecture-layers.md |
| optimizing performance / tuning code | references/performance.md |
| new project / module setup / planning | references/project-state.md |
| quality check / informal desk check | references/quality.md |
| code review / PR review / merge readiness check | references/git-workflow.md, references/project-state.md, references/quality.md |
| installing doc-gardening or code GC on a project (rot prevention, drift checks) | references/gc-rules.md |

`references/overrides.md` 和 `references/warning-signs.md` 适用于所有编码活动 — 先加载，再加载路由表对应文件。

PR review 还要按变更内容继续路由：改了 API 加 design.md / defense.md，改了样式加 layout.md，改了测试加 quality.md。

通用 implementation 任务（"实现一个 X"、"加一个功能"）按它**实际包含的操作**对号入座 — 通常会是 "writing functions / methods" + "designing classes / modules / interfaces" + "writing tests" 的组合，按需多行同时加载。

## Usage

写代码前先判断是否需要项目状态路由以收敛事实集，再在路由表里找当前任务，加载列出的 reference，应用 `[必须]` 规则、避免 `[禁止]` 规则。规则归属不清时，默认正确性和可读性。

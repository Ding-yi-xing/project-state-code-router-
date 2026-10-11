---
name: project-state-code-router
description: >-
  Route project work through current repo docs: identify responsibility, active
  truth, plans, and write-back destinations before implementation. Use for project
  status, handoffs, plans, docs audits/repairs, scope, blockers, archives, and
  cross-unit work. Not a replacement for project or language-specific coding rules.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Project State Router and Code Constraints

Skill 入口（地图层）。详细规则全部下沉到 `references/`，按需加载。

**维护者自律**：本文件目标 ≤ 150 行。详细行为规则不放在这里，全部到对应 reference。新增内容前先问"这是路由决策还是详细规则"，详细规则一律下沉。这是给 skill 维护者的自律提示，不靠脚本强制。

## 两层模型

| 层 | 解决什么 | 主入口 |
|---|---|---|
| 项目状态层 | 当前任务属于哪个工作单元、可信事实集是什么、事实变更应写回哪里、跨单元如何避免脏读 | `references/project-state.md` |
| 代码约束层 | 无项目 / ECC / 语言规则时的兜底编码约束；若存在项目规则或 ECC rules，以它们为主 | `references/overrides.md` 先加载，再按路由表 |

使用顺序：先项目状态层缩小可信上下文，再代码约束层执行规范。如果项目已经有 ECC / language / framework 规则，代码约束层只补项目状态和文档写回缺口，不覆盖这些规则。

## 文档现行原则

非平凡编码、架构、跨文件修改或计划推进前，先落轻量计划或 active exec plan（目标、范围、步骤、验证、docs 写回目标、恢复点），再动代码。

## 模式判定（项目状态层）

| 模式 | 进入条件 | 行为 |
|---|---|---|
| `bootstrap` | 无 `docs/`、无 manifest、无活动层文档 | 只创建最小骨架，不预创建业务单元和条目 |
| `patch` | 有 `docs/` 但 manifest / 活动层 / 单元入口缺失 | 只补缺失文件，不覆盖已有非空文件 |
| `normal` | manifest、活动层、当前单元入口都存在 | 不新建结构，只读最小必要文档，只在当前单元内做最小更新 |
| `audit` | 用户要求审计、合规检查或 docs 治理 | 全面只读检查；分类报告，不自动修复 |
| `repair` | 用户明确要求按审计结果整改 | 按确认范围最小增量修复，再运行审计验证 |

详细规则、各模式具体行为、骨架结构 → `references/project-state.md` 和 `references/bootstrap-templates.md`。
`audit` / `repair` → `references/audit-protocol.md`。

`audit` 默认只读，不得顺手修复；区分当前规则违规与历史迁移债务。可用脚本时运行 `scripts/audit_project_docs.py <project-root>`，脚本结果是证据而非完整判断，必须结合代码、测试和近期过程记录核对 current truth。

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

**强制深读**：PM/范围或批准决策、跨单元工作、恢复/推进计划、非平凡编码前规划、重新激活归档时，完整读取 `references/project-state.md`；批准判断还须列出已检查的否决条件及触发规则。

## 轻量任务快速通道

单文件、非结构性、非首次且非安全关键的小改动可走快速通道，仅加载 `references/warning-signs.md` 核心规则；一旦范围扩展，立即回到完整路由。

## 完成前写回检查

每次项目工作结束前，必须检查本次是否改变了需求、问题、阻塞、跨单元协同、共享范围、验收标准、过程记录、活动计划或归档状态。`status.md` 只是 dashboard / index，不得作为需求、问题、阻塞、协同、过程或完成项的唯一事实源。按 `references/project-state.md` 的 write-back routing 更新权威文档；若无需同步，说明为什么除了 `status.md` 不需要更新其他 docs。

## 代码约束层加载协议

先读 `references/overrides.md` 核心覆盖，再读目标 reference 的核心规则；复杂任务、公开 API 或高风险才读扩展规则。语言规则仅在语言匹配时读，历史规则仅在相关旧模式出现时读；新文件/公开函数再读 `templates.md`。

## 优先级与冲突解决

优先级：correctness > readability > maintainability > simplicity > consistency > performance。规则冲突时，窄范围优先，其次按此序；仍相同时选更安全者并简记理由。

## 规则标签

`[必须]` / `[禁止]` 是强制项；`[核心]` 通用必读，`[扩展]` 情境化，`[语言特定]` 仅匹配语言时适用，`[历史]` 仅对应旧模式适用。核心规则须通用且最小可执行。

## Routing

| When you are | Load |
|---|---|
| planning project collaboration / project state / current truth / archive policy | references/project-state.md |
| continuing previous work / resuming interrupted work | references/project-state.md |
| advancing active exec plans / project plan progress | references/project-state.md, references/bootstrap-templates.md |
| planning before non-trivial coding or architecture | references/project-state.md, references/bootstrap-templates.md |
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
| docs / project-state audit or repair | references/audit-protocol.md; optional scripts/audit_project_docs.py |
| quality check / informal desk check | references/quality.md |
| code review / PR review / merge readiness check | references/git-workflow.md, references/project-state.md, references/quality.md |
| installing doc-gardening or code GC on a project (rot prevention, drift checks) | references/gc-rules.md |

`references/overrides.md` 和 `references/warning-signs.md` 适用于所有编码活动 — 先加载，再加载路由表对应文件。

PR review 还要按变更内容继续路由：改了 API 加 design.md / defense.md，改了样式加 layout.md，改了测试加 quality.md。

通用 implementation 任务（"实现一个 X"、"加一个功能"）按它**实际包含的操作**对号入座 — 通常会是 "writing functions / methods" + "designing classes / modules / interfaces" + "writing tests" 的组合，按需多行同时加载。

## Usage

写代码前先判断是否需要项目状态路由以收敛事实集；继续任务时从 active docs / active exec plans 恢复，不只依赖 chat history；非平凡编码或架构前先落持久计划；完成前按 write-back checklist 同步 repo docs。规则归属不清时，默认正确性、当前 active 事实和可恢复协作。

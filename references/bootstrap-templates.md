# Bootstrap Templates Guidance

author=DingYiXing

**Scope:** Minimum collaboration docs to create during bootstrap or patch.
**Core:** create only the smallest structure that supports current truth, responsibility lookup, and work-unit routing.
**Extended:** suggested headings and minimal contents.
**Often used with:** project-state.md.
**Read Next If:** the project will use architecture-enforced layer boundaries → architecture-layers.md; the project needs doc-gardening or code-rot GC → gc-rules.md; writing CLAUDE.md routing contract → project-state.md (Responsibility routing section).

## Create only these directories by default

These collaboration docs belong at the project root directory and should sit alongside the project's top-level code or app directories.

```text
<project-root-directory>/
├── CLAUDE.md
├── docs/
│   ├── .project-docs-manifest.yaml
│   ├── DESIGN.md            # 长期设计原则（可选）
│   ├── FRONTEND.md          # 前端原则（可选）
│   ├── RELIABILITY.md       # 可靠性原则（可选）
│   ├── SECURITY.md          # 安全原则（可选）
│   ├── PRODUCT_SENSE.md     # 产品判断原则（可选）
│   ├── GOLDEN_RULES.md      # 项目级机械规则清单（可选，见 gc-rules.md）
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
│   │   ├── exec-plans/
│   │   │   ├── active/
│   │   │   ├── completed/
│   │   │   └── tech-debt-tracker.md
│   │   ├── generated/
│   │   └── archive/
│   ├── units/
│   │   └── .template/
│   ├── references/          # 喂给 AI 的稳定外部参考（可选）
│   │   ├── <lib-a>-llms.txt
│   │   └── <lib-b>-llms.txt
│   └── process/
│       └── 000-项目初始化.md
├── <top-level-code-dir-a>/
└── <top-level-code-dir-b>/
```

## Bootstrap input

Before creating work-unit entries, ask the project manager or current user for:
- work units to create under `docs/units/` (for example: `order-service`, `admin-web`, `miniapp`, `billing`, `auth`)
- owner or team for each work unit
- optional human-readable labels when the directory key and display name differ

Only create work units that are currently confirmed as needed.
Do not prefill future work units in the manifest just because they might exist later.

Do not hardcode `frontend` or `backend` as the only work-unit categories.
If the project currently needs only one unit, create only that unit.

## Create only these files by default

### CLAUDE.md
Must include:
- Claude 进入项目后必须先读哪些文件
- 责任归属默认去哪里查询（例如 `docs/.project-docs-manifest.yaml`）
- 当前开发者负责范围不明确时应先询问项目经理或当前用户
- 默认不要自行猜测当前开发者负责的工作单元

Suggested minimal shape:

```md
# Project collaboration entry

Before doing implementation work in this project:
1. Read this file first.
2. Then read `docs/.project-docs-manifest.yaml`.
3. Then read only the entry files and active docs for the relevant work unit.
4. Read reference or archive docs only when the current task truly needs them.

## Responsibility lookup
- Source of truth: `docs/.project-docs-manifest.yaml`
- If the current developer's work unit is unclear, ask the user or project manager

## Active docs
- Shared facts: `docs/shared/current/`
- Work-unit entry files: see manifest entries
```

## Plans as first-class artifacts

OpenAI 在 Harness Engineering 一文里把"计划"提升为一流工件：

> 计划被视为一流的工件。临时轻量计划用于小幅变更，而复杂工作则记录在执行计划中，并附带进度和决策日志，这些日志会被提交到代码仓库。活跃计划、已完成计划和已知的技术债务都已进行版本控制并集中存放。

skill 推荐的对应位置：

| 类型 | 位置 | 用途 |
|---|---|---|
| **轻量计划**（小幅变更） | 不落盘，直接在对话或 PR 描述里说清 | 1-3 步能完成、不需要回看的变更 |
| **执行计划（active）** | `docs/shared/exec-plans/active/` | 进行中的复杂工作；每份含进度日志 + 决策日志 |
| **执行计划（completed）** | `docs/shared/exec-plans/completed/` | 完成后从 active/ 移过来，作为历史决策可查证；不删 |
| **技术债** | `docs/shared/exec-plans/tech-debt-tracker.md` | 已知但暂不修的债，定期被 GC 巡检（见 gc-rules.md） |
| **生成态契约** | `docs/shared/generated/` | 由代码或工具自动生成的契约文件（如 db-schema.md、openapi.json）；不手改 |

执行计划文件建议结构：

```md
# <计划标题>

status: active | completed
owner: <person or team>
created_at: 2026-05-26
started_at: 2026-05-26
completed_at: -
related_units: [<unit-key>, ...]

## 目标
<这个计划要达成什么>

## 拆解
- [ ] 步骤 1：...
- [ ] 步骤 2：...
- [x] 步骤 3：（已完成）

## 进度日志
- 2026-05-26: 启动
- 2026-05-27: 完成步骤 3，发现步骤 1 需要拆分为 1a/1b

## 决策日志
- 2026-05-26: 选 zod 而非 yup（理由：与现有 schema 一致）
- 2026-05-27: 不在本期处理 X，挪到 tech-debt-tracker.md
```

完成后只需要把 `status` 改成 `completed`、填 `completed_at`、把文件从 `active/` 移到 `completed/`。

**为什么提升计划为一流工件**：智能体下次接手时可以**只读这一份文件**就理解上下文、之前的尝试、为什么这么做 — 不需要去翻 chat 历史或外部系统。这正是 OpenAI 帖子里讲的"代码仓库即 system of record"。

## 长期原则文件 vs 当前阶段事实

`docs/shared/current/` 关注**当前阶段**（这一期要做什么、阻塞、验收）— 内容会随版本演进。

`docs/` 根级则放**跨阶段、长期稳定**的原则文件 — 内容半年甚至一年才动一次。这两层是不同维度，不应该混。

OpenAI 仓库根级的对应文件：

| 文件 | 内容 | 谁该写 |
|---|---|---|
| `DESIGN.md` | 设计哲学、核心理念、什么算"好的实现" | 团队技术决策者 |
| `FRONTEND.md` | 前端原则（如统一组件库、状态管理范式、可访问性底线） | 前端负责人 |
| `RELIABILITY.md` | 可用性目标、错误预算、降级策略、SLO | SRE / 后端负责人 |
| `SECURITY.md` | 威胁模型、必须遵守的安全约束、审计点 | 安全负责人 |
| `PRODUCT_SENSE.md` | 产品判断准则、用户优先级、什么是"我们要做的产品" | 产品 / 设计 |
| `GOLDEN_RULES.md` | 项目级机械规则清单（见 gc-rules.md） | 团队共识 |
| `ARCHITECTURE.md` | 顶层架构图、域和包分层（详见 `references/architecture-layers.md`） | 技术负责人 |

不强制必须有几份；按项目实际需要选。命名也可按团队习惯改（如中文名）。

skill 默认不创建这些文件 — 它们的内容只能由人写，不能模板化。bootstrap 时只创建空文件 + 一段 "TODO: fill in" 占位，或者根本不创建，等首次需要时再写。

## docs/references/ — 喂给 AI 的稳定外部参考

OpenAI 仓库里把 `design-system-reference-llms.txt`、`nixpacks-llms.txt`、`uv-llms.txt` 等放在 `references/` 下。这些是**外部依赖的精炼参考**，专门为智能体准备：

> 对智能体来说，通常被称为"枯燥"的技术，由于其可组合性、API 稳定性和在训练集里的表现，往往更容易建立模型。

文件来源：
- 直接拷贝该库的 `llms.txt`（越来越多库自带，如 `https://docs.<lib>.com/llms.txt`）
- 从该库文档里精简一份"我们这个项目用到的子集"
- 自己写的"我们怎么用这个库 + 已知陷阱"

示例命名：
- `docs/references/zod-llms.txt`
- `docs/references/playwright-mcp-llms.txt`
- `docs/references/our-design-system-llms.txt`

注意：这里说的是**下游项目内部的 references/**（即 `docs/references/`），与本 skill 仓库自己的 `references/` 是两个不同的目录。下游项目不应该把 skill 的 reference 文件复制过去。

### docs/.project-docs-manifest.yaml

This is the single source of truth for responsibility routing and active-layer discovery. Every field described below must be present in a valid manifest.

#### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | integer | Schema format version. Current: `1`. Skill checks this to detect incompatibility. |
| `structure_version` | integer | Project-specific layout version. Increment when the docs directory structure changes. |
| `initialized_by` | string | Identifier of the tool/skill/person that created the manifest. |
| `initialized_at` | string | ISO 8601 date (e.g. `2026-05-24`). |
| `responsibility_lookup` | object | Defines how to resolve responsibility for a task. Must contain `primary_source` (path to the file that owns responsibility mapping) and `fallback_action` (one of `ask-user`, `ask-pm`, `prompt-create-unit`). |
| `roles` | object | Maps role keys (`pm`, `cross_area`, or custom roles) to their entry files. Each role entry must have an `entry` field pointing to the navigation or status file for that role. |
| `work_units` | array | List of work unit objects. May be empty (`[]`) if no units have been created yet. |
| `active_core_files` | array of strings | Ordered list of paths (relative to project root) that form the default active-layer reading set. Files are read in the order listed. |

#### Work unit entries

Each entry in `work_units`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Machine-readable unit identifier (e.g. `order-service`). Used as the directory name under `docs/units/`. |
| `label` | string | yes | Human-readable display name (e.g. `订单服务`). |
| `owner` | string | yes | Team or person responsible for this unit. |
| `entry` | string | yes | Path to the unit's `manifest.md` file. |

#### Optional fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | One-line description of the project. |
| `docs_root` | string | Custom docs directory path. Defaults to `docs/`. |
| `archive_readonly` | boolean | Whether archive is strictly read-only. Defaults to `true`. |
| `reactivation_required` | boolean | Whether archived items must be reactivated (new entry) rather than directly edited. Defaults to `true`. |
| `layer_priority` | array of strings | Override precedence order. Default: `["active", "reference", "archive"]`. For modern-override behavior, set to `["modern_override", "active", "reference", "archive"]`. |

Suggested minimal shape:

```yaml
schema_version: 1
structure_version: 1
initialized_by: project-state-code-router
initialized_at: 2026-05-07
responsibility_lookup:
  primary_source: docs/.project-docs-manifest.yaml
  fallback_action: ask-user
roles:
  pm:
    entry: docs/navigation/项目导航.md
  cross_area:
    entry: docs/navigation/项目导航.md
work_units: []
active_core_files:
  - docs/shared/current/当前阶段目标与范围.md
  - docs/shared/current/当前任务优先级清单.md
  - docs/shared/current/当前阻塞与待修复问题清单.md
  - docs/shared/current/当前验收标准清单.md
  - docs/shared/current/当前实现边界对照.md
  - docs/shared/current/当前锁定范围与禁止主动重构清单.md
```

When a work unit is created, add an entry like:
```yaml
work_units:
  - key: order-service
    label: 订单服务
    owner: backend-team
    entry: docs/units/order-service/manifest.md
```

### Active-file header

For newly created active-layer markdown files, prefer this minimal header block:

```yaml
---
status: active
authority: current
owner: pm
last_verified: 2026-05-07
---
```

Use the owner value that matches the file's responsibility area (`pm`, a work-unit owner, or `cross-area`).
Do not retrofit this header by overwriting existing non-empty user files during patch mode.

### docs/navigation/项目导航.md
Must include:
- 当前目标看哪里
- 当前范围看哪里
- 当前优先级看哪里
- 当前验收看哪里
- 当前风险/锁定范围看哪里
- 责任归属应去哪里查询

### docs/shared/README.md
Must include:
- 共享区用途说明
- 当前层（current/）的默认读取优先级
- 参考层（contracts/、decisions/、milestones/）的按需读取原则
- 归档层（archive/）的显式按需读取原则

### docs/shared/current/当前阶段目标与范围.md
Must include:
- 当前阶段目标
- 当前范围
- 明确不在范围内（**粒度原则**：每一项必须包含具体名称——字段名、接口路径、文件名、包名，禁止使用"排序/筛选功能"等分类概括）
- 成功定义

### docs/shared/current/当前任务优先级清单.md
Must include:
- P0 / P1 / P2 或同等优先级划分
- 当前进行中的核心事项
- 暂缓事项

### docs/shared/current/当前阻塞与待修复问题清单.md
Must include:
- 问题标题
- 所属工作单元
- 问题类型（bug / 联调 / 环境 / 待确认）
- 复现步骤
- 请求参数/响应摘要（如适用）
- 期望结果
- 实际结果
- 当前责任归属
- 当前状态
- 最后确认时间

### docs/shared/current/当前验收标准清单.md
Must include:
- 当前功能验收标准
- 当前接口验收标准
- 不允许破坏的既有能力

### docs/shared/current/当前实现边界对照.md
Must include:
- 当前已实现边界
- 当前未实现边界
- 当前需要维持兼容的区域

### docs/shared/current/当前锁定范围与禁止主动重构清单.md
Must include:
- 已完成且锁定的工作单元/模块/接口（**粒度原则**：每项必须包含具体接口路径、类名、文件名或字段名）
- 禁止主动改动的原因
- 允许修改的边界
- 被明确否决的扩展请求及否决依据（如：priority 字段 — 不在 MVP 范围，详见 当前阶段目标与范围.md）

## Work unit minimum structure

Each work unit under `docs/units/<unit-name>/` should have:

```text
docs/units/<unit-name>/
├── README.md
├── manifest.md
├── status.md
├── requirements/
│   ├── index.md
│   └── _item.template.md
├── blockers/
│   ├── index.md
│   └── _item.template.md
├── issues/
│   ├── index.md
│   ├── _item.template.md
│   └── _reopened.template.md
├── sync/
│   └── outward-needs.md
└── archive/
    ├── index.md
    └── _archived-item.template.md
```

### docs/units/<unit>/README.md
给人看的单元简介。说明这个单元大致负责什么。

Suggested minimal shape:
```md
# <unit-label>

<一句话说明本工作单元负责的范围>。

## 负责范围
- <负责项 1>
- <负责项 2>

## 不负责范围
- <不负责项 1>
```

### docs/units/<unit>/manifest.md
给 Claude 的单元路由文件。

Suggested minimal shape:
```md
---
unit: <unit-key>
label: <unit-label>
owner: <owner>
---

# <unit-label> — 路由入口

## 负责范围
- <负责项>

## 不负责范围
- <不负责项>

## 路由线索
- 当任务涉及 <关键词 A>、<关键词 B> 时，属于本单元
- 当任务涉及 <排除关键词> 时，不属于本单元

## 默认读取顺序
1. 本文件（manifest.md）
2. status.md
3. 仅在需要时读 requirements/index.md
4. 仅在需要时读 blockers/index.md
5. 仅在需要时读 issues/index.md
6. 仅跨单元协作时读 sync/outward-needs.md
```

### docs/units/<unit>/status.md
当前状态总览。

Suggested minimal shape:
```md
---
status: active
authority: current
owner: <unit-owner>
last_verified: <date>
---

# <unit-label> — 当前状态

## 当前目标
- <当前阶段目标>

## 当前待完成
- [ ] <待完成项 1>
- [ ] <待完成项 2>

## 当前阻塞
- <阻塞项>（详见 blockers/index.md）

## 当前待修复/待处理问题
- <问题>（详见 issues/index.md）

## 最近完成
- [x] <已完成项>

## 下一步
- <下一步动作>
```

### docs/units/<unit>/requirements/index.md
当前需求摘要清单。

Suggested minimal shape:
```md
# <unit-label> — 需求清单

## 进行中
- [ ] REQ-001: <需求标题> — 负责人: <> — 截止: <>

## 待开始
- [ ] REQ-002: <需求标题>

## 已完成
- [x] REQ-000: <需求标题> — 完成日期: <>
```

### docs/units/<unit>/blockers/index.md
当前阻塞摘要清单。

Suggested minimal shape:
```md
# <unit-label> — 阻塞清单

## 当前阻塞
- [ ] BLK-001: <阻塞标题> — 类型: <联调/环境/待确认/依赖> — 影响: <>

## 已解除
- [x] BLK-000: <阻塞标题> — 解除日期: <>
```

### docs/units/<unit>/issues/index.md
当前问题摘要清单。

Suggested minimal shape:
```md
# <unit-label> — 问题清单

## 待修复
- [ ] ISS-001: <问题标题> — 严重程度: <高/中/低> — 发现日期: <>

## 已修复
- [x] ISS-000: <问题标题> — 修复日期: <>
```

### docs/units/<unit>/sync/outward-needs.md
当前单元对外提出的协同请求、依赖或同步事项。

Suggested minimal shape:
```md
# <unit-label> — 对外协同需求

## 当前对外依赖
- <依赖项 1>：需要 <目标单元> 提供 <具体事项>

## 当前对外通知
- <通知项 1>：已变更 <接口/行为>，影响 <目标单元>
```

### docs/units/<unit>/archive/index.md
当前单元归档索引。

Suggested minimal shape:
```md
# <unit-label> — 归档索引

## 已归档需求
- ARC-001: <需求标题> — 归档日期: <> — 原因: <已完成/已取消>

## 已归档问题
- ARC-002: <问题标题> — 归档日期: <> — 原因: <已修复/不再复现>
```

## Item templates

### docs/units/<unit>/requirements/_item.template.md
```md
---
id: REQ-<nnn>
title: <需求标题>
status: <pending | in-progress | completed>
owner: <负责人>
created_at: <date>
updated_at: <date>
---

# <title>

## 摘要
<一句话描述>

## 详情
<详细描述>

## 验收标准
- [ ] <验收条件 1>
- [ ] <验收条件 2>

## 关联
- 相关单元: <>
- 相关阻塞: <>
```

### docs/units/<unit>/blockers/_item.template.md
```md
---
id: BLK-<nnn>
title: <阻塞标题>
status: <active | resolved>
owner: <负责人>
created_at: <date>
updated_at: <date>
---

# <title>

## 阻塞类型
<联调 | 环境 | 待确认 | 外部依赖>

## 影响范围
<受影响的工作单元或功能>

## 当前状态
<当前排查/等待的进展>

## 下一步
<下一步动作>

## 关联
- 相关问题: <>
```

### docs/units/<unit>/issues/_item.template.md
```md
---
id: ISS-<nnn>
title: <问题标题>
severity: <high | medium | low>
status: <open | in-progress | resolved>
owner: <负责人>
created_at: <date>
updated_at: <date>
---

# <title>

## 复现步骤
1. <步骤 1>
2. <步骤 2>

## 期望结果
<期望的正确行为>

## 实际结果
<当前的错误行为>

## 影响范围
<受影响的功能或单元>

## 根因
<如已定位>

## 修复方案
<如已有方案>
```

### docs/units/<unit>/issues/_reopened.template.md
```md
---
id: ISS-<nnn>-R<count>
title: <问题标题>（重新激活）
status: reopened
owner: <负责人>
created_at: <date>
reopened_at: <date>
original_id: ISS-<nnn>
original_archive: docs/units/<unit>/archive/<archived-file>.md
---

# <title>

## 重新激活原因
<为什么需要重新处理这个已归档问题>

## 与原问题的差异
<当前情况与原归档时的差异>

## 引用原归档
详见: <original_archive>
```

### docs/units/<unit>/archive/_archived-item.template.md
```md
---
id: ARC-<nnn>
title: <归档标题>
type: <requirement | issue | blocker>
status: archived
owner: <原负责人>
created_at: <date>
archived_at: <date>
archived_reason: <已完成 | 已取消 | 不再复现 | 已修复>
---

# <title>

## 关键结论
<最终结果或结论>

## 必要引用
- 原活动条目: <>
- 相关决策: <>
```

## docs/units/.template/

The `.template/` directory holds the canonical copies of the item templates above.
When creating a new work unit, copy from `.template/` into the new unit's directories.

## docs/process/000-项目初始化.md
Must include:
- 初始化时间
- 初始化原因
- 创建了哪些目录和文件
- 当前哪些内容仍待人工补充
- 项目经理输入了哪些工作单元

## Minimal-content rule

For bootstrap and patch, prefer short files with section headings and placeholders over long prose.
The goal is to establish current-truth anchors, not to generate a complete handbook.

## Patch rule

If a project already has rich historical docs but lacks the active layer:
- create only the missing active-layer files
- do not migrate or rewrite historical docs immediately
- leave historical detail where it is until a dedicated cleanup task happens

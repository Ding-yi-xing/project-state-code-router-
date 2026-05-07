# Bootstrap Templates Guidance

author=DingYiXing

**Scope:** Minimum collaboration docs to create during bootstrap or patch.
**Core:** create only the smallest structure that supports current truth, responsibility lookup, and work-unit routing.
**Extended:** suggested headings and minimal contents.
**Often used with:** project-state.md.

## Create only these directories by default

These collaboration docs belong at the project root directory and should sit alongside the project's top-level code or app directories.

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
│   │   └── .template/
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

### docs/.project-docs-manifest.yaml
Must include:
- schema_version
- structure_version
- initialized_by
- initialized_at
- responsibility_lookup
- roles
- work_units
- active_core_files

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
- 明确不在范围内
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
- 已完成且锁定的工作单元/模块/接口
- 禁止主动改动的原因
- 允许修改的边界

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

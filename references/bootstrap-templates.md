# Bootstrap Templates Guidance

anthor=DingYiXing

**Scope:** Minimum collaboration docs to create during bootstrap or patch.
**Core:** create only the smallest structure that supports current truth, responsibility lookup, and responsibility-area routing.
**Extended:** suggested headings and minimal contents.
**Often used with:** project-state.md.

## Create only these directories by default

These collaboration docs belong at the project root directory and should sit alongside the project's top-level code or app directories when multiple code areas exist.
Here, “project root directory” means the root of the current project scope, not a literal folder named `project-root`.

```text
<project-root-directory>/
├── CLAUDE.md
├── docs/
│   ├── .project-docs-manifest.yaml
│   ├── 00-导航/
│   ├── 10-共享状态/
│   ├── 20-交付面/
│   ├── 30-服务域/
│   ├── 40-项目治理/
│   ├── 90-过程记录/
│   └── 99-归档/
├── <top-level-code-dir-a>/
└── <top-level-code-dir-b>/
```

## Bootstrap input

Before creating responsibility-specific entries, ask the project manager or current user for:
- delivery surfaces to create under `docs/20-交付面/` (for example: web, ios, android, miniapp, admin)
- service domains to create under `docs/30-服务域/` when the project needs server-side or shared service routing (for example: api, jobs, data)
- owner or team for each responsibility area
- optional human-readable labels when directory key and display name differ

Only create responsibility areas that are currently confirmed as needed.
Do not prefill future delivery surfaces or service domains in the manifest just because they might exist later.

Do not hardcode `frontend` or `backend` as the only responsibility areas.
If the project currently needs only delivery surfaces or only service domains, create only the relevant side.

## Create only these files by default

### CLAUDE.md
Must include:
- Claude 进入项目后必须先读哪些文件
- 责任归属默认去哪里查询（例如 `docs/.project-docs-manifest.yaml`）
- 当前开发者负责范围不明确时应先询问项目经理或当前用户
- 默认不要自行猜测当前开发者负责的交付面、服务域或模块

Suggested minimal shape:

```md
# Project collaboration entry

Before doing implementation work in this project:
1. Read this file first.
2. Then read `docs/.project-docs-manifest.yaml`.
3. Then read only the entry files and active docs for the relevant responsibility area.
4. Read reference or archive docs only when the current task truly needs them.

## Responsibility lookup
- Source of truth: `docs/.project-docs-manifest.yaml`
- If the current developer's responsibility area is unclear, ask the user or project manager

## Active docs
- Shared facts: `docs/10-共享状态/`
- Responsibility-specific entry files: see manifest entries
```

### docs/.project-docs-manifest.yaml
Must include:
- schema_version
- structure_version
- initialized_by
- initialized_at
- responsibility_lookup
- roles
- delivery_surfaces
- service_domains
- active_core_files

Suggested minimal shape:

```yaml
schema_version: 1
structure_version: 1
initialized_by: code-constraints
initialized_at: 2026-05-06
responsibility_lookup:
  primary_source: docs/.project-docs-manifest.yaml
  fallback_action: ask-user
roles:
  pm:
    entry: docs/00-导航/项目经理导航文档.md
  cross_area:
    entry: docs/00-导航/项目经理导航文档.md
delivery_surfaces: []
service_domains: []
active_core_files:
  - docs/10-共享状态/当前阶段目标与范围.md
  - docs/10-共享状态/当前任务优先级清单.md
  - docs/10-共享状态/当前阻塞与待修复问题清单.md
  - docs/10-共享状态/当前验收标准清单.md
  - docs/10-共享状态/当前实现边界对照.md
  - docs/10-共享状态/当前锁定范围与禁止主动重构清单.md
```

## Active-file header

For newly created active-layer markdown files, prefer this minimal header block:

```yaml
---
status: active
authority: current
owner: pm
last_verified: 2026-05-06
---
```

Use the owner value that matches the file's responsibility area (`pm`, a delivery-surface owner, a service-domain owner, or `cross-area`).
Do not retrofit this header by overwriting existing non-empty user files during patch mode.
The blocker list may stay as a short placeholder when the project currently has no open blockers.
Responsibility-area task lists are execution views derived from the project-level priority list, not separate master backlogs.

### docs/00-导航/项目经理导航文档.md
Must include:
- 当前目标看哪里
- 当前范围看哪里
- 当前优先级看哪里
- 当前验收看哪里
- 当前风险/锁定范围看哪里
- 责任归属应去哪里查询

### docs/10-共享状态/当前阶段目标与范围.md
Must include:
- 当前阶段目标
- 当前范围
- 明确不在范围内
- 成功定义

### docs/10-共享状态/当前任务优先级清单.md
Must include:
- P0 / P1 / P2 或同等优先级划分
- 当前进行中的核心事项
- 暂缓事项

### docs/10-共享状态/当前阻塞与待修复问题清单.md
Must include:
- 问题标题
- 所属页面/模块/API
- 问题类型（bug / 联调 / 环境 / 待确认）
- 复现步骤
- 请求参数/响应摘要（如适用）
- 期望结果
- 实际结果
- 当前责任归属
- 当前状态
- 最后确认时间

### docs/10-共享状态/当前验收标准清单.md
Must include:
- 当前功能验收标准
- 当前页面/接口验收标准
- 不允许破坏的既有能力

### docs/10-共享状态/当前实现边界对照.md
Must include:
- 当前已实现边界
- 当前未实现边界
- 当前需要维持兼容的区域

### docs/10-共享状态/当前锁定范围与禁止主动重构清单.md
Must include:
- 已完成且锁定的页面/模块/接口
- 禁止主动改动的原因
- 允许修改的边界

### docs/20-交付面/<surface>/接手入口.md
Must include:
- 当前交付面默认先读哪些 active 文件
- 当前交付面实现关注点
- 当前交付面禁止主动重构范围
- 当前责任归属

### docs/20-交付面/<surface>/任务推进清单.md
Must include:
- 来源任务（映射项目级优先级项）
- 当前子任务
- 当前状态
- 当前阻塞
- 下一步
- 对应验收点

### docs/20-交付面/<surface>/交付面检查清单.md
Must include:
- 是否符合当前边界
- 是否破坏锁定交互/页面/能力
- 是否补充必要验收点

### docs/30-服务域/<domain>/接手入口.md
Must include:
- 当前服务域默认先读哪些 active 文件
- 当前服务域实现关注点
- 当前服务域禁止主动重构范围
- 当前责任归属

### docs/30-服务域/<domain>/任务推进清单.md
Must include:
- 来源任务（映射项目级优先级项）
- 当前子任务
- 当前状态
- 当前阻塞
- 下一步
- 对应验收点

### docs/30-服务域/<domain>/服务域检查清单.md
Must include:
- 是否符合当前边界
- 是否破坏锁定接口/模块/数据约束
- 是否补充必要验收点

### docs/40-项目治理/项目协作与开发原则.md
Must include:
- active/reference/archive 三层定义
- 默认最小阅读原则
- patch 而非重建原则
- 责任归属查询原则

### docs/40-项目治理/AI防脏读与防回滚规则.md
Must include:
- 活跃层优先级
- 归档默认不读
- 锁定项禁止主动重构
- 文档冲突时如何裁决

### docs/90-过程记录/000-项目初始化.md
Must include:
- 初始化时间
- 初始化原因
- 创建了哪些目录和文件
- 当前哪些内容仍待人工补充
- 项目经理输入了哪些交付面和服务域

## Minimal-content rule

For bootstrap and patch, prefer short files with section headings and placeholders over long prose.
The goal is to establish current-truth anchors, not to generate a complete handbook.

## Patch rule

If a project already has rich historical docs but lacks the active layer:
- create only the missing active-layer files
- do not migrate or rewrite historical docs immediately
- leave historical detail where it is until a dedicated cleanup task happens

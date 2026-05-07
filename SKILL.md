---
name: project-state-code-router
description: >
  This skill should be used when the user asks to write, modify, refactor, review,
  debug, or continue code and project work. It fuses two layers: a project-state /
  collaboration router plus actionable coding constraints distilled from Code
  Complete 2. Trigger on: initializing or patching project collaboration docs,
  routing work through project-defined units, avoiding dirty reads in multi-person
  documentation workflows, writing functions, designing classes, naming variables,
  handling errors, writing comments/documentation, testing, debugging, refactoring,
  optimizing performance, setting up projects, and code review. Use when the user
  mentions docs setup, project collaboration, current status, requirements,
  blockers, archive, implementation, refactor, fix bug, add function, create class,
  write test, add comment, review code, or any code-related request that benefits
  from minimal current context plus coding-governance guidance.
compatibility:
  tools:
    - Read
    - Write
    - Edit
    - Glob
    - Grep
---

# Project State Router and Code Constraints

这是一个把**项目状态路由**与**代码规范约束**融合在一起的 skill。

它有两个互相配合的层：
- **项目状态层**：负责判断当前任务属于哪个工作单元、应该读取哪些最小当前事实、是否需要初始化或补齐协作文档结构，以及如何避免多人协作下的脏读与误改。
- **代码约束层**：在项目状态和上下文范围清晰后，继续为实现、重构、调试、测试、命名、错误处理、性能优化、代码评审等任务提供可执行的约束与路由入口。

使用顺序始终是：
1. 先用项目状态层缩小当前可信上下文
2. 再进入代码约束层执行具体编码规范

它的目标不是生成一大套漂亮文档，也不是脱离项目状态孤立地谈代码规范，而是让 Claude 在多人协作、文档可能局部过时、且不同项目责任边界不同的情况下，仍然能：
- 找到当前最小且可信的事实集
- 只改当前应该改的那部分文档或代码上下文
- 避免把旧设计、旧计划、旧归档当成当前执行依据
- 在缺结构时只补最小骨架，不重建整棵 docs 树
- 在项目状态清晰后，把代码工作继续路由到合适的约束与规范入口

## 项目状态层适用对象

把项目文档按“工作单元”组织，而不是预设成固定的 frontend / backend / mobile。
工作单元由项目经理或团队按项目实际情况创建，例如：
- `order-service`
- `admin-web`
- `miniapp`
- `billing`
- `auth`
- `ops-panel`

Claude 只负责：
- 识别当前任务属于哪个工作单元
- 读取该单元及最少量共享事实
- 在需要时补齐单元骨架
- 按安全规则更新文档

不要预设项目一定有哪几个单元。

## 核心概念

### 1. 工作单元
工作单元是最小责任边界。
每个工作单元拥有自己的：
- 当前状态
- 需求清单
- 阻塞清单
- 问题清单
- 对外协同需求
- 归档

默认认为：
- A 改自己的单元文档，不应影响 B 的单元
- B 改自己的单元文档，不应反向要求 A 的文档同步变更
- 跨单元协作通过共享层或 `sync/` 完成，不直接改别人的内部文档

### 2. 共享区
共享区只放跨单元的当前事实，不放某个单元自己的过程性细节。

典型共享事实：
- 当前阶段目标与范围
- 当前任务优先级
- 当前验收标准
- 当前实现边界
- 当前锁定范围
- 当前跨单元阻塞

### 3. 当前 / 参考 / 归档
把文档分成三层：

#### 当前（current）
当前执行事实。
默认只读这一层。

#### 参考（reference）
长期设计资料，例如接口设计、架构设计、数据设计。
只在当前任务真的需要时读取。

#### 归档（archive）
历史记录、已完成事项、旧计划、旧过程。
默认不读。
只有在回溯、迁移、重新激活历史事项、解释当前约束来源时才读。

当前层永远优先于参考层和归档层。

### 4. 可见 / 半可见 / 不可见冲突
多人协作下，不要把“没有 git 冲突”理解成“没有协作风险”。

- **可见冲突**：远端已发生变化，当前操作者可以看到
- **半可见冲突**：当前操作者本地工作区已有未提交修改
- **不可见冲突**：其他协作者本地有未推送修改，当前操作者看不到

因此默认编辑策略必须保守：
- 不整篇重写
- 不大范围重排
- 不把多个事项混改到一起
- 优先做区块级、字段级、追加式更新

## 绝对安全规则

### 永远不要覆盖已有非空文件
如果文件存在且非空：
- 不重写
- 不替换
- 不用模板覆盖
- 不因为模板升级而强制迁移

只允许：
- 创建缺失文件
- 在明确需要时补一个 companion file
- 在明确用户要求后，对已有内容做最小修改

### 永远不要在初始化时捏造业务事实
初始化和补齐结构时：
- 可以创建标题
- 可以创建固定章节
- 可以创建空清单
- 可以创建模板字段

不可以：
- 猜需求
- 猜负责人
- 猜优先级
- 猜完成状态
- 猜验收标准

### 永远不要把归档当当前执行面
归档默认只读。
不要：
- 直接在归档里继续编辑未完成工作
- 把归档里的旧结论自动当成今天仍然成立
- 因为归档里写过某种方案就回滚当前实现

### 永远不要默认跨单元写入
默认写入范围只限当前单元。
涉及跨单元信息时：
- 优先写共享层
- 或写当前单元的 `sync/outward-needs.md`
- 不直接改其他单元的内部状态、需求、阻塞、问题文档

## 运行模式

每次使用这个 skill，都先判断项目处于以下哪一种模式。

### bootstrap
项目基本还没有协作文档结构。

进入条件：
- 根目录没有 `docs/`
- 没有 `.project-docs-manifest.yaml`
- 没有可识别的活动层文档
- 用户明确要求初始化项目文档

行为：
- 创建最小骨架
- 创建共享层核心文件
- 创建 `docs/units/.template/`
- 不预创建具体业务单元
- 不预创建具体需求/问题/阻塞条目

### patch
项目有部分文档，但缺少必要骨架或入口文件。

进入条件：
- `docs/` 已存在，但 manifest 缺失
- 共享层不完整
- 某个工作单元缺少必要文件
- 项目只有历史长文档，没有紧凑活动层

行为：
- 只补缺失目录和文件
- 不覆盖已有非空文件
- 优先补活动层，再补更深层结构

### normal
项目已经具备完整活动层和路由结构。

进入条件：
- `docs/.project-docs-manifest.yaml` 存在
- 活动层文件存在
- 当前任务对应的工作单元入口存在

行为：
- 不新建结构
- 只读最小必要文档
- 只在当前单元范围内做最小更新

## 目标目录结构

默认目录结构如下：

```text
<project-root>/
├─ CLAUDE.md
├─ docs/
│  ├─ .project-docs-manifest.yaml
│  ├─ navigation/
│  │  └─ 项目导航.md
│  ├─ shared/
│  │  ├─ README.md
│  │  ├─ current/
│  │  │  ├─ 当前阶段目标与范围.md
│  │  │  ├─ 当前任务优先级清单.md
│  │  │  ├─ 当前验收标准清单.md
│  │  │  ├─ 当前实现边界对照.md
│  │  │  └─ 当前锁定范围与禁止主动重构清单.md
│  │  ├─ contracts/
│  │  ├─ decisions/
│  │  ├─ milestones/
│  │  └─ archive/
│  ├─ units/
│  │  ├─ .template/
│  │  └─ <unit-name>/
│  └─ process/
│     └─ 000-项目初始化.md
```

其中：
- `navigation/` 是人和 Claude 的导航入口
- `shared/current/` 是默认可读的共享当前事实
- `units/` 是项目自定义工作单元目录
- `process/` 只记录过程，不是默认读取入口

## 工作单元最小结构

每个具体工作单元至少应具备：

```text
docs/units/<unit-name>/
├─ README.md
├─ manifest.md
├─ status.md
├─ requirements/
│  └─ index.md
├─ blockers/
│  └─ index.md
├─ issues/
│  └─ index.md
├─ sync/
│  └─ outward-needs.md
└─ archive/
   └─ index.md
```

### 文件职责

#### `README.md`
给人看的单元简介。
说明这个单元大致负责什么。

#### `manifest.md`
给 Claude 的单元路由文件。
至少包含：
- 单元名称
- 负责范围
- 不负责范围
- 路由线索
- 默认读取顺序

#### `status.md`
当前状态总览。
应只保留当前最重要事实，例如：
- 当前目标
- 当前待完成
- 当前阻塞
- 当前待修复 / 待处理问题
- 最近完成
- 下一步

#### `requirements/index.md`
当前需求摘要清单。

#### `blockers/index.md`
当前阻塞摘要清单。

#### `issues/index.md`
当前问题摘要清单。

#### `sync/outward-needs.md`
当前单元对外提出的协同请求、依赖或同步事项。
这是默认跨单元写入出口。

#### `archive/index.md`
当前单元归档索引。
只记录归档事项，不作为默认执行入口。

## 状态与清单规则

可以使用 Markdown checklist 跟踪状态：
- `[ ]` 未完成
- `[x]` 已完成

但 checklist 只能作为**摘要层**，不能作为唯一事实来源。

正确做法：
- `status.md` 和各类 `index.md` 只放摘要
- 复杂事项应落到独立条目文件
- 索引里只保留标题、编号、状态、简短说明

不要把所有上下文都塞进一个长清单里。

## 独立条目规则

对于复杂需求、问题、阻塞，使用“索引 + 条目文件”模式。

建议保留模板文件：
- `requirements/_item.template.md`
- `blockers/_item.template.md`
- `issues/_item.template.md`
- `issues/_reopened.template.md`
- `archive/_archived-item.template.md`

条目文件可以包含：
- id
- title
- status
- owner
- created_at / updated_at
- summary
- details
- acceptance / impact / next action
- links

skill 在初始化时可以创建模板，但不要自动创建业务条目。

## 归档与重新激活规则

### 归档
完全完成的需求或问题，可以从活动层移入归档。

归档应该是独立管理的，只保留：
- 已完成快照
- 归档原因
- 关键结论
- 必要引用

### 重新激活
如果之后又要继续处理一个已归档事项：
- 不直接修改原归档文件
- 新建一个活动条目
- 在新条目里引用原归档来源
- 把状态标记为 `reopened`

也就是说：
- 归档是快照
- 重新激活是新生命周期

不要把“归档恢复”实现成“回去继续改原归档文件”。

## 初始化与补齐规则

### bootstrap 时创建什么
只创建最小骨架：
- `CLAUDE.md`（如果用户希望该项目有根级协作入口）
- `docs/.project-docs-manifest.yaml`
- `docs/navigation/项目导航.md`
- `docs/shared/README.md`
- `docs/shared/current/` 下核心当前事实文件
- `docs/units/.template/` 及其模板骨架
- `docs/process/000-项目初始化.md`

不要在 bootstrap 时：
- 创建具体业务单元
- 创建具体需求条目
- 创建具体问题条目
- 猜测项目结构细节

### patch 时怎么补
如果发现某个工作单元已经存在，例如 `docs/units/admin-web/`：
- 只补它缺失的最小文件
- 不覆盖已有人写过内容的文件
- 不因为模板更新就重写该单元已有文档

## 默认读取顺序

每次执行时，按以下顺序做最小读取。

### 第 1 步：先读根入口
如果存在根级 `CLAUDE.md`，先读它。

### 第 2 步：读项目 manifest
读 `docs/.project-docs-manifest.yaml`，确认：
- docs 根目录
- 导航入口
- shared/current 入口
- unit 根目录
- 单元发现方式
- 编辑边界规则

### 第 3 步：定位当前工作单元
优先依据：
- 用户明确提到的单元名
- 任务涉及的功能/模块/页面/服务
- 单元 `manifest.md` 的路由线索

### 第 4 步：只读当前单元最小集
默认只读：
1. `manifest.md`
2. `status.md`
3. 只有在需要时才读 `requirements/index.md`
4. 只有在需要时才读 `blockers/index.md`
5. 只有在需要时才读 `issues/index.md`
6. 只有跨单元协作时才读 `sync/outward-needs.md`

### 第 5 步：只在必要时读共享层
只有以下情况才读 `shared/current/`：
- 涉及跨单元边界
- 涉及共享验收标准
- 涉及共享实现边界
- 涉及共享优先级
- 涉及共享阻塞

### 第 6 步：归档是显式按需读取
只有以下情况才读 archive：
- 用户明确要求看历史
- 当前任务是回溯、迁移、复盘、恢复历史事项
- 活动层明确引用了归档来源

不要默认扫完整个 docs 树。
不要默认读 process。
不要默认读 archive。

## 默认编辑策略

### 当前单元优先
默认只编辑当前工作单元内的文档。

### 共享层谨慎编辑
只有在任务明确涉及共享事实时，才更新 `shared/current/`。

### 跨单元默认只读
需要别的单元配合时：
- 优先写入当前单元的 `sync/outward-needs.md`
- 或更新共享层里的跨单元阻塞 / 协同信息
- 不直接改对方单元的内部管理文档

### 最小修改原则
在已有文件里，优先：
- 区块级修改
- 字段级修改
- 追加式记录

避免：
- 全文改写
- 全文重排
- 顺手统一格式导致大 diff
- 把多个事项揉成一次大更新

## manifest 期望表达的内容

`docs/.project-docs-manifest.yaml` 至少应能回答这些问题：
- docs 根在哪里
- 导航文件在哪里
- shared/current 的默认入口有哪些
- units 根在哪里
- 如何发现单位目录
- 一个单元最少要有什么文件
- 默认读取顺序是什么
- 默认编辑边界是什么
- archive 是否只读
- 是否要求“重新激活而不是直接改归档”

skill 在需要创建或修补 manifest 时，应优先写这些结构性事实，不要写业务猜测。

## 输出要求

当 skill 被要求初始化或补齐结构时，输出应包含：
1. 当前判断的模式：`bootstrap` / `patch` / `normal`
2. 当前识别到的工作单元范围
3. 实际创建或补齐了哪些文件
4. 哪些文件因已存在且非空而被保留未覆盖
5. 哪些业务事实需要用户后续补充

当 skill 被要求更新现有文档时，输出应包含：
1. 读取了哪些最小入口文件
2. 为什么本次只改这些文件
3. 是否涉及共享层或跨单元信息
4. 是否明确避开了归档或其他单元内部文档

## 不要做的事

- 不要预设固定的 frontend / backend / mobile 目录
- 不要默认创建所有可能的工作单元
- 不要在初始化时生成大量长文档
- 不要把 process 日志当成当前事实主入口
- 不要把归档直接拿来继续编辑
- 不要因为看到旧设计就回滚当前实现
- 不要为了“整洁”而重写已有非空文档
- 不要在不确定责任边界时扫描整个 docs 树
- 不要把 checklist 当成唯一事实来源
- 不要直接修改其他工作单元的内部管理文档


## 代码约束层

Coding rules distilled from Code Complete 2. Load reference files from `references/` as needed.

这一层保留原 `code-constraints` 的主体行为：
- 代码任务本身应稳定触发本 skill
- 先按项目状态层收缩上下文，再按下面的规则路由到具体参考文件
- 如果任务只是纯代码任务而没有额外协作文档需求，仍然直接进入这层执行

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

## Reading Protocol

1. **First, scan `[核心]` rules** in the target file(s) — these cover ~10-30% of rules, are the minimal safe working surface, and always apply.
2. **Then, read `[扩展]` rules** only when:
   - The task is complex (multi-file, multi-class, or architectural)
   - You're writing public API surfaces
   - The code handles money, security, or safety-critical operations
3. **Skip `[语言特定]` rules** unless the language matches the current file.
4. **Skip `[历史]` rules** — they describe obsolete patterns (goto, global data patterns from pre-OOP era). Only apply if the project explicitly uses those patterns.
5. **Templates** in `references/templates.md` — only load when creating new files or new public functions. Skip for small edits and bug fixes.

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
| code review / quality check / inspection | references/process.md |
| code review / PR review / merge readiness check | references/process.md, references/git-workflow.md, references/project-state.md |

`references/warning-signs.md` applies to all coding activities — load it when uncertain.

## Usage

Before writing code, first determine whether project-state routing is needed to identify the smallest current fact set. Then find your action in the Routing table, read the listed reference files, apply all `[必须]` rules, and avoid all `[禁止]` rules. When in doubt about which rules apply, default to correctness and readability.

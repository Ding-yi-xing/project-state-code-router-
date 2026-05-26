# Project-state and Collaboration Rules

author=DingYiXing

**Scope:** Project-state routing, active/reference/archive layering, bootstrap/patch behavior, collaboration docs, and dirty-read prevention.
**Core:** minimal current truth, conflict resolution, non-destructive initialization — always apply.
**Extended:** archive retrieval, responsibility-area loading, template guidance.
**Often used with:** git-workflow.md, warning-signs.md.
**Read Next If:** bootstrapping docs → bootstrap-templates.md; writing code after routing → naming.md / design.md / defense.md and other task-specific references.

## Project-state governance

- [核心][必须] 将项目文档分为 active、reference、archive 三层，只允许 active 层作为当前任务的默认事实源。
- [核心][必须] 将当前真相收敛到最小活跃集，避免同一事实在多个文档中重复声明。
- [核心][必须] 如果 active 层与 reference 或 archive 冲突，以 active 层为准。
- [核心][必须] 已归档文档不得单独作为当前实现依据。
- [核心][必须] 已完成且锁定的页面、模块、接口或需求，除非用户明确要求，否则不得主动重构、改版或按旧文档回滚。
- [核心][必须] 当发现代码与文档冲突时，先判断谁过期，再决定更新代码还是更新 active 层文档。
- [核心][必须] 发现 active 层文档过期时，优先修正 active 层事实源，而不是立即用旧文档回拖当前实现。
- [扩展][必须] 在 active 层文档头部使用统一状态字段，如 `status`、`authority`、`owner`、`last_verified`，帮助模型和人类快速判断权威性。
- [扩展][必须] 对已完成的事项，在 active 层保留简短结论，将详细过程、旧方案和历史推进记录下沉到 archive。
- [扩展][禁止] 不要把历史过程记录、旧 handoff、旧设计讨论继续当作当前默认入口。

## Responsibility routing

- [核心][必须] 每次任务先判断当前责任范围：单一工作单元、pm、cross-area，选择最窄的适用范围。
- [核心][必须] 若项目根目录存在 `CLAUDE.md`，应先读取它，再决定读取哪类入口文档和当前责任范围。
- [核心][必须] 当前开发者负责范围应优先从 `docs/.project-docs-manifest.yaml` 的责任归属配置中查询；仍不明确时，先询问用户或项目经理，不要自行猜测。
- [核心][必须] 当 manifest 中 `work_units` 为空（零个工作单元）时，不得自行创建或猜测工作单元——必须在输出中提示："当前项目未定义任何工作单元，请项目经理在 manifest 中添加 work_units，或明确告知本次任务暂不按工作单元路由"。只有在用户明确确认跳过或提供单元信息后才能继续。
- [核心][必须] 当任务不属于任何已有工作单元且用户未声明角色时，应主动询问："本任务涉及的内容目前不属于任何已定义的工作单元，是否需要创建新工作单元？或者本次以 pm / cross-area 角色处理？"
- [核心][必须] 单一工作单元任务默认只读该单元的 manifest.md + status.md + 当前边界 + 当前验收 + 当前锁定范围 + 必需的 API 契约或数据契约。
- [核心][必须] PM 任务默认只读目标范围、优先级、验收标准、锁定范围，以及必要时读风险阻塞。
- [扩展][必须] 仅在任务确实跨边界时进入 cross-area 模式，避免无关文档进入上下文。
- [扩展][禁止] 不要把 cross-area 文档作为单一工作单元日常任务的默认入口。

## Project state machine

- [核心][必须] 每次任务先判断项目处于 normal、bootstrap、patch 三种模式之一。
- [核心][必须] 当项目没有 docs、没有 manifest、没有核心 active 文件时进入 bootstrap 模式。
- [核心][必须] 当项目已有 docs 但缺少 manifest、缺少 active 核心文件或缺少当前责任范围入口时进入 patch 模式。
- [核心][必须] 当 manifest、active 核心文件和当前责任范围入口都存在时进入 normal 模式。
- [扩展][必须] bootstrap 模式只创建最小协作文档结构，不预先生成大量长期设计文档。
- [扩展][必须] patch 模式只补齐缺失项，不重建整个 docs 目录。

## Shared execution views & blockers

- [核心][必须] 项目级 `当前任务优先级清单.md` 是唯一主任务事实源，各工作单元不得各自维护脱离它的独立主清单。
- [核心][必须] `docs/units/<unit>/status.md` 是工作单元的执行视图，用于承接本单元当前要做的子任务、当前阻塞和下一步动作。
- [核心][必须] 联调失败、接口报错、环境差异、验收阻塞和待确认归属的问题，统一记录到 `当前阻塞与待修复问题清单.md`，而不是散落在聊天记录或过程记录中。
- [核心][必须] 过程记录只用于保留推进经过和结论，不作为当前待修复事项的默认事实源。
- [扩展][必须] 已解决的问题在 active 层保留简短结论；详细排查过程、旧日志和历史讨论下沉到 archive 或过程记录。
- [扩展][禁止] 不要把多个工作单元的 status.md 和共享阻塞清单混写成一份长过程周报。

## Initialization and patch safety

- [核心][必须] 创建目录仅在目录不存在时进行。
- [核心][必须] 创建文件仅在文件不存在时进行。
- [核心][必须] 对已存在且非空的文件绝不覆盖。
- [核心][必须] 若项目根目录缺少 `CLAUDE.md`，bootstrap 时应创建一个最小入口文件，用于声明读取顺序与责任归属查询位置。
- [核心][必须] `docs/.project-docs-manifest.yaml` 应记录 active_core_files，作为默认事实源白名单。
- [核心][必须] `docs/` 作为项目级共享协作层，应位于项目根目录下，并与项目的顶层代码或应用目录同级；不要把这套共享事实源塞进某一侧源码目录。
- [核心][必须] 不在 active_core_files 中的文档，不应仅因"名字看起来相关"就自动进入默认上下文。
- [核心][必须] 当模板升级时，创建迁移说明或缺失的伴随文件，而不是自动重写用户内容。
- [扩展][必须] 使用 `docs/.project-docs-manifest.yaml` 记录结构版本、核心文件列表和责任归属查询信息，作为后续 patch 的哨兵文件。
- [扩展][必须] bootstrap 或 patch 后，在过程记录中写入一次初始化/补齐记录。
- [扩展][禁止] 不要因为发现少量缺失文件就整体重建整个文档树。

## Manifest error recovery

- [核心][必须] 若 `docs/.project-docs-manifest.yaml` 存在但 YAML 解析失败（格式损坏、非法字符），不得静默跳过——应在输出中明确报告解析错误，并降级为 patch 模式继续执行。
- [核心][必须] manifest 解析失败时，不得覆盖原文件；应提示用户手动修复，或经用户同意后备份原文件（如 `.project-docs-manifest.yaml.bak`）再创建最小有效 manifest。
- [核心][必须] 若 manifest 可解析但缺少 `active_core_files` 字段，应以 `docs/shared/current/` 下实际存在的文件推导默认白名单，并将推导结果写入 manifest 的 `active_core_files`。
- [核心][必须] 若 manifest 可解析但缺少 `work_units` 字段，应扫描 `docs/units/` 下实际存在的子目录（排除 `.template/`）来发现现有工作单元，并将发现结果补入 manifest。
- [核心][必须] 若 manifest 中声明的 `active_core_files` 条目指向不存在的文件，应在输出中列出失效引用并从白名单中移除；不要假装失效文件仍然有效。
- [核心][必须] 若 manifest 中声明的 `work_units` 条目指向不存在的目录或缺少 `manifest.md` 的单元，应将该单元标记为不完整并在输出中提示用户补充。
- [扩展][必须] 若 manifest 的 `schema_version` 高于当前 skill 支持的版本，应提示版本不兼容并降级为 patch 模式、仅补缺失文件，不自动迁移 schema。
- [扩展][必须] 若 manifest 同时缺少 `responsibility_lookup` 和 `roles`，应回退到询问用户当前责任范围，而不是自行分配。

## Minimal reading protocol

- [核心][必须] 默认只加载当前责任范围的最小活跃集，控制上下文体积并降低脏读概率。
- [核心][必须] 除非当前任务真的需要，否则不要读取长过程记录、旧规划、归档需求、旧设计推导过程。
- [核心][必须] 单一工作单元任务在推进当前工作时，可读取该单元的 `status.md`；仅在存在联调或缺陷阻塞时再读取 `当前阻塞与待修复问题清单.md`。
- [核心][必须] pm 任务在推进、风险同步、验收推进时，可读取 `当前阻塞与待修复问题清单.md`，但不应默认带入所有过程记录。
- [扩展][必须] 如果 active 层已足够完成当前任务，就不要继续扩展到 reference 或 archive。
- [扩展][必须] 若当前任务只是实现或修复，不要主动引入与任务无关的模块设计、视觉规范、阶段记录。

## Archive retrieval protocol

- [核心][必须] 只有在明确需要历史追溯时，才允许读取 archive。
- [核心][必须] archive 读取应先从索引或摘要开始，再精确提取最相关的 1-2 份材料。
- [核心][必须] 当前任务若是再次改造、迁移、回溯已完成事项，可读取对应归档，但不得默认扩大到整个归档目录。
- [扩展][必须] 当 active 层引用了历史设计或旧需求结论时，仅按引用提取对应归档。
- [扩展][禁止] 不要默认扫描整个 archive 目录寻找"可能相关"的历史材料。

## Conflict handling examples

- [扩展][必须] 当前实现已完成且样式锁定，而旧设计文档仍显示旧样式时，以当前锁定实现为准；若文档过期，更新 active 层，不重构页面。
- [扩展][必须] 某模块已按新接口落地，而过程记录仍保留旧字段命名时，以 active 层 API 当前事实源为准，过程记录仅作背景。
- [扩展][必须] 若新任务明确是"回看一期为什么这么设计"，再读取归档或过程记录；若任务只是"继续实现某个工作单元"，不要读取这些材料。

## Work-unit file responsibilities

每个工作单元至少应有：`README.md` `manifest.md` `status.md` `requirements/index.md` `blockers/index.md` `issues/index.md` `sync/outward-needs.md` `archive/index.md`。

- [核心][必须] `manifest.md` 是 Claude 的单元路由文件，至少包含：单元名称、负责范围、不负责范围、路由线索、默认读取顺序。
- [核心][必须] `status.md` 只保留当前最重要事实（当前目标、当前待完成、当前阻塞、待修复问题、最近完成、下一步），不堆历史。
- [核心][必须] `sync/outward-needs.md` 是当前单元对外提出协同请求的唯一默认出口；跨单元写入优先走这里或共享层，不直接改对方内部文档。
- [扩展][必须] `requirements/`、`blockers/`、`issues/` 下的 `index.md` 只放摘要清单（标题、编号、状态、简短说明），复杂事项落到独立条目文件。
- [扩展][必须] checklist (`[ ]` / `[x]`) 只能作为摘要层，不能作为唯一事实来源；详情见独立条目文件。
- [扩展][必须] 归档是已完成快照；重新激活历史事项时，新建活动条目并引用原归档来源，状态标记为 `reopened`，不直接修改原归档文件。

## Default editing policy

- [核心][必须] 默认只编辑当前工作单元内的文档；只有任务明确涉及共享事实时，才更新 `shared/current/`。
- [核心][必须] 跨单元协作时，优先写入当前单元的 `sync/outward-needs.md` 或共享层的跨单元阻塞 / 协同信息；不直接改对方单元的内部状态、需求、阻塞、问题文档。
- [核心][必须] 在已有文件里优先做区块级、字段级、追加式更新；避免全文改写、全文重排、顺手统一格式造成大 diff、把多个事项揉成一次大更新。
- [扩展][禁止] 不要为了"整洁"重写已有非空文档。

## Veto-first decision principle

做任何"是否批准 / 是否纳入 / 是否执行"的决策时，必须先读取否决条件，再评估触发条件。

- [核心][必须] 先读锁定范围文档：`当前锁定范围与禁止主动重构清单.md` + `当前阶段目标与范围.md` 中的"明确不在范围内"段落。
- [核心][必须] 将禁止事项列为否决条件 — 任何匹配禁止事项的请求自动否决；否决后不进入评估，不需要再分析利弊、可行性、技术方案。
- [核心][必须] 只有未被否决的请求才进入下一步：评估优先级、资源、影响范围。
- [核心][必须] PM 做范围决策时必须在输出中显式列出：读了哪些否决条件文档、本次请求中有哪些被否决（如有）、否决依据是哪个文档的哪条规则。
- [核心][必须] 如果一个请求看起来"很合理"但触及当前范围的禁止事项，必须先经正常流程更新范围文档，再批准请求；不得跳过范围文档直接批准。

典型禁止事项（应出现在锁定范围文档中）：不在当前阶段范围内的功能扩展；已锁定的接口 / 模型变更；未经 cross-area 评估的共享模型修改；单人决策的跨单元契约变更。

## Prohibition granularity principle

- [核心][必须] 禁止事项必须使用具体名称，禁止使用分类概括 — 模型会对"看起来合理的功能"产生合理化偏见，绕过模糊条款。
- [核心][必须] 每条禁止事项必须至少包含一个具体的字段名、接口路径、文件名或包名；如果某条无法举出具体名称，说明它还不够清晰，需要细化。
- [核心][必须] bootstrap 和 patch 模式下创建的范围模板，应包含具体名称的占位符，不应预填分类概括。

错误写法（分类概括 — 模型会自己找理由 bypass）：
- "禁止新增排序 / 筛选功能"
- "禁止扩展数据模型"
- "不在范围内的功能暂时不做"

正确写法（具体点名 — 模型无法 bypass）：
- "禁止修改 Task 接口已有字段（id, title, status, assignee, createdAt, updatedAt）"
- "禁止新增 Task 接口字段，包括但不限于：priority, dueDate, tags, labels, category, order"
- "禁止新增 GET /tasks 的查询参数（如 ?sort, ?filter, ?page）"
- "禁止引入新的 npm 依赖（如 react-query, zustand, dayjs）"

## Output requirements when initializing or updating docs

- [核心][必须] 初始化或补齐结构时，输出包含：当前判断的模式（bootstrap / patch / normal）、识别到的工作单元范围、实际创建或补齐了哪些文件、哪些文件因已存在且非空被保留未覆盖、哪些业务事实需要用户后续补充。
- [核心][必须] 更新现有文档时，输出包含：读取了哪些最小入口文件、为什么本次只改这些文件、是否涉及共享层或跨单元信息、是否明确避开了归档或其他单元内部文档。

## Things never to do

- [核心][禁止] 不要预设固定的 frontend / backend / mobile 目录。
- [核心][禁止] 不要默认创建所有可能的工作单元。
- [核心][禁止] 不要在初始化时生成大量长文档。
- [核心][禁止] 不要把 process 日志当成当前事实主入口。
- [核心][禁止] 不要把归档直接拿来继续编辑。
- [核心][禁止] 不要因为看到旧设计就回滚当前实现。
- [核心][禁止] 不要为了"整洁"而重写已有非空文档。
- [核心][禁止] 不要在不确定责任边界时扫描整个 docs 树。
- [核心][禁止] 不要把 checklist 当成唯一事实来源。
- [核心][禁止] 不要直接修改其他工作单元的内部管理文档。

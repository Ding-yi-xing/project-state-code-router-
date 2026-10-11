# Project-state and Collaboration Rules

author=DingYiXing

**Scope:** Project-state routing, active/reference/archive layering, bootstrap/patch behavior, collaboration docs, and dirty-read prevention.
**Core:** minimal current truth, conflict resolution, non-destructive initialization — always apply.
**Extended:** archive retrieval, responsibility-area loading, template guidance.
**Often used with:** git-workflow.md, warning-signs.md.
**Read Next If:** bootstrapping docs → bootstrap-templates.md; writing code after routing → naming.md / design.md / defense.md and other task-specific references.

## Project-state modes

- [核心][必须] `bootstrap`：项目没有协作 docs；仅建最小骨架，不推测业务单元或事项。
- [核心][必须] `patch`：已有 docs 但入口/结构不完整；补缺失项，不重写已有非空内容。对历史 schema 先识别兼容映射，报告缺失，不直接替换 manifest。
- [核心][必须] `normal`：路由入口可用；按最小活跃集执行日常任务。
- [核心][必须] `audit`：用户要求审计/治理时使用；全面只读检查，默认不改文件，输出分级发现及证据。
- [核心][必须] `repair`：仅在用户明确要求整改后使用；按已确认范围修复并复跑审计。
- [核心][必须] 不得将历史结构差异自动判成当前违规；区分会影响当前路由/恢复的规则违规、可分批处理的迁移债务、纯信息项。

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

## Current truth verification protocol

- [核心][必须] 任务开始前若发现用户当前指令、代码行为、测试结果、active 文档互相冲突，必须先执行当前事实验证，不得直接按旧文档开工。
- [核心][必须] 当前事实判断优先级：用户本轮明确指令 > 当前代码和测试行为 > active 层文档 > reference 层设计 > archive / process 历史。
- [核心][必须] 若代码已通过测试且代表当前分支实现，而 active 文档仍描述旧行为，优先更新 active 文档；若代码明显未完成或测试失败，优先修代码并记录问题。
- [核心][禁止] 不要用 archive、旧 process、旧 handoff 或旧计划推翻当前 active 层和当前代码；需要恢复历史时必须走 Archive reactivation protocol。
- [扩展][必须] 当 `last_verified` 过旧、缺失或与当前代码不符时，更新对应 active 文档的 `last_verified` 或记录待验证问题。

## Documentation-first planning principle

- [核心][必须] 非平凡编码、架构、跨文件修改、跨单元协作、风险修复或计划推进前，先在对应权威文档中落下轻量计划或 active exec plan，再动代码。
- [核心][必须] 计划至少包含：目标、范围、不做什么、步骤、验证方式、预计 docs 写回目标、中断恢复点。
- [核心][必须] 1-3 步、单文件、无结构性风险的轻量任务可不落盘，但必须在输出中说明为何不需要持久计划。
- [核心][必须] 多步骤计划应写入 `docs/shared/exec-plans/active/`；工作单元内部小计划可写入对应 `requirements/`、`issues/`、`blockers/` 条目，并在 `status.md` 只保留 PLAN/REQ/ISS/BLK 链接。
- [扩展][禁止] 不要把完整计划只留在聊天里；聊天可用于讨论，repo docs 才是中断恢复事实源。

## Responsibility routing

- [核心][必须] 每次任务先判断当前责任范围：单一工作单元、pm、cross-area，选择最窄的适用范围。
- [核心][必须] 若项目根目录存在 `CLAUDE.md`，应先读取它，再决定读取哪类入口文档和当前责任范围。
- [扩展][必须] `CLAUDE.md` 作为稳定路由合同，不重复维护易变的阶段、当前工作单元清单、优先级、阻塞或活动计划进度；这些事实应引用 manifest / current docs 的单一权威位置。
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
- [核心][必须] `docs/units/<unit>/status.md` 是工作单元的执行视图和索引，用于承接本单元当前要做的子任务、当前阻塞和下一步动作，但不得替代 requirements / issues / blockers / sync / archive / process 的权威记录。
- [核心][必须] 联调失败、接口报错、环境差异、验收阻塞和待确认归属的问题，统一记录到 `当前阻塞与待修复问题清单.md` 或对应工作单元 `blockers/`，而不是散落在聊天记录或过程记录中。
- [核心][必须] 过程记录只用于保留推进经过和结论，不作为当前待修复事项的默认事实源。
- [扩展][必须] 已解决的问题在 active 层保留简短结论；详细排查过程、旧日志和历史讨论下沉到 archive 或过程记录。
- [扩展][禁止] 不要把多个工作单元的 status.md 和共享阻塞清单混写成一份长过程周报。

## Write-back routing and state synchronization

- [核心][必须] 每次推进项目工作后，必须判断本次产生了哪些事实变更，并同步到对应权威文档。
- [核心][必须] `status.md` 只是当前工作单元 dashboard / index，不是需求、问题、阻塞、协同、过程、归档的唯一事实源。
- [核心][禁止] 不要把长需求、长问题复现、长阻塞排查、跨单元协同、过程记录或历史结论堆进 `status.md`。
- [核心][必须] 任何具有独立生命周期、负责人、状态、验收标准或历史价值的信息，都必须拆到对应目录的独立条目文件。
- [核心][必须] `status.md` 中出现需求、问题、阻塞、协同、计划、归档事项时，应引用对应 REQ / ISS / BLK / SYNC / PLAN / ARC 编号或文件路径。
- [核心][必须] 更新代码后若发现项目文档过期，优先更新对应权威文档，再让 `status.md` 指向它；不要只在 `status.md` 写一份新事实。

### Documentation write-back matrix

| Fact change | Authoritative destination | `status.md` role |
|---|---|---|
| New requirement or changed requirement | `docs/units/<unit>/requirements/` | Link REQ id only |
| Bug, defect, failed acceptance, implementation mismatch | `docs/units/<unit>/issues/` | Link ISS id only |
| Blocker, failed integration, environment issue, external dependency | `docs/units/<unit>/blockers/` or `docs/shared/current/当前阻塞与待修复问题清单.md` | Link BLK id only |
| Cross-unit request or notification | `docs/units/<unit>/sync/outward-needs.md` | Mention waiting state only |
| Project-level scope, priority, acceptance, lock change | `docs/shared/current/*.md` | Do not duplicate |
| Completed or cancelled item | `docs/units/<unit>/archive/` and `archive/index.md` | Keep short ARC link |
| Investigation narrative, failed attempt, handoff note | `docs/process/` or active exec-plan progress log | Do not paste narrative |
| Active multi-step plan | `docs/shared/exec-plans/active/` | Link PLAN file only |
| Long-term architecture or principle | `docs/ARCHITECTURE.md`, `docs/DESIGN.md`, `docs/GOLDEN_RULES.md` | Do not duplicate |

### Completion docs sync checklist

Before finishing any project work, check and record the result in the response or task record:

1. Did scope, priority, or acceptance criteria change? If yes, update `docs/shared/current/`.
2. Did a new requirement appear or an existing requirement change? If yes, update `requirements/`.
3. Did a bug, defect, failed acceptance, or mismatch appear? If yes, update `issues/`.
4. Did an external dependency or blocker appear? If yes, update `blockers/` or the shared blocker list.
5. Does another work unit need to know or act? If yes, update `sync/outward-needs.md`.
6. Was work completed, cancelled, or superseded? If yes, update `archive/` and `archive/index.md`.
7. Was there a meaningful investigation, decision, failed attempt, or handoff? If yes, update `docs/process/` or the active exec plan.
8. If none apply, explicitly say no docs sync was needed beyond `status.md`, and why.

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

## Resume work protocol

当用户说“继续”“接着上次”“按计划推进”“继续当前任务”或恢复中断工作时：

1. 先读根 `CLAUDE.md`。
2. 读 `docs/.project-docs-manifest.yaml`。
3. 定位当前工作单元或 pm / cross-area 角色。
4. 读该单元 `manifest.md`、`status.md`、`requirements/index.md`、`issues/index.md`、`blockers/index.md`、`sync/outward-needs.md`。
5. 若存在相关 active exec plan，优先读 `docs/shared/exec-plans/active/*.md` 中当前计划。
6. 只在 status、active plan 或条目文件明确引用时读取 process note。
7. archive 默认不读；只有重新激活历史事项或 active 明确引用时才精确读取。
8. 开工前输出当前目标、当前阻塞、下一步动作、不会读取哪些历史材料及原因。

## Plan advancement protocol

- [核心][必须] 当任务是“按计划推进”或存在 active exec plan 时，先找到第一个未完成且未阻塞的步骤，再执行。
- [核心][必须] 执行前检查该步骤是否在当前范围内，是否触发锁定范围、阻塞、验收或跨单元依赖。
- [核心][必须] 完成步骤后更新 active plan checklist、进度日志、相关 requirements/issues/blockers/sync、以及 `status.md` dashboard 链接。
- [核心][必须] 若发现新阻塞，更新 `blockers/` 或 shared blocker list 后停止推进后续步骤，等待解除或用户确认。
- [核心][必须] 若计划全部完成，将 active plan 标记为 completed，记录 completed_at，并移动/归入 `docs/shared/exec-plans/completed/`；相关完成项按 Archive trigger rules 归档。

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

## Work item lifecycle

| Type | Active states | Terminal state | Archive rule |
|---|---|---|---|
| Requirement | pending → in-progress → accepted | cancelled | accepted/cancelled 后归档 |
| Issue | open → in-progress → resolved | wontfix | resolved/wontfix 且验证后归档 |
| Blocker | active → waiting-external → resolved | dropped | resolved/dropped 后归档 |
| Sync need | open → waiting-response → answered | obsolete | answered/obsolete 后保留短结论 |
| Plan | active → completed | cancelled | completed/cancelled 后移到 completed/ |

- [核心][必须] 每个正式 REQ / ISS / BLK / SYNC / PLAN 条目应有 id、status、owner、created_at、updated_at。
- [扩展][必须] 仅当事项需要中断恢复/历史追踪，或涉及跨单元、外部依赖、生产风险、数据迁移、公开契约、多步骤时，才强制拆独立条目；1–3 步、单单元、低风险、无需追踪的事项可留在 index，但需标清状态和下一步。
- [核心][必须] 状态变化必须更新对应 index 和 `status.md` 链接；不要只改其中一个。
- [核心][必须] Plan 只允许 `active`、`completed`、`cancelled`；不得用 `done`、`finished`、`closed` 代替终态。完成时需验证步骤和 docs 写回、填写 `completed_at`，再移入 `completed/`。
- [核心][禁止] 归档条目默认不可直接编辑；重新处理历史事项必须新建 active 条目并引用原归档。

## Archive trigger rules

必须归档：已验收需求、已验证修复的问题、已解除阻塞、被取消/否决/替代的事项、已完成或取消的 active exec plan。历史迁移时先核对验证证据和引用；不确定是否完成的条目保持原状并报告，不根据文件名或 checklist 单独归档。
不得归档：未验收完成项、仍待确认责任归属的问题、仍被其他工作单元引用为当前阻塞的事项、未写清结论的排查过程。
归档后 active 层只保留短结论和 ARC 链接。

## Archive reactivation protocol

1. 先读 archive index。
2. 精确读取相关 1 个归档项；不要扫整个 archive。
3. 创建新的 active item（例如 `REQ-012-R1` 或 `ISS-008-R1`）。
4. 在新 active item 中引用原 archive 路径和重新激活原因。
5. 不修改原 archive。
6. `status.md` 只引用新的 active item。

## Conflict handling examples

- [扩展][必须] 当前实现已完成且样式锁定，而旧设计文档仍显示旧样式时，以当前锁定实现为准；若文档过期，更新 active 层，不重构页面。
- [扩展][必须] 某模块已按新接口落地，而过程记录仍保留旧字段命名时，以 active 层 API 当前事实源为准，过程记录仅作背景。
- [扩展][必须] 若新任务明确是"回看一期为什么这么设计"，再读取归档或过程记录；若任务只是"继续实现某个工作单元"，不要读取这些材料。

## Work-unit file responsibilities

新建的工作单元至少应有：`README.md` `manifest.md` `status.md` `requirements/index.md` `blockers/index.md` `issues/index.md` `sync/outward-needs.md` `archive/index.md`。历史单元缺项属于 patch/audit 发现：仅在该单元需要路由或承载当前事项时补齐，不要求一次性迁移所有遗留单元。

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

## Code-to-doc sync triggers

代码或配置发生以下变化时必须执行 docs 写回检查：

- Public API、参数、响应、数据模型变化 → 更新 contracts / requirements / acceptance。
- 用户可见行为、UI 流程、权限、错误提示变化 → 更新 requirements / acceptance。
- 修复 bug、绕过缺陷、发现实现不一致 → 更新 issues，并在验证后归档。
- 发现新阻塞、外部依赖、联调失败 → 更新 blockers 或 shared blocker list。
- 跨单元契约、接口或依赖变化 → 更新 sync/outward-needs.md 和 shared contracts。
- 架构边界、依赖方向、长期原则变化 → 更新 ARCHITECTURE / GOLDEN_RULES。
- 功能删除、取消或被替代 → 更新 scope / requirements，并归档旧事项。

## Session task vs repo docs

- [核心][必须] Claude Code task/todo 只用于当前会话执行管理；repo docs 才是项目持久事实源。
- [核心][必须] 会话 task 完成不等于项目文档完成；结束前仍要执行 Completion docs sync checklist。
- [核心][必须] 任何对未来协作有价值的事实，必须写入 repo docs，而不是只留在 task/todo、聊天记录或 hook state。

## Subagent handoff

- [核心][必须] 委派给 ECC agents 或其他 subagents 时，主会话必须传入当前工作单元范围、已读取的 active 事实源、禁止默认读取 archive 的约束，以及本文件的 write-back routing 要求。
- [核心][必须] subagent 返回时，主会话必须要求其列出：changed facts、new requirements、new issues、new blockers、cross-unit needs、completion/archive candidates、可能需要更新的 docs 路径。
- [核心][必须] subagent 不直接承担最终文档写回责任；主会话收到结果后，仍必须按 Documentation write-back matrix 判断并更新权威文档。
- [扩展][禁止] 不要因为 ECC agent 已完成代码审查、修复或测试，就跳过 `requirements/`、`issues/`、`blockers/`、`sync/`、`archive/`、`process/` 的写回检查。

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

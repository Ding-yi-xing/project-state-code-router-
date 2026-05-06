# Project-state and Collaboration Rules

anthor=DingYiXing

**Scope:** Project-state routing, active/reference/archive layering, bootstrap/patch behavior, collaboration docs, and dirty-read prevention.
**Core:** minimal current truth, conflict resolution, non-destructive initialization — always apply.
**Extended:** archive retrieval, responsibility-area loading, template guidance.
**Often used with:** process.md, warning-signs.md.
**Read Next If:** bootstrapping docs → bootstrap-templates.md; writing code after routing → writing.md and task-specific references.

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

- [核心][必须] 每次任务先判断当前责任范围：单一交付面、单一服务域、pm、cross-area，选择最窄的适用范围。
- [核心][必须] 若项目根目录存在 `CLAUDE.md`，应先读取它，再决定读取哪类入口文档和当前责任范围。
- [核心][必须] 当前开发者负责范围应优先从 `docs/.project-docs-manifest.yaml` 的责任归属配置中查询；仍不明确时，先询问用户或项目经理，不要自行猜测。
- [核心][必须] 单一交付面任务默认只读该交付面的入口文档 + 当前边界 + 当前验收 + 当前锁定范围 + 必需的 API 契约。
- [核心][必须] 单一服务域任务默认只读该服务域的入口文档 + 当前边界 + 当前验收 + 当前锁定范围 + 必需的接口或数据契约。
- [核心][必须] PM 任务默认只读目标范围、优先级、验收标准、锁定范围，以及必要时的风险阻塞。
- [扩展][必须] 仅在任务确实跨边界时进入 cross-area 模式，避免无关文档进入上下文。
- [扩展][禁止] 不要把 cross-area 文档作为单一交付面或单一服务域日常任务的默认入口。

## Project state machine

- [核心][必须] 每次任务先判断项目处于 normal、bootstrap、patch 三种模式之一。
- [核心][必须] 当项目没有 docs、没有 manifest、没有核心 active 文件时进入 bootstrap 模式。
- [核心][必须] 当项目已有 docs 但缺少 manifest、缺少 active 核心文件或缺少当前责任范围入口时进入 patch 模式。
- [核心][必须] 当 manifest、active 核心文件和当前责任范围入口都存在时进入 normal 模式。
- [扩展][必须] bootstrap 模式只创建最小协作文档结构，不预先生成大量长期设计文档。
- [扩展][必须] patch 模式只补齐缺失项，不重建整个 docs 目录。

## Shared execution views & blockers

- [核心][必须] 项目级 `当前任务优先级清单.md` 是唯一主任务事实源，各交付面和服务域不得各自维护脱离它的独立主清单。
- [核心][必须] `docs/20-交付面/<surface>/任务推进清单.md` 与 `docs/30-服务域/<domain>/任务推进清单.md` 只是责任范围执行视图，用于承接本范围当前要做的子任务、当前阻塞和下一步动作。
- [核心][必须] 联调失败、接口报错、环境差异、验收阻塞和待确认归属的问题，统一记录到 `当前阻塞与待修复问题清单.md`，而不是散落在聊天记录或过程记录中。
- [核心][必须] 过程记录只用于保留推进经过和结论，不作为当前待修复事项的默认事实源。
- [扩展][必须] 已解决的问题在 active 层保留简短结论；详细排查过程、旧日志和历史讨论下沉到 archive 或过程记录。
- [扩展][禁止] 不要把多个交付面任务推进清单、多个服务域任务推进清单和共享阻塞清单混写成一份长过程周报。

## Initialization and patch safety

- [核心][必须] 创建目录仅在目录不存在时进行。
- [核心][必须] 创建文件仅在文件不存在时进行。
- [核心][必须] 对已存在且非空的文件绝不覆盖。
- [核心][必须] 若项目根目录缺少 `CLAUDE.md`，bootstrap 时应创建一个最小入口文件，用于声明读取顺序与责任归属查询位置。
- [核心][必须] `docs/.project-docs-manifest.yaml` 应记录 active_core_files，作为默认事实源白名单。
- [核心][必须] `docs/` 作为项目级共享协作层，应位于项目根目录下，并与项目的顶层代码或应用目录同级；不要把这套共享事实源塞进某一侧源码目录。
- [核心][必须] 不在 active_core_files 中的文档，不应仅因“名字看起来相关”就自动进入默认上下文。
- [核心][必须] 当模板升级时，创建迁移说明或缺失的伴随文件，而不是自动重写用户内容。
- [扩展][必须] 使用 `docs/.project-docs-manifest.yaml` 记录结构版本、核心文件列表和责任归属查询信息，作为后续 patch 的哨兵文件。
- [扩展][必须] bootstrap 或 patch 后，在过程记录中写入一次初始化/补齐记录。
- [扩展][禁止] 不要因为发现少量缺失文件就整体重建整个文档树。

## Minimal reading protocol

- [核心][必须] 默认只加载当前责任范围的最小活跃集，控制上下文体积并降低脏读概率。
- [核心][必须] 除非当前任务真的需要，否则不要读取长过程记录、旧规划、归档需求、旧设计推导过程。
- [核心][必须] 单一交付面任务在推进当前工作时，可读取该交付面的 `任务推进清单.md`；仅在存在联调或缺陷阻塞时再读取 `当前阻塞与待修复问题清单.md`。
- [核心][必须] 单一服务域任务在推进当前工作时，可读取该服务域的 `任务推进清单.md`；仅在存在联调或缺陷阻塞时再读取 `当前阻塞与待修复问题清单.md`。
- [核心][必须] pm 任务在推进、风险同步、验收推进时，可读取 `当前阻塞与待修复问题清单.md`，但不应默认带入所有过程记录。
- [扩展][必须] 如果 active 层已足够完成当前任务，就不要继续扩展到 reference 或 archive。
- [扩展][必须] 若当前任务只是实现或修复，不要主动引入与任务无关的模块设计、视觉规范、阶段记录。

## Archive retrieval protocol

- [核心][必须] 只有在明确需要历史追溯时，才允许读取 archive。
- [核心][必须] archive 读取应先从索引或摘要开始，再精确提取最相关的 1-2 份材料。
- [核心][必须] 当前任务若是再次改造、迁移、回溯已完成事项，可读取对应归档，但不得默认扩大范围到整个归档目录。
- [扩展][必须] 当 active 层引用了历史设计或旧需求结论时，仅按引用提取对应归档。
- [扩展][禁止] 不要默认扫描整个 archive 目录寻找“可能相关”的历史材料。

## Conflict handling examples

- [扩展][必须] 当前实现已完成且样式锁定，而旧设计文档仍显示旧样式时，以当前锁定实现为准；若文档过期，更新 active 层，不重构页面。
- [扩展][必须] 某模块已按新接口落地，而过程记录仍保留旧字段命名时，以 active 层/API 当前事实源为准，过程记录仅作背景。
- [扩展][必须] 若新任务明确是“回看一期为什么这么设计”，再读取归档或过程记录；若任务只是“继续实现某个交付面或服务域”，不要读取这些材料。

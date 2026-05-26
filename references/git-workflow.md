# Git Workflow Rules

author=DingYiXing

**Scope:** Branching, staging, commits, merge preparation, conflict handling, pull request / merge request hygiene.
**Core:** active-first submission timing, commit boundaries, validation before submission, conflict resolution discipline.
**Extended:** branch naming, commit message structure, PR/MR linkage, history cleanup.
**Often used with:** project-state.md, quality.md.
**Read Next If:** preparing a release or merge gate → quality.md; resolving task/document conflicts → project-state.md.

## Submission timing

- [核心][必须] 在提交代码之前，先确认当前变更仍符合 active 层当前事实源，而不是迎合旧需求、旧设计或旧过程记录。
- [核心][必须] 一个提交应对应一个已经达到最小可验证状态的任务片段：至少能说明它解决了什么，并完成了与该片段相称的最小验证。
- [核心][必须] 未完成联调、未通过最基本验证、或仍处于"主要行为不确定"的变更，不应伪装成完成态提交。
- [核心][必须] 如果当前问题只是排查中间状态，可以保留本地变更，但不应将其当作已完成工作推进到共享主线。
- [核心][必须] 当问题仍处于待确认归属时，先更新共享阻塞清单，再决定是否提交代码；不要用提交行为替代问题同步。
- [扩展][必须] 对于跨前后端联调问题，优先让每次提交只承载一侧已确认有效的修复，避免把"猜测性修复"与"已验证修复"混在一起。

## Do not submit yet when

- [核心][禁止] 当前变更仍依赖临时调试代码、临时日志、手工 mock 数据或本地特判才能工作时，不要提交为完成态。
- [核心][禁止] 接口契约、需求边界或问题归属仍未确认，且共享阻塞清单也未同步时，不要用提交来代替沟通和确认。
- [核心][禁止] 暂存区中混入了无关文件、临时文件、顺手重构或不打算共享的修改时，不要直接提交。
- [核心][禁止] 当前提交既没有完成最小验证，也没有明确记录未验证项和剩余风险时，不要伪装成可合并结果。
- [核心][禁止] 当代码与 active 文档冲突、且尚未判断谁已过期时，不要仓促提交到共享分支。
- [扩展][禁止] 仅为了"先存一下"而把尚未成形的排查过程提交到共享主线；如需保留中间状态，优先保留在本地分支或继续整理为可验证片段后再提交。

## Commit boundaries

- [核心][必须] 每次提交只承载一个明确意图：一个功能点、一个缺陷修复、一个联调修复，或一次纯重构。
- [核心][必须] 不得把无关重构与当前功能/修复混在同一次提交中。
- [核心][必须] 如果为了实现当前修复必须做小范围配套清理，清理范围应限制在直接相关区域。
- [核心][必须] 纯重命名、格式化、移动文件等机械性修改，如与功能修复无直接耦合，应独立提交。
- [扩展][必须] 当一次工作自然分成"准备提交"和"结果提交"两步时，拆成两个提交通常比一个大提交更利于评审与回滚。

## Commit message

- [核心][必须] commit message 应优先说明"为什么提交这次变更"，而不是只罗列"改了哪些文件"。
- [核心][必须] 第一行应简短、具体、可独立理解，避免 `update`、`fix issues`、`misc changes` 之类空泛描述。
- [核心][必须] 当提交对应共享阻塞项或项目级任务时，message 或 PR/MR 描述应能追溯到对应事项。
- [扩展][必须] 推荐结构：`type(scope): summary`，其中 type 只需表达意图，不必教条固定。
- [扩展][必须] 常见 type 可使用：`feat`、`fix`、`refactor`、`test`、`docs`、`chore`。
- [扩展][必须] 如需补充正文，正文解释背景、约束、权衡和验证方式，而不是重复标题。

### Commit message examples

- `fix(api): align course list params with current contract`
- `fix(frontend): stop retry loop after 401 response`
- `refactor(auth): isolate token parsing from session refresh`
- `test(order): cover duplicate callback idempotency case`

### Commit message templates

#### Minimal template

```text
type(scope): summary
```

#### Extended template

```text
type(scope): summary

Background:
- why this change is needed

Validation:
- what was verified

Risk:
- what remains unverified or needs follow-up
```

#### Writing guidance

- [核心][必须] `summary` 应直接表达本次提交解决的核心问题，避免只写文件动作，例如"update config"或"change code"。
- [核心][必须] 若本次提交仍有未验证项，可写进正文 `Risk`，不要把不确定状态藏起来。
- [扩展][必须] 若本次提交对应共享阻塞项、任务编号或当前 active 约束，可在正文补一行引用，帮助评审快速建立上下文。
- [扩展][必须] 当提交足够小且背景明显时，可只保留单行模板；正文不是必填，但一旦写就应提供有效信息。

## Branch usage

- [核心][必须] 分支应围绕单一任务、单一修复或单一联调问题建立，避免一个分支同时承载多条无关工作线。
- [核心][必须] 当 active 层已将某区域标记为锁定时，不得借同一分支顺手做主动重构或样式回滚。
- [扩展][必须] 分支命名可包含任务意图和责任侧，例如 `fix/login-401`、`feat/frontend-course-filter`、`fix/backend-order-sync`。
- [扩展][必须] 如果同一问题需要前后端各自修复，优先使用两个意图清晰的分支，而不是把两侧变更长期堆在一个混合分支里。

## Pre-commit checks

- [核心][必须] 提交前确认本次变更的范围、意图和验证结果已经清楚，不清楚时先缩小提交范围。
- [核心][必须] 提交前运行与本次修改直接相关的最小验证：相关测试、最小手工验证、或关键联调验证。
- [核心][必须] 若提交修复了文档与代码不一致的问题，应同时确认究竟是代码过期还是 active 文档过期，避免把代码拖回旧状态。
- [扩展][必须] 提交前检查暂存区，确保没有把无关文件、临时文件、调试输出或不打算共享的修改一并提交。
- [扩展][必须] 若无法完成完整验证，在提交说明或 PR/MR 描述中明确写出未验证项和剩余风险。

### Pre-commit checklist template

```markdown
## Pre-commit checklist

- [ ] 本次提交只承载一个明确意图，没有混入无关修改
- [ ] 临时日志、临时 mock、本地特判、排查代码已清理或明确不提交
- [ ] 当前实现与 active 层事实源一致；若不一致，已判断谁过期
- [ ] 已完成与本次改动相称的最小验证
- [ ] 未验证项、剩余风险或后续事项已准备写入 commit 正文或 PR/MR 描述
- [ ] 若存在阻塞、契约变更或跨角色影响，已准备引用对应 active 文件或阻塞项
```

#### Usage guidance

- [核心][必须] 这份 checklist 用于提交前最后一次自检，不应用来替代实际验证或事实确认。
- [核心][必须] 只要其中任一项无法勾选，就应先继续整理变更、缩小范围或补充说明，而不是把提交动作提前。
- [扩展][必须] 当任务属于"部分交付"时，允许提交，但前提是 checklist 中关于验证、风险和剩余事项的描述已经准备完整。
- [扩展][必须] 若项目已有自己的提交流程，可将此模板压缩为更短版本，但不要丢掉"范围纯度、事实一致、验证、风险"这四类检查。

## Conflict handling

- [核心][必须] 处理冲突前先判断冲突双方谁代表当前 active 事实源，不能机械地"保留 ours/theirs"。
- [核心][必须] 不得因为历史分支或旧文档中的方案存在，就在冲突处理时回滚当前锁定实现。
- [核心][必须] 冲突解决后重新执行受影响的最小验证，确认合并结果仍满足当前边界和验收。
- [扩展][必须] 如果冲突暴露出需求边界已变化，应先更新 active 层事实源，再继续合并，而不是靠口头约定解决。

## Rebase, squash, merge

- [核心][必须] 重写历史前确认不会掩盖仍未解决的阻塞问题，也不会把多个独立问题压扁成不可追溯的一次提交。
- [核心][必须] merge 或 squash 前确认提交集合整体仍对应同一任务目标，避免把无关工作一起带入主线。
- [扩展][必须] 当评审更关注最终结果而非中间嗓声时，可在合并前整理历史；但不要以整理历史为由抹掉关键背景。
- [扩展][必须] 若项目更依赖排障可追溯性，保留几个边界清晰的小提交通常优于单次大 squash。

## PR / MR hygiene

- [核心][必须] PR / MR 描述应能说明：对应主任务、对应阻塞项（如有）、本次改动意图、验证方式。
- [核心][必须] 若本次提交只解决了问题的一部分，明确标出剩余未解决项，避免评审误以为整项工作已完成。
- [扩展][必须] 当改动触及前后端契约、锁定区域或验收标准时，在 PR / MR 描述中直接引用对应 active 文件。
- [扩展][必须] 若需要 reviewer 快速理解联调问题，优先附上最小复现信息，而不是大段聊天摘录。

### PR / MR description templates

#### Minimal template

```markdown
## Summary

- what changed
- why this change is needed

## Validation

- tests or manual checks performed

## Risk / Follow-up

- remaining risk, unverified items, or next step
```

#### Contract-change template

```markdown
## Summary

- what changed
- why the old behavior or contract was no longer correct

## Active references

- current boundary: `path/to/active-file.md`
- current acceptance: `path/to/active-file.md`
- current contract/blocker: `path/to/active-file.md`

## Validation

- tests or manual checks performed
- integration path verified

## Risk / Follow-up

- remaining risk, unverified items, or next step
```

#### Writing guidance

- [核心][必须] `Summary` 至少同时回答"改了什么"和"为什么现在要改"，不要只贴实现细节。
- [核心][必须] `Validation` 只写真实完成的验证；未做的内容应留在 `Risk / Follow-up`，不要默认写成"已验证"。
- [扩展][必须] 当问题来源于联调阻塞、需求收口或 active 文档更新时，优先在描述里直接挂出对应文件，而不是只说"已同步"。
- [扩展][必须] 如果 PR / MR 只交付整个任务的一部分，应在 `Risk / Follow-up` 中明确剩余范围和责任侧。

## Review / merge gate

- [核心][必须] reviewer 在判断是否可合并前，应先确认该变更仍符合当前 active 事实源，而不是仅凭历史上下文、作者口头说明或旧截图判断。
- [核心][必须] 若提交意图不单一、验证不足、风险未写明或仍混入临时排查代码，不应给出"可直接合并"的建议。
- [核心][必须] 若 PR / MR 只解决了总问题的一部分，review 结论必须明确它是"部分可合并"还是"整体未完成"，避免把阶段性结果误判为整项完成。
- [扩展][必须] 当改动涉及契约变化、锁定区域或 active 文档更新时，review 反馈应明确指出引用的当前事实源。
- [扩展][必须] 当问题本质是范围混杂而不是代码错误时，优先建议拆分提交或拆分 PR，而不是在混合变更上做含糊批准。

### Reviewer checklist template

```markdown
## Reviewer checklist

- [ ] 这次提交或 PR / MR 的意图单一且边界清楚，没有混入无关修改
- [ ] 描述说明了改动内容、当前修改原因，以及是否只交付了部分范围
- [ ] Validation 只声称真实完成的验证，没有把未验证内容伪装成已完成
- [ ] 当前实现与 active 层事实源一致；若不一致，已经明确指出谁过期
- [ ] 没有把临时日志、临时 mock、本地特判或排查代码当成完成态结果合并
- [ ] 剩余风险、后续事项和责任侧在批准前已经明确
```

#### Reviewer guidance

- [核心][必须] 这份 checklist 用于判断"是否适合批准或继续要求补充信息"，不是机械打勾流程。
- [核心][必须] 若关键事实、验证结论或剩余范围不清楚，应先要求作者补描述或补验证，再判断是否可合并。
- [扩展][必须] 当问题主要在提交边界而不是代码正确性时，优先要求拆分，而不是在同一 PR / MR 上累积大量条件式意见。
- [扩展][必须] 即使项目强调快速合并，也不应跳过"active 一致性、验证真实性、剩余风险显式化"这三类检查。

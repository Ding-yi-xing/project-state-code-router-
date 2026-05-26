# Garbage Collection for Projects Using This Skill

**Scope:** Doc-gardening and code-rot prevention for projects that use this skill — not for this skill repo itself.
**Core:** invariants worth checking, semantic checks worth running, the small-PR fix shape — always apply when introducing GC to a project.
**Often used with:** project-state.md (defines the docs being gardened), naming.md / design.md / defense.md (define the code rules being garbage-collected).
**Read Next If:** writing the project's golden-rule list → architecture-layers.md; bootstrapping the docs structure GC will guard → bootstrap-templates.md; copying a starter lint script → references/downstream-samples/gc-lint.example.mjs.

灵感来自 OpenAI 在《Harness Engineering: leveraging Codex in an agent-first world》里实践的两个机制：

> 一个定期运行的 "doc-gardening" 智能体会扫描那些不再反映真实代码行为的过时或废弃文档，并发起修复用的 Pull Request。

> 我们会定期运行一组后台 Codex 任务，扫描偏差、更新质量等级，并发起有针对性的重构 Pull Request。其功能类似于垃圾回收。

两套机制本质是同一个工程模式：**约束被编码 → 智能体定期扫偏离 → 自动开小 PR → 通常一分钟内审完合入**。一条扫文档腐烂，一条扫代码腐烂。本文件给你的项目装这两条。

## 谁应该装

- 多人协作的真实项目，使用本 skill 维护 `docs/units/<unit>/` 这套协作文档结构
- 有持续演进的代码库，已经定义了 lint / 命名约定 / 架构边界
- 改动频繁，技术债容易堆积，文档容易脱节

skill 仓库本身不装：维护方一人、改动稀少、不满足 GC 性价比的前提。

## 第一类：文档 GC（doc-gardening）

### 不变式（机械可检）

下面以本 skill 推荐的目录结构为蓝本，给出常见检查项。具体路径按你项目的 manifest 调整。

- **DOC.M.01** `docs/.project-docs-manifest.yaml` 中声明的 `active_core_files` 全部存在
- **DOC.M.02** `docs/.project-docs-manifest.yaml` 中声明的 `work_units` 在 `docs/units/` 下都有对应目录且含 `manifest.md`
- **DOC.M.03** 反向：`docs/units/` 下每个非 `.template/` 目录都在 manifest 的 `work_units` 中
- **DOC.M.04** 每个工作单元包含必备文件：`manifest.md` `status.md` `requirements/index.md` `blockers/index.md` `issues/index.md` `sync/outward-needs.md` `archive/index.md`
- **DOC.M.05** `shared/current/` 下文件不超过约定行数（如 `当前任务优先级清单.md` ≤ 200 行 — 长了说明该归档）
- **DOC.M.06** 引用归档文件的链接必须真实存在，归档目录只增不删
- **DOC.M.07** 每个 `archive/` 下条目必须有归档原因和归档时间字段

### 语义检查（智能体周期跑）

- **DOC.S.01** `status.md` 中标记 `[x]` 但未归档的项超过 N 天 → 提示是否归档
- **DOC.S.02** `blockers/index.md` 中已解决的阻塞超过 N 天未清理 → 提示
- **DOC.S.03** 文档描述的接口 / 字段在代码里已不存在 → 提示文档过期
- **DOC.S.04** 多个 status.md 都引用同一个归档项当作"当前依据" → 这是脏读复发的信号
- **DOC.S.05** 某个工作单元 status.md 长期不动（≥ 30 天）→ 是已完成？是僵尸？提示 PM 判断
- **DOC.S.06** `sync/outward-needs.md` 写入但其他单元从未读取或回应 → 提示协同断裂

### 修复 PR 形态

- 单文件、单类型问题、< 30 行 diff
- 标题包含触发的 GC 编号（如 `DOC.M.04: add missing blockers/index.md to admin-web`）
- 描述：触发条件、问题位置、修复方式、是否需要人工再判断
- 不在同一 PR 修多类问题，便于回滚

## 第二类：代码 GC（OpenAI 原版"垃圾回收"）

### 黄金原则（Golden Rules）— 项目级品味不变式

OpenAI 原文称之为 **黄金原则**：带有主观意见的机械规则，**保持代码库可读性和一致性、便于将来运行智能体**。它不是 CC2 那种通用规则的现代化（那是 `references/overrides.md` 干的事），而是**项目自己的品味共识**。

> 我们更倾向于使用共享的实用程序包，而不是手工编写的辅助工具，以便将不变式集中管理；我们不会使用"YOLO 式"探测数据 — 我们会验证边界，或依赖类型化的 SDK，这样智能体就不会意外地基于猜测的结构进行构建。

每个项目应该把自己的黄金原则**显式写下来**（例如 `docs/GOLDEN_RULES.md`），随着审查反馈和重构 PR 持续回灌。OpenAI 的几条作为起点参考：

- **GR.01 优先共享工具包**：不手写辅助工具；不变式集中在 `utils/` 或 `core/` 等共享包，便于一处修改全局生效
- **GR.02 边界处解析数据形状**（不只是校验）：所有外部数据进入业务逻辑前用 schema 解析为强类型（如 zod / pydantic / serde），不让"形状不确定"渗透进系统
- **GR.03 不 YOLO 式探测**：不靠 `data?.user?.profile?.name ?? ''` 这种连续可选链猜结构；用类型化 SDK 或 schema 强制
- **GR.04 横切关注点统一注入**：日志、鉴权、特征开关、遥测从单一 Providers 入口进入业务代码（详见 `references/architecture-layers.md`）
- **GR.05 一段代码只在一个地方维护**：发现 ≥ 3 处复制时立刻提取共享工具，不留"等下次再合并"
- **GR.06 失败要响**：所有 I/O / FFI / 子进程 / 网络调用必须显式处理错误；不允许 silent catch
- **GR.07 不引入不在 allowed list 的依赖**：每个新依赖经讨论加入清单后才能用，避免供应链失控

写黄金原则的几个要点：

- **机械可检的优先**：能写成 lint / 架构测试的，就别只放在文档里
- **每条解释为什么**：原则下面附一句"不这么做会发生什么"，便于未来智能体判断边界
- **例子比规则更值钱**：每条配一个错误写法 + 正确写法对比
- **持续回灌**：审查评论里反复出现的"建议"如果机械可检，就提升为黄金原则 + lint

### 它防的"偏差"是什么

不是新写代码的 lint 错误（那是 pre-commit / CI 的事），而是**老代码在规则演进或新工具引入后产生的漂移**：

- 新引入了共享工具包，但老代码还在用手写版本
- 命名约定升级（如统一加前缀 / 改大小写），老代码没跟上
- 新增了文件大小 / 嵌套深度上限，老文件超标
- 架构边界规则更严（如 UI 层不能直接调 Repo），老代码跨越边界
- 日志规范升级（如统一结构化），老代码还在用 print
- 拒绝某种依赖（如停用某 npm 包），老代码还在用

### 不变式（按你的项目自定义）

下面是常见类别的检查思路，具体规则需要你项目自己定。约束由 lint / 单元测试 / 架构测试编码进系统：

- **CODE.M.01** 架构边界：UI → Service → Repo 单向依赖，反向 import 即违规
- **CODE.M.02** 文件大小上限（如单文件 ≤ 400 行，函数 ≤ 100 行，参数 ≤ 7 个）
- **CODE.M.03** 命名约定：模式名 / 类型名 / 函数名前后缀符合最新规则
- **CODE.M.04** 禁用清单：禁用某些 API（如 `eval`、裸 `except:`）、禁用某些依赖
- **CODE.M.05** 必用清单：所有 SQL 走参数化、所有外部输入走 schema 校验
- **CODE.M.06** 结构化日志：所有日志调用走统一封装，不允许直接 `print` / `console.log`

实现可以是：自定义 ESLint / RuboCop / Pylint 规则、`go vet` 自定义 analyzer、custom rust lint、架构测试（如 ts-arch、ArchUnit）。

### 语义检查

- **CODE.S.01** 同一工具 / 函数被复制实现 ≥ 3 次 → 提示该提取
- **CODE.S.02** 跨多个文件相同的 try / catch / log 三件套 → 提示该走统一拦截器
- **CODE.S.03** 性能热点（profile 标记的 top N）有明显改进空间 → 提示评估
- **CODE.S.04** 测试覆盖率长期低于阈值的关键模块 → 提示补
- **CODE.S.05** 已知漏洞依赖（npm audit / pip-audit）未升级 → 提示

### 修复 PR 形态

OpenAI 原话："其中大多数都可以在一分钟内完成审查并自动合并。"

- 单一关注点，单一规则，最小 diff
- 标题：`CODE.M.0X: <rule short name> in <module>`
- 通常是：rename / extract / replace API / move file / add missing call — 都是机械操作
- 复杂的（涉及行为变更、API 兼容）不进自动 GC，由人来开 PR

## 巡检节奏

- **机械检查**：每次 commit / pre-commit hook / PR 流水线
- **语义检查**：每周一次（cron / scheduled CI / Claude `/loop 7d`）

## 启用方式（按你项目环境装配）

skill 不绑定具体执行器。下面是常见装法：

### 文档 GC

- 写一个脚本（Node / Python / Bash 任你）扫描 `docs/` 验证 DOC.M.01-07
- 挂到 pre-commit hook、GitHub Action、或 Claude `/loop`
- 参考实现：`references/downstream-samples/gc-lint.example.mjs`（本仓库自带的最小示例，改改路径就能用）

### 代码 GC

- 把 CODE.M.0X 编码进你项目的 lint / 架构测试 / 自定义 analyzer
- 用语言生态的工具：ESLint custom rules、Pylint / Ruff custom checkers、Go analysis、ArchUnit、ts-arch、dependency-cruiser
- 定期跑：把"扫全仓库 + 提 PR"包成 Claude 命题，每周 `/loop 7d` 一次

### Claude 触发的语义巡检

```
/loop 7d 按 references/gc-rules.md 给本项目跑 GC：
  1. 文档 GC：扫 docs/，按 DOC.M.* 和 DOC.S.* 给我违规清单
  2. 代码 GC：扫源码，按本项目定义的 CODE.M.* 和 CODE.S.* 给我违规清单
  3. 不直接改文件，输出违规清单 + 建议修复 PR 草稿
  等用户确认后再合入。
```

## 关键原则（不要省）

1. **单 PR 单关注点**：批量合并诱惑很大但回滚困难
2. **机械先行**：能 lint 抓的就别人工
3. **小步偿还**：OpenAI 的比喻 — 技术债是高息贷款，每天还几块比攒到年底还几万划算
4. **失败即提示**：GC 报错时不静默，列清楚哪条规则、哪个文件、哪一行
5. **不破坏正常工作流**：GC 跑慢、误报多、阻塞合并，会被关掉 — 装 GC 比不装好但比"装得难用"差
6. **lint 错误信息 = 修复指令**：为 AI 项目写 lint 时，错误信息要直接告诉智能体怎么改，而不是只说什么错了。原文："由于这些 lint 是自定义的，我们编写错误信息时会**在智能体情境中注入修复指令**。" 详见 `references/architecture-layers.md` 的"Lint 错误信息原则"段

# project-state-code-router

一个用于 **repo-as-system-of-record 项目协作**的 Claude Code skill：先通过当前项目状态路由收敛事实源，再进入实现；防止从过期文档产生脏读；只有在项目 / ECC / 语言规则没有覆盖时，才加载兜底编码约束。

它帮 Claude（或其它编码 Agent）在改代码或文档之前先决定：**当前真相是什么、要读什么、不该读什么、事实该写回哪里、该套用哪些规则**。

---

## 这个 skill 做什么

被触发时，它会引导 Agent：

1. 判断项目处于 `bootstrap`、`patch`、`normal`、`audit` 还是 `repair` 模式
2. 识别最窄责任范围：某个工作单元、`pm`、或 `cross-area`
3. 只读取该范围所需的最小 active 事实集
4. 不让归档、旧计划、过程日志或已完成事项泄漏进当前上下文
5. 在非平凡工作前落下轻量计划或 active execution plan
6. 完成前把变化的事实写回对应权威文档
7. 只有在项目状态定界后，才加载分层兜底编码规则

它有明确立场：**当前真相小、归档默认不读、责任路由优于全仓扫描、计划写在仓库里、实现规则延后加载**。

---

## 为什么需要它

大多数 AI coding 工作流在两个地方失败：

1. **读得太多** — 旧计划、归档、过程记录混进上下文，造成脏读
2. **过早施加约束** — Agent 还没搞清楚自己负责哪一块时，就开始套风格、套抽象、套结构

这个 skill 把流程拆成两层，**先路由，再规则**。

---

## 两层架构

### 1. 项目状态层

- 识别当前责任范围
- 判断当前真相
- 把默认读取限制在最小必要 active 集
- 仅在需要时初始化或补齐协作文档
- 强制执行 veto-first 决策、禁止事项粒度、脏读防护
- 定义 requirements、issues、blockers、sync、plans、archive、process notes 的写回路由

主入口：`references/project-state.md`

### 2. 代码约束层

- 只有在项目状态定界后，才从 `references/` 按需加载具体实现规则
- 始终先加载 `references/overrides.md`，再加载任务相关兜底 reference
- 使用 `references/warning-signs.md` 作为跨场景红旗清单
- 应用受 Code Complete 2 启发并经现代化覆盖层收窄 / 替换后的规则
- 不替代项目 `CLAUDE.md`、ECC rules、语言 / 框架规则、hooks、安全规则、测试规则或性能规则

路由表在 `SKILL.md` 里。

---

## 与项目规则 / ECC 规则的兼容性

这个 skill 不是一个会覆盖本地实践的通用风格指南。

如果项目已经有 `CLAUDE.md`、ECC rules、语言规则、框架规则或 hook 检查，这些规则负责实现质量。本 skill 负责：

- 项目状态路由
- 工作单元范围
- active / reference / archive 分层
- 脏读防护
- 文档优先计划
- 权威 docs 写回
- 只有在没有更具体规则时才启用的兜底编码约束

实际优先级是：

```text
用户请求 + system/developer instructions
> 项目 CLAUDE.md / ECC / 语言 / 框架规则
> project-state-code-router 项目状态层
> project-state-code-router 兜底编码 references
```

---

## 来自 OpenAI Harness Engineering 的实践

这个 skill 吸收了 OpenAI [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/zh-Hans-CN/index/harness-engineering/) 里的若干做法：

| 实践 | 落点 |
|---|---|
| AGENTS.md 当短地图用，而不是百科全书 | `SKILL.md`（地图层：路由 + 安全规则；详细规则下沉到 `references/`） |
| 仓库即 system of record | `docs/` 协作结构与写回路由 |
| Doc-gardening Agent + 代码 GC | `references/gc-rules.md` |
| 严格架构层级 + 自定义 lint | `references/architecture-layers.md` |
| 计划即一流工件 | `docs/shared/exec-plans/{active,completed}/` |
| 项目级黄金原则 | `references/gc-rules.md` 与下游 `docs/GOLDEN_RULES.md` |
| Lint 错误信息 = 修复指令 | `references/architecture-layers.md` + `references/gc-rules.md` |
| 顶层原则文件 | 下游可选 `docs/{DESIGN,FRONTEND,RELIABILITY,SECURITY,PRODUCT_SENSE,GOLDEN_RULES,ARCHITECTURE}.md` |
| `references/<lib>-llms.txt` 提供稳定外部上下文 | bootstrap 模板里的下游 `docs/references/` |

---

## skill 仓库结构

```text
project-state-code-router/
├── SKILL.md                          # 地图层：两层、模式、安全规则、路由表
├── README.md / README.zh-CN.md
├── LICENSE
├── scripts/
│   └── audit_project_docs.py         # 只读 docs 审计（需要 PyYAML）
└── references/
    ├── audit-protocol.md             # audit / repair 分级与流程
    ├── overrides.md                  # 现代兜底规则覆盖层；先加载
    ├── warning-signs.md              # 跨场景红旗清单
    ├── project-state.md              # 项目状态层规则
    ├── bootstrap-templates.md        # 最小 docs 骨架、manifest schema、工作单元与计划
    ├── architecture-layers.md        # 分层架构 + 边界 lint
    ├── gc-rules.md                   # 文档 / 代码 GC、黄金原则
    ├── design.md                     # 类 / 模块 / 接口设计
    ├── naming.md                     # 变量、函数、类型命名
    ├── layout.md                     # 代码格式、注释
    ├── control.md                    # 控制流、条件、循环
    ├── defense.md                    # 输入校验、断言、错误
    ├── debugging.md                  # 复现、隔离、验证
    ├── quality.md                    # 测试设计、可测性、评审
    ├── performance.md                # 优化策略
    ├── git-workflow.md               # 提交、分支、PR
    ├── templates.md                  # 文件 / 函数模板
    └── downstream-samples/
        └── gc-lint.example.mjs       # 下游项目可复制的参考实现
```

---

## 推荐的下游项目结构

bootstrap 时建议的目录是刻意保持最小的，并且位于项目根目录：

```text
<project-root>/
├── CLAUDE.md                         # 路由入口契约
├── docs/
│   ├── .project-docs-manifest.yaml   # 责任查询、roles、
│   │                                 # work_units、active_core_files
│   ├── DESIGN.md / FRONTEND.md / RELIABILITY.md / …  # 可选长期原则
│   ├── GOLDEN_RULES.md               # 可选项目级机械规则
│   ├── ARCHITECTURE.md               # 可选顶层层级图
│   ├── navigation/
│   ├── shared/
│   │   ├── current/                  # active 事实：范围、优先级、
│   │   │                             # 阻塞、验收、锁定范围
│   │   ├── contracts/
│   │   ├── decisions/
│   │   ├── milestones/
│   │   ├── exec-plans/
│   │   │   ├── active/               # 进行中的执行计划
│   │   │   ├── completed/            # 历史决策，不删
│   │   │   └── tech-debt-tracker.md
│   │   ├── generated/                # 自动生成的契约；不要手改
│   │   └── archive/
│   ├── units/                        # 只放已确认的工作单元
│   │   └── .template/
│   ├── references/                   # 下游依赖的 llms.txt
│   └── process/
└── <code-dirs>/
```

文件名可本地化（中文也行），结构语义比字面文件名更重要。不要预创建猜测性的工作单元；应向项目经理或当前用户确认实际需要的工作单元。

---

## 项目状态

| 模式 | 进入条件 | 行为 |
|---|---|---|
| `bootstrap` | 无 `docs/`、无 manifest、无 active 层 | 只创建最小骨架，不捏造业务单元或事项 |
| `patch` | 有 `docs/` 但 manifest / active 层 / 单元入口缺失 | 只补缺失项，绝不覆盖已有非空文件 |
| `normal` | manifest、active 层、当前单元入口都存在 | 只读最小必要集，只在当前范围内编辑 |
| `audit` | 用户要求审计 / docs 治理 | 全面只读检查，分级报告，不自动修复 |
| `repair` | 用户明确要求整改 | 只修复确认项，再运行审计验证 |

Manifest 恢复策略是保守的：解析错误、字段缺失、过期的 `active_core_files`、不完整的 `work_units` 都要明确报告，并且只用最小安全方式修复。旧 manifest 先兼容映射；不得在 patch 模式直接覆盖或重写。审计默认不修改文件。详见 `references/audit-protocol.md`；可运行 `python scripts/audit_project_docs.py <project-root>`。

---

## 文档模型

文档分三层：

- **Active**（当前真相）— 默认只加载这一层
- **Reference**（长期设计资料）— 任务真的需要时才读
- **Archive**（历史材料）— 默认不读；如需重新激活，新建 active 条目，不直接改归档

冲突时**以 active 为准**。如果 active 与当前代码或测试行为冲突，先验证当前事实，再决定是修代码还是更新权威 active 文档。

---

## 文档优先计划

在非平凡编码、架构、跨文件修改、跨单元协作、风险修复或计划推进前，应先在仓库里创建或更新轻量计划 / active exec plan。

计划至少写明：

- 目标
- 范围与不做什么
- 步骤
- 验证方式
- docs 写回目标
- 中断恢复点

1-3 步、单文件、低风险的小改动可以跳过持久计划，但 Agent 应说明为什么。

---

## 完成前写回路由

每次项目工作结束前都要做 docs sync 检查。`status.md` 只是 dashboard / index；它不得成为需求、缺陷、阻塞、协同、过程记录或归档状态的唯一事实源。

| 事实变化 | 权威写回位置 |
|---|---|
| 需求变化 | `docs/units/<unit>/requirements/` |
| bug、缺陷、验收失败 | `docs/units/<unit>/issues/` |
| 阻塞或外部依赖 | `docs/units/<unit>/blockers/` 或 `docs/shared/current/当前阻塞与待修复问题清单.md` |
| 跨单元请求 | `docs/units/<unit>/sync/outward-needs.md` |
| 项目级范围 / 优先级 / 验收 / 锁定范围变化 | `docs/shared/current/*.md` |
| 完成或取消的事项 | `docs/units/<unit>/archive/` 与 `archive/index.md` |
| 排查或 handoff 叙事 | `docs/process/` 或 active exec-plan progress log |
| 进行中的多步骤计划 | `docs/shared/exec-plans/active/` |
| 长期架构或原则 | `docs/ARCHITECTURE.md`、`docs/DESIGN.md`、`docs/GOLDEN_RULES.md` 等 |

---

## 轻量任务快速通道

如果任务同时满足：

- 单文件
- 非结构性
- 非首次 setup
- 非安全关键

Agent 可以跳过完整项目状态路由，只加载核心 warning signs。若执行中范围扩大，则回退完整路由协议。

---

## 如何使用

下面这些场景适合触发该 skill：

- 从项目文档继续 / 恢复工作
- 推进 active execution plan
- bootstrap 或 patch 协作文档
- 判断当前真相、范围、阻塞、需求或验收标准
- review、debug、refactor、写测试，且不想被无关历史拖累
- 给下游项目装 doc-gardening 或代码 GC
- 建立架构层级与边界强制
- 执行可能改变项目事实的实现工作

skill 会根据 `SKILL.md` frontmatter 里的触发词自动激活。

### 推荐工作流

1. 如果存在根目录 `CLAUDE.md`，先读它
2. 读取 `docs/.project-docs-manifest.yaml`
3. 判断最窄责任范围
4. 判断项目模式（`bootstrap` / `patch` / `normal` / `audit` / `repair`）
5. 只读取当前范围所需的最小 active 文档集
6. 仅在历史追溯真的需要时读 archive
7. 在非平凡工作前落下轻量计划 / active exec plan
8. 任务定界后再加载兜底实现 references
9. 完成前运行写回检查，并更新权威 docs

---

## 给下游项目装 GC

skill 仓库自身**不**给自己跑 GC（单人维护、改动稀少，性价比不够）。但它给下游项目准备了完整的 GC 方案：

- **文档 GC** — `docs/` 结构不变式，对过期 status / 已解决 blocker / 归档误引用的语义巡检
- **代码 GC** — 架构层级偏离、命名约定漂移、文件大小、被禁依赖、黄金原则违规
- **参考实现** — `references/downstream-samples/gc-lint.example.mjs`（Node.js 零依赖，可直接复制改路径）

完整方案见 `references/gc-rules.md`。

---

## 可定制项

你大概率会想调整：

- 责任范围名称、工作单元分类
- 协作文档文件名（英文 / 中文 / 团队习惯）
- manifest 的 `roles`、`work_units`、`active_core_files`
- 保留哪些顶层原则文件
- `architecture-layers.md` 里的层级模型
- 项目自己的黄金原则

最适合定制的位置：

- 根目录 `CLAUDE.md` — 路由契约
- `docs/.project-docs-manifest.yaml` — 责任查询与 active 文件发现
- `docs/GOLDEN_RULES.md` — 项目级机械规则
- `docs/ARCHITECTURE.md` — 你的层级模型
- `docs/shared/exec-plans/` — active 和 completed plans
- `references/overrides.md` — 仅当某条 CC2 派生兜底规则与你团队现代实践冲突时

---

## 适合谁

如果你的项目有以下特征，这个 skill 会特别有用：

- 多个工作单元或多个团队
- 既有当前活跃工作，又有大量历史文档
- 在项目根目录维护共享协作文档
- 需要防止 AI 脏读、防止意外回滚到旧设计
- 想要兜底编码规范，但不想强制采用沉重的历史仪式
- 同时让多个 Agent（Claude / Codex / 其它）读同一个仓库

如果你的项目偏好“默认全量文档”、“单体过程记录”、“在定界前就全局执行风格约束”，那这个 skill 会显得刻意克制。

---

## 致谢与归属

由 `DingYiXing` 创建与整理。

编码指导部分来自 *Code Complete 2*，并通过现代覆盖层做了重新筛选，以减少仪式感和过时流程对当前实现的拖拽。

Harness 工程实践（AGENTS.md 即地图、doc-gardening、代码 GC、架构层级、计划即工件、lint 错误即修复指令）来自 OpenAI 的 [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/zh-Hans-CN/index/harness-engineering/)。

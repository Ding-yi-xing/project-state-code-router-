# project-state-code-router

一个把**项目状态协作路由**与 **Code Complete 2 编码规范**融合在一起的 Claude Code skill。在原有 CC2 现代化覆盖层之上，又吸收了 **OpenAI Harness Engineering** 一文里的"入口即目录、定期回收、严格架构边界、计划即一流工件"等实践。

它帮 Claude（或其它编码 Agent）在动手之前先决定：**当前真相是什么、要读什么、不该读什么、该套用哪些规则**。

---

## 这个 skill 做什么

被触发时，它会引导 Agent：

1. 判断项目处于 `bootstrap`、`patch` 还是 `normal` 模式
2. 识别最窄的责任范围（某个工作单元、`pm`、或 `cross-area`）
3. 只读取该范围所需的最小活跃事实集
4. 不让归档、旧计划、过程日志泄漏进上下文
5. 按层加载编码规则 — overrides 先行，再按任务路由到具体 reference

它有明确立场：**当前真相小、归档默认不读、责任路由优于全仓扫描、编码规则延后加载**。

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

主入口：`references/project-state.md`

### 2. 代码约束层
- 从 `references/` 按需加载具体规则
- 始终先加载 `references/overrides.md` 和 `references/warning-signs.md`
- 应用受 Code Complete 2 启发并经现代化的规则
- 按任务类型（命名、设计、防御、调试等）路由到对应文件

路由表在 `SKILL.md` 里。

---

## 来自 OpenAI Harness Engineering 的实践

这个 skill 吸收了 OpenAI [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/zh-Hans-CN/index/harness-engineering/) 里的若干做法：

| 实践 | 落点 |
|---|---|
| AGENTS.md 当目录用，约 100 行 | `SKILL.md`（≤ 150 行，纯路由 + 安全规则） |
| 仓库即 system of record | 整套 `docs/` 结构 |
| Doc-gardening Agent + 代码 GC | `references/gc-rules.md` |
| 严格架构层级 + 自定义 lint | `references/architecture-layers.md` |
| 计划即一流工件 | `docs/shared/exec-plans/{active,completed}/` |
| 项目级黄金原则 | `references/gc-rules.md`（Golden Rules 段） |
| Lint 错误信息 = 修复指令 | `references/architecture-layers.md` + `references/gc-rules.md` |
| 顶层原则文件 | `docs/{DESIGN,FRONTEND,RELIABILITY,SECURITY,…}.md` |
| `references/<lib>-llms.txt` 提供稳定外部上下文 | bootstrap 模板里的 `docs/references/` |

---

## skill 仓库结构

```text
project-state-code-router/
├── SKILL.md                          # 地图（约 130 行）：两层、模式、
│                                     # 安全规则、路由表
├── README.md / README.zh-CN.md
├── LICENSE
└── references/
    ├── overrides.md                  # 现代化覆盖层 — 始终先加载
    ├── warning-signs.md              # 通用红旗 — 始终加载
    ├── project-state.md              # 项目状态层完整规则
    ├── bootstrap-templates.md        # 文档骨架、manifest、单元模板、
    │                                 # 计划即工件、原则文件、llms.txt
    ├── architecture-layers.md        # 分层架构 + 边界 lint
    ├── gc-rules.md                   # 文档 / 代码 GC、黄金原则
    ├── design.md                     # 类 / 模块 / 接口设计
    ├── naming.md                     # 变量、函数、类型命名
    ├── layout.md                     # 代码格式、注释
    ├── control.md                    # 控制流、条件、循环
    ├── defense.md                    # 输入校验、断言、错误
    ├── debugging.md                  # 复现、二分、验证
    ├── quality.md                    # 测试设计、可测性、评审
    ├── performance.md                # 优化策略
    ├── git-workflow.md               # 提交、分支、PR
    ├── templates.md                  # 文件 / 函数模板
    └── downstream-samples/
        └── gc-lint.example.mjs       # 下游项目可复制的 doc-gardening
                                      # 参考实现
```

---

## 推荐的下游项目结构

bootstrap 时建议的目录：

```text
<project-root>/
├── CLAUDE.md                         # 路由入口契约
├── docs/
│   ├── .project-docs-manifest.yaml   # 责任查询、active_core_files
│   ├── DESIGN.md / FRONTEND.md / RELIABILITY.md / …  # 长期原则
│   ├── GOLDEN_RULES.md               # 项目级机械规则
│   ├── ARCHITECTURE.md               # 顶层层级图
│   ├── navigation/
│   ├── shared/
│   │   ├── current/                  # 当前阶段事实（这一期在做什么）
│   │   ├── contracts/
│   │   ├── decisions/
│   │   ├── milestones/
│   │   ├── exec-plans/
│   │   │   ├── active/               # 进行中的执行计划
│   │   │   ├── completed/            # 历史决策，不删
│   │   │   └── tech-debt-tracker.md
│   │   ├── generated/                # 自动生成的契约（不要手改）
│   │   └── archive/
│   ├── units/                        # 工作单元（按责任范围）
│   │   └── .template/
│   ├── references/                   # 你依赖的库的 llms.txt
│   └── process/
└── <code-dirs>/
```

文件名可本地化（中文也行），结构语义比字面文件名更重要。

---

## 项目状态

| 模式 | 进入条件 | 行为 |
|---|---|---|
| `bootstrap` | 无 `docs/`、无 manifest、无活动层 | 创建最小骨架，不预创建业务单元和条目 |
| `patch` | 有 `docs/` 但 manifest / 活动层 / 单元入口缺失 | 只补缺失，不覆盖已有非空文件 |
| `normal` | manifest、活动层、当前单元入口都存在 | 只读最小集，只在当前单元内做最小修改 |

---

## 文档模型

文档分三层：

- **Active**（当前真相）— 默认只加载这一层
- **Reference**（长期设计资料）— 任务真的需要时才读
- **Archive**（历史材料）— 默认不读；如需重新激活，新建活动条目，不直接改归档

冲突时**以 active 为准**。

---

## 如何使用

下面这些场景会触发该 skill：

- 在某个工作单元内继续推进任务
- 在已有项目里编写或修改代码
- 给新仓库 bootstrap 协作文档
- 给已有但残缺的协作文档做 patch
- review、debug、refactor、写测试，且不想被无关历史拖累
- 给项目装 doc-gardening 或代码 GC
- 建立架构层级与边界强制

skill 会根据 SKILL.md frontmatter 里的触发词自动激活。

### 推荐工作流

1. 如果存在根目录 `CLAUDE.md`，先读它
2. 判断最窄责任范围
3. 判断项目模式（`bootstrap` / `patch` / `normal`）
4. 只读取当前范围所需的最小 active 文档集
5. 仅在历史追溯真的需要时读 archive
6. 任务定界后再从 `references/` 加载实现规则
7. 永远先加载 `overrides.md` 和 `warning-signs.md`，让现代覆盖胜出

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
- manifest 的 `active_core_files` 列表
- 保留哪些顶层原则文件
- `architecture-layers.md` 里的层级模型
- 项目自己的黄金原则

最适合定制的位置：

- 根目录 `CLAUDE.md` — 路由契约
- `docs/.project-docs-manifest.yaml` — 责任查询
- `docs/GOLDEN_RULES.md` — 项目级机械规则
- `docs/ARCHITECTURE.md` — 你的层级模型
- `references/overrides.md` — 当某条 CC2 默认与你团队现代实践冲突时

---

## 适合谁

如果你的项目有以下特征，这个 skill 会特别有用：

- 多个工作单元或多个团队
- 既有当前活跃工作，又有大量历史文档
- 在项目根目录维护共享协作文档
- 需要防止 AI 脏读、防止意外回滚到旧设计
- 想要编码规范，但不想强制采用沉重的历史仪式
- 同时让多个 Agent（Claude / Codex / 其它）读同一个仓库

如果你的项目偏好"默认全量文档"、"单体过程记录"、"在定界前就全局执行风格约束"，那这个 skill 会显得刻意克制。

---

## 致谢与归属

由 `DingYiXing` 创建与整理。

编码指导部分来自 *Code Complete 2*，并通过现代覆盖层做了重新筛选，以减少仪式感和过时流程对当前实现的拖拽。

Harness 工程实践（AGENTS.md 即地图、doc-gardening、代码 GC、架构层级、计划即工件、lint 错误即修复指令）来自 OpenAI 的 [Harness Engineering: leveraging Codex in an agent-first world](https://openai.com/zh-Hans-CN/index/harness-engineering/)。

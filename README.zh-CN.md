# project-state-code-router

一个 Claude Code 技能，用来**先根据项目当前状态路由编码任务**，再通过**最小读取、低脏读风险**的流程应用实现约束。

这个技能适用于这样一类仓库：AI coding 不应该无差别扫描整个仓库，不应该默认相信旧计划，也不应该在任务尚未定界时就套用宽泛的风格规则。它帮助 Claude 判断：

- 当前事实源是什么
- 任务属于哪个责任范围
- 当前项目处于 `normal`、`bootstrap` 还是 `patch` 模式
- 现在应该读取哪些文档
- 哪些文档在没有明确需要时不应进入上下文
- 在任务定界之后应应用哪些编码规则

## 为什么需要这个技能

大多数 AI coding 工作流会在两个地方出问题：

1. **读得太多。**
   旧计划、归档说明、过时过程记录混进上下文，导致脏读。

2. **过早施加编码约束。**
   Agent 在还没搞清楚当前负责的是项目哪一块之前，就开始强加风格、抽象、注释或结构规则。

这个技能通过把流程拆成两层来解决这个问题：

1. **Project-state layer（项目状态层）**
   - 识别当前责任范围
   - 判断哪里是当前真相
   - 把默认读取限制在最小必要 active 集
   - 仅在需要时初始化或补齐协作文档

2. **Coding-constraints layer（编码约束层）**
   - 从 `references/` 中按需加载实现规则
   - 在任务定界后应用受 Code Complete 2 启发的规则
   - 通过 modern override 层压制过重、过时、过度仪式化的默认行为

## 核心理念

### 1. Active facts first
默认只让最小的当前事实集进入上下文。

### 2. CLAUDE.md before routing
如果项目根目录存在 `CLAUDE.md`，Claude 应先读取它，并把它作为协作入口契约。

### 3. Archive is opt-in
归档的计划、过程记录和旧设计，不是当前执行依据。

### 4. Patch, don't rebuild
如果协作文档不完整，只补缺失项，不整体重建。

### 5. Responsibility-aware reading
技能会把任务路由到最窄、最合适的责任范围：

- `delivery-surface`
- `service-domain`
- `pm`
- `cross-area`

### 6. Modern default behavior overrides
技能会保留安全性和正确性规则，但压制以下这类沉重的历史默认：

- 强制大量注释的工作流
- 默认加文件头仪式
- 不必要的抽象脚手架
- 对已可信内部流重复做防御性校验
- 只会增加噪音、却不提升正确性的历史过程仪式

## 项目状态

每次调用都先把项目归类到以下三种状态之一：

### `normal`
当仓库已经具备 active 协作结构时使用。

### `bootstrap`
当仓库实际上尚未初始化，需要最小协作文档结构时使用。

### `patch`
当仓库已经有部分协作文档，但缺失必要的 active 文件或责任范围入口时使用。

## 文档模型

这个技能把项目文档分成三层：

### Active
当前真相。默认只应加载这一层。

典型示例：
- 当前范围
- 当前优先级
- 当前验收标准
- 当前实现边界
- 已锁定/禁止主动重构区域
- 责任范围入口文件

### Reference
长期存在的设计资料。

典型示例：
- API 设计
- 架构设计
- 数据设计
- UI/视觉设计
- 模块设计

### Archive
历史材料。

典型示例：
- 旧计划
- 已完成阶段记录
- 已废弃约束
- 历史 handoff 记录

**规则：** 如果 active 与 reference 或 archive 冲突，以 active 为准。

## 建议的协作文档结构

在 bootstrap 模式下，这个技能期望最小共享文档结构大致如下：

```text
<project-root-directory>/
├── CLAUDE.md
├── docs/
│   ├── .project-docs-manifest.yaml
│   ├── 00-导航/
│   │   └── 项目经理导航文档.md
│   ├── 10-共享状态/
│   │   ├── 当前阶段目标与范围.md
│   │   ├── 当前任务优先级清单.md
│   │   ├── 当前阻塞与待修复问题清单.md
│   │   ├── 当前验收标准清单.md
│   │   ├── 当前实现边界对照.md
│   │   └── 当前锁定范围与禁止主动重构清单.md
│   ├── 20-交付面/
│   ├── 30-服务域/
│   ├── 40-项目治理/
│   │   ├── 项目协作与开发原则.md
│   │   └── AI防脏读与防回滚规则.md
│   ├── 90-过程记录/
│   │   └── 000-项目初始化.md
│   └── 99-归档/
```

文件名可以本地化或按项目习惯调整，但结构语义建议保持一致：

- 一个根协作入口
- 一个用于责任归属查询的 manifest
- 一个小而明确的 active 层
- 一个与当前执行显式隔离的 archive 层

## 仓库结构

```text
project-state-code-router/
├── SKILL.md
└── references/
    ├── bootstrap-templates.md
    ├── comments.md
    ├── control.md
    ├── debugging.md
    ├── defense.md
    ├── design.md
    ├── git-workflow.md
    ├── layout.md
    ├── naming.md
    ├── performance.md
    ├── process.md
    ├── project-state.md
    ├── quality.md
    ├── refactoring.md
    ├── templates.md
    ├── warning-signs.md
    └── writing.md
```

### 关键文件

- `SKILL.md`
  - 主路由器和策略入口
  - 定义项目状态、文档分层、责任路由、最小读取协议以及编码规则加载方式

- `references/project-state.md`
  - 协作文档治理规则
  - 责任归属查询
  - active/reference/archive 处理方式
  - bootstrap/patch 安全约束

- `references/bootstrap-templates.md`
  - 协作文档的最小内容模板与期望

- `references/comments.md`、`references/writing.md`、`references/defense.md` 等
  - 只有在任务范围明确后才加载的实现指导

## 如何使用这个技能

当 Claude 被要求执行以下工作时，可以使用这个技能：

- 继续某个交付面或服务域中的工作
- 在已有项目中编写或修改代码
- 为新仓库初始化协作文档
- 为已有但结构不完整的仓库补齐协作文档
- 在不被无关历史材料干扰的前提下进行 review、debug、refactor 或测试

### 推荐工作流

1. 如果存在根目录 `CLAUDE.md`，先读它。
2. 判断最窄的责任范围。
3. 判断项目处于 `normal`、`bootstrap` 还是 `patch` 模式。
4. 只读取当前范围所需的最小 active 文档集。
5. 只有在任务明确需要历史追溯时才读取 archive。
6. 只有在任务定界之后才从 `references/` 加载实现规则。
7. 当通用历史规则与现代清晰性冲突时，应用 modern override 层。

## 责任路由示例

### 示例：前端页面任务
只读取当前交付面的入口、边界、验收标准和锁定区域。

### 示例：API 缺陷修复
只读取相关服务域入口；接口/数据契约按需读取；只有在任务真实阻塞时才读取 blocker 列表。

### 示例：PM 协调任务
读取范围、优先级、验收标准和锁定决策，不带入所有工程细节。

### 示例：跨域联调问题
只读取直接相关的责任范围入口、共享阻塞，以及任务特定契约。

## 本技能的注释哲学

这个技能包含一套详细的注释规则，但默认行为已经被有意现代化。

实际默认值更接近：

- 优先写自说明代码
- 注释意图和约束，而不是显而易见的执行细节
- 不要用注释弥补代码本身的不清晰
- 不默认添加文件头或作者块仪式
- 仅在非显然行为、不变量、workaround、边界假设等场景保留注释

## 适用对象

如果你希望 Claude 在以下仓库中更稳定地工作，这个技能会特别有用：

- 存在多个交付面或服务域
- 既有当前活跃工作，又有大量历史文档
- 在项目根目录维护共享协作文档
- 需要防止 AI 脏读和意外回滚到旧设计
- 希望有编码规范，但不想强制采用沉重的历史仪式

## 可定制项

你大概率会想按项目实际情况调整：

- 责任范围名称
- 协作文档文件名
- active-core 文件列表
- delivery surface / service domain 的分类方式
- 语言特定的 reference 规则
- 注释与文档规范期望

最适合定制的地方包括：

- 根目录 `CLAUDE.md`：定义路由契约
- `docs/.project-docs-manifest.yaml`：定义责任归属查询
- `references/`：定义编码指导
- `SKILL.md` 中的 modern override 段落：调整默认行为

## 给开源使用者的说明

这个技能是有明确立场的。

它默认认为：

- 当前真相应该小而明确
- 归档材料不应悄悄主导当前实现
- 责任路由优于全仓扫描
- 编码规则应该延后加载，而不是提前强加
- 现代清晰性应优先于流程仪式，除非安全性或正确性要求例外

如果你的项目偏好“默认全量文档”“单体过程记录”或“在定界前就全局执行风格约束”，那这个技能会显得刻意克制。

## 致谢与归属

由 `DingYiXing` 创建与整理。

其中部分编码指导受 *Code Complete 2* 启发，并通过 modern default-behavior override 层进行再筛选，以减少仪式感和陈旧流程对当前实现的拖拽。

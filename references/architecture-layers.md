# Architecture Layers and Boundary Enforcement

**Scope:** Layer model, dependency direction, and mechanical enforcement of architecture boundaries for projects using this skill.
**Core:** one-way layer dependencies, explicit cross-cutting entry, machine-checked enforcement — always apply.
**Extended:** layer naming variants, language-ecosystem tools, error-message-as-fix-instruction.
**Often used with:** design.md (general boundary principles), gc-rules.md (architecture-drift GC), naming.md.
**Read Next If:** designing the class/module boundary inside a layer → design.md; preventing drift over time → gc-rules.md.

灵感来自 OpenAI 在《Harness Engineering》里的实践：

> 智能体在具有严格边界和可预测结构的环境中最为高效。每个业务域都划分为一组固定的层，依赖方向经过严格验证，并且仅允许有限的一组边。这些约束是通过自定义的 linter 和结构测试机械地强制执行的。

人类团队通常等到几百人规模才上严格架构；对智能体协作来说，这是**早期先决条件**。约束越早编码进 lint，速度越不会下降，架构越不会漂移。

## 推荐层级模板（业务域内部）

```
Types → Config → Repo → Service → Runtime → UI
                                    ↑
                                    │
横切关注点（auth / connectors / telemetry / feature flags）
通过单一显式入口注入：Providers
```

| 层 | 职责 | 不允许 |
|---|---|---|
| **Types** | 类型、模式、枚举、领域实体的形状 | 引用任何上层 |
| **Config** | 静态配置、特征开关默认值、常量 | 引用 Repo / Service / Runtime / UI |
| **Repo** | 数据访问、外部 API 客户端、I/O 边界 | 引用 Service / Runtime / UI |
| **Service** | 业务规则、领域逻辑、用例编排 | 引用 Runtime / UI |
| **Runtime** | 进程编排、生命周期、调度、worker | 引用 UI |
| **UI** | 视图、控制器、前端状态、路由 | 反向引用任何层 |
| **Providers**（横切入口） | 单一接口注入 auth / connectors / telemetry / flags | 任何层都通过它取，不直连横切实现 |

层级名字可以按项目调整（如 Domain → Application → Adapters → Interface），但**单向 + 横切走 Providers** 是不变量。

## 不变式（机械可检）

- **ARCH.M.01** 任意 import / require / use 语句不得跨越箭头反向（如 `Types/foo.ts` 不得 import `Service/...`）
- **ARCH.M.02** 同层内允许互相引用，但跨业务域（domain）的同层引用必须显式声明
- **ARCH.M.03** 横切关注点只能从 `Providers/` 入口取，业务代码不得直接 import auth / telemetry / flags 实现包
- **ARCH.M.04** Types 层不依赖任何运行时（不 import Node / browser / framework 包）
- **ARCH.M.05** UI 层不直接调用 Repo（必须经 Service）
- **ARCH.M.06** 平台不可移植代码（OS API、浏览器 / Node 特有 API、硬件相关、依赖特定运行时的代码）必须隔离在专门的 adapter 层或子程序中，业务层不直接调用 | anchor=CC2.CH18.S04 (originally tagged `keep` in overrides.md)

## 机械化强制工具

按你项目的语言生态选：

| 语言 | 推荐工具 | 检查点 |
|---|---|---|
| TypeScript / JavaScript | `dependency-cruiser`、`ts-arch`、`eslint-plugin-boundaries` | 配 layer 标签 + forbidden rule |
| Python | `import-linter`（contracts）、`pylint --enable=cyclic-import` | layered contract |
| Go | 自写 `go/analysis` analyzer、`go-cleanarch`、`depgraph` | package 依赖图断言 |
| Java / Kotlin | `ArchUnit`、`Spotbugs` 自定义规则 | layer rule + slice rule |
| Rust | `cargo-modules`、自写 lint via `clippy_utils` | crate-level 边界 |
| 多语言 | `dependency-cruiser` 支持 TS/JS；架构测试自写 | — |

## Lint 错误信息原则

**为 AI 项目写 lint 时，错误信息要直接告诉智能体怎么修，而不是只说什么错了。**

错误写法（描述问题）：
```
ARCH.M.01: forbidden cross-layer dependency
  src/repo/userRepo.ts -> src/service/userService.ts
```

正确写法（描述如何修复）：
```
ARCH.M.01: Repo layer cannot import from Service layer.
  Offender: src/repo/userRepo.ts imports src/service/userService.ts
  Fix: move the shared logic down to a lower layer (Types/Config), or
       invert the call so Service consumes Repo. If userService computes
       something Repo needs, extract it as a Types-layer pure function.
```

OpenAI 原文："由于这些 lint 是自定义的，我们编写错误信息时会**在智能体情境中注入修复指令**。"

## 局部自主、全局边界

借自原文："像领导一个大型工程平台组织：在中央层面强制执行边界，在本地层面允许自主权。"

skill 的应用：
- **强制（lint 抓）**：层间方向、横切入口、文件大小、命名约定、必用清单
- **不强制（让智能体自由发挥）**：函数内部实现风格、变量取名细节、注释多寡、代码组织方式
- 生成的代码不必符合人类的风格偏好；只要正确、可维护、对未来智能体清晰可读，就达标

## 何时引入

OpenAI 经验：**在仓库第一次提交时就装上**，不要等代码写多了再倒腾。

bootstrap 阶段就该：
1. 确定层级模型（可参考上表）
2. 装好 lint / 架构测试工具
3. 写 1-2 条最关键的 ARCH.M.* 规则（不必一次写全）
4. 把 `npm run arch-test` 或等价命令挂到 pre-commit / CI

剩下的规则随项目演进逐条补，每条都通过 GC（见 gc-rules.md）回灌已有代码。

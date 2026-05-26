# Class and Module Design Rules

**Scope:** Class / module / interface design: responsibilities, boundaries, dependency direction, cohesion.
**Core:** single responsibility, explicit boundaries, one-way dependencies — always apply.
**Extended:** abstraction levels, inheritance vs composition, visibility tuning.
**Often used with:** naming.md, defense.md, layout.md.
**Read Next If:** naming the new class/interface → naming.md; deciding error-handling strategy → defense.md.

## Boundaries and responsibility

- [核心][必须] 每个类 / 模块只承担一个明确职责；用一句话能说清"它负责什么"才算合格。 | anchor=CC2.CH06.S02
- [核心][必须] 抽象层次必须一致：同一个类的公开方法应在同一个抽象层级，不要把"打开文件"和"解析 token"放在一起。 | anchor=CC2.CH06.S02
- [核心][禁止] 公开内部实现细节（暴露内部数据结构、把私有成员设成 public 让外部直改）。 | anchor=CC2.CH06.S02
- [核心][必须] 接口比实现稳定 — 设计时优先想"调用方需要什么"，再想"内部如何实现"。 | anchor=CC2.CH06.S01

## Dependency direction

- [核心][必须] 依赖方向必须单向：业务 → 基础设施、UI → 业务 → 数据，反向引用 = 红旗。 | anchor=CC2.CH05.S03
- [核心][禁止] 循环依赖（A 依赖 B，B 又依赖 A），无论是类之间、模块之间、还是包之间。 | anchor=CC2.CH05.S03
- [核心][必须] 跨层调用走显式接口 / 注入，不要在低层直接 import 高层。 | author=DingYiXing
- [扩展][必须] 横切关注点（日志、鉴权、配置、特征开关）通过统一入口注入，不在业务代码里散落取用。 | author=DingYiXing

## Cohesion

- [扩展][必须] 同一个类内的成员函数应共享数据 / 协作完成单一目的；如果一半方法不用任何成员变量，说明该拆分。 | anchor=CC2.CH06.S02
- [扩展][必须] 优先组合（has-a），其次接口实现（implements），最后才考虑继承（is-a），且继承层次不超过 3 层。 | anchor=CC2.CH06.S03

## Module boundaries

- [核心][必须] 模块对外暴露的入口（public API）必须显式列出，其余默认私有。 | anchor=CC2.CH05.S03
- [扩展][必须] 模块边界处必须做输入校验和错误转换，不要把内部异常类型直接抛给外部调用方。 | author=DingYiXing
- [扩展][禁止] 跨模块直接读写对方的内部状态、表、字段 — 必须走对方的公开接口。 | anchor=CC2.CH06.S02

## Modification and review

- [扩展][必须] 设计完成后，问自己：增加新功能需要改几处？如果超过 3 处，说明抽象边界没找对。 | anchor=CC2.CH05.S02
- [扩展][必须] 设计完成后，问自己：删除一个功能能否独立完成？如果牵一发动全身，说明耦合过强。 | anchor=CC2.CH05.S02

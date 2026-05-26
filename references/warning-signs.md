# Cross-cutting Warning Signs

**Scope:** Universal red flags applicable to every coding task, regardless of language or domain.
**Core:** correctness and safety hazards that must be checked before completion — always apply.
**Extended:** style and maintainability red flags worth flagging during review.
**Often used with:** defense.md, naming.md, control.md.
**Read Next If:** untrusted input → defense.md; complex booleans → control.md; unclear names → naming.md.

This file is loaded **before** any other reference. If a warning sign here conflicts with a rule elsewhere, prefer the safer choice.

## Correctness red flags

- [核心][必须] 凡是来自外部（用户输入、网络、文件、子进程、环境变量、数据库结果）的数据，进入业务逻辑前必须显式校验范围、长度、类型、格式。 | anchor=CC2.CH08.S01
- [核心][禁止] 用字符串拼接构造 SQL、shell 命令、HTML、文件路径、正则、URL — 必须用参数化 / 转义 API。 | anchor=CC2.CH08.S01
- [核心][必须] I/O、网络、FFI、子进程、加解密 调用必须检查返回值或捕获异常；不允许吞错误。 | anchor=CC2.CH08.S04
- [核心][禁止] 在断言中放有副作用的代码（生产模式下断言可能被关闭，副作用会消失）。 | anchor=CC2.CH08.S02
- [核心][必须] 整数运算涉及外部数据时，检查溢出 / 下溢 / 除零；金融或安全敏感场景必须用定点或检查算术。 | anchor=CC2.CH08.S01
- [核心][必须] 并发代码必须显式声明同步机制；共享可变状态没有锁、原子或不可变保证 = 红旗。 | author=DingYiXing
- [核心][禁止] 删除、重命名、覆盖文件 / 数据库行 / 远端资源前，没有备份、确认、或可回滚机制 = 红旗。 | author=DingYiXing

## Boundary red flags

- [核心][必须] 函数中"看起来不会发生"的分支必须显式处理（assert / raise / log），不能空 else 或 silent fall-through。 | anchor=CC2.CH15.S01
- [核心][必须] 边界值（0、1、空集合、单元素、最大值、null/undefined）必须有专门测试或显式判断。 | anchor=CC2.CH19.S06
- [核心][禁止] 用 `==` 比较浮点数、用 `is` 比较值类型（Python 之外类似的引用 / 值混淆）。 | anchor=CC2.CH19.S01

## Naming and clarity red flags

- [核心][禁止] 用 `temp`、`x`、`flag`、`data`、`obj`、`info` 等无信息名作为非循环变量。 | anchor=CC2.CH11.S02
- [核心][必须] 名字与实际行为不符 = 红旗（getter 有副作用、`is_valid` 会修改状态、`load` 会触发网络）。 | anchor=CC2.CH11.S01

## Maintainability red flags

- [扩展][必须] 同一规则、同一常量、同一字符串字面量在 3 处以上重复 = 应该提取。 | anchor=CC2.CH24.S02
- [扩展][必须] 函数超过 100 行、嵌套超过 4 层、参数超过 7 个 = 红旗，需要拆分。 | anchor=CC2.CH07.S04
- [扩展][禁止] 注释内容与代码不一致（描述了旧版本行为 / 与代码相反）= 必须删除或修正。 | anchor=CC2.CH32.S05
- [扩展][必须] 留下 `TODO`、`FIXME`、`XXX` 时必须包含 issue 号或负责人；裸标记不允许。 | author=DingYiXing

## Process red flags

- [扩展][必须] 当前任务超出锁定范围（见 project-state.md "否决条件优先原则"）= 立即停手并询问。 | author=DingYiXing
- [扩展][必须] 同一问题已在两次尝试中失败 = 不再继续微调，回到根因分析或换思路。 | author=DingYiXing

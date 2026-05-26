# Quality and Testing Rules

**Scope:** Test design, testability, assertions, code review readiness.
**Core:** test-first for new logic, boundary coverage, assertion correctness — always apply.
**Extended:** test organization, coverage tuning, test-data strategy.
**Often used with:** defense.md, design.md, debugging.md.
**Read Next If:** writing assertions → defense.md; investigating a failing test → debugging.md.

This file replaces the legacy desk-check / formal-inspection rules. Modern equivalent: PR review + CI tests + assertions.

## Test-first basics

- [核心][必须] 修复 bug 前先写一个能复现该 bug 的失败测试；测试通过后这个测试必须保留。 | anchor=CC2.CH22.S03
- [核心][必须] 新增公开函数 / 接口时必须同时写测试，覆盖：典型路径、边界值、错误路径。 | anchor=CC2.CH22.S02
- [核心][必须] 测试运行必须独立 — 任意单测可以单独跑、可乱序跑、不依赖外部状态（除非显式 setup）。 | anchor=CC2.CH22.S04

## Boundary and edge coverage

- [核心][必须] 数值参数：覆盖 0、1、最大值、最小值、负数、溢出阈值。 | anchor=CC2.CH22.S02
- [核心][必须] 集合参数：覆盖空、单元素、典型、最大容量。 | anchor=CC2.CH22.S02
- [核心][必须] 字符串：覆盖空串、单字符、超长、含特殊字符 / Unicode、含分隔符。 | anchor=CC2.CH22.S02
- [扩展][必须] 时间相关逻辑覆盖：跨日、跨月、跨年、闰年、夏令时、时区转换。 | author=DingYiXing

## Testability of production code

- [核心][必须] 副作用通过参数 / 注入引入，不要在函数内直接读全局变量、当前时间、随机数 — 否则测试无法稳定。 | anchor=CC2.CH06.S02
- [扩展][必须] 公开函数应是可测的：输入明确、输出明确、副作用集中可替身。 | anchor=CC2.CH06.S02
- [扩展][禁止] 在生产代码里写"测试模式"分支（如 `if env == 'test':`）— 用注入或替身代替。 | author=DingYiXing

## Assertion strategy

- [核心][必须] 用断言表达"绝不应发生"的不变量；用错误处理表达"可能发生"的异常情况。 | anchor=CC2.CH08.S02
- [核心][禁止] 在断言里放有副作用的表达式（生产模式下断言可能被关闭）。 | anchor=CC2.CH08.S02

## Review readiness

- [扩展][必须] 提交 PR 前自查：每个公开变更都有测试 / 文档 / changelog 更新；CI 必须绿。 | author=DingYiXing
- [扩展][必须] 自我评审：把 diff 当成别人的代码读一遍，标记任何"看起来不太对"的地方再修。 | anchor=CC2.CH21.S02

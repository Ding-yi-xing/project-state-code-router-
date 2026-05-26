# Debugging Rules

**Scope:** Systematic debugging — reproducing, isolating, hypothesizing, verifying.
**Core:** reproduce first, change one variable at a time, verify the fix — always apply.
**Extended:** instrumentation, bisection, post-mortem hygiene.
**Often used with:** defense.md, quality.md.
**Read Next If:** writing test for the bug → quality.md; adding defensive checks → defense.md.

## Reproduce before debugging

- [核心][必须] 先把 bug 稳定复现，再开始改代码 — 没有复现路径的"修复"不是修复。 | anchor=CC2.CH23.S02
- [核心][必须] 把复现路径写成失败测试或最小复现样例（MRE），加入测试套件防止回归。 | anchor=CC2.CH23.S02
- [核心][必须] 复现失败时先检查环境差异（版本、配置、数据、并发）— 不要假设"我这就是不行"是代码 bug。 | anchor=CC2.CH23.S02

## Isolate by hypothesis

- [核心][必须] 每次只改一个变量（一行代码、一个配置、一个输入）— 改多个会让因果不可分。 | anchor=CC2.CH23.S03
- [核心][必须] 用二分法定位：在已知正常和已知出错之间不断对半折叠，直到锁定最小变更。 | anchor=CC2.CH23.S03
- [核心][必须] 形成假设 → 设计可证伪的检查 → 跑检查 → 根据结果修正假设；不接受"猜一个就改"的循环。 | anchor=CC2.CH23.S03
- [核心][禁止] 同样的修改尝试两次仍失败时，停手回到根因分析；不要继续微调。 | author=DingYiXing

## Verify the fix

- [核心][必须] 修完后必须先把代码改回出 bug 的状态确认能复现，再改回修复版确认能消除 — 否则你不知道"是不是这个改动修好的"。 | anchor=CC2.CH23.S04
- [核心][必须] 修复后跑相邻区域的测试，防止引入新回归。 | anchor=CC2.CH23.S04
- [扩展][必须] 修复合入后，把 bug、根因、修复方式记录在 issue / commit / changelog；不写就会再来一次。 | author=DingYiXing

## Instrumentation

- [扩展][必须] 加日志或断言定位时，写明触发条件和期望值；调试结束后清理临时探针。 | anchor=CC2.CH23.S03
- [扩展][禁止] 用 `print` 调试后忘记删 — 至少改成结构化日志并加上明确的开关。 | author=DingYiXing

# Code Smells & Warning Signs

**Scope:** Code smells, design problems, process red flags.
**Core:** defect concentration, warning signals — always apply.
**Extended:** process heuristics, methodology warnings.
**Often used with:** quality.md, refactoring.md.
**Read Next If:** code smells detected → refactoring.md; design concerns → design.md.

- [扩展][必须] 对编程和开发过程做试验，用小程序检验不熟悉的语言特性 | anchor=CC2.CH33.S03
- [扩展][必须] 在行动之前做分析和计划 | anchor=CC2.CH33.S03
- [扩展][必须] 调试时如果一段时间没有进展（约15分钟），放弃当前思路另辟蹊径 | anchor=CC2.CH33.S08
- [核心][必须] 如果类中含有比平均数目更多的错误，考虑重写该类 | anchor=CC2.CH34.S07
- [扩展][禁止] 以大量调试掩盖糟糕的设计 | anchor=CC2.CH34.S07
- [扩展][必须] 当发现代码有重复或修改很相似时，质疑子程序或类中的控制是否得当 | anchor=CC2.CH34.S07
- [扩展][必须] 当发现不能方便地单独使用某个类或很难为其创建测试脚手架时，质疑该类是否耦合过紧 | anchor=CC2.CH34.S07
- [扩展][必须] 当出现无聊的命名或无法在注释中精确描述一段代码时，重新考虑设计 | anchor=CC2.CH34.S07
- [扩展][禁止] 仅靠猜测而非读懂代码来理解程序 | anchor=CC2.CH34.S07
- [扩展][禁止] 释放指针后不将其置为空 | anchor=CC2.CH34.S07
- [核心][禁止] 对程序出现的警告或错误睁一只眼闭一只眼 | anchor=CC2.CH34.S07
- [扩展][必须] 区分私用程序和公用程序，公用程序必须小心编写、可靠、易修改 | anchor=CC2.CH34.S03
- [扩展][必须] 用编程规范弥补语言的弱项 | anchor=CC2.CH34.S04
- [扩展][禁止] 使用语言中有危险的编程特性 | anchor=CC2.CH34.S04

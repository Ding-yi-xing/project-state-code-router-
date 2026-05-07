# Defensive Programming Rules

**Scope:** Input validation, error handling, assertions, exception strategy, security boundaries.
**Core:** input validation, error detection, assertion usage — always apply.
**Extended:** error propagation style, recovery strategies, debugging aids.
**Often used with:** writing.md, debugging.md.
**Read Next If:** writing public functions → writing.md; investigating a crash → debugging.md; designing error-handling strategy → design.md.

## Input Validation

- [扩展][必须] 检查所有来源于外部（文件、用户、网络等）的数据的值，确保其在允许的范围内。 | anchor=CC2.CH08.S01

- [扩展][必须] 对于数值型的输入数据，确保其在可接受的取值范围内；对于字符串，确保其不超长。 | anchor=CC2.CH08.S01

- [扩展][必须] 如果字符串代表特定范围内的数据（如金融交易ID），须确认其取值合乎用途，否则拒绝接受。 | anchor=CC2.CH08.S01

- [核心][必须] 在开发需要确保安全的应用程序时，要格外注意可能攻击系统的数据：包括企图令缓冲区溢出的数据、注入的SQL命令、注入的HTML或XML代码、整数溢出以及传递给系统调用的数据。 | anchor=CC2.CH08.S01

- [扩展][必须] 检查子程序所有输入参数的值，与检查来源于外部的数据一样对待。 | anchor=CC2.CH08.S01

- [扩展][必须] 决定如何处理错误的输入数据——在所有检测到非法数据的地方选择适当的错误处理方案。 | anchor=CC2.CH08.S01

- [扩展][必须] 在防御式编程之前优先使用迭代式设计、编码前先写伪代码、写代码前先写测试用例、低层设计检查等技术。 | anchor=CC2.CH08.S01


## Assertions

- [核心][必须] 用错误处理代码来处理预期会发生的状况，用断言来处理绝不应该发生的状况。 | anchor=CC2.CH08.S02

- [核心][必须] 用断言来注解并验证前条件和后条件。 | anchor=CC2.CH08.S02

- [核心][禁止] 避免把需要执行的代码放到断言中。 | anchor=CC2.CH08.S02

- [核心][必须] 对于源于系统外部的变量，使用错误处理代码来检查和处理非法数值，而不是断言。 | anchor=CC2.CH08.S02

- [扩展][必须] 对于高健壮性的代码（特别是大型、长期运行的系统），应同时使用断言和错误处理代码来处理同一错误。 | anchor=CC2.CH08.S02

- [扩展][必须] 使用断言检查以下假定：输入/输出参数取值在预期范围内；文件打开/关闭状态；文件读写位置；容器容量；表已初始化；高度优化子程序与缓慢但清晰的子程序的运算结果一致。 | anchor=CC2.CH08.S02

- [核心][必须] 断言为假时必须让程序终止运行，不能养成一碰到已知问题就跳过断言的坏习惯。 | anchor=CC2.CH08.S02


## Error Handling Techniques

- [扩展][必须] 根据应用的安全性和可靠性需求，在十多种可用技术中选择恰当的错误处理方法。 | anchor=CC2.CH08.S03

- [核心][必须] 对于人身安全攸关的应用程序，错误处理应更侧重于正确性——不返回结果也比返回错误的结果好。 | anchor=CC2.CH08.S03

- [核心][必须] 对于消费类应用软件，错误处理应更侧重于健壮性——不断尝试以保证软件可持续运转，哪怕有时做出不够准确的结果。 | anchor=CC2.CH08.S03

- [扩展][必须] 在架构层次上确定一种通用的处理错误参数的方法，并在整个程序里一致地贯彻。 | anchor=CC2.CH08.S03

- [扩展][必须] 检查所有函数的返回值，即使你认定某个函数绝对不会出错。 | anchor=CC2.CH08.S03

- [扩展][必须] 在每个系统调用后检查错误码，除非已确立了一套不对系统调用进行错误检查的架构性指导建议。 | anchor=CC2.CH08.S03

- [核心][必须] 如果高层代码处理错误而低层代码只报告错误，确保高层代码确实检查了低层报告的错误。 | anchor=CC2.CH08.S03

- [扩展][禁止] 在显示出错消息时，不要告诉系统的潜在攻击者太多信息。 | anchor=CC2.CH08.S03

- [扩展][必须] 在输入数据时立即将其转换为恰当的类型。 | anchor=CC2.CH08.S03

## Exceptions

- [核心][必须] 用异常通知程序的其他部分发生了不可忽略的错误。 | anchor=CC2.CH08.S04

- [核心][禁止] 只在真正例外的情况下才抛出异常——即仅在其他编码实践方法无法解决的情况下才使用。 | anchor=CC2.CH08.S04

- [核心][禁止] 不能用异常来推卸责任——如果某种错误情况可以在局部处理，就应该在局部处理掉它。 | anchor=CC2.CH08.S04

- [语言特定][禁止] 避免在构造函数和析构函数中抛出异常，除非在同一地方把它们捕获。 | anchor=CC2.CH08.S04

- [核心][必须] 在恰当的抽象层次上抛出异常——抛出的异常应与子程序接口的抽象层次一致。 | anchor=CC2.CH08.S04

- [扩展][必须] 在异常消息中加入导致异常发生的全部信息。 | anchor=CC2.CH08.S04

- [扩展][禁止] 避免使用空的catch语句。 | anchor=CC2.CH08.S04

- [扩展][必须] 了解所用函数库可能抛出的异常。 | anchor=CC2.CH08.S04

- [扩展][必须] 考虑创建一个集中的异常报告机制。 | anchor=CC2.CH08.S04

- [扩展][必须] 把项目中对异常的使用标准化。 | anchor=CC2.CH08.S04

- [扩展][必须] 考虑异常的替换方案：在局部处理错误、使用错误码、在日志文件中记录调试信息、关闭系统等。 | anchor=CC2.CH08.S04

- [核心][禁止] 把异常当做正常处理逻辑的一部分。 | anchor=CC2.CH08.S04

## Barricades and Security

- [扩展][必须] 把某些接口选定为"安全区域"的边界，对穿越边界的数据进行合法性校验。 | anchor=CC2.CH08.S05

- [扩展][必须] 在类的层次应用隔栏：类的公用方法假设数据不安全并负责检查和清理，类的私用方法假设数据安全。 | anchor=CC2.CH08.S05

- [扩展][必须] 在得到外部数据时立即进行清理，数据往往需要经过一层以上的清理。 | anchor=CC2.CH08.S05

- [核心][必须] 在隔栏外部使用错误处理技术，在隔栏内部使用断言技术。 | anchor=CC2.CH08.S05

- [扩展][必须] 隔栏的位置设定是一个架构层次上的决策。 | anchor=CC2.CH08.S05

## Debugging Aids

- [扩展][禁止] 不要自动地把产品版的限制强加于开发版之上。 | anchor=CC2.CH08.S06

- [扩展][必须] 尽早引入辅助调试的代码。 | anchor=CC2.CH08.S06

- [核心][必须] 采用进攻式编程——在开发阶段让异常情况显现出来，在产品代码运行时让它能自我恢复。 | anchor=CC2.CH08.S06

- [核心][必须] 确保case语句中的default分支或if语句中的else分支在开发阶段产生严重错误（如让程序终止运行），或至少让这些错误不会被忽视。 | anchor=CC2.CH08.S06

- [语言特定][必须] 完全填充分配到的所有内存，以检测内存分配错误。 | anchor=CC2.CH08.S06

- [语言特定][必须] 在删除一个对象之前把它填满垃圾数据，以便检测对已释放内存的引用。 | anchor=CC2.CH08.S06

- [语言特定][必须] 在 Python 中：捕获具体异常类型而非裸 `except:`；使用 `finally` 或 `with`（context manager）确保资源释放；对外部数据使用 `pydantic`/`dataclasses` 做结构化验证而非手工字段检查；永远不要 `eval()`/`exec()` 外部字符串；数据库查询使用参数化而非字符串拼接。 | author=DingYiXing
- [语言特定][必须] 在 Python 中：在生产环境起用 `PYTHONDEVMODE=1`（3.7+）进行开发期检测；使用 `assert` 仅用于不该发生的条件（会被 `-O` 优化掉），安全关键检查用显式 `if/raise`。 | author=DingYiXing

- [语言特定][必须] 在 Go 中：每个可能返回错误的调用必须检查 `err != nil`；使用 `defer` 确保资源释放（`defer f.Close()`）；通过 `recover()` 捕获 panic 避免整个进程崩溃；使用 `go vet` 和 `staticcheck` 作为 lint 补充；对并发代码运行 `go test -race` 检测数据竞争。 | author=DingYiXing
- [语言特定][必须] 在 Go 中：对外部输入使用显式边界检查和类型验证；使用 `html/template` 而非 `text/template` 渲染 HTML 防 XSS；避免裸的 `interface{}` 类型断言——优先用具体类型。 | author=DingYiXing

- [语言特定][必须] 在 Rust 中：利用所有权与借用系统在编译期消除 use-after-free、double-free、数据竞争；使用 `Result<T, E>` 而非 panic 处理可恢复错误；panic 仅用于不可恢复的编程错误；`unsafe` 块应最小化并用注释写明安全不变量。 | author=DingYiXing
- [语言特定][必须] 在 Rust 中：对外部数据优先使用 `serde` 反序列化为强类型结构体并验证字段；整数运算使用 `checked_add`/`saturating_add` 防止溢出；对 C FFI 边界使用 `std::ffi` 和 `unsafe` 隔离层。 | author=DingYiXing

- [语言特定][必须] 在 TypeScript 中：启用 `strict: true`（含 strictNullChecks、noImplicitAny、strictFunctionTypes）；使用 `readonly` 和 `as const` 防止意外修改；对 API 响应使用 zod/io-ts 做运行时校验而非仅靠编译时类型。 | author=DingYiXing
- [语言特定][必须] 在 TypeScript 中：避免 `any` 类型——优先使用 `unknown` 并按需 narrowing；DOM 操作中对用户输入用 `textContent` 而非 `innerHTML`；使用 `eslint-plugin-security` 检测安全隐患。 | author=DingYiXing

- [扩展][必须] 让程序把错误日志文件用电子邮件发给开发人员（如果适用的话）。 | anchor=CC2.CH08.S06

- [扩展][必须] 事先计划好如何移除调试辅助代码，避免调试代码和程序代码纠缠不清。 | anchor=CC2.CH08.S06

- [扩展][必须] 使用版本控制工具和make工具从同一套源码编译出不同版本（开发版包含调试代码，产品版排除调试代码）。 | anchor=CC2.CH08.S06

- [扩展][必须] 使用预处理器或预处理器宏来控制调试代码的编译（如 #define DEBUG 配合 #if defined(DEBUG)）。 | anchor=CC2.CH08.S06

- [扩展][必须] 使用调试存根（debugging stubs）：开发阶段执行完整检查，产品代码中用简单的存根子程序替代。 | anchor=CC2.CH08.S06

## Production Code

- [扩展][必须] 保留那些检查重要错误的代码。 | anchor=CC2.CH08.S07

- [扩展][必须] 去掉检查细微错误的代码——通过版本控制或预处理器开关编译不含此代码的版本。 | anchor=CC2.CH08.S07

- [核心][必须] 从最终软件产品中去掉可以导致程序硬性崩溃的调试代码。 | anchor=CC2.CH08.S07

- [核心][必须] 保留可以让程序稳妥地崩溃的代码。 | anchor=CC2.CH08.S07

- [扩展][必须] 为技术支持人员保留记录错误信息的能力——在产品代码中改变调试代码的工作方式（如把断言改为向日志文件记录信息）。 | anchor=CC2.CH08.S07

- [扩展][必须] 确认留在产品代码中的错误消息对用户是友好的。 | anchor=CC2.CH08.S07

- [扩展][禁止] 出错消息中避免出现有助于攻击者攻入系统所需的信息。 | anchor=CC2.CH08.S07

- [扩展][禁止] 不要在每一个能想到的地方用每一种能想到的方法检查传入的数据。 | anchor=CC2.CH08.S08

- [扩展][必须] 考虑好在什么地方需要进行防御，然后因地制宜地调整防御式编程的优先级。 | anchor=CC2.CH08.S08

- [扩展][禁止] 不应随手编写防御式编程代码。 | anchor=CC2.CH08.S08



# Control Flow Rules

**Scope:** Straight-line code, conditionals, loops, control flow complexity.
**Core:** loop correctness, boundary checks, boolean expression clarity — always apply.
**Extended:** control flow style, table-driven methods, optimization.
**Often used with:** writing.md, quality.md.
**Read Next If:** writing conditionals/loops → writing.md; complex boolean expressions → naming.md.

## Straight-Line Code

- [核心][必须] 当语句之间存在顺序依赖关系时，应组织代码使依赖关系变得明显 | anchor=CC2.CH14.S01
- [核心][必须] 选用能突显依赖关系的子程序名，使子程序名准确反映其全部功能 | anchor=CC2.CH14.S01
- [扩展][禁止] 让一个子程序在完成其主要功能之外还隐式地执行初始化等额外操作 | anchor=CC2.CH14.S01
- [核心][必须] 利用子程序参数在子程序之间传递共享数据，以明确显示顺序依赖关系 | anchor=CC2.CH14.S01
- [核心][必须] 将子程序设计为接收输入数据并返回更新后数据的函数形式，使顺序依赖关系更明显 | anchor=CC2.CH14.S01
- [核心][必须] 优先编写没有顺序依赖关系的代码；其次编写依赖关系明显的代码；最后才用注释文档说明不清晰的依赖关系 | anchor=CC2.CH14.S01
- [核心][必须] 用注释对不清晰的依赖关系进行说明，描述编程意图 | anchor=CC2.CH14.S01
- [核心][必须] 用断言或错误处理代码配合状态变量来检查关键顺序依赖关系 | anchor=CC2.CH14.S01
- [核心][必须] 组织直线型代码的最主要原则是按照依赖关系进行排列 | anchor=CC2.CH14.S01
- [核心][必须] 用好的子程序名、参数列表、注释以及内务管理变量（housekeeping variables）让依赖关系变得明显 | anchor=CC2.CH14.S01
- [扩展][必须] 使代码易于自上而下地阅读，遵循就近原则（Principle of Proximity），将相关操作放在一起 | anchor=CC2.CH14.S02
- [核心][必须] 把处理相同数据、执行相似任务或具有顺序依赖关系的相关语句组织在一起 | anchor=CC2.CH14.S02
- [扩展][必须] 把相对独立的语句组提取成独立的子程序 | anchor=CC2.CH14.S02
- [扩展][必须] 检查子程序中相关语句的组织：打印代码后用方框框出相关语句组，确保各框不交叠 | anchor=CC2.CH14.S02
- [核心][必须] 如果代码之间没有顺序依赖关系，设法使相关的语句尽可能地接近 | anchor=CC2.CH14.S02

## Conditionals

- [核心][必须] 首先写正常代码路径，再处理不常见/异常情况 | anchor=CC2.CH15.S01
- [扩展][必须] 确保条件语句中对等量分支的判断是正确的，避免用">"代替">="或用"<"代替"<=" | anchor=CC2.CH15.S01
- [扩展][必须] 把正常情况的处理放在 if 后面而不要放在 else 后面 | anchor=CC2.CH15.S01
- [扩展][禁止] 编写空的 if 子句 | anchor=CC2.CH15.S01
- [扩展][必须] 即使是简单的 if 语句，也要考虑是否需要 if-then-else 子句 | anchor=CC2.CH15.S01
- [扩展][必须] 当 if 语句不包含 else 子句时，用注释解释为什么 else 子句是不必要的 | anchor=CC2.CH15.S01
- [核心][必须] 测试 else 子句的正确性，不能只测试 if 子句 | anchor=CC2.CH15.S01
- [扩展][必须] 检查 if 和 else 子句是否被弄反了 | anchor=CC2.CH15.S01
- [扩展][必须] 对于简单的 if-else 语句，注意 if 子句和 else 子句的顺序，确认正常的情况是清晰的 | anchor=CC2.CH15.S01
- [核心][必须] 利用布尔函数调用简化复杂的检测条件，将复杂判断封装为布尔函数 | anchor=CC2.CH15.S02
- [扩展][必须] 在 if-then-else 语句串中把最常见的情况放在最前面 | anchor=CC2.CH15.S02
- [核心][必须] 在 if-then-else 语句串中确保所有的情况都考虑到了，使用最后的 else 子句或断言来捕捉未预期的情况 | anchor=CC2.CH15.S02
- [扩展][必须] 如果语言支持，优先使用 case/switch 语句替代 if-then-else 语句串 | anchor=CC2.CH15.S02
- [扩展][必须] 对于 if-then-else 语句串和 case 语句，选择一种最有利于阅读的排序 | anchor=CC2.CH15.S02
- [核心][必须] 为了捕捉错误，使用 case 语句中的 default 子句，或使用 if-then-else 语句串中的最后那个 else 子句 | anchor=CC2.CH15.S02
- [扩展][必须] 为 case 语句选择有效的排列顺序：按字母/数字顺序、把正常情况放在前面、或按执行频率排列 | anchor=CC2.CH15.S03
- [扩展][必须] 简化每种 case 情况对应的操作，使其短小精悍；复杂操作应封装为子程序再调用 | anchor=CC2.CH15.S03
- [扩展][禁止] 为了使用 case 语句而刻意制造一个变量 | anchor=CC2.CH15.S03
- [扩展][必须] 把 default 子句只用于检查真正的默认情况 | anchor=CC2.CH15.S03
- [核心][必须] 利用 default 子句来检测错误，对未预期的值输出诊断消息 | anchor=CC2.CH15.S03
- [核心][必须] 如果 default 子句已用于其他目的，仍应仔细检查每个进入 case 语句的值的合法性，将不合法值交给 default 做错误检测 | anchor=CC2.CH15.S03
- [语言特定][必须] 在 C/C++/Java 中，确保每个 case 子句末尾都有 break，避免代码意外执行越过 case 子句末尾 | anchor=CC2.CH15.S03
- [语言特定][禁止] 在 C/C++/Java 中，避免代码执行路径越过 case 子句末尾的无注释贯穿 | anchor=CC2.CH15.S03
- [语言特定][必须] 在 C/C++/Java 中，如果故意让代码穿越 case 子句末尾，需给出明确注释解释原因 | anchor=CC2.CH15.S03
- [语言特定][必须] 在 Python 3.10+ 中，优先使用 match-case 语句替代长串 if-elif-else；利用模式匹配的值解构和守卫子句简化嵌套判断；match 会自动拒绝贯穿，无需 break。 | author=DingYiXing
- [语言特定][必须] 在 Rust 中，match 表达式必须穷尽所有变体；使用 _ => 作为通配分支；对 Option/Result 类型优先使用 if let / while let 替代单分支 match。 | author=DingYiXing
- [语言特定][必须] 在 Go 中，switch 默认不贯穿（无需 break）；如需贯穿显式使用 fallthrough；switch 可无表达式作为 if-else 链的替代。 | author=DingYiXing
- [语言特定][必须] 在 TypeScript 中，使用 discriminated union 配合 switch 实现穷尽检查——在 default 分支中用 never 类型确保所有变体已处理。 | author=DingYiXing
- [扩展][必须] 为代码的每个部分选用最合适的控制结构 | anchor=CC2.CH15.S01

## Loops

- [扩展][必须] 当预先不知道循环迭代次数时，使用 while 循环 | anchor=CC2.CH16.S01
- [核心][必须] 当循环终止条件自然出现在循环中间时，使用带退出循环（loop-with-exit）以避免半循环（loop-and-a-half）导致的代码重复 | anchor=CC2.CH16.S01
- [扩展][必须] 将带退出循环中的所有退出条件集中放在一处 | anchor=CC2.CH16.S01
- [扩展][必须] 在不直接支持带退出循环的语言中使用 break 模拟时，用注释阐明操作意图 | anchor=CC2.CH16.S01
- [扩展][必须] 当需要执行次数固定的循环时，使用 for 循环 | anchor=CC2.CH16.S01
- [扩展][必须] for 循环应仅用于不需要循环内部控制的简单操作，循环控制应为简单的递增或递减 | anchor=CC2.CH16.S01
- [扩展][必须] 如果存在必须从循环中跳出的条件，应改用 while 循环而非 for 循环 | anchor=CC2.CH16.S01
- [扩展][禁止] 不要在 for 循环中通过直接修改下标值的方式迫使其终止 | anchor=CC2.CH16.S01
- [语言特定][必须] 对数组或其他容器的各项元素执行操作时，使用 foreach 循环或其等价物（C# foreach、Visual Basic For-Each、Python for-in） | anchor=CC2.CH16.S01
- [语言特定][必须] 在 Python 中遍历序列使用 `for item in iterable`；不要使用 `for i in range(len(seq))` 再通过下标访问；需要下标时使用 `enumerate()`；遍历多个序列用 `zip()`；使用生成器表达式和列表推导替代显式 for 循环构建列表。 | author=DingYiXing
- [语言特定][必须] 在 Rust 中，使用 `for item in &collection` 或 `iter()`/`iter_mut()`/`into_iter()` 遍历；优先使用 Iterator 组合器（map/filter/fold/collect）替代手动 for 循环；避免在迭代中修改集合。 | author=DingYiXing
- [语言特定][必须] 在 Go 1.22+ 中，使用 `for _, item := range slice`；遍历 map 时注意迭代顺序不固定；对 channel 使用 `for msg := range ch`；不要用 range 遍历字符串——用 `for _, r := range s` 处理 rune。 | author=DingYiXing
- [语言特定][必须] 在 TypeScript 中，优先使用 `for...of`（而非 `for...in`）遍历可迭代对象；对数组使用 `.forEach()`/`.map()`/.`filter()` 链式方法；对 Map/Set 使用 `.forEach()`。 | author=DingYiXing
- [核心][必须] 当循环至少需要执行一次时，使用在结尾处检测的循环（do-while 或等价结构） | anchor=CC2.CH16.S01
- [扩展][必须] 尽量减少能影响循环的各种因素的数量——简化、简化、再简化 | anchor=CC2.CH16.S02
- [扩展][必须] 将循环内部视为一个黑盒子，把循环控制条件放在循环体外，让外围程序只知其控制条件而不知其内容 | anchor=CC2.CH16.S02
- [扩展][必须] 只从一个位置进入循环——每次从循环头部进入 | anchor=CC2.CH16.S02
- [扩展][必须] 把初始化代码紧放在循环前面 | anchor=CC2.CH16.S02
- [扩展][必须] 用 while(true) 表示无限循环（或在 C++ 中用 for(;;)） | anchor=CC2.CH16.S02
- [扩展][禁止] 不要用 for i = 1 to 99999 这样的代码假造无限循环 | anchor=CC2.CH16.S02
- [扩展][必须] 在适当的情况下多使用 for 循环而非 while 循环 | anchor=CC2.CH16.S02
- [扩展][禁止] 在 while 循环更适用时，不要使用 for 循环 | anchor=CC2.CH16.S02
- [核心][必须] 将 for 循环头保留给循环控制语句——仅放置用于初始化循环、检测循环终止和使循环趋向终止的语句 | anchor=CC2.CH16.S02
- [扩展][必须] 始终使用括号 {} 将循环体括起来 | anchor=CC2.CH16.S02
- [核心][禁止] 避免空循环——不要将循环的工作代码和终止检测代码写在同一行 | anchor=CC2.CH16.S02
- [扩展][必须] 把循环内务操作（housekeeping）要么放在循环的开始，要么放在循环的末尾 | anchor=CC2.CH16.S02
- [核心][必须] 每个循环只做一件事，并且把它做好 | anchor=CC2.CH16.S02
- [扩展][必须] 如果确实需要将两个循环合并以提高效率，先写成两个清晰的循环，加注释说明可合并，等性能测量数据显示瓶颈时再合并 | anchor=CC2.CH16.S02
- [核心][必须] 设法确认循环在所有情况下都能终止——在脑海里模拟执行循环，考虑正常情况、端点情况和每一种异常情况 | anchor=CC2.CH16.S02
- [核心][必须] 使循环终止条件看起来很明显——将所有控制语句集中在一个地方（for 循环头、while 子句或 repeat-until 子句） | anchor=CC2.CH16.S02
- [扩展][禁止] 不要为了终止循环而胡乱改动 for 循环的下标 | anchor=CC2.CH16.S02
- [扩展][禁止] 避免出现依赖于循环下标最终取值的代码 | anchor=CC2.CH16.S02
- [核心][必须] 在关键循环中考虑使用安全计数器（safety counter）确保循环终止 | anchor=CC2.CH16.S02
- [扩展][必须] 考虑在 while 循环中使用 break 语句代替布尔标记来简化循环控制 | anchor=CC2.CH16.S02
- [扩展][禁止] 小心有很多 break 散布其中的循环——大量 break 可能意味着对循环结构缺乏清晰认识 | anchor=CC2.CH16.S02
- [核心][禁止] 避免在循环中错误嵌套 break 导致退出层级错误（如 break 实际退出了 switch 而非预期的循环） | anchor=CC2.CH16.S02
- [扩展][必须] 将 continue 用于循环开始处的条件判断过滤（跳过非目标元素），而非循环中部或末尾 | anchor=CC2.CH16.S02
- [扩展][必须] 如果语言支持，使用带标号的 break（labeled break）明确退出的目标层级 | anchor=CC2.CH16.S02
- [扩展][必须] 使用 break 和 continue 时要保持警惕——如果无法证明使用它们的正当性就不要使用 | anchor=CC2.CH16.S02
- [核心][必须] 检查循环的端点——在创建循环时模拟开始情况、任意选择的中间情况和最终情况，确认不会出现 off-by-one 错误 | anchor=CC2.CH16.S02
- [扩展][必须] 用整数或枚举类型表示数组和循环的边界，不要使用浮点数 | anchor=CC2.CH16.S02
- [扩展][必须] 在嵌套循环中使用有意义的变量名（而非 i、j、k）以提高可读性 | anchor=CC2.CH16.S02
- [扩展][必须] 用有意义的名字避免循环下标串话（cross-talk）——同一循环变量名被用于不同的嵌套层级 | anchor=CC2.CH16.S02
- [扩展][必须] 把循环下标变量的作用域限制在循环内部（在 for 循环内部声明） | anchor=CC2.CH16.S02
- [扩展][必须] 使循环保持简短以便一目了然——理想情况下不超过 15-20 行，最大不超过一屏（约 50 行） | anchor=CC2.CH16.S02
- [扩展][必须] 将循环嵌套限制在 3 层以内 | anchor=CC2.CH16.S02
- [扩展][必须] 把长循环的内容提取为单独的子程序，在循环体内调用 | anchor=CC2.CH16.S02
- [扩展][必须] 长循环要格外清晰——使用单一出口，保持退出条件清晰无误 | anchor=CC2.CH16.S02
- [扩展][必须] 通过"由内而外"的方式构建复杂循环——从具体实例和字面量开始，逐步添加循环包裹并泛化 | anchor=CC2.CH16.S03
- [扩展][必须] 在编写循环代码之前，先用注释写下循环体需要执行的操作步骤 | anchor=CC2.CH16.S03
- [扩展][必须] 在"由内而外"构建循环时，步幅要小，每一步的目的要容易理解 | anchor=CC2.CH16.S03
- [扩展][必须] 在"由内而外"构建循环时，先写具体数据再逐步推广（generalize）为循环下标和表达式 | anchor=CC2.CH16.S03
- [扩展][必须] 先完成循环体的核心逻辑，再在外面加上循环结构，最后添加初始化代码 | anchor=CC2.CH16.S03
- [扩展][必须] 优先使用语言提供的数组/容器批量操作功能（如 APL 数组运算、Fortran 90+ 数组操作），而非手动编写循环 | anchor=CC2.CH16.S04

## Unusual Control Structures

- [核心][必须] 使用防卫子句（guard clause，即早返回/早退出）来简化复杂的错误处理，在执行正常操作前先检查错误条件并为正常执行路径清路 | anchor=CC2.CH17.S01
- [扩展][必须] 减少每个子程序中return的数量，有节制地使用return | anchor=CC2.CH17.S01
- [扩展][必须] 仅在return能增强可读性时才使用return | anchor=CC2.CH17.S01
- [核心][必须] 确认递归子程序中包含一条非递归的路径（停止条件），确保递归能够停止 | anchor=CC2.CH17.S02
- [核心][必须] 在不允许使用简单停止条件测试的环境中，使用安全计数器（safety counter）防止无穷递归 | anchor=CC2.CH17.S02
- [核心][必须] 安全计数器必须是不随每次子程序调用而重新创建的变量（使用类成员变量，或作为参数传递） | anchor=CC2.CH17.S02
- [扩展][必须] 把递归限制在一个子程序内，避免循环递归（A调用B，B调用C，C调用A） | anchor=CC2.CH17.S02
- [核心][必须] 如果无法避免循环递归，则使用安全计数器作为保险策略 | anchor=CC2.CH17.S02
- [核心][必须] 使用递归时需留心栈空间，将安全计数器的上限设置得足够低以防止栈溢出 | anchor=CC2.CH17.S02
- [历史][必须] 在递归函数中，用new在堆（heap）上创建大对象和内存消耗大的对象，不要让编译器在栈（stack）上自动创建 | anchor=CC2.CH17.S02
- [扩展][禁止] 不要用递归去计算阶乘或斐波纳契数列 | anchor=CC2.CH17.S02
- [扩展][必须] 在使用递归之前，先考虑替换方案——用递归能做到的，同样也可以用栈加循环的方式做到 | anchor=CC2.CH17.S02
- [扩展][必须] 在定下来使用递归还是迭代之前，把两者都考虑并比较一下 | anchor=CC2.CH17.S02
- [历史][必须] 在那些不直接支持结构化控制语句的语言里，用goto去模拟那些控制结构，且应准确地模拟，不要滥用goto带来的灵活性 | anchor=CC2.CH17.S03
- [扩展][禁止] 如果语言内置了等价的控制结构，就不要用goto | anchor=CC2.CH17.S03
- [扩展][必须] 如果为提高代码效率而使用goto，必须衡量此举实际带来的性能提升，并加以说明 | anchor=CC2.CH17.S03
- [扩展][必须] 除非在模拟结构化语句，否则每个子程序内最多只使用一个goto标号 | anchor=CC2.CH17.S03
- [扩展][必须] 除非在模拟结构化语句，否则尽量让goto向前跳转，不要向后跳转 | anchor=CC2.CH17.S03
- [扩展][必须] 确认所有的goto标号都被用到了；未使用的标号应删除 | anchor=CC2.CH17.S03
- [扩展][必须] 确认goto不会产生某些执行不到的代码 | anchor=CC2.CH17.S03
- [扩展][必须] 对于那1%使用goto是合理解决方案的罕见情况，在使用的同时予以详细的说明和辩解 | anchor=CC2.CH17.S03
- [扩展][必须] 虚心参考别的程序员提出的不用goto的方法——也许他们发现了被忽视的更好的替代方案 | anchor=CC2.CH17.S03
- [核心][必须] 在错误处理和资源清理场景中，对于支持try-finally的语言，优先使用try-finally来替代goto | anchor=CC2.CH17.S03
- [扩展][必须] 当try-finally不可用时，使用状态变量（state variable）来消除goto，状态变量版本优于嵌套if版本和直接使用goto的版本 | anchor=CC2.CH17.S03
- [历史][必须] 在选择错误处理策略（goto、嵌套if、状态变量、try-finally）后，在整个项目中持续一致地应用所选方法 | anchor=CC2.CH17.S03
- [扩展][必须] 当需要共享else子句中的代码时，将公共代码提取到一个单独的子程序中再在两处调用，而不是使用goto | anchor=CC2.CH17.S03
- [扩展][禁止] 不要使用goto来共享else子句中的代码 | anchor=CC2.CH17.S03
- [历史][必须] 管理层应认识到：对某个goto用法所展开的争论并不是事关全局的；如果程序员知道存在替代方案并且也愿意为使用goto辩护，那么用goto也无妨 | anchor=CC2.CH17.S03
- [扩展][必须] 对非传统的控制结构（如动态计算goto跳转目标、从子程序中部跳转到另一子程序、根据行号调用子程序、应用程序动态生成并执行代码等）持高度怀疑态度 | anchor=CC2.CH17.S04

## Table-Driven Methods

- [扩展][必须] 使用表驱动法替代复杂的逻辑控制结构。当发现程序中存在大量 if/else-if/else 或 case 分支时，考虑使用查询表来简化 | anchor=CC2.CH18.S01
- [扩展][必须] 使用表驱动法替代复杂的继承结构。当继承树关系变得令人困惑时，评估是否可以通过一张查询表来简化设计 | anchor=CC2.CH18.S01
- [扩展][必须] 使用表驱动法时，首先确定如何从表中查询条目：直接访问、索引访问或阶梯访问 | anchor=CC2.CH18.S01
- [扩展][必须] 使用表驱动法时，确定表中存储的内容：存储数据（查询结果为数据）或存储动作（查询结果为动作代码或子程序引用） | anchor=CC2.CH18.S01
- [扩展][必须] 用直接访问表代替长串的 if-else-if 判断。例如用 month 索引的数组代替 12 路的月份判断 | anchor=CC2.CH18.S02
- [扩展][必须] 将多维费率/规则数据存入由所有维度索引的表中，代替多层嵌套的条件判断 | anchor=CC2.CH18.S02
- [扩展][必须] 使用表来描述那些变化太多、无法用硬编码逻辑表示的数据格式。将消息格式的描述放在表中而非程序中 | anchor=CC2.CH18.S02
- [扩展][必须] 当表中需要存储动作而非数据时，使用函数指针（或面向对象语言中的多态对象表）代替 case 语句 | anchor=CC2.CH18.S02
- [扩展][必须] 将表数据存放在外部文件中，在程序运行时读入，以实现不改动程序本身即可调整参数和数据 | anchor=CC2.CH18.S02
- [扩展][必须] 当数据不能直接用作表键值时，通过复制信息使数据能够直接作为键值使用。（例如为 0-17 岁每个年龄复制一份"18岁以下"的费率，使年龄能直接用作下标。这种方式表结构简单，访问操作简单直接）| anchor=CC2.CH18.S02
- [核心][必须] 当数据不能直接用作表键值时，通过转换函数（如 min()/max()）将数据映射为合法的键值。（例如用 max(min(66, age), 17) 将 age 约束到 17-66 区间作为键值，避免了大表或越界访问）| anchor=CC2.CH18.S02
- [扩展][必须] 将键值转换提取成独立的子程序（如 KeyFromAge()），而不是在代码中重复计算 | anchor=CC2.CH18.S02
- [扩展][必须] 当直接键值映射会浪费大量空间时，使用索引访问表。先用基本数据从索引表中查出键值，再用该键值访问主数据表。（索引访问用较小的索引数组替代巨大的主表，显著节省内存（书中示例：索引方案用 30000 字节，直接主表用 1000000 字节））| anchor=CC2.CH18.S03
- [扩展][必须] 将索引访问代码提取成单独的子程序，不要在应用程序中随意散落 | anchor=CC2.CH18.S03
- [扩展][必须] 当数据按范围（而非离散点）归类时，使用阶梯访问表。将每个区间的上限存入表中，通过循环确定所属分类 | anchor=CC2.CH18.S04
- [扩展][必须] 使用阶梯访问表时，仔细确认每个阶梯区间的边界端点，正确处理范围的上下界 | anchor=CC2.CH18.S04
- [扩展][禁止] 在阶梯访问表中误用 < 和 <=。必须明确区分"小于"和"小于等于" | anchor=CC2.CH18.S04
- [核心][必须] 确保阶梯表循环能在找出最高一级区间后恰当终止 | anchor=CC2.CH18.S04
- [扩展][必须] 当阶梯表很大时，考虑用（准）二分查找替代顺序查找以提高性能 | anchor=CC2.CH18.S04
- [扩展][必须] 当执行速度比节省空间更重要时，考虑用索引访问表替代阶梯访问表 | anchor=CC2.CH18.S04
- [扩展][必须] 将阶梯表查询操作提取成单独的子程序 | anchor=CC2.CH18.S04
- [扩展][必须] 考虑将表驱动法作为复杂逻辑的替换方案 | anchor=CC2.CH18.S05
- [扩展][必须] 考虑将表驱动法作为复杂继承结构的替换方案 | anchor=CC2.CH18.S05
- [扩展][必须] 考虑将表数据存储在外部并在运行时读入，以便在不修改代码的情况下改变数据 | anchor=CC2.CH18.S05
- [扩展][必须] 如果无法用简单的数组索引直接访问表，将计算访问键值的功能提取成单独的子程序，不在代码中重复计算 | anchor=CC2.CH18.S05

## Control Issues & Complexity

- [扩展][必须] 在布尔表达式中使用 true 和 false（或语言内置的布尔标识符），而不要使用 1 和 0 等数值。（true/false 语义清晰，1/0 的含义含混（如 1 可能代表"第一份报告"而非"真"），容易混淆和写错）| anchor=CC2.CH19.S01
- [扩展][禁止] 将布尔表达式与 true 或 false 做显式比较。应使用隐式比较，写成 while (!done) 而非 while (done == false) | anchor=CC2.CH19.S01
- [扩展][必须] 拆分复杂的布尔判断，引入新的布尔变量来承载中间结果，使最终判断更简单 | anchor=CC2.CH19.S01
- [扩展][必须] 将需要重复使用或搅乱主流程理解的复杂布尔判断提取成独立的布尔函数 | anchor=CC2.CH19.S01
- [扩展][必须] 当判断涉及多个变量且逻辑复杂时，用决策表（decision-table）代替 if 或 case 语句 | anchor=CC2.CH19.S01
- [扩展][必须] 在 if-else 语句中，将否定形式的条件转换为肯定形式，并互换 if 和 else 子句中的代码 | anchor=CC2.CH19.S01
- [扩展][必须] 使用狄摩根定理（DeMorgan's Theorems）简化否定的布尔判断。将 not A and not B 转换为 not (A or B)，将 not A or not B 转换为 not (A and B) | anchor=CC2.CH19.S01
- [扩展][必须] 用括号使布尔表达式更清晰，不要依赖语言的操作符优先级 | anchor=CC2.CH19.S01
- [扩展][必须] 使用计数技巧检查括号是否配对：从左到右扫描，遇左括号+1，遇右括号-1，最终结果为0表示括号配对 | anchor=CC2.CH19.S01
- [扩展][必须] 将整个布尔表达式括在括号中，作为一种良好的编码习惯 | anchor=CC2.CH19.S01
- [扩展][必须] 理解所用语言中布尔表达式的求值方式（短路求值或完全求值），特别关注第一个判断结果控制第二个判断是否执行的情况 | anchor=CC2.CH19.S01
- [扩展][必须] 使用嵌套的判断语句来明确意图，而不是依赖求值顺序或短路求值行为 | anchor=CC2.CH19.S01
- [扩展][必须] 按照数轴顺序编写数值比较表达式：从左到右、从小到大排列元素 | anchor=CC2.CH19.S01
- [扩展][必须] 在数值比较中，使用显式的 0 比较（写成 while (balance != 0) 而非 while (balance)）。（数值 0 与逻辑 false 语义不同，显式比较区分了数值运算和逻辑运算）| anchor=CC2.CH19.S01
- [扩展][必须] 在 C 语言中，对字符与零终止符的比较使用显式写法（while (*charPtr != '\0') 而非 while (*charPtr)） | anchor=CC2.CH19.S01
- [语言特定][必须] 在 C/C++ 中，对指针使用显式的 NULL 比较（while (bufferPtr != NULL) 而非 while (bufferPtr)） | anchor=CC2.CH19.S01
- [语言特定][禁止] 在 C++ 中滥用 #define 宏替换 &&、|| 和 ==。应当优先打开编译器全部警告来捕获这类错误 | anchor=CC2.CH19.S01
- [语言特定][必须] 在 Java 中，区分 a == b（引用同一性）和 a.equals(b)（值相等）的差异。在判断对象值相等时应使用 a.equals(b) | anchor=CC2.CH19.S01
- [语言特定][必须] 在 Python 中，使用 `is` 判断 None 和单例（`x is None`），使用 `==` 判断值相等；对布尔值使用隐式真值检测（`if items:` 而非 `if len(items) > 0:`）；自定义类定义 `__bool__` 或 `__len__` 来支持真值检测。 | author=DingYiXing
- [语言特定][必须] 在 Rust 中，使用 `==` 比较值（需实现 PartialEq）；使用 `matches!` 宏进行模式匹配布尔检测；对 Option 使用 `.is_some()`/`.is_none()`；对 Result 使用 `.is_ok()`/`.is_err()`。 | author=DingYiXing
- [语言特定][必须] 在 Go 中，使用 `==` 比较基本类型和可比较类型；interface/nil 检查使用显式写法 `if err != nil` 而非简写 `if err`；slice/map/function 只能与 nil 比较。 | author=DingYiXing
- [语言特定][必须] 在 TypeScript 中，使用 `===` 和 `!==`（严格相等），禁止 `==` 和 `!=`；启用 strictNullChecks 后使用 `??`（空值合并）和 `?.`（可选链）简化空值判断。 | author=DingYiXing
- [扩展][必须] 先写出块结构的开始和结束部分（括号对），再填充中间内容 | anchor=CC2.CH19.S02
- [扩展][必须] 始终使用括号/块来清晰地表达条件语句的范围，即使块内只有一条语句 | anchor=CC2.CH19.S02
- [扩展][必须] 突出显示空语句的存在：将空语句的分号单独放在一行并适当缩进，或使用空括号 {} 来强调 | anchor=CC2.CH19.S03
- [扩展][必须] 创建 DoNothing() 预处理宏或内联函数来替代裸空语句，明确表达"此处有意不做任何操作"的意图 | anchor=CC2.CH19.S03
- [扩展][禁止] 编写超过 3-4 层嵌套深度的 if 语句。（研究表明很少有人能理解超过 3 层 if 嵌套，深层嵌套与"管理复杂度"这一首要技术使命相违背）| anchor=CC2.CH19.S04
- [核心][必须] 当出现深层嵌套时，通过重复检测部分条件来减少嵌套层次。（虽然重复条件使判断变复杂，但将嵌套从 4 层减到 2 层是很大的改进，利远大于弊）| anchor=CC2.CH19.S04
- [扩展][必须] 将嵌套的 if 语句转换为一组 if-then-else 语句（else if 链） | anchor=CC2.CH19.S04
- [扩展][必须] 将嵌套的 if 语句转换为 case/switch 语句 | anchor=CC2.CH19.S04
- [扩展][必须] 将深层嵌套的代码抽取出来放进单独的子程序 | anchor=CC2.CH19.S04
- [扩展][必须] 在面向对象环境中，使用多态派分（polymorphic dispatch）替代嵌套的条件逻辑 | anchor=CC2.CH19.S04
- [扩展][必须] 重新设计深层嵌套的代码。深层嵌套表明你尚未充分理解程序，无法将其简化。如果决定不修改，必须给出充分的理由 | anchor=CC2.CH19.S04
- [核心][必须] 使用单入单出（单一入口、单一出口）的控制结构：顺序、选择和迭代 | anchor=CC2.CH19.S05
- [扩展][禁止] 随意使用标准结构化控制结构（顺序、选择、迭代）之外的 break、continue、return、throw-catch 等控制结构 | anchor=CC2.CH19.S05
- [扩展][必须] 确保子程序的决策点数量控制在 0-5 个。6-10 个时需要设法简化。超过 10 个时，必须将子程序的一部分拆分为另一个子程序 | anchor=CC2.CH19.S06
- [扩展][必须] 拆分子程序以降低单个子程序的决策点数量，即降低在同一时间必须关注的复杂度水平。（人的大脑难以同时处理超过 5-9 个智力实体，降低给定子程序的复杂度有助于理解）| anchor=CC2.CH19.S06
- [扩展][禁止] 盲目拆解 case 语句中超过 10 个元素的情况。是否拆分取决于具体场景 | anchor=CC2.CH19.S06

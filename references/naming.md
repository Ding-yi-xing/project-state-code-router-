# Naming Rules

**Scope:** Variable, function, class, type, and constant naming conventions.
**Core:** identifier clarity — names must accurately describe what they represent.
**Extended:** naming conventions, prefixes, length guidelines.
**Often used with:** layout.md, design.md.
**Read Next If:** defining types/classes → design.md; project naming conventions in architecture context → architecture-layers.md.

- [核心][必须] 变量名要完全、准确地描述出该变量所代表的事物 | anchor=CC2.CH11.S01
- [核心][禁止] 使用x、x1、x2等无意义名字作为变量名（传统上用x代表一个未知量；如果不希望变量代表的是未知量，请考虑取更好的名字。即使知道x代表什么，也无法获知x1和x2之间的关系）| anchor=CC2.CH11.S01
- [扩展][禁止] 使用像cd、c这样太短且不具有描述性的名字 | anchor=CC2.CH11.S01
- [扩展][禁止] 使用含义不完整的名词（如date而未指明"当前日期"） | anchor=CC2.CH11.S01
- [扩展][必须] 名字应该尽可能地明确，避免泛泛得可以用于多种目的的名字（如x、temp、i） | anchor=CC2.CH11.S01
- [扩展][必须] 变量名应反映问题（what）而非解决方案（how），以问题为导向 | anchor=CC2.CH11.S01
- [扩展][必须] 变量名长度应控制在8到20个字符之间，平均10到16个字符时调试最省力（太短的名字无法传达足够的信息；太长的名字很难写，同时也会使程序的视觉结构变得模糊不清。Gorla、Benander和Benander的研究发现，当变量名平均长度在10到16个字符时，调试所需气力最小）| anchor=CC2.CH11.S01
- [扩展][必须] 短变量名适用于局部变量或循环变量（作用域很小），长名字适用于很少用到的变量或全局变量 | anchor=CC2.CH11.S01
- [扩展][必须] 对位于全局命名空间中的名字加以限定词（通过namespace、package或命名前缀如uiEmployee、dbEmployee） | anchor=CC2.CH11.S01
- [扩展][必须] 把计算值限定词（如Total、Average、Max、Min、Sum）加到名字的最后 | anchor=CC2.CH11.S01
- [扩展][禁止] 混用Num在变量名不同位置表示不同含义 | anchor=CC2.CH11.S01
- [扩展][必须] 准确使用常用对仗词：begin/end、first/last、locked/unlocked、min/max、next/previous、old/new、opened/closed、visible/invisible、source/target、source/destination、up/down | anchor=CC2.CH11.S01
### 11.2 为特定类型的数据命名

- [扩展][必须] 简单循环中，循环下标可以使用约定俗成的i、j、k | anchor=CC2.CH11.S02
- [扩展][必须] 如果循环变量要在循环之外使用，就应该为它取一个比i、j、k更有意义的名字（如recordCount） | anchor=CC2.CH11.S02
- [扩展][必须] 如果循环长度超过几行，给循环下标换一个更有意义的名字 | anchor=CC2.CH11.S02
- [扩展][必须] 嵌套循环中给循环变量赋予更长、更有意义的名字（如teamIndex、eventIndex） | anchor=CC2.CH11.S02
- [扩展][禁止] 将i、j、k用于简单循环下标之外的任何场合 | anchor=CC2.CH11.S02

- [扩展][禁止] 在标记的名字中使用flag | anchor=CC2.CH11.S02
- [扩展][必须] 状态变量应该用枚举类型、具名常量或用作具名常量的全局变量来对其赋值，其值应与它们做比较（像statusFlag=0x80这样的语句反映不出代码能做什么，除非你亲自写了这段代码或有文档告诉你含义。if (dataReady) 比 if (flag) 更有意义；if (reportType == ReportType_Annual) 比 if (printFlag == 16) 更为清晰）| anchor=CC2.CH11.S02
- [扩展][必须] 如果发现自己需要猜测某段代码的含义，就该考虑为变量重新命名 | anchor=CC2.CH11.S02

- [扩展][禁止] 使用temp、x或其他模糊且缺乏描述性的名字为临时变量命名 | anchor=CC2.CH11.S02
- [扩展][必须] 为存储中间结果的变量赋予准确且具有描述性的名字（如用discriminant代替temp存储判别式结果） | anchor=CC2.CH11.S02
- [扩展][必须] 警惕"临时"变量——程序中的大多数变量都是临时性的，把其中几个称为临时的可能表明你还没有弄清它们的实际用途 | anchor=CC2.CH11.S02

- [核心][必须] 使用典型的布尔变量名：done（表示完成）、error（表示错误）、found（表示找到）、success或ok（表示成功） | anchor=CC2.CH11.S02
- [扩展][必须] 如果可以，用更具体的名字代替success：如processingComplete（处理完成即成功）、found（找到值即成功） | anchor=CC2.CH11.S02
- [扩展][必须] 给布尔变量赋予隐含"真/假"含义的名字 | anchor=CC2.CH11.S02
- [扩展][禁止] 使用像status或sourceFile这样没有明确true/false含义的名字作为布尔变量名 | anchor=CC2.CH11.S02
- [扩展][必须] 把status替换为error或statusOK，把sourceFile替换为sourceFileAvailable或sourceFileFound等能体现变量含义的名字 | anchor=CC2.CH11.S02
- [扩展][必须] 使用肯定的布尔变量名 | anchor=CC2.CH11.S02

- [扩展][必须] 使用组前缀（如Color_、Planet_、Month_）来明确表示枚举类型的成员都同属于一个组 | anchor=CC2.CH11.S02
- [扩展][必须] 在支持命名空间的语言中，如果枚举成员已被冠以枚举名前缀（如Color.Color_Red），则可以简化为Color.Red | anchor=CC2.CH11.S02

- [扩展][必须] 具名常量应根据该常量所表示的含义（抽象事物），而不是该常量所具有的数值来命名（FIVE是个很糟的常量名（不论其所代表的值是否为5.0）。CYCLES_NEEDED可以等于5.0或6.0，是个不错的名字，而FIVE=6.0就显得太可笑了。BAKERS_DOZEN很不错，DONUTS_MAX也不错）| anchor=CC2.CH11.S02
### 11.3 命名规则的力量
- [扩展][必须] 采用任何一项命名规则都好于没有规则 | anchor=CC2.CH11.S03
- [扩展][必须] 在以下任一情况下建立命名规则：多个程序员合作开发一个项目时；计划把程序转交给另一位程序员修改和维护时；组织中的其他程序员评估你写的程序时；程序规模太大以致于无法在脑海里同时了解事情全貌而必须分而治之时；程序生命期足够长，长到可能在搁置几个星期或几个月之后又重新启动时；项目中存在不常见术语且希望在编写代码阶段使用标准术语或缩写时 | anchor=CC2.CH11.S03
- [扩展][必须] 命名规则的正式程度取决于为同一程序而工作的人员数量、程序的规模以及程序预期的生命期 | anchor=CC2.CH11.S03
### 11.4 非正式命名规则

- [扩展][必须] 区分变量名和子程序名字：变量名以小写字母开始，子程序名字以大写字母开始（variableName vs RoutineName()） | anchor=CC2.CH11.S04
- [扩展][必须] 区分类和对象/类型和变量。可选方案：通过大写字母开头区分（Widget widget）、通过全部大写区分（WIDGET widget）、通过给类型加t_前缀区分（t_Widget widget）、通过给变量加a_前缀区分（Widget aWidget）、通过对变量采用更明确的名字区分（Widget employeeWidget） | anchor=CC2.CH11.S04
- [历史][必须] 在所有全局变量名前加上g_前缀 | anchor=CC2.CH11.S04
- [历史][必须] 用m_前缀标识类的成员变量 | anchor=CC2.CH11.S04
- [历史][必须] 为类型名增加t_前缀（如t_Color、t_Menu）或采用全部大写来标识类型声明 | anchor=CC2.CH11.S04
- [历史][必须] 给具名常量增加c_前缀（如c_LinesPerPageMax、c_RecsMax），或全部用大写并用下划线分隔单词（如RECS_MAX、LINES_PER_PAGE_MAX） | anchor=CC2.CH11.S04
- [扩展][必须] 标识枚举类型的元素：全部用大写，或者为类型名增加e_或E_前缀，同时为该类型成员名增加基于特定类型的前缀（如Color_Red、Planet_Earth） | anchor=CC2.CH11.S04
- [扩展][必须] 在不能保证输入参数只读的语言里，通过命名约定标识只读参数（如增加const或final前缀） | anchor=CC2.CH11.S04
- [扩展][必须] 格式化命名以提高可读性：用大小写和分隔符（下划线）来分隔单词（如gymnasticsPointTotal或gymnastics_point_total） | anchor=CC2.CH11.S04
- [扩展][禁止] 混用大小写和下划线两种分隔方法 | anchor=CC2.CH11.S04

- [扩展][必须] 遵循你所用语言的命名规则和风格约定 | anchor=CC2.CH11.S04
- [语言特定][必须] C语言：c和ch是字符变量；i和j是整数下标；n表示某物的数量；p是指针；s是字符串；预处理宏全部大写（ALL_CAPS）；变量名和子程序名全部小写（all_lowercase）；下划线用做分隔符（letters_in_lowercase） | anchor=CC2.CH11.S04
- [语言特定][必须] C++语言：i和j是整数下标；p是指针；常量、typedef和预处理宏全部大写（ALL_CAPS）；类和其他类型的名字混合大小写（首字母大写）；变量名和函数名第一个单词小写后续单词首字母大写；不把下划线用做名字中的分隔符，除非用于全部大写的名字以及特定的前缀中（如g_前缀） | anchor=CC2.CH11.S04
- [扩展][必须] Java语言：i和j是整数下标；常量全部大写并用下划线分隔；类名和接口名混合大小写首字母大写（ClassOrInterfaceName）；变量名和方法名第一个单词首字母小写后续单词首字母大写；除全部大写的名字外不使用下划线作为分隔符；访问器子程序使用get和set前缀 | anchor=CC2.CH11.S04
- [扩展][必须] 在混合语言编程环境中，对命名规则做出优化以提高整体一致性和可读性——即使这意味着优化后的规则会与其中某种语言所用的规则相冲突 | anchor=CC2.CH11.S04
- [扩展][必须] 变量名应包含三类信息：变量的内容（它代表什么）、数据的种类（具名常量、简单变量、用户自定义类型或类）、变量的作用域（私用的、类的、包的或者全局的） | anchor=CC2.CH11.S04

- [语言特定][必须] C++/Java：类名混合使用大小写且首字母大写（ClassName） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：类型定义（包括枚举和typedef）混合使用大小写且首字母大写（TypeName） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：枚举类型以复数形式表示 | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：局部变量混合使用大小写且首字母小写，名字与底层数据类型无关且反映变量所代表的事物（localVariable） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：子程序参数的格式与局部变量相同（routineParameter） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：子程序名混合使用大小写（RoutineName()） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：只对类内多个子程序可见的成员变量用m_前缀（m_classVariable） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：全局变量名用g_前缀（g_GlobalVariable） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：具名常量全部大写（CONSTANT） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：宏全部大写（MACRO） | anchor=CC2.CH11.S04
- [语言特定][必须] C++/Java：枚举类型名用能够反映其基础类型的、单数形式的前缀（Base_EnumeratedType），如Color_Red、Color_Blue | anchor=CC2.CH11.S04

- [语言特定][必须] C：类型名混合使用大小写且首字母大写（TypeName） | anchor=CC2.CH11.S04
- [语言特定][必须] C：公用子程序名混合使用大小写（GlobalRoutineName()） | anchor=CC2.CH11.S04
- [语言特定][必须] C：单一模块（文件）私用的子程序名用f_前缀（f_FileRoutineName()） | anchor=CC2.CH11.S04
- [语言特定][必须] C：模块（文件）变量名用f_前缀（f_Filestaticvariable） | anchor=CC2.CH11.S04
- [语言特定][必须] C：全局变量名以G_前缀加上反映定义该变量模块的、全部大写的名字开始（G_GLOBAL_GlobalVariable），如G_SCREEN_Dimensions | anchor=CC2.CH11.S04
- [语言特定][必须] C：单一子程序或模块（文件）私用的具名常量全部大写（LOCAL_CONSTANT），如ROWS_MAX | anchor=CC2.CH11.S04
- [语言特定][必须] C：全局具名常量名全部大写，以G_前缀和反映定义该具名常量模块的、全部大写的名字开始（G_GLOBALCONSTANT），如G_SCREEN_ROWS_MAX | anchor=CC2.CH11.S04
- [语言特定][必须] C：单一子程序或模块（文件）私用的宏定义全部大写（LOCALMACRO()） | anchor=CC2.CH11.S04
- [语言特定][必须] C：全局宏定义全部大写，以G_前缀和反映定义该宏模块的、全部大写的名字开始（G_GLOBALMACRO()），如G_SCREEN_LOCATION() | anchor=CC2.CH11.S04

- [语言特定][必须] Visual Basic：类名混合使用大小写且首字母大写，加C_前缀（C_ClassName） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：类型定义（包括枚举和typedef）混合使用大小写且首字母大写，加T_前缀（T_TypeName） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：枚举类型以复数形式表示（T_EnumeratedTypes） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：局部变量混合使用大小写且首字母小写，名字与底层数据类型无关且反映变量所代表的事物（localVariable） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：子程序参数格式与局部变量相同（routineParameter） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：子程序名混合使用大小写（RoutineName()） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：全局变量名以g_前缀开始（g_GlobalVariable） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：具名常量全部大写（CONSTANT） | anchor=CC2.CH11.S04
- [语言特定][必须] Visual Basic：枚举类型名以反映其基础类型的、单数形式的前缀开始（Base_EnumeratedType），如Color_Red、Color_Blue | anchor=CC2.CH11.S04

- [语言特定][必须] Python：类名和异常名用 PascalCase（ClassName）；函数名、方法名、变量名用 snake_case（function_name, my_var）；常量用 UPPER_SNAKE_CASE（MAX_SIZE）；模块名用 short_lowercase；包名用 shortlowercase；私有成员以单下划线前缀（_private_method）；内部私有以双下划线前缀（__internal）；避免与 Python 内置名冲突。遵循 PEP 8。 | author=DingYiXing
- [语言特定][必须] Python：布尔变量名使用 is_ 或 has_ 前缀（is_valid、has_items）；访问器使用普通名词（size）而非 get/set（get_size → 用 @property）。 | author=DingYiXing

- [语言特定][必须] Go：导出标识符首字母大写（PublicFunction、ExportedType）；非导出标识符首字母小写（privateFunc、internalVar）；包名使用小写单数短词、不使用下划线（httputil 不是 http_util）；常量用 PascalCase 或全大写；接口名通常以 -er 结尾（Reader、Writer）；避免使用 this、self、me 作为接收者名——使用类型首字母缩写（如 c 用于 Client，s 用于 Server）。遵循 Effective Go。 | author=DingYiXing
- [语言特定][必须] Go：仅方法的接收者变量允许使用单字母名（如 c *Client）；获取器不要加 Get 前缀（Size() 而非 GetSize()）；错误变量名为 err，不另起名。 | author=DingYiXing

- [语言特定][必须] Rust：类型名、trait 名、枚举变体用 PascalCase（TypeName、TraitName）；变量名、函数名、方法名用 snake_case（variable_name、fn do_something()）；常量、静态变量用 UPPER_SNAKE_CASE（MAX_SIZE）；宏名用 snake_case 或 PascalCase；模块名用 snake_case。遵循 Rust RFC 430。 | author=DingYiXing
- [语言特定][必须] Rust：构造器默认命名为 new()；转换方法以 from_/into_/to_/as_ 前缀（from_utf8()、to_string()、as_bytes()）；布尔函数用 is_/has_ 前缀（is_empty()）；析构/移除用 drop/remove/clear/take；不要使用 get_ 前缀除非返回 Option<T>（如 get(key) → Option<&V>）。 | author=DingYiXing

- [语言特定][必须] TypeScript：类名、接口名、类型别名、枚举名用 PascalCase（ClassName、IUser 或 User）；变量名、函数名、方法名、属性名用 camelCase（localVariable、doSomething()）；常量用 UPPER_SNAKE_CASE 或 camelCase（团队统一即可）；枚举成员用 PascalCase（Color.Red）；私有成员不使用下划线前缀（用 private 关键字）。 | author=DingYiXing
- [语言特定][必须] TypeScript：布尔变量以 is/has/should/can 开头（isActive、hasPermission）；数组变量名用复数或带 List 后缀（users 或 userList）；回调/事件处理函数以 on/handle 前缀（onClick、handleSubmit）；类型守卫函数以 is 前缀（isString(x)）。 | author=DingYiXing

### 11.5 标准前缀
- [扩展][必须] 对具有通用含义的前缀标准化 | anchor=CC2.CH11.S05
- [扩展][必须] 使用用户自定义类型（UDT）缩写来标识被命名对象或变量的数据类型 | anchor=CC2.CH11.S05
- [扩展][必须] 为项目环境中最常用的UDT创建标准的UDT缩写 | anchor=CC2.CH11.S05
- [扩展][必须] 使用语义前缀描述变量或对象是如何使用的：c（count，数量）、first（当前操作中第一个元素）、g（global，全局变量）、i（index，数组下标）、last（当前操作中最后一个元素）、lim（数组上限，非合法下标，lim=last+1）、m（class-level，类一级变量）、max（数组中绝对最后一个元素）、min（数组中绝对第一个元素）、p（pointer，指针） | anchor=CC2.CH11.S05
- [扩展][禁止] 在使用语义前缀的同时忽略给变量起有意义的名字 | anchor=CC2.CH11.S05
### 11.6 创建具备可读性的短名字
- [扩展][必须] 在现代语言（C++、Java、Visual Basic）中创建足够长的名字，几乎没有任何理由去缩短具有丰富含义的名字 | anchor=CC2.CH11.S06

- [扩展][必须] 如果必须创建短名字，应使用以下缩写策略：使用标准的缩写（字典中的常见缩写）；去掉所有非前置元音（computer→cmptr）；去掉虚词；使用每个单词的第一个或前几个字母；统一地在每个单词的第一、第二或第三个字母后截断；保留每个单词的第一个和最后一个字母；使用名字中的每一个重要单词最多不超过三个；去除无用的后缀；保留每个音节中最引人注意的发音；确保不改变变量的含义（有些缩短名字的方法要好于其他方法。熟悉多种缩写技巧很有用，因为没有哪种方法适用于所有情况。反复使用上述技术直到变量名长度缩减到8到20个字符或达到语言限制字符数）| anchor=CC2.CH11.S06
- [扩展][禁止] 使用语音缩写（如sk8ing代替skating、b4代替before、xqt代替execute、hilite代替highlight） | anchor=CC2.CH11.S06
- [扩展][禁止] 不要用从每个单词中删除一个字符的方式来缩写 | anchor=CC2.CH11.S06
- [扩展][必须] 缩写要一致：全用Num或全用No，不要在有些地方使用完整单词而在其他地方使用缩写 | anchor=CC2.CH11.S06
- [扩展][必须] 创建能读出来的名字（用xPos而不用xPstn，用needsCompu而不用ndsCmptg） | anchor=CC2.CH11.S06
- [扩展][必须] 避免使用容易看错或读错的字符组合（如ENDB要比BEND更好） | anchor=CC2.CH11.S06
- [扩展][必须] 使用辞典（同义词）来解决缩写后命名冲突 | anchor=CC2.CH11.S06
- [扩展][必须] 当编程语言只允许用非常短的名字时，在代码里增加一张缩写对照表作为注释，解释极短名字的含义 | anchor=CC2.CH11.S06
- [扩展][必须] 在一份项目级的"标准缩写"文档中记录项目中用到的全部编码缩写，该文档应签入（check in）到版本控制系统（解决两个常见风险：(1)代码读者可能不理解这些缩写；(2)其他程序员可能用多个缩写代表相同的词。文档中的词条应按完整单词排序而非缩写排序。只有当缩写应用非常广泛、程序员不惜花精力编写缩写文档时，该缩写才应当被创建。只有先check out标准缩写文档、输入新缩写并check in回去，才能创建新缩写。这种方法降低程序员创建多余缩写的可能性）| anchor=CC2.CH11.S06
- [扩展][必须] 名字应更侧重于阅读方便而不是编写方便 | anchor=CC2.CH11.S06
### 11.7 应该避免的名字
- [核心][禁止] 避免使用令人误解的名字或缩写 | anchor=CC2.CH11.S07
- [扩展][禁止] 避免使用具有相似含义的名字 | anchor=CC2.CH11.S07
- [扩展][禁止] 避免使用具有不同含义但却有相似名字的变量 | anchor=CC2.CH11.S07
- [扩展][禁止] 避免使用发音相近的名字（如wrap和rap） | anchor=CC2.CH11.S07
- [扩展][禁止] 避免在名字中使用数字（如file1和file2、total1和total2）（如果名字中的数字真的非常重要，请使用数组代替一组单个变量。如果数组不合适，那么数字就更不合适。几乎总能想出比在名字最后加1或2更好的区分方法）| anchor=CC2.CH11.S07
- [扩展][禁止] 避免在名字中拼错单词（如把highlight错拼为hilite） | anchor=CC2.CH11.S07
- [扩展][禁止] 避免使用英语中常常拼错的单词（如absense, acummulate, acsend, calender, concieve, defferred, definate, independance, occassionally, prefered, reciept, superseed等） | anchor=CC2.CH11.S07
- [扩展][禁止] 不要仅靠大小写来区分变量名（如frd、FRD、Frd分别代表不同含义） | anchor=CC2.CH11.S07
- [扩展][禁止] 避免使用多种自然语言 | anchor=CC2.CH11.S07
- [扩展][禁止] 避免使用标准类型、变量和子程序的保留名或预定义名 | anchor=CC2.CH11.S07
- [扩展][禁止] 不要使用与变量含义完全无关的名字（如男朋友名字、妻子名字、最喜欢的啤酒名字，或其他自作聪明的名字） | anchor=CC2.CH11.S07
- [扩展][禁止] 避免在名字中包含易混淆的字符（有些字符看上去非常接近，很难区分。易混淆对包括：1（数字1）和l（小写字母L）；1和I（大写字母i）；.和,；0（零）和O（大写字母o）；2和Z；;和:；S和5；G和6。历史上曾因Fortran FORMAT语句中句号错写成逗号，导致科学家算错太空飞船轨道，造成太空探测器丢失——损失高达16亿美元）| anchor=CC2.CH11.S07


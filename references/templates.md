# Code Templates

**Scope:** Reusable patterns for files, functions, tests.
**Core:** — this file is entirely selection guidance.
**Extended:** template selection criteria — when to use each template.
**Often used with:** layout.md, quality.md, naming.md.
**Read Next If:** creating new files → layout.md; writing functions / tests → quality.md; naming the new symbol → naming.md.

## Quick Selection Guide

| You're creating | Use template | Condition |
|---|---|---|
| A new .py file | file-header | Multi-file project |
| A new non-trivial class | class | Skip for @dataclass/namedtuple |
| A new public or >30-line function | large-function-header | Public API or complex logic |
| A private helper or <15-line function | small-function-header | Needs doc but small |
| A new unit test | test-naming + test-aaa | Always use AAA structure |
| Many equivalent test cases | test-parametrized | Pure function, many I/O pairs |

## module — Module Docstring

**Use When:** Creating a new Python module (.py file).
**Must Include:** One-line summary, Dependencies, Inputs, Outputs.
**May Omit:** Extended description, Boundaries.
**Do Not Use When:** File is a trivial entry-point script with zero imports.

```python
"""<一句话概述模块职责>.

<扩展描述，可选>。

Boundaries:
    <模块负责的边界，不负责的内容>。

Dependencies:
    - <外部依赖 1>
    - <外部依赖 2>

Inputs:
    <模块接收的输入数据流或配置>。

Outputs:
    <模块产出的输出数据流或副作用>。
"""
```

## class — Class Docstring

**Use When:** Defining any non-trivial class or data structure.
**Must Include:** One-line summary, Invariants.
**May Omit:** Extended description, Collaborators, Lifecycle.
**Do Not Use When:** Class is a plain data holder (use @dataclass or namedtuple).

```python
class MyClass:
    """<一句话概述类抽象>.

    <扩展描述，可选>。

    Invariants:
        <始终为真的约束条件>。

    Collaborators:
        - <协作类 1>
        - <协作类 2>

    Lifecycle:
        <创建 → 使用 → 销毁的关键阶段>。
    """
```

## function — Function Docstring

**Use When:** Writing a public function or any function with non-obvious behavior.
**Must Include:** One-line summary, Args, Returns.
**May Omit:** Extended description, Raises, Side Effects, Preconditions.
**Do Not Use When:** Function body is a one-liner that self-documents.

```python
def my_func(param1, param2):
    """<一句话概述函数目的>.

    <扩展描述，可选>。

    Args:
        param1 (Type): <参数说明>.
        param2 (Type): <参数说明>.

    Returns:
        Type: <返回值说明；无返回值时写 None>。

    Raises:
        ErrorType: <在什么条件下抛出此异常>.

    Side Effects:
        <修改全局状态、写入文件、发送网络请求等>.

    Preconditions:
        <调用前必须满足的条件>.
    """
```

## file-header — File Header Block

**Use When:** Creating a new source file in a multi-file project.
**Must Include:** FILE, BRIEF.
**May Omit:** MODULE, FUNCTIONS list, DEPENDS.
**Do Not Use When:** Project convention uses a simpler header or the file is a single-use script.

```
# //////////////////////////////////////////////////////////////////////////////
# //  FILE:    <filename.ext>
# //  MODULE:  <parent_package.module_name>
# //  BRIEF:   <一句话概述本文件职责>
# //
# //  FUNCTIONS:
# //    <function_name_1>  — <一句话功能>
# //    <function_name_2>  — <一句话功能>
# //
# //  DEPENDS: <外部包/模块列表，逗号分隔>
# //////////////////////////////////////////////////////////////////////////////
```

## large-function-header — Public Function Header Block

**Use When:** Writing a public API function or a function longer than ~30 lines.
**Must Include:** NAME, PURPOSE, INPUT (all params), OUTPUT.
**May Omit:** SIDE-FX (when none), RAISES (when none).
**Do Not Use When:** Function is small (<15 lines), private, or self-documenting.

```
# ==============================================================================
# NAME:      <function_name>
# PURPOSE:   <一句话概述函数目的>
# INPUT:     <param1> | <type1> | <说明>
#            <param2> | <type2> | <说明>
# OUTPUT:    <return_type> — <返回值说明；无返回值写 None>
# SIDE-FX:   <副作用说明；无副作用写 "none">
# RAISES:    <ExceptionType> — <在什么条件下抛出；不抛异常写 "none">
# ==============================================================================
```

- INPUT 每行一个参数，三个信息用 ` | ` 分隔，按输入→修改→输出顺序排列。
- OUTPUT 若返回结构复杂，分行列出各字段含义。
- SIDE-FX 含修改全局状态、写文件、发网络请求、打印输出等。不遗漏。
- RAISES 只列调用方应感知的异常，不列内部实现抛出的异常。

## small-function-header — Compact Function Header

**Use When:** Writing a private helper or small (<15 lines) function that still needs documentation.
**Must Include:** Function name, one-line purpose, return type.
**May Omit:** Parameter type annotations (if obvious), parameter names (if >80 chars).
**Do Not Use When:** Function is public API or has complex semantics — use large-function-header.

```
# --- <function_name> --- <一句话功能>. IN: (<param1>: <type1>, ...). OUT: <return_type> — <说明>. ---
```

- 单行内完成，不换行。若参数列表过长（>80 字符），可省略为类型名省略参数名。

## test-naming — Test Function Naming

**Use When:** Writing any test function.
**Must Include:** test_ prefix, unit under test, scenario.
**May Omit:** Expected result (when testing for exceptions with pytest.raises).
**Do Not Use When:** Using a test framework with incompatible naming rules.

```
# test_<被测单元>_<场景>_<预期结果>
def test_process_orders_empty_input_raises_value_error():
    ...

def test_process_orders_single_valid_row_returns_one_record():
    ...

def test_process_orders_invalid_email_reports_error():
    ...
```

## test-aaa — AAA Test Structure

**Use When:** Writing unit tests for deterministic functions or methods.
**Must Include:** Arrange, Act, Assert sections with blank-line separation.
**May Omit:** Comments labeling sections (when sections are trivially distinguishable).
**Do Not Use When:** Testing async code, stateful integrations, or non-deterministic behavior.

```python
def test_<unit>_<scenario>_<expected>():
    # -- Arrange: 准备被测对象和输入数据 --
    input_data = ...
    expected = ...

    # -- Act: 执行被测行为 --
    result = some_function(input_data)

    # -- Assert: 验证结果与预期一致 --
    assert result == expected
```

- AAA 三步不合并，空行分隔，断言不引入第三方框架。

## test-parametrized — Parameterized Test

**Use When:** Testing a pure function with many equivalent input/output pairs.
**Must Include:** Parametrize decorator, case comments labeling category (边界/正常/异常), fail-fast first case.
**May Omit:** Exhaustive edge cases (use a separate property-based test).
**Do Not Use When:** Test logic branches significantly per case — use separate test functions.

```python
@pytest.mark.parametrize("input_val, expected", [
    (None,             ValueError),     # 边界：None
    ("",               ValueError),     # 边界：空字符串
    ("a@b.c",          True),           # 正常：最小有效
    ("a"*100 + "@b.c", True),           # 边界：长 local-part
])
def test_validate_email(input_val, expected):
    if expected is ValueError:
        with pytest.raises(ValueError):
            validate_email(input_val)
    else:
        assert validate_email(input_val) == expected
```

- 参数化列表中每条 case 注释说明覆盖的测试类别（边界/正常/异常）。
- 第一个 case 通常放最常触发的错误路径。

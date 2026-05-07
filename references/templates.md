# Code Templates

**Scope:** Reusable patterns for files, functions, tests.
**Core:** 鈥?this file is entirely selection guidance.
**Extended:** template selection criteria 鈥?when to use each template.
**Often used with:** writing.md, quality.md, layout.md.
**Read Next If:** creating new files 鈫?layout.md; writing functions 鈫?writing.md; writing tests 鈫?quality.md.

## Quick Selection Guide

| You're creating | Use template | Condition |
|---|---|---|
| A new .py file | file-header | Multi-file project |
| A new non-trivial class | class | Skip for @dataclass/namedtuple |
| A new public or >30-line function | large-function-header | Public API or complex logic |
| A private helper or <15-line function | small-function-header | Needs doc but small |
| A new unit test | test-naming + test-aaa | Always use AAA structure |
| Many equivalent test cases | test-parametrized | Pure function, many I/O pairs |

## module 鈥?Module Docstring

**Use When:** Creating a new Python module (.py file).
**Must Include:** One-line summary, Dependencies, Inputs, Outputs.
**May Omit:** Extended description, Boundaries.
**Do Not Use When:** File is a trivial entry-point script with zero imports.

```python
"""<涓€鍙ヨ瘽姒傝堪妯″潡鑱岃矗>.

<鎵╁睍鎻忚堪锛屽彲閫?銆?
Boundaries:
    <妯″潡璐熻矗鐨勮竟鐣岋紝涓嶈礋璐ｇ殑鍐呭>銆?
Dependencies:
    - <澶栭儴渚濊禆 1>
    - <澶栭儴渚濊禆 2>

Inputs:
    <妯″潡鎺ユ敹鐨勮緭鍏ユ暟鎹祦鎴栭厤缃?銆?
Outputs:
    <妯″潡浜у嚭鐨勮緭鍑烘暟鎹祦鎴栧壇浣滅敤>銆?"""
```

## class 鈥?Class Docstring

**Use When:** Defining any non-trivial class or data structure.
**Must Include:** One-line summary, Invariants.
**May Omit:** Extended description, Collaborators, Lifecycle.
**Do Not Use When:** Class is a plain data holder (use @dataclass or namedtuple).

```python
class MyClass:
    """<涓€鍙ヨ瘽姒傝堪绫绘娊璞?.

    <鎵╁睍鎻忚堪锛屽彲閫?銆?
    Invariants:
        <濮嬬粓涓虹湡鐨勭害鏉熸潯浠?銆?
    Collaborators:
        - <鍗忎綔绫?1>
        - <鍗忎綔绫?2>

    Lifecycle:
        <鍒涘缓 鈫?浣跨敤 鈫?閿€姣佺殑鍏抽敭闃舵>銆?    """
```

## function 鈥?Function Docstring

**Use When:** Writing a public function or any function with non-obvious behavior.
**Must Include:** One-line summary, Args, Returns.
**May Omit:** Extended description, Raises, Side Effects, Preconditions.
**Do Not Use When:** Function body is a one-liner that self-documents.

```python
def my_func(param1, param2):
    """<涓€鍙ヨ瘽姒傝堪鍑芥暟鐩殑>.

    <鎵╁睍鎻忚堪锛屽彲閫?銆?
    Args:
        param1 (Type): <鍙傛暟璇存槑>.
        param2 (Type): <鍙傛暟璇存槑>.

    Returns:
        Type: <杩斿洖鍊艰鏄庯紱鏃犺繑鍥炲€兼椂鍐?None>銆?
    Raises:
        ErrorType: <鍦ㄤ粈涔堟潯浠朵笅鎶涘嚭姝ゅ紓甯?.

    Side Effects:
        <淇敼鍏ㄥ眬鐘舵€併€佸啓鍏ユ枃浠躲€佸彂閫佺綉缁滆姹傜瓑>.

    Preconditions:
        <璋冪敤鍓嶅繀椤绘弧瓒崇殑鏉′欢>.
    """
```

## file-header 鈥?File Header Block

**Use When:** Creating a new source file in a multi-file project.
**Must Include:** FILE, BRIEF.
**May Omit:** MODULE, FUNCTIONS list, DEPENDS.
**Do Not Use When:** Project convention uses a simpler header or the file is a single-use script.

```
# //////////////////////////////////////////////////////////////////////////////
# //  FILE:    <filename.ext>
# //  MODULE:  <parent_package.module_name>
# //  BRIEF:   <涓€鍙ヨ瘽姒傝堪鏈枃浠惰亴璐?
# //
# //  FUNCTIONS:
# //    <function_name_1>  鈥?<涓€鍙ヨ瘽鍔熻兘>
# //    <function_name_2>  鈥?<涓€鍙ヨ瘽鍔熻兘>
# //
# //  DEPENDS: <澶栭儴鍖?妯″潡鍒楄〃锛岄€楀彿鍒嗛殧>
# //////////////////////////////////////////////////////////////////////////////
```

## large-function-header 鈥?Public Function Header Block

**Use When:** Writing a public API function or a function longer than ~30 lines.
**Must Include:** NAME, PURPOSE, INPUT (all params), OUTPUT.
**May Omit:** SIDE-FX (when none), RAISES (when none).
**Do Not Use When:** Function is small (<15 lines), private, or self-documenting.

```
# ==============================================================================
# NAME:      <function_name>
# PURPOSE:   <涓€鍙ヨ瘽姒傝堪鍑芥暟鐩殑>
# INPUT:     <param1> | <type1> | <璇存槑>
#            <param2> | <type2> | <璇存槑>
# OUTPUT:    <return_type> 鈥?<杩斿洖鍊艰鏄庯紱鏃犺繑鍥炲€煎啓 None>
# SIDE-FX:   <鍓綔鐢ㄨ鏄庯紱鏃犲壇浣滅敤鍐?"none">
# RAISES:    <ExceptionType> 鈥?<鍦ㄤ粈涔堟潯浠朵笅鎶涘嚭锛涗笉鎶涘紓甯稿啓 "none">
# ==============================================================================
```

- INPUT 姣忚涓€涓弬鏁帮紝涓変釜淇℃伅鐢?` | ` 鍒嗛殧锛屾寜杈撳叆鈫掍慨鏀光啋杈撳嚭椤哄簭鎺掑垪銆?- OUTPUT 鑻ヨ繑鍥炵粨鏋勫鏉傦紝鍒嗚鍒楀嚭鍚勫瓧娈靛惈涔夈€?- SIDE-FX 鍚慨鏀瑰叏灞€鐘舵€併€佸啓鏂囦欢銆佸彂缃戠粶璇锋眰銆佹墦鍗拌緭鍑虹瓑銆備笉閬楁紡銆?- RAISES 鍙垪璋冪敤鏂瑰簲鎰熺煡鐨勫紓甯革紝涓嶅垪鍐呴儴瀹炵幇鎶涘嚭鐨勫紓甯搞€?
## small-function-header 鈥?Compact Function Header

**Use When:** Writing a private helper or small (<15 lines) function that still needs documentation.
**Must Include:** Function name, one-line purpose, return type.
**May Omit:** Parameter type annotations (if obvious), parameter names (if >80 chars).
**Do Not Use When:** Function is public API or has complex semantics 鈥?use large-function-header.

```
# --- <function_name> --- <涓€鍙ヨ瘽鍔熻兘>. IN: (<param1>: <type1>, ...). OUT: <return_type> 鈥?<璇存槑>. ---
```

- 鍗曡鍐呭畬鎴愶紝涓嶆崲琛屻€傝嫢鍙傛暟鍒楄〃杩囬暱锛?80 瀛楃锛夛紝鍙缉鐣ヤ负绫诲瀷鍚嶇渷鐣ュ弬鏁板悕銆?
## test-naming 鈥?Test Function Naming

**Use When:** Writing any test function.
**Must Include:** test_ prefix, unit under test, scenario.
**May Omit:** Expected result (when testing for exceptions with pytest.raises).
**Do Not Use When:** Using a test framework with incompatible naming rules.

```
# test_<琚祴鍗曞厓>_<鍦烘櫙>_<棰勬湡缁撴灉>
def test_process_orders_empty_input_raises_value_error():
    ...

def test_process_orders_single_valid_row_returns_one_record():
    ...

def test_process_orders_invalid_email_reports_error():
    ...
```

## test-aaa 鈥?AAA Test Structure

**Use When:** Writing unit tests for deterministic functions or methods.
**Must Include:** Arrange, Act, Assert sections with blank-line separation.
**May Omit:** Comments labeling sections (when sections are trivially distinguishable).
**Do Not Use When:** Testing async code, stateful integrations, or non-deterministic behavior.

```python
def test_<unit>_<scenario>_<expected>():
    # -- Arrange: 鍑嗗琚祴瀵硅薄鍜岃緭鍏ユ暟鎹?--
    input_data = ...
    expected = ...

    # -- Act: 鎵ц琚祴琛屼负 --
    result = some_function(input_data)

    # -- Assert: 楠岃瘉缁撴灉涓庨鏈熶竴鑷?--
    assert result == expected
```

- AAA 涓夋涓嶅悎骞讹紝绌鸿鍒嗛殧锛屾柇瑷€涓嶅紩鍏ョ涓夋柟妗嗘灦銆?
## test-parametrized 鈥?Parameterized Test

**Use When:** Testing a pure function with many equivalent input/output pairs.
**Must Include:** Parametrize decorator, case comments labeling category (杈圭晫/姝ｅ父/寮傚父), fail-fast first case.
**May Omit:** Exhaustive edge cases (use a separate property-based test).
**Do Not Use When:** Test logic branches significantly per case 鈥?use separate test functions.

```python
@pytest.mark.parametrize("input_val, expected", [
    (None,     ValueError),     # 杈圭晫锛歂one
    ("",       ValueError),     # 杈圭晫锛氱┖瀛楃涓?    ("a@b.c",  True),           # 姝ｅ父锛氭渶灏忔湁鏁?    ("a"*100 + "@b.c", True),   # 杈圭晫锛氶暱 local-part
])
def test_validate_email(input_val, expected):
    if expected is ValueError:
        with pytest.raises(ValueError):
            validate_email(input_val)
    else:
        assert validate_email(input_val) == expected
```

- 鍙傛暟鍖栧垪琛ㄤ腑姣忔潯 case 娉ㄩ噴璇存槑瑕嗙洊鐨勬祴璇曠被鍒紙杈圭晫/姝ｅ父/寮傚父锛夈€?- 绗竴涓?case 閫氬父鏀炬渶甯歌Е鍙戠殑閿欒璺緞銆?

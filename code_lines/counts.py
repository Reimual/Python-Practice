import argparse, os


def _py_triple_close(line: str, i: int, quote: str) -> bool:
    return (
        i + 2 < len(line)
        and line[i] == quote
        and line[i + 1] == quote
        and line[i + 2] == quote
    )


def _py_line_continues(stripped: str) -> bool:
    if not stripped:
        return False
    s = stripped.rstrip()
    return s.endswith(("(", "[", "{", ",", "\\"))


def _py_triple_is_code(stripped: str, i: int, prev_continues: bool) -> bool:
    """三引号出现在表达式中或上一行未结束时，视为代码字符串而非伪注释。"""
    if prev_continues:
        return True
    for j in range(i):
        if not stripped[j].isspace():
            return True
    return False


def py_counts(filename: str) -> int:
    CODE, STRING, LINE_COMMENT, BLOCK_COMMENT, TEXT_BLOCK = range(5)
    state = CODE
    quote = ""
    count = 0
    prev_continues = False

    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            stripped = raw_line.strip()
            if not stripped:
                prev_continues = False
                continue

            i = 0
            n = len(stripped)
            code_found = False

            while i < n:
                ch = stripped[i]

                if state == CODE:
                    if ch == "#":
                        state = LINE_COMMENT
                        i += 1

                    elif ch in "\"'":
                        if _py_triple_close(stripped, i, ch):
                            if _py_triple_is_code(stripped, i, prev_continues):
                                state = TEXT_BLOCK
                                quote = ch
                                code_found = True
                            else:
                                state = BLOCK_COMMENT
                                quote = ch
                            i += 3

                        else:
                            state = STRING
                            quote = ch
                            code_found = True
                            i += 1

                    elif not ch.isspace():
                        code_found = True
                        i += 1

                    else:
                        i += 1

                elif state == LINE_COMMENT:
                    break

                elif state in (BLOCK_COMMENT, TEXT_BLOCK):
                    if _py_triple_close(stripped, i, quote):
                        if state == TEXT_BLOCK:
                            code_found = True
                        state = CODE
                        quote = ""
                        i += 3
                    else:
                        i += 1

                elif state == STRING:
                    if ch == "\\" and i + 1 < n:
                        i += 2
                    elif ch == quote:
                        state = CODE
                        quote = ""
                        i += 1
                    else:
                        i += 1

            if state == LINE_COMMENT:
                state = CODE

            if code_found or state == TEXT_BLOCK:
                count += 1

            prev_continues = _py_line_continues(stripped)

    return count


def cpp_counts(filename: str) -> int:
    """返回 C++ 文件中实际代码行数（忽略空白行和纯注释行）。
    使用状态机处理字符串、字符与注释，避免误判。
    """

    CODE, LINE_COMMENT, BLOCK_COMMENT, STRING, CHAR = range(5)
    state = CODE
    count = 0

    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            i = 0
            n = len(line)
            code_found = False

            while i < n:
                ch = line[i]

                if state == CODE:
                    if ch == '"':
                        state = STRING
                        code_found = True
                        i += 1
                    elif ch == "'":
                        state = CHAR
                        code_found = True
                        i += 1
                    elif ch == "/" and i + 1 < n:
                        if line[i + 1] == "/":
                            state = LINE_COMMENT
                            i += 2
                        elif line[i + 1] == "*":
                            state = BLOCK_COMMENT
                            i += 2
                        else:
                            code_found = True
                            i += 1
                    elif not ch.isspace():
                        code_found = True
                        i += 1
                    else:
                        i += 1

                elif state == LINE_COMMENT:
                    # 直接丢弃本行剩余部分
                    break

                elif state == BLOCK_COMMENT:
                    if ch == "*" and i + 1 < n and line[i + 1] == "/":
                        state = CODE
                        i += 2
                    else:
                        i += 1

                elif state == STRING:
                    if ch == "\\" and i + 1 < n:
                        # 转义字符，跳过下一个字符
                        i += 2
                    elif ch == '"':
                        state = CODE
                        i += 1
                    else:
                        i += 1

                elif state == CHAR:
                    if ch == "\\" and i + 1 < n:
                        i += 2
                    elif ch == "'":
                        state = CODE
                        i += 1
                    else:
                        i += 1

            # 行结束时，若处于单行注释状态则重置
            if state == LINE_COMMENT:
                state = CODE

            if code_found:
                count += 1

    return count


def java_counts(filename: str) -> int:
    CODE, LINE_COMMENT, BLOCK_COMMENT, STRING, CHAR, TEXT_BLOCKS = range(6)
    state = CODE
    count = 0

    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            i = 0
            n = len(line)
            code_found = False

            while i < n:
                ch = line[i]

                if state == CODE:
                    if ch == '"':
                        if (
                            i + 2 < len(line)
                            and ch == line[i + 1]
                            and ch == line[i + 2]
                        ):
                            state = TEXT_BLOCKS
                            code_found = True
                            i += 3
                        else:
                            state = STRING
                            code_found = True
                            i += 1
                    elif ch == "'":
                        state = CHAR
                        code_found = True
                        i += 1
                    elif ch == "/" and i + 1 < n:
                        if line[i + 1] == "/":
                            state = LINE_COMMENT
                            i += 2
                        elif line[i + 1] == "*":
                            state = BLOCK_COMMENT
                            i += 2
                        else:
                            code_found = True
                            i += 1
                    elif not ch.isspace():
                        code_found = True
                        i += 1
                    else:
                        i += 1

                elif state == LINE_COMMENT:
                    # 直接丢弃本行剩余部分
                    break

                elif state == BLOCK_COMMENT:
                    if ch == "*" and i + 1 < n and line[i + 1] == "/":
                        state = CODE
                        i += 2
                    else:
                        i += 1

                elif state == STRING:
                    if ch == "\\" and i + 1 < n:
                        # 转义字符，跳过下一个字符
                        i += 2
                    elif ch == '"':
                        state = CODE
                        i += 1
                    else:
                        i += 1

                elif state == CHAR:
                    if ch == "\\" and i + 1 < n:
                        i += 2
                    elif ch == "'":
                        state = CODE
                        i += 1
                    else:
                        i += 1

                elif state == TEXT_BLOCKS:
                    if (
                        i + 2 < len(line)
                        and ch == line[i]
                        and ch == line[i + 1]
                        and ch == line[i + 2]
                    ):
                        state = CODE
                        i += 3
                    else:
                        i += 1

            # 行结束时，若处于单行注释状态则重置
            if state == LINE_COMMENT:
                state = CODE

            if code_found or state == TEXT_BLOCKS:
                count += 1

    return count


def args_func() -> tuple[str]:
    parser = argparse.ArgumentParser(prog="*.py", description="Count lines of code")

    parser.add_argument("-py", nargs="+", help="source python file")
    parser.add_argument("-cpp", nargs="+", help="source c++ file")
    parser.add_argument("-java", nargs="+", help="source java file")

    try:
        arg = parser.parse_args()

        return arg
    except FileNotFoundError:
        print("No such file or directory: arg")
    except SystemExit:
        ...

    return ""


def main():
    filenames = args_func()
    py_filenames: list[str] = filenames.py
    cpp_filenames: list[str] = filenames.cpp
    java_filenames: list[str] = filenames.java

    py_nums: int = 0
    cpp_nums: int = 0
    java_nums: int = 0

    if py_filenames != None:
        for py_filename in py_filenames:
            if ".py" not in py_filename:
                print(f"{py_filename} is not python file !")
                break
            py_nums += py_counts(py_filename)
            print(f"Total python code lines: {py_nums}")

    if cpp_filenames != None:
        for filename in cpp_filenames:
            cpp_nums += cpp_counts(filename)
            print(f"Total c++ code lines: {cpp_nums}")

    if java_filenames != None:
        for filename in java_filenames:
            java_nums += java_counts(filename)
            print(f"Total c++ code lines: {java_nums}")


if __name__ == "__main__":
    main()

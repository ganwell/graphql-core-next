__all__ = ["dedent_block_string_value", "print_block_string"]


def dedent_block_string_value(raw_string: str) -> str:
    """Produce the value of a block string from its parsed raw value.

    Similar to CoffeeScript's block string, Python's docstring trim or Ruby's
    strip_heredoc.

    This implements the GraphQL spec's BlockStringValue() static algorithm.
    """
    lines = raw_string.splitlines()

    common_indent = None
    for line in lines[1:]:
        indent = leading_whitespace(line)
        if indent < len(line) and (common_indent is None or indent < common_indent):
            common_indent = indent
        if common_indent == 0:
            break

    if common_indent:
        lines[1:] = [line[common_indent:] for line in lines[1:]]

    while lines and not lines[0].strip():
        lines = lines[1:]

    while lines and not lines[-1].strip():
        lines = lines[:-1]

    return "\n".join(lines)


def leading_whitespace(s):
    i = 0
    n = len(s)
    while i < n and s[i] in " \t":
        i += 1
    return i


def print_block_string(
    value: str, indentation: str = "", prefer_multiple_lines: bool = False
) -> str:
    """Print a block string in the indented block form.

    Prints a block string in the indented block form by adding a leading and
    trailing blank line. However, if a block string starts with whitespace and
    is a single-line, adding a leading blank line would strip that whitespace.
    """
    is_single_line = "\n" not in value
    has_leading_space = value.startswith(" ") or value.startswith("\t")
    has_trailing_quote = value.endswith('"')
    print_as_multiple_lines = (
        not is_single_line or has_trailing_quote or prefer_multiple_lines
    )

    # Format a multi-line block quote to account for leading space.
    if print_as_multiple_lines and not (is_single_line and has_leading_space):
        result = "\n" + indentation
    else:
        result = ""
    result += value.replace("\n", "\n" + indentation) if indentation else value
    if print_as_multiple_lines:
        result += "\n"

    return '"""' + result.replace('"""', '\\"""') + '"""'
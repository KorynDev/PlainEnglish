"""
PlainEnglish error classes.

Every error message is written in plain English so that a complete
beginner can understand what went wrong and how to fix it.
"""


class PlainEnglishError(Exception):
    """Base class for all PlainEnglish errors."""

    def __init__(self, message: str, line: int | None = None):
        self.line = line
        if line is not None:
            full = f"On line {line}: {message}"
        else:
            full = message
        super().__init__(full)


class ParseError(PlainEnglishError):
    """Raised when the parser cannot understand a statement."""
    pass


class RuntimeError_(PlainEnglishError):
    """Raised when something goes wrong while running the program."""
    pass


# ---------------------------------------------------------------------------
# Factory helpers – keep error text consistent across the codebase
# ---------------------------------------------------------------------------

def unknown_statement(line: int) -> ParseError:
    return ParseError(
        "I do not understand this sentence. Every statement should start "
        "with a keyword like Let, Set, Display, If, Repeat, While, For each, "
        "Define, Call, Add, Remove, Ask, Give back, or Note.",
        line,
    )


def missing_period(line: int) -> ParseError:
    return ParseError(
        "It looks like this statement is missing a period at the end. "
        "Every sentence in PlainEnglish must end with a period.",
        line,
    )


def undefined_variable(name: str, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'I do not know what "{name}" means. '
        "Did you forget to create it with a Let statement first?",
        line,
    )


def type_mismatch_arithmetic(value, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'I cannot do math with the value "{value}" because it is not a number.',
        line,
    )


def division_by_zero(line: int) -> RuntimeError_:
    return RuntimeError_(
        "I cannot divide by zero. Please check your math.",
        line,
    )


def wrong_arg_count(name: str, expected: int, got: int, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'The function "{name}" expects {expected} parameter(s) '
        f"but you gave it {got}. Please check your Call statement.",
        line,
    )


def undefined_function(name: str, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'I do not know a function called "{name}". '
        "Did you forget to define it with a Define a function called statement?",
        line,
    )


def unexpected_eof(start_keyword: str, end_keyword: str, line: int) -> ParseError:
    return ParseError(
        f"The program ended before I found {end_keyword} to close the "
        f"block that started here.",
        line,
    )


def list_item_not_found(value, list_name: str, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'I could not find "{value}" in the list "{list_name}". '
        "The item must be in the list before you can remove it.",
        line,
    )


def index_out_of_range(index: int, list_name: str, length: int, line: int) -> RuntimeError_:
    return RuntimeError_(
        f"Item number {index} is out of range for the list "
        f'"{list_name}". The list only has {length} item(s).',
        line,
    )


def file_not_found(filename: str) -> PlainEnglishError:
    return PlainEnglishError(
        f'I cannot find the file "{filename}". '
        "Please check the file name and try again.",
    )


def empty_program(filename: str) -> PlainEnglishError:
    return PlainEnglishError(
        f'The file "{filename}" appears to be empty. '
        "Try writing some PlainEnglish statements and run it again.",
    )


def library_not_found(name: str, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'I cannot find a library called "{name}". '
        'Please make sure there is a matching file in the libs folder.',
        line,
    )


def library_load_error(name: str, detail: str, line: int) -> RuntimeError_:
    return RuntimeError_(
        f'I had trouble loading the library "{name}": {detail}',
        line,
    )

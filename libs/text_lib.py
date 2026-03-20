from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use text."""
    interpreter.native_functions['uppercase'] = _pe_uppercase
    interpreter.native_functions['lowercase'] = _pe_lowercase
    interpreter.native_functions['length of text'] = _pe_length
    interpreter.native_functions['replace text'] = _pe_replace
    interpreter.native_functions['split text'] = _pe_split

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_uppercase(args, line):
    _ensure_args("uppercase", args, 1, line)
    return str(args[0]).upper()

def _pe_lowercase(args, line):
    _ensure_args("lowercase", args, 1, line)
    return str(args[0]).lower()

def _pe_length(args, line):
    _ensure_args("length of text", args, 1, line)
    return len(str(args[0]))

def _pe_replace(args, line):
    _ensure_args("replace text", args, 3, line)
    source = str(args[0])
    old_str = str(args[1])
    new_str = str(args[2])
    return source.replace(old_str, new_str)

def _pe_split(args, line):
    _ensure_args("split text", args, 2, line)
    source = str(args[0])
    delimiter = str(args[1])
    return source.split(delimiter)

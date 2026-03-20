from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use type."""
    interpreter.native_functions['type of'] = _pe_type_of
    interpreter.native_functions['to text'] = _pe_to_text
    interpreter.native_functions['to number'] = _pe_to_number

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_type_of(args, line):
    _ensure_args("type of", args, 1, line)
    val = args[0]
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, (int, float)):
        return "number"
    if isinstance(val, str):
        return "text"
    if isinstance(val, list):
        return "list"
    if isinstance(val, dict):
        return "dictionary"
    return "unknown"

def _pe_to_text(args, line):
    _ensure_args("to text", args, 1, line)
    val = args[0]
    if isinstance(val, bool):
        return 'true' if val else 'false'
    return str(val)

def _pe_to_number(args, line):
    _ensure_args("to number", args, 1, line)
    val = args[0]
    try:
        f = float(str(val))
        if f == int(f) and '.' not in str(val):
            return int(f)
        return f
    except ValueError:
        raise RuntimeError_(f'I cannot convert "{val}" into a number.', line)

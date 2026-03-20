import re
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use regex."""
    interpreter.native_functions['regex match'] = _pe_regex_match
    interpreter.native_functions['regex search'] = _pe_regex_search
    interpreter.native_functions['regex replace'] = _pe_regex_replace
    interpreter.native_functions['regex split'] = _pe_regex_split

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_regex_match(args, line):
    _ensure_args("regex match", args, 2, line)
    pattern = str(args[0])
    text = str(args[1])
    try:
        # Fullmatch requires the entire string to match
        return bool(re.fullmatch(pattern, text))
    except Exception as e:
        raise RuntimeError_(f'Invalid regex pattern "{pattern}": {e}', line)

def _pe_regex_search(args, line):
    _ensure_args("regex search", args, 2, line)
    pattern = str(args[0])
    text = str(args[1])
    from interpreter.interpreter import _NO_RETURN
    try:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        return _NO_RETURN
    except Exception as e:
        raise RuntimeError_(f'Invalid regex pattern "{pattern}": {e}', line)

def _pe_regex_replace(args, line):
    _ensure_args("regex replace", args, 3, line)
    pattern = str(args[0])
    replacement = str(args[1])
    text = str(args[2])
    try:
        return re.sub(pattern, replacement, text)
    except Exception as e:
        raise RuntimeError_(f'Invalid regex pattern "{pattern}": {e}', line)

def _pe_regex_split(args, line):
    _ensure_args("regex split", args, 2, line)
    pattern = str(args[0])
    text = str(args[1])
    try:
        return re.split(pattern, text)
    except Exception as e:
        raise RuntimeError_(f'Invalid regex pattern "{pattern}": {e}', line)

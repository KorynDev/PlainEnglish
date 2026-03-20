import random
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use random."""
    interpreter.native_functions['random integer'] = _pe_random_int
    interpreter.native_functions['random decimal'] = _pe_random_decimal
    interpreter.native_functions['random choice'] = _pe_random_choice

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_random_int(args, line):
    _ensure_args("random integer", args, 2, line)
    try:
        min_val = int(args[0])
        max_val = int(args[1])
        return random.randint(min_val, max_val)
    except (ValueError, TypeError):
        from interpreter.errors import type_mismatch_arithmetic
        raise type_mismatch_arithmetic(args[0] if not isinstance(args[0], (int, float)) else args[1], line)

def _pe_random_decimal(args, line):
    _ensure_args("random decimal", args, 0, line)
    return random.random()

def _pe_random_choice(args, line):
    _ensure_args("random choice", args, 1, line)
    lst = args[0]
    if not isinstance(lst, list):
        raise RuntimeError_(f'I can only pick a random choice from a list.', line)
    if not lst:
        raise RuntimeError_(f'I cannot pick a random choice from an empty list.', line)
    return random.choice(lst)

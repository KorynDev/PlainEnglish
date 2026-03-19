import math
from interpreter.errors import wrong_arg_count, type_mismatch_arithmetic

def register(interpreter):
    """Called when the user writes: Use math."""
    interpreter.native_functions['round'] = _pe_round
    interpreter.native_functions['floor'] = _pe_floor
    interpreter.native_functions['ceiling'] = _pe_ceiling
    interpreter.native_functions['square root'] = _pe_sqrt
    interpreter.native_functions['power'] = _pe_power
    interpreter.native_functions['absolute value'] = _pe_abs
    interpreter.native_functions['minimum'] = _pe_min
    interpreter.native_functions['maximum'] = _pe_max

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _ensure_number(val, line: int):
    if not isinstance(val, (int, float)):
        raise type_mismatch_arithmetic(val, line)
    return val

def _format_result(val):
    if isinstance(val, float) and val == int(val):
        return int(val)
    return val

def _pe_round(args, line):
    _ensure_args("round", args, 1, line)
    return _format_result(round(_ensure_number(args[0], line)))

def _pe_floor(args, line):
    _ensure_args("floor", args, 1, line)
    return math.floor(_ensure_number(args[0], line))

def _pe_ceiling(args, line):
    _ensure_args("ceiling", args, 1, line)
    return math.ceil(_ensure_number(args[0], line))

def _pe_sqrt(args, line):
    _ensure_args("square root", args, 1, line)
    # Python math.sqrt raises ValueError for negative numbers
    try:
        return _format_result(math.sqrt(_ensure_number(args[0], line)))
    except ValueError as e:
        from interpreter.errors import RuntimeError_
        raise RuntimeError_(f"I cannot calculate the square root: {e}", line)

def _pe_power(args, line):
    _ensure_args("power", args, 2, line)
    base = _ensure_number(args[0], line)
    exp = _ensure_number(args[1], line)
    try:
        return _format_result(math.pow(base, exp))
    except Exception as e:
        from interpreter.errors import RuntimeError_
        raise RuntimeError_(f"I had trouble calculating the power: {e}", line)

def _pe_abs(args, line):
    _ensure_args("absolute value", args, 1, line)
    return _format_result(abs(_ensure_number(args[0], line)))

def _pe_min(args, line):
    _ensure_args("minimum", args, 2, line)
    a = _ensure_number(args[0], line)
    b = _ensure_number(args[1], line)
    return a if a < b else b

def _pe_max(args, line):
    _ensure_args("maximum", args, 2, line)
    a = _ensure_number(args[0], line)
    b = _ensure_number(args[1], line)
    return a if a > b else b

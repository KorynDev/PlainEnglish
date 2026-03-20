import time
import datetime
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use time."""
    interpreter.native_functions['current time'] = _pe_current_time
    interpreter.native_functions['current date'] = _pe_current_date
    interpreter.native_functions['unix timestamp'] = _pe_unix_timestamp
    interpreter.native_functions['sleep'] = _pe_sleep

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_current_time(args, line):
    _ensure_args("current time", args, 0, line)
    return datetime.datetime.now().strftime("%H:%M:%S")

def _pe_current_date(args, line):
    _ensure_args("current date", args, 0, line)
    return datetime.date.today().isoformat()

def _pe_unix_timestamp(args, line):
    _ensure_args("unix timestamp", args, 0, line)
    return int(time.time())

def _pe_sleep(args, line):
    _ensure_args("sleep", args, 1, line)
    val = args[0]
    if not isinstance(val, (int, float)):
        from interpreter.errors import type_mismatch_arithmetic
        raise type_mismatch_arithmetic(val, line)
    time.sleep(val)

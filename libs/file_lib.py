import os
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use file."""
    interpreter.native_functions['read file'] = _pe_read_file
    interpreter.native_functions['write file'] = _pe_write_file
    interpreter.native_functions['append file'] = _pe_append_file
    interpreter.native_functions['file exists'] = _pe_file_exists

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_read_file(args, line):
    _ensure_args("read file", args, 1, line)
    filename = str(args[0])
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError_(f'I could not find the file "{filename}" to read it.', line)
    except Exception as e:
        raise RuntimeError_(f'I had trouble reading "{filename}": {e}', line)

def _pe_write_file(args, line):
    _ensure_args("write file", args, 2, line)
    filename = str(args[0])
    contents = str(args[1])
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(contents)
    except Exception as e:
        raise RuntimeError_(f'I had trouble writing to "{filename}": {e}', line)

def _pe_append_file(args, line):
    _ensure_args("append file", args, 2, line)
    filename = str(args[0])
    contents = str(args[1])
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(contents)
    except Exception as e:
        raise RuntimeError_(f'I had trouble appending to "{filename}": {e}', line)

def _pe_file_exists(args, line):
    _ensure_args("file exists", args, 1, line)
    filename = str(args[0])
    return os.path.exists(filename)

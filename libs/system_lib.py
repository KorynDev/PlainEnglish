import os
import sys
import subprocess
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use system."""
    interpreter.native_functions['operating system'] = _pe_operating_system
    interpreter.native_functions['current directory'] = _pe_current_directory
    interpreter.native_functions['shell'] = _pe_shell

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_operating_system(args, line):
    _ensure_args("operating system", args, 0, line)
    if sys.platform.startswith('win'):
        return 'windows'
    elif sys.platform.startswith('darwin'):
        return 'darwin'
    elif sys.platform.startswith('linux'):
        return 'linux'
    return sys.platform

def _pe_current_directory(args, line):
    _ensure_args("current directory", args, 0, line)
    return os.getcwd()

def _pe_shell(args, line):
    _ensure_args("shell", args, 1, line)
    cmd = str(args[0])
    try:
        # Run command, capture stdout/stderr, block until complete
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        raise RuntimeError_(f'I had a problem running the shell command "{cmd}": {e}', line)

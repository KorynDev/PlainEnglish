import hashlib
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use crypto."""
    interpreter.native_functions['md5 hash'] = _pe_md5_hash
    interpreter.native_functions['sha256 hash'] = _pe_sha256_hash

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_md5_hash(args, line):
    _ensure_args("md5 hash", args, 1, line)
    text = str(args[0])
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def _pe_sha256_hash(args, line):
    _ensure_args("sha256 hash", args, 1, line)
    text = str(args[0])
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

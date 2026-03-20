import base64
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use base64."""
    interpreter.native_functions['base64 encode'] = _pe_base64_encode
    interpreter.native_functions['base64 decode'] = _pe_base64_decode

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_base64_encode(args, line):
    _ensure_args("base64 encode", args, 1, line)
    text = str(args[0])
    try:
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    except Exception as e:
        raise RuntimeError_(f'I could not encode the base64 string: {e}', line)

def _pe_base64_decode(args, line):
    _ensure_args("base64 decode", args, 1, line)
    text = str(args[0])
    try:
        decoded_bytes = base64.b64decode(text.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise RuntimeError_(f'I could not decode the base64 string. Are you sure it is valid base64? {e}', line)

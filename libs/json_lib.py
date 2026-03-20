import json
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use json."""
    interpreter.native_functions['parse json'] = _pe_parse_json
    interpreter.native_functions['to json string'] = _pe_to_json_string

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_parse_json(args, line):
    _ensure_args("parse json", args, 1, line)
    text = str(args[0])
    try:
        return json.loads(text)
    except Exception as e:
        raise RuntimeError_(f'I could not parse the JSON text because it is invalid: {e}', line)

def _pe_to_json_string(args, line):
    _ensure_args("to json string", args, 1, line)
    data = args[0]
    try:
        return json.dumps(data, indent=2)
    except Exception as e:
        raise RuntimeError_(f'I could not convert the data into a JSON string: {e}', line)

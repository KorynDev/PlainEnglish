from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use dictionary."""
    interpreter.native_functions['create dictionary'] = _pe_create_dictionary
    interpreter.native_functions['put in dictionary'] = _pe_put_in_dictionary
    interpreter.native_functions['get from dictionary'] = _pe_get_from_dictionary
    interpreter.native_functions['remove from dictionary'] = _pe_remove_from_dictionary
    interpreter.native_functions['dictionary keys'] = _pe_dictionary_keys

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_create_dictionary(args, line):
    _ensure_args("create dictionary", args, 0, line)
    return {}

def _pe_put_in_dictionary(args, line):
    _ensure_args("put in dictionary", args, 3, line)
    d = args[0]
    key = str(args[1])
    val = args[2]
    if not isinstance(d, dict):
        raise RuntimeError_(f'The first parameter must be a dictionary to put "{key}" into.', line)
    d[key] = val

def _pe_get_from_dictionary(args, line):
    _ensure_args("get from dictionary", args, 2, line)
    d = args[0]
    key = str(args[1])
    if not isinstance(d, dict):
        raise RuntimeError_(f'The first parameter must be a dictionary to get "{key}" from.', line)
    from interpreter.interpreter import _NO_RETURN
    if key not in d:
        return _NO_RETURN # Will be treated as error or text literal
    return d[key]

def _pe_remove_from_dictionary(args, line):
    _ensure_args("remove from dictionary", args, 2, line)
    d = args[0]
    key = str(args[1])
    if not isinstance(d, dict):
        raise RuntimeError_(f'The first parameter must be a dictionary to remove "{key}" from.', line)
    if key in d:
        del d[key]

def _pe_dictionary_keys(args, line):
    _ensure_args("dictionary keys", args, 1, line)
    d = args[0]
    if not isinstance(d, dict):
        raise RuntimeError_(f'The parameter must be a dictionary to get its keys.', line)
    return list(d.keys())

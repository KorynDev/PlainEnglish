import sqlite3
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use database."""
    interpreter.native_functions['connect to database'] = _pe_connect
    interpreter.native_functions['execute sql'] = _pe_execute
    interpreter.native_functions['fetch query'] = _pe_fetch
    interpreter.native_functions['close database'] = _pe_close

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_connect(args, line):
    _ensure_args("connect to database", args, 1, line)
    filename = str(args[0])
    try:
        return sqlite3.connect(filename)
    except Exception as e:
        raise RuntimeError_(f'I could not connect to database "{filename}": {e}', line)

def _pe_execute(args, line):
    # args: [conn, query]
    _ensure_args("execute sql", args, 2, line)
    conn = args[0]
    query = str(args[1])
    if not isinstance(conn, sqlite3.Connection):
        raise RuntimeError_(f'The first parameter to execute sql must be a valid database connection.', line)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        raise RuntimeError_(f'Database error while running "{query}": {e}', line)

def _pe_fetch(args, line):
    # args: [conn, query]
    _ensure_args("fetch query", args, 2, line)
    conn = args[0]
    query = str(args[1])
    if not isinstance(conn, sqlite3.Connection):
        raise RuntimeError_(f'The first parameter to fetch query must be a valid database connection.', line)
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        # return list of lists instead of list of tuples
        return [list(row) for row in cursor.fetchall()]
    except Exception as e:
        raise RuntimeError_(f'Database error while fetching "{query}": {e}', line)

def _pe_close(args, line):
    _ensure_args("close database", args, 1, line)
    conn = args[0]
    if not isinstance(conn, sqlite3.Connection):
        raise RuntimeError_(f'The parameter to close database must be a valid database connection.', line)
    try:
        conn.close()
    except Exception as e:
        raise RuntimeError_(f'Could not close database: {e}', line)

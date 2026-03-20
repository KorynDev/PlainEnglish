import csv
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use csv."""
    interpreter.native_functions['read csv'] = _pe_read_csv
    interpreter.native_functions['write csv'] = _pe_write_csv

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_read_csv(args, line):
    _ensure_args("read csv", args, 1, line)
    filename = str(args[0])
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            return [row for row in reader]
    except FileNotFoundError:
        raise RuntimeError_(f'I could not find the CSV file "{filename}".', line)
    except Exception as e:
        raise RuntimeError_(f'I had trouble reading the CSV "{filename}": {e}', line)

def _pe_write_csv(args, line):
    _ensure_args("write csv", args, 2, line)
    filename = str(args[0])
    rows = args[1]
    
    if not isinstance(rows, list):
        raise RuntimeError_(f'The second parameter to write csv must be a list of lists representing rows.', line)

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in rows:
                if isinstance(row, list):
                    writer.writerow([str(i) for i in row])
                else:
                    writer.writerow([str(row)])
    except Exception as e:
        raise RuntimeError_(f'I had trouble writing the CSV file "{filename}": {e}', line)

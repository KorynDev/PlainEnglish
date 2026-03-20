import urllib.request
import urllib.error
from interpreter.errors import wrong_arg_count, RuntimeError_

def register(interpreter):
    """Called when the user writes: Use network."""
    interpreter.native_functions['fetch url'] = _pe_fetch_url
    interpreter.native_functions['download file'] = _pe_download_file

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_fetch_url(args, line):
    _ensure_args("fetch url", args, 1, line)
    url = str(args[0])
    try:
        # Standard urllib GET request, specifying User-Agent because some APIs reject urllib
        req = urllib.request.Request(url, headers={'User-Agent': 'PlainEnglish/1.0'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        raise RuntimeError_(f'I had trouble fetching "{url}": {e}', line)

def _pe_download_file(args, line):
    _ensure_args("download file", args, 2, line)
    url = str(args[0])
    filename = str(args[1])
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PlainEnglish/1.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            with open(filename, 'wb') as f:
                f.write(data)
    except Exception as e:
        raise RuntimeError_(f'I had trouble downloading "{url}" to "{filename}": {e}', line)

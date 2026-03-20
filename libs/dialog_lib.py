from interpreter.errors import wrong_arg_count, RuntimeError_

# Delay importing tkinter until needed so server-only code doesn't crash if X11/Display is absent
_tkinter_loaded = False
messagebox = None
simpledialog = None
tk_root = None

def _init_tkinter():
    global _tkinter_loaded, messagebox, simpledialog, tk_root
    if not _tkinter_loaded:
        import tkinter
        from tkinter import messagebox as mb
        from tkinter import simpledialog as sd
        messagebox = mb
        simpledialog = sd
        
        # Create a hidden root window
        tk_root = tkinter.Tk()
        tk_root.withdraw()
        tk_root.attributes('-topmost', True)
        
        _tkinter_loaded = True

def register(interpreter):
    """Called when the user writes: Use dialog."""
    interpreter.native_functions['show info'] = _pe_show_info
    interpreter.native_functions['show error'] = _pe_show_error
    interpreter.native_functions['ask yes no'] = _pe_ask_yes_no
    interpreter.native_functions['ask string'] = _pe_ask_string

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_show_info(args, line):
    _ensure_args("show info", args, 2, line)
    title = str(args[0])
    message = str(args[1])
    _init_tkinter()
    messagebox.showinfo(title, message)

def _pe_show_error(args, line):
    _ensure_args("show error", args, 2, line)
    title = str(args[0])
    message = str(args[1])
    _init_tkinter()
    messagebox.showerror(title, message)

def _pe_ask_yes_no(args, line):
    _ensure_args("ask yes no", args, 2, line)
    title = str(args[0])
    message = str(args[1])
    _init_tkinter()
    return messagebox.askyesno(title, message)

def _pe_ask_string(args, line):
    _ensure_args("ask string", args, 2, line)
    title = str(args[0])
    prompt = str(args[1])
    _init_tkinter()
    from interpreter.interpreter import _NO_RETURN
    result = simpledialog.askstring(title, prompt, parent=tk_root)
    if result is None:
        return _NO_RETURN # user pressed cancel
    return result

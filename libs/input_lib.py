import sys
import string
from interpreter.errors import wrong_arg_count, RuntimeError_

glfw = None
_key_map = {}

def register(interpreter):
    """Called when the user writes: Use input."""
    global glfw, _key_map
    try:
        import glfw as _glfw
        glfw = _glfw
        
        # Build dictionary of keynames to GLFW constants
        for char in string.ascii_lowercase:
            _key_map[char] = getattr(glfw, f'KEY_{char.upper()}', -1)
        for digit in string.digits:
            _key_map[digit] = getattr(glfw, f'KEY_{digit}', -1)
            
        _key_map['space'] = glfw.KEY_SPACE
        _key_map['escape'] = glfw.KEY_ESCAPE
        _key_map['enter'] = glfw.KEY_ENTER
        _key_map['return'] = glfw.KEY_ENTER
        _key_map['up'] = glfw.KEY_UP
        _key_map['down'] = glfw.KEY_DOWN
        _key_map['left'] = glfw.KEY_LEFT
        _key_map['right'] = glfw.KEY_RIGHT
        
    except ImportError:
        raise RuntimeError_(
            "I could not load the input library because glfw is not installed. "
            "Please run 'pip install glfw' and try again.",
            None
        )
        
    interpreter.native_functions['check events'] = _pe_check_events
    interpreter.native_functions['is key pressed'] = _pe_is_key_pressed
    interpreter.native_functions['mouse position'] = _pe_mouse_position
    interpreter.native_functions['is mouse pressed'] = _pe_is_mouse_pressed

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _get_window(line: int):
    """Tries to get the GLFW window handle, which is created by graphics_lib.py."""
    if not glfw:
        raise RuntimeError_("Input library loaded, but glfw failed to initialize.", line)
    
    # We use glfw.get_current_context() which tracks the active graphic window
    win = glfw.get_current_context()
    if not win:
        # Fallback: graphics_lib might have a window hidden somewhere if context wasn't current
        import sys
        if 'plainenglish.libs.graphics' in sys.modules:
            mod = sys.modules['plainenglish.libs.graphics']
            if hasattr(mod, '_get_window'):
                win = mod._get_window()
    if not win:
        raise RuntimeError_("You must create a window (Use graphics) before checking events or input.", line)
    return win

def _pe_check_events(args, line):
    """
    Pumps GLFW events.
    Returns True if the user clicked the close [X] button, False otherwise.
    """
    _ensure_args("check events", args, 0, line)
    win = _get_window(line)
    glfw.poll_events()
    return bool(glfw.window_should_close(win))

def _pe_is_key_pressed(args, line):
    _ensure_args("is key pressed", args, 1, line)
    win = _get_window(line)
    
    key_name = str(args[0]).lower().strip()
    glfw.poll_events()
    
    if key_name in _key_map:
        key_code = _key_map[key_name]
        if key_code == -1:
            return False
        return glfw.get_key(win, key_code) == glfw.PRESS
        
    raise RuntimeError_(f"I don't know the key '{key_name}'. Try letters, numbers, 'space', 'up', etc.", line)

def _pe_mouse_position(args, line):
    _ensure_args("mouse position", args, 0, line)
    win = _get_window(line)
        
    glfw.poll_events()
    x, y = glfw.get_cursor_pos(win)
    return [int(x), int(y)]

def _pe_is_mouse_pressed(args, line):
    _ensure_args("is mouse pressed", args, 0, line)
    win = _get_window(line)
        
    glfw.poll_events()
    return glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS

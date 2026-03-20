import sys
import math
import time
from interpreter.errors import wrong_arg_count, RuntimeError_

# Defer imports so we don't crash the interpreter if not installed
glfw = None
gl = None

# Global state for the graphics window
window = None
current_color = (1.0, 1.0, 1.0)
_width_store = 800
_height_store = 600

def _get_window():
    """Returns the current globally created window. Shared with input_lib."""
    return window

def register(interpreter):
    """Called when the user writes: Use graphics."""
    global glfw, gl
    try:
        import glfw as _glfw
        from OpenGL import GL as _gl
        glfw = _glfw
        gl = _gl
    except ImportError:
        raise RuntimeError_(
            "I could not load the graphics library because PyOpenGL or glfw is not installed. "
            "Please run 'pip install PyOpenGL glfw' and try again.",
            None
        )
        
    interpreter.native_functions['create window'] = _pe_create_window
    interpreter.native_functions['set background'] = _pe_set_background
    interpreter.native_functions['draw rectangle'] = _pe_draw_rect
    interpreter.native_functions['draw circle'] = _pe_draw_circle
    interpreter.native_functions['set colour'] = _pe_set_color
    interpreter.native_functions['update display'] = _pe_update_display
    interpreter.native_functions['wait'] = _pe_wait
    interpreter.native_functions['close window'] = _pe_close_window

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _ensure_int(val, name: str, line: int):
    if not isinstance(val, (int, float)):
        from interpreter.errors import type_mismatch_arithmetic
        raise type_mismatch_arithmetic(val, line)
    return float(val)

def _check_screen(line: int):
    if window is None:
        raise RuntimeError_(
            "You must create a window before you can draw on it. "
            "Use Call create window with width, height.",
            line
        )

def _pe_create_window(args, line):
    global window, _width_store, _height_store
    _ensure_args("create window", args, 2, line)
    width = int(_ensure_int(args[0], "width", line))
    height = int(_ensure_int(args[1], "height", line))
    
    if not glfw.init():
        raise RuntimeError_("I could not initialize the graphics system.", line)
        
    # Create a simple generic OpenGL context
    window = glfw.create_window(width, height, "PlainEnglish Graphics", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError_("I could not create the graphics window.", line)
        
    glfw.make_context_current(window)
    _width_store = width
    _height_store = height
    
    # Set up 2D orthographic projection matching Pygame (top-left is 0,0)
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0.0, width, height, 0.0, -1.0, 1.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    
def _pe_set_background(args, line):
    _check_screen(line)
    _ensure_args("set background", args, 3, line)
    r = _ensure_int(args[0], "red", line) / 255.0
    g = _ensure_int(args[1], "green", line) / 255.0
    b = _ensure_int(args[2], "blue", line) / 255.0
    
    gl.glClearColor(r, g, b, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

def _pe_set_color(args, line):
    global current_color
    _ensure_args("set colour", args, 3, line)
    r = _ensure_int(args[0], "red", line) / 255.0
    g = _ensure_int(args[1], "green", line) / 255.0
    b = _ensure_int(args[2], "blue", line) / 255.0
    
    current_color = (r, g, b)
    gl.glColor3f(r, g, b)

def _pe_draw_rect(args, line):
    _check_screen(line)
    _ensure_args("draw rectangle", args, 4, line)
    x = _ensure_int(args[0], "x", line)
    y = _ensure_int(args[1], "y", line)
    w = _ensure_int(args[2], "width", line)
    h = _ensure_int(args[3], "height", line)
    
    # Ensure current color is active
    gl.glColor3f(*current_color)
    
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + w, y)
    gl.glVertex2f(x + w, y + h)
    gl.glVertex2f(x, y + h)
    gl.glEnd()

def _pe_draw_circle(args, line):
    _check_screen(line)
    _ensure_args("draw circle", args, 3, line)
    x = _ensure_int(args[0], "x", line)
    y = _ensure_int(args[1], "y", line)
    radius = _ensure_int(args[2], "radius", line)
    
    gl.glColor3f(*current_color)
    
    # 32 segments is usually enough for a plain 2D circle
    segments = 32
    gl.glBegin(gl.GL_POLYGON)
    for i in range(segments):
        theta = 2.0 * math.pi * float(i) / float(segments)
        cx = radius * math.cos(theta)
        cy = radius * math.sin(theta)
        gl.glVertex2f(x + cx, y + cy)
    gl.glEnd()

def _pe_update_display(args, line):
    _check_screen(line)
    _ensure_args("update display", args, 0, line)
    glfw.swap_buffers(window)

def _pe_wait(args, line):
    _ensure_args("wait", args, 1, line)
    ms = _ensure_int(args[0], "milliseconds", line)
    time.sleep(ms / 1000.0)

def _pe_close_window(args, line):
    global window
    _ensure_args("close window", args, 0, line)
    if window:
        glfw.destroy_window(window)
        window = None
    if glfw:
        glfw.terminate()

import sys
from interpreter.errors import wrong_arg_count, RuntimeError_

# Defer pygame import so we don't crash the interpreter if it's not installed
# unless the user actually tries to Use graphics.
pygame = None

# Global state for the graphics window
screen = None
clock = None
current_color = (255, 255, 255)

def register(interpreter):
    """Called when the user writes: Use graphics."""
    global pygame
    try:
        # Hide the pygame import "Hello from the pygame community" message
        import os
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        import pygame as pg
        pygame = pg
    except ImportError:
        raise RuntimeError_(
            "I could not load the graphics library because Pygame is not installed. "
            "Please run 'pip install pygame' and try again.",
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
    return int(val)

def _check_screen(line: int):
    if screen is None:
        raise RuntimeError_(
            "You must create a window before you can draw on it. "
            "Use Call create window with width, height.",
            line
        )

def _pe_create_window(args, line):
    global screen, clock
    _ensure_args("create window", args, 2, line)
    width = _ensure_int(args[0], "width", line)
    height = _ensure_int(args[1], "height", line)
    
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PlainEnglish Graphics")
    clock = pygame.time.Clock()
    
def _pe_set_background(args, line):
    _check_screen(line)
    _ensure_args("set background", args, 3, line)
    r = _ensure_int(args[0], "red", line)
    g = _ensure_int(args[1], "green", line)
    b = _ensure_int(args[2], "blue", line)
    screen.fill((r, g, b))

def _pe_set_color(args, line):
    global current_color
    _ensure_args("set colour", args, 3, line)
    r = _ensure_int(args[0], "red", line)
    g = _ensure_int(args[1], "green", line)
    b = _ensure_int(args[2], "blue", line)
    current_color = (r, g, b)

def _pe_draw_rect(args, line):
    _check_screen(line)
    _ensure_args("draw rectangle", args, 4, line)
    x = _ensure_int(args[0], "x", line)
    y = _ensure_int(args[1], "y", line)
    w = _ensure_int(args[2], "width", line)
    h = _ensure_int(args[3], "height", line)
    pygame.draw.rect(screen, current_color, (x, y, w, h))

def _pe_draw_circle(args, line):
    _check_screen(line)
    _ensure_args("draw circle", args, 3, line)
    x = _ensure_int(args[0], "x", line)
    y = _ensure_int(args[1], "y", line)
    radius = _ensure_int(args[2], "radius", line)
    pygame.draw.circle(screen, current_color, (x, y), radius)

def _pe_update_display(args, line):
    _check_screen(line)
    _ensure_args("update display", args, 0, line)
    pygame.display.flip()

def _pe_wait(args, line):
    _ensure_args("wait", args, 1, line)
    ms = _ensure_int(args[0], "milliseconds", line)
    if clock:
        pygame.time.wait(ms)
    else:
        import time
        time.sleep(ms / 1000.0)

def _pe_close_window(args, line):
    global screen
    _ensure_args("close window", args, 0, line)
    if pygame and pygame.get_init():
        pygame.quit()
    screen = None

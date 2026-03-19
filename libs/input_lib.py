from interpreter.errors import wrong_arg_count, RuntimeError_

pygame = None
_key_map = {}

def register(interpreter):
    """Called when the user writes: Use input."""
    global pygame, _key_map
    try:
        import pygame as pg
        pygame = pg
        
        # Build a handy reverse-lookup map for key names matching Pygame's K_ constants.
        # e.g., 'a' -> pg.K_a, 'space' -> pg.K_SPACE, 'escape' -> pg.K_ESCAPE
        import string
        for char in string.ascii_lowercase:
            _key_map[char] = getattr(pg, f'K_{char}')
        for digit in string.digits:
            _key_map[digit] = getattr(pg, f'K_{digit}')
            
        _key_map['space'] = pg.K_SPACE
        _key_map['escape'] = pg.K_ESCAPE
        _key_map['enter'] = pg.K_RETURN
        _key_map['return'] = pg.K_RETURN
        _key_map['up'] = pg.K_UP
        _key_map['down'] = pg.K_DOWN
        _key_map['left'] = pg.K_LEFT
        _key_map['right'] = pg.K_RIGHT
        
    except ImportError:
        raise RuntimeError_(
            "I could not load the input library because Pygame is not installed. "
            "Please run 'pip install pygame' and try again.",
            None
        )
        
    interpreter.native_functions['check events'] = _pe_check_events
    interpreter.native_functions['is key pressed'] = _pe_is_key_pressed
    interpreter.native_functions['mouse position'] = _pe_mouse_position
    interpreter.native_functions['is mouse pressed'] = _pe_is_mouse_pressed

def _ensure_args(name: str, args: list, expected: int, line: int):
    if len(args) != expected:
        raise wrong_arg_count(name, expected, len(args), line)

def _pe_check_events(args, line):
    """
    Pumps the the Pygame event queue. 
    Returns True if the user clicked the close [X] button, False otherwise.
    """
    _ensure_args("check events", args, 0, line)
    if not (pygame and pygame.get_init()):
        raise RuntimeError_("You must create a window (Use graphics) before checking events.", line)
        
    quit_requested = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_requested = True
            
    return quit_requested

def _pe_is_key_pressed(args, line):
    _ensure_args("is key pressed", args, 1, line)
    if not (pygame and pygame.get_init()):
        raise RuntimeError_("You must create a window (Use graphics) before checking keys.", line)
        
    key_name = str(args[0]).lower().strip()
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    
    if key_name in _key_map:
        return bool(keys[_key_map[key_name]])
        
    raise RuntimeError_(f"I don't know the key '{key_name}'. Try letters, numbers, 'space', 'up', etc.", line)

def _pe_mouse_position(args, line):
    _ensure_args("mouse position", args, 0, line)
    if not (pygame and pygame.get_init()):
        raise RuntimeError_("You must create a window (Use graphics) before getting mouse position.", line)
        
    pygame.event.pump()
    x, y = pygame.mouse.get_pos()
    return [x, y]

def _pe_is_mouse_pressed(args, line):
    _ensure_args("is mouse pressed", args, 0, line)
    if not (pygame and pygame.get_init()):
        raise RuntimeError_("You must create a window (Use graphics) before checking mouse.", line)
        
    pygame.event.pump()
    buttons = pygame.mouse.get_pressed()
    return bool(buttons[0]) # Left click

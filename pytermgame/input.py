"""
Input module - Keyboard input handling
"""

try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False

from enum import IntEnum
from typing import Optional, Set


class Keys(IntEnum):
    """Key codes for common keys"""
    # Arrow keys (curses values)
    UP = 259      # curses.KEY_UP
    DOWN = 258    # curses.KEY_DOWN
    LEFT = 260    # curses.KEY_LEFT
    RIGHT = 261   # curses.KEY_RIGHT
    
    # Common keys
    ENTER = 10
    SPACE = 32
    ESCAPE = 27
    BACKSPACE = 127
    TAB = 9
    
    # Letters (lowercase)
    A = ord('a')
    B = ord('b')
    C = ord('c')
    D = ord('d')
    E = ord('e')
    F = ord('f')
    G = ord('g')
    H = ord('h')
    I = ord('i')
    J = ord('j')
    K = ord('k')
    L = ord('l')
    M = ord('m')
    N = ord('n')
    O = ord('o')
    P = ord('p')
    Q = ord('q')
    R = ord('r')
    S = ord('s')
    T = ord('t')
    U = ord('u')
    V = ord('v')
    W = ord('w')
    X = ord('x')
    Y = ord('y')
    Z = ord('z')
    
    # Numbers
    NUM_0 = ord('0')
    NUM_1 = ord('1')
    NUM_2 = ord('2')
    NUM_3 = ord('3')
    NUM_4 = ord('4')
    NUM_5 = ord('5')
    NUM_6 = ord('6')
    NUM_7 = ord('7')
    NUM_8 = ord('8')
    NUM_9 = ord('9')


class InputHandler:
    """
    Handles keyboard input for games.
    
    Supports both curses key codes and WASD controls.
    """
    
    # WASD to Arrow key mapping
    WASD_MAP = {
        ord('w'): Keys.UP,
        ord('W'): Keys.UP,
        ord('a'): Keys.LEFT,
        ord('A'): Keys.LEFT,
        ord('s'): Keys.DOWN,
        ord('S'): Keys.DOWN,
        ord('d'): Keys.RIGHT,
        ord('D'): Keys.RIGHT,
    }
    
    def __init__(self, use_wasd: bool = True):
        """
        Initialize input handler.
        
        Args:
            use_wasd: Whether to map WASD keys to arrow keys
        """
        self.use_wasd = use_wasd
        self._pressed_keys: Set[int] = set()
        self._just_pressed: Set[int] = set()
        self._just_released: Set[int] = set()
        self._last_key: Optional[int] = None
    
    def process_key(self, key: Optional[int]) -> Optional[int]:
        """
        Process a key press and update internal state.
        
        Args:
            key: The key code from screen.get_input()
            
        Returns:
            Processed key code (with WASD mapping if enabled)
        """
        if key is None:
            return None
        
        # Apply WASD mapping if enabled
        if self.use_wasd and key in self.WASD_MAP:
            key = self.WASD_MAP[key]
        
        self._last_key = key
        
        # Track pressed keys
        if key not in self._pressed_keys:
            self._just_pressed.add(key)
        self._pressed_keys.add(key)
        
        return key
    
    def update(self):
        """Update input state (call once per frame)"""
        self._just_pressed.clear()
        self._just_released.clear()
    
    def clear(self):
        """Clear all input state"""
        self._pressed_keys.clear()
        self._just_pressed.clear()
        self._just_released.clear()
        self._last_key = None
    
    def is_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed"""
        return key in self._pressed_keys
    
    def is_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame"""
        return key in self._just_pressed
    
    @property
    def last_key(self) -> Optional[int]:
        """Get the last pressed key"""
        return self._last_key
    
    def is_direction_key(self, key: int) -> bool:
        """Check if a key is a direction key (arrow or WASD)"""
        return key in (Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT)
    
    def get_direction(self, key: int) -> tuple[int, int]:
        """
        Get direction vector for a direction key.
        
        Returns:
            (dx, dy) tuple where each is -1, 0, or 1
        """
        directions = {
            Keys.UP: (0, -1),
            Keys.DOWN: (0, 1),
            Keys.LEFT: (-1, 0),
            Keys.RIGHT: (1, 0),
        }
        return directions.get(key, (0, 0))

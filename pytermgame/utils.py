"""
Utils module - Utility functions and constants
"""

import random
from typing import Tuple, List


# Color constants (curses color pair numbers)
class Color:
    """Color pair numbers for curses"""
    DEFAULT = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


def random_position(
    min_x: int, max_x: int,
    min_y: int, max_y: int
) -> Tuple[int, int]:
    """
    Generate a random position within bounds.
    
    Returns:
        (x, y) tuple
    """
    return (
        random.randint(min_x, max_x - 1),
        random.randint(min_y, max_y - 1)
    )


def random_position_excluding(
    min_x: int, max_x: int,
    min_y: int, max_y: int,
    exclude: List[Tuple[int, int]],
    max_attempts: int = 100
) -> Tuple[int, int]:
    """
    Generate a random position that doesn't overlap with excluded positions.
    
    Args:
        min_x, max_x, min_y, max_y: Bounds
        exclude: List of (x, y) positions to avoid
        max_attempts: Maximum attempts before giving up
        
    Returns:
        (x, y) tuple, may overlap if max_attempts exceeded
    """
    for _ in range(max_attempts):
        pos = random_position(min_x, max_x, min_y, max_y)
        if pos not in exclude:
            return pos
    return random_position(min_x, max_x, min_y, max_y)


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b"""
    return a + (b - a) * t


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate distance between two points"""
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """Calculate Manhattan distance between two points"""
    return abs(x2 - x1) + abs(y2 - y1)


def sign(value: float) -> int:
    """Get the sign of a value (-1, 0, or 1)"""
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0


def center_text(text: str, width: int) -> str:
    """Center a text string within a given width"""
    if len(text) >= width:
        return text[:width]
    padding = (width - len(text)) // 2
    return ' ' * padding + text


def wrap_text(text: str, width: int) -> List[str]:
    """Wrap text to fit within a given width"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) <= width:
            current_line.append(word)
            current_length += len(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

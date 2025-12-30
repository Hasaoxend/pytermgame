"""
PyTermGame - A Python ASCII Game Engine for Terminal

A lightweight game engine for creating ASCII games in the terminal.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Lazy imports to avoid curses dependency issues during testing
def __getattr__(name):
    """Lazy import to handle missing curses gracefully."""
    if name == "Game":
        from .engine import Game
        return Game
    elif name == "SimpleGame":
        from .engine import SimpleGame
        return SimpleGame
    elif name == "Screen":
        from .screen import Screen
        return Screen
    elif name == "Entity":
        from .entities import Entity
        return Entity
    elif name == "Sprite":
        from .entities import Sprite
        return Sprite
    elif name == "EntityGroup":
        from .entities import EntityGroup
        return EntityGroup
    elif name == "InputHandler":
        from .input import InputHandler
        return InputHandler
    elif name == "Keys":
        from .input import Keys
        return Keys
    elif name == "check_collision":
        from .collision import check_collision
        return check_collision
    elif name == "point_in_rect":
        from .collision import point_in_rect
        return point_in_rect
    elif name == "Color":
        from .utils import Color
        return Color
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Game",
    "SimpleGame",
    "Screen", 
    "Entity",
    "Sprite",
    "EntityGroup",
    "InputHandler",
    "Keys",
    "check_collision",
    "point_in_rect",
    "Color",
]

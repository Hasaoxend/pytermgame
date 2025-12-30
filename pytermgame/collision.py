"""
Collision module - Collision detection utilities
"""

from typing import Tuple, Optional
from .entities import Entity


def check_collision(entity1: Entity, entity2: Entity) -> bool:
    """
    Check AABB collision between two entities.
    
    Args:
        entity1: First entity
        entity2: Second entity
        
    Returns:
        True if entities overlap
    """
    return entity1.collides_with(entity2)


def point_in_rect(px: int, py: int, rx: int, ry: int, rw: int, rh: int) -> bool:
    """
    Check if a point is inside a rectangle.
    
    Args:
        px, py: Point coordinates
        rx, ry: Rectangle top-left corner
        rw, rh: Rectangle width and height
        
    Returns:
        True if point is inside rectangle
    """
    return rx <= px < rx + rw and ry <= py < ry + rh


def rect_collision(
    x1: int, y1: int, w1: int, h1: int,
    x2: int, y2: int, w2: int, h2: int
) -> bool:
    """
    Check AABB collision between two rectangles.
    
    Args:
        x1, y1, w1, h1: First rectangle
        x2, y2, w2, h2: Second rectangle
        
    Returns:
        True if rectangles overlap
    """
    return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )


def check_bounds(
    x: int, y: int,
    min_x: int, min_y: int,
    max_x: int, max_y: int
) -> Tuple[bool, bool, bool, bool]:
    """
    Check if a point is outside bounds.
    
    Args:
        x, y: Point to check
        min_x, min_y: Minimum bounds
        max_x, max_y: Maximum bounds
        
    Returns:
        Tuple of (hit_left, hit_right, hit_top, hit_bottom)
    """
    return (
        x < min_x,   # hit left
        x >= max_x,  # hit right
        y < min_y,   # hit top
        y >= max_y   # hit bottom
    )


def is_out_of_bounds(
    x: int, y: int,
    min_x: int, min_y: int,
    max_x: int, max_y: int
) -> bool:
    """
    Check if a point is outside bounds.
    
    Returns:
        True if point is outside bounds
    """
    return x < min_x or x >= max_x or y < min_y or y >= max_y


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))


def clamp_to_bounds(
    x: int, y: int,
    min_x: int, min_y: int,
    max_x: int, max_y: int
) -> Tuple[int, int]:
    """
    Clamp a point to stay within bounds.
    
    Returns:
        Clamped (x, y) tuple
    """
    return (
        int(clamp(x, min_x, max_x - 1)),
        int(clamp(y, min_y, max_y - 1))
    )

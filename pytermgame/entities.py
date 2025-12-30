"""
Entities module - Game objects and sprites
"""

from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class Sprite:
    """
    ASCII sprite representation.
    
    A sprite is a multi-line ASCII art that can be drawn to the screen.
    """
    
    lines: List[str] = field(default_factory=list)
    color: int = 0
    
    @classmethod
    def from_string(cls, art: str, color: int = 0) -> 'Sprite':
        """
        Create a sprite from a multi-line string.
        
        Args:
            art: Multi-line ASCII art string
            color: Color pair number
            
        Returns:
            New Sprite instance
        """
        lines = art.strip('\n').split('\n')
        return cls(lines=lines, color=color)
    
    @classmethod
    def from_char(cls, char: str, color: int = 0) -> 'Sprite':
        """
        Create a single-character sprite.
        
        Args:
            char: Single character
            color: Color pair number
            
        Returns:
            New Sprite instance
        """
        return cls(lines=[char], color=color)
    
    @property
    def width(self) -> int:
        """Get sprite width"""
        return max(len(line) for line in self.lines) if self.lines else 0
    
    @property
    def height(self) -> int:
        """Get sprite height"""
        return len(self.lines)


@dataclass
class Entity:
    """
    Base class for all game entities.
    
    An entity has a position, velocity, and optional sprite.
    """
    
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    sprite: Optional[Sprite] = None
    active: bool = True
    tag: str = ""
    
    @property
    def ix(self) -> int:
        """Get integer X position"""
        return int(self.x)
    
    @property
    def iy(self) -> int:
        """Get integer Y position"""
        return int(self.y)
    
    @property
    def width(self) -> int:
        """Get entity width (from sprite or 1)"""
        return self.sprite.width if self.sprite else 1
    
    @property
    def height(self) -> int:
        """Get entity height (from sprite or 1)"""
        return self.sprite.height if self.sprite else 1
    
    @property
    def bounds(self) -> tuple[int, int, int, int]:
        """Get bounding box (x, y, width, height)"""
        return (self.ix, self.iy, self.width, self.height)
    
    def move(self, dx: float = 0, dy: float = 0):
        """Move entity by delta"""
        self.x += dx
        self.y += dy
    
    def move_to(self, x: float, y: float):
        """Move entity to position"""
        self.x = x
        self.y = y
    
    def update(self, dt: float = 1.0):
        """
        Update entity position based on velocity.
        
        Args:
            dt: Delta time (unused in simple games)
        """
        self.x += self.vx
        self.y += self.vy
    
    def set_velocity(self, vx: float, vy: float):
        """Set entity velocity"""
        self.vx = vx
        self.vy = vy
    
    def stop(self):
        """Stop entity movement"""
        self.vx = 0
        self.vy = 0
    
    def draw(self, screen: 'Screen'):
        """
        Draw entity to screen.
        
        Args:
            screen: Screen instance to draw to
        """
        if not self.active:
            return
            
        if self.sprite:
            for row, line in enumerate(self.sprite.lines):
                for col, char in enumerate(line):
                    if char != ' ':  # Skip transparent pixels
                        screen.draw_char(
                            self.ix + col,
                            self.iy + row,
                            char,
                            self.sprite.color
                        )
        else:
            # Default: draw a single character
            screen.draw_char(self.ix, self.iy, '█')
    
    def collides_with(self, other: 'Entity') -> bool:
        """
        Check collision with another entity (AABB).
        
        Args:
            other: Other entity to check
            
        Returns:
            True if entities overlap
        """
        return (
            self.ix < other.ix + other.width and
            self.ix + self.width > other.ix and
            self.iy < other.iy + other.height and
            self.iy + self.height > other.iy
        )
    
    def contains_point(self, px: int, py: int) -> bool:
        """
        Check if a point is inside the entity bounds.
        
        Args:
            px: Point X coordinate
            py: Point Y coordinate
            
        Returns:
            True if point is inside
        """
        return (
            self.ix <= px < self.ix + self.width and
            self.iy <= py < self.iy + self.height
        )


class EntityGroup:
    """
    A collection of entities for batch operations.
    """
    
    def __init__(self):
        self.entities: List[Entity] = []
    
    def add(self, entity: Entity) -> Entity:
        """Add an entity to the group"""
        self.entities.append(entity)
        return entity
    
    def remove(self, entity: Entity):
        """Remove an entity from the group"""
        if entity in self.entities:
            self.entities.remove(entity)
    
    def clear(self):
        """Remove all entities"""
        self.entities.clear()
    
    def update(self, dt: float = 1.0):
        """Update all active entities"""
        for entity in self.entities:
            if entity.active:
                entity.update(dt)
    
    def draw(self, screen: 'Screen'):
        """Draw all active entities"""
        for entity in self.entities:
            if entity.active:
                entity.draw(screen)
    
    def get_by_tag(self, tag: str) -> List[Entity]:
        """Get all entities with a specific tag"""
        return [e for e in self.entities if e.tag == tag]
    
    def remove_inactive(self):
        """Remove all inactive entities"""
        self.entities = [e for e in self.entities if e.active]
    
    def __iter__(self):
        return iter(self.entities)
    
    def __len__(self):
        return len(self.entities)

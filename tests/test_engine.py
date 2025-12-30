"""
Unit tests for PyTermGame engine.
"""

import pytest
from pytermgame.entities import Entity, Sprite, EntityGroup
from pytermgame.collision import (
    check_collision, 
    point_in_rect, 
    rect_collision,
    is_out_of_bounds,
    clamp
)
from pytermgame.utils import (
    random_position,
    center_text,
    manhattan_distance,
    sign
)


class TestEntity:
    """Tests for Entity class."""
    
    def test_entity_creation(self):
        """Test basic entity creation."""
        entity = Entity(x=10, y=20)
        assert entity.x == 10
        assert entity.y == 20
        assert entity.vx == 0
        assert entity.vy == 0
        assert entity.active is True
        
    def test_entity_integer_position(self):
        """Test integer position properties."""
        entity = Entity(x=10.5, y=20.7)
        assert entity.ix == 10
        assert entity.iy == 20
        
    def test_entity_move(self):
        """Test entity movement."""
        entity = Entity(x=10, y=10)
        entity.move(5, -3)
        assert entity.x == 15
        assert entity.y == 7
        
    def test_entity_velocity(self):
        """Test velocity-based movement."""
        entity = Entity(x=0, y=0, vx=2, vy=3)
        entity.update()
        assert entity.x == 2
        assert entity.y == 3
        
    def test_entity_stop(self):
        """Test stopping an entity."""
        entity = Entity(x=0, y=0, vx=5, vy=5)
        entity.stop()
        assert entity.vx == 0
        assert entity.vy == 0


class TestSprite:
    """Tests for Sprite class."""
    
    def test_sprite_from_char(self):
        """Test single character sprite."""
        sprite = Sprite.from_char('@')
        assert sprite.width == 1
        assert sprite.height == 1
        assert sprite.lines == ['@']
        
    def test_sprite_from_string(self):
        """Test multi-line sprite."""
        art = """
###
# #
###
"""
        sprite = Sprite.from_string(art)
        assert sprite.width == 3
        assert sprite.height == 3


class TestEntityGroup:
    """Tests for EntityGroup class."""
    
    def test_add_remove_entities(self):
        """Test adding and removing entities."""
        group = EntityGroup()
        e1 = Entity(x=0, y=0)
        e2 = Entity(x=10, y=10)
        
        group.add(e1)
        group.add(e2)
        assert len(group) == 2
        
        group.remove(e1)
        assert len(group) == 1
        
    def test_get_by_tag(self):
        """Test filtering by tag."""
        group = EntityGroup()
        group.add(Entity(tag="enemy"))
        group.add(Entity(tag="enemy"))
        group.add(Entity(tag="player"))
        
        enemies = group.get_by_tag("enemy")
        assert len(enemies) == 2


class TestCollision:
    """Tests for collision functions."""
    
    def test_entity_collision(self):
        """Test entity-to-entity collision."""
        e1 = Entity(x=0, y=0, sprite=Sprite.from_char('#'))
        e2 = Entity(x=0, y=0, sprite=Sprite.from_char('#'))
        assert check_collision(e1, e2) is True
        
        e2.move_to(10, 10)
        assert check_collision(e1, e2) is False
        
    def test_point_in_rect(self):
        """Test point-in-rectangle check."""
        assert point_in_rect(5, 5, 0, 0, 10, 10) is True
        assert point_in_rect(15, 15, 0, 0, 10, 10) is False
        assert point_in_rect(0, 0, 0, 0, 10, 10) is True
        assert point_in_rect(9, 9, 0, 0, 10, 10) is True
        assert point_in_rect(10, 10, 0, 0, 10, 10) is False
        
    def test_rect_collision(self):
        """Test rectangle-to-rectangle collision."""
        # Overlapping
        assert rect_collision(0, 0, 10, 10, 5, 5, 10, 10) is True
        # Not overlapping
        assert rect_collision(0, 0, 5, 5, 10, 10, 5, 5) is False
        # Adjacent (not overlapping)
        assert rect_collision(0, 0, 5, 5, 5, 0, 5, 5) is False
        
    def test_out_of_bounds(self):
        """Test bounds checking."""
        assert is_out_of_bounds(5, 5, 0, 0, 10, 10) is False
        assert is_out_of_bounds(-1, 5, 0, 0, 10, 10) is True
        assert is_out_of_bounds(10, 5, 0, 0, 10, 10) is True
        
    def test_clamp(self):
        """Test value clamping."""
        assert clamp(5, 0, 10) == 5
        assert clamp(-5, 0, 10) == 0
        assert clamp(15, 0, 10) == 10


class TestUtils:
    """Tests for utility functions."""
    
    def test_random_position(self):
        """Test random position generation."""
        for _ in range(100):
            x, y = random_position(0, 10, 0, 10)
            assert 0 <= x < 10
            assert 0 <= y < 10
            
    def test_center_text(self):
        """Test text centering."""
        result = center_text("hi", 10)
        assert len(result) >= len("hi")
        assert "hi" in result
        
    def test_manhattan_distance(self):
        """Test Manhattan distance."""
        assert manhattan_distance(0, 0, 3, 4) == 7
        assert manhattan_distance(5, 5, 5, 5) == 0
        
    def test_sign(self):
        """Test sign function."""
        assert sign(10) == 1
        assert sign(-10) == -1
        assert sign(0) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

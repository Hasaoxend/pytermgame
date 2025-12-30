"""
Snake Game - Classic snake game using PyTermGame engine.

Controls:
    - Arrow keys or WASD to move
    - Q or ESC to quit
    - R to restart after game over

Run with:
    python -m games.snake
"""

import random
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pytermgame.engine import Game
from pytermgame.input import Keys
from pytermgame.utils import Color, random_position_excluding

# Game constants
GAME_WIDTH = 60
GAME_HEIGHT = 20
PLAY_AREA_X = 2
PLAY_AREA_Y = 3
PLAY_WIDTH = GAME_WIDTH - 4
PLAY_HEIGHT = GAME_HEIGHT - 4

# Snake characters (ASCII compatible)
SNAKE_HEAD = '#'
SNAKE_BODY = 'O'
FOOD = '*'

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame(Game):
    """Classic Snake game implementation."""
    
    def __init__(self):
        super().__init__(
            width=GAME_WIDTH,
            height=GAME_HEIGHT,
            fps=8,  # Snake moves 8 times per second
            title="Snake Game"
        )
        
    def setup(self):
        """Initialize game state."""
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to initial state."""
        # Snake starts in the center
        center_x = PLAY_AREA_X + PLAY_WIDTH // 2
        center_y = PLAY_AREA_Y + PLAY_HEIGHT // 2
        
        # Snake body as list of (x, y) tuples, head is first
        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        
        # Initial direction
        self.direction = RIGHT
        self.next_direction = RIGHT
        
        # Game state
        self.score = 0
        self.high_score = getattr(self, 'high_score', 0)
        self.game_over = False
        self.paused = False
        
        # Vertical movement compensation (skip frames when moving up/down)
        self.vertical_frame_skip = 0
        
        # Boost mechanic - hold SPACE to go 2x speed but lose length
        self.boosting = False
        self.boost_frame_counter = 0
        self.MIN_SNAKE_LENGTH = 3  # Can't boost below this length
        
        # Spawn initial food
        self.spawn_food()
        
    def spawn_food(self):
        """Spawn food at a random position not occupied by snake."""
        self.food = random_position_excluding(
            PLAY_AREA_X, PLAY_AREA_X + PLAY_WIDTH,
            PLAY_AREA_Y, PLAY_AREA_Y + PLAY_HEIGHT,
            self.snake
        )
        
    def update(self, dt: float):
        """Update game logic."""
        if self.game_over:
            # Check for restart
            if self.is_key_pressed(Keys.R) or self.is_key_pressed(ord('r')):
                self.reset_game()
            return
            
        if self.paused:
            if self.is_key_pressed(Keys.P) or self.is_key_pressed(ord('p')):
                self.paused = False
            return
        
        # Check for boost - SPACE key activates boost if snake is long enough
        key = self.get_key()
        can_boost = len(self.snake) > self.MIN_SNAKE_LENGTH
        
        # Only boost if SPACE is pressed AND we can boost
        if key == Keys.SPACE:
            self.boosting = can_boost
            # Still allow movement while boosting - don't block other keys
        else:
            self.boosting = False
        
        # Handle input - change direction (process all keys including during boost)
        if key:
            new_dir = None
            if key in (Keys.UP, ord('w'), ord('W')):
                new_dir = UP
            elif key in (Keys.DOWN, ord('s'), ord('S')):
                new_dir = DOWN
            elif key in (Keys.LEFT, ord('a'), ord('A')):
                new_dir = LEFT
            elif key in (Keys.RIGHT, ord('d'), ord('D')):
                new_dir = RIGHT
            elif key in (Keys.P, ord('p')):
                self.paused = True
                return
                
            # Prevent 180-degree turns
            if new_dir:
                opposite = (-self.direction[0], -self.direction[1])
                if new_dir != opposite:
                    self.next_direction = new_dir
        
        # Apply direction change
        self.direction = self.next_direction
        
        # Skip every other frame when moving vertically (compensate for tall characters)
        # But don't skip if boosting
        is_vertical = self.direction in (UP, DOWN)
        if is_vertical and not self.boosting:
            self.vertical_frame_skip += 1
            if self.vertical_frame_skip % 2 == 0:
                return  # Skip this frame for vertical movement
        
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < PLAY_AREA_X or 
            new_head[0] >= PLAY_AREA_X + PLAY_WIDTH or
            new_head[1] < PLAY_AREA_Y or 
            new_head[1] >= PLAY_AREA_Y + PLAY_HEIGHT):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
            # Increase speed slightly every 50 points
            if self.score % 50 == 0 and self.target_fps < 15:
                self.target_fps += 1
        else:
            # Remove tail (snake doesn't grow)
            self.snake.pop()
            
        # Boost mechanic: shrink snake while boosting
        if self.boosting and len(self.snake) > self.MIN_SNAKE_LENGTH:
            self.boost_frame_counter += 1
            # Shrink every 3 frames while boosting
            if self.boost_frame_counter % 3 == 0:
                self.snake.pop()  # Remove extra tail segment
            
    def draw(self):
        """Draw the game."""
        # Draw border
        self.screen.draw_box(0, 0, GAME_WIDTH, GAME_HEIGHT, color=Color.CYAN)
        
        # Draw title bar
        title = " SNAKE GAME "
        self.screen.draw_text(
            (GAME_WIDTH - len(title)) // 2, 0,
            title,
            Color.GREEN
        )
        
        # Draw score
        score_text = f" Score: {self.score} "
        self.screen.draw_text(2, 1, score_text, Color.YELLOW)
        
        high_score_text = f" High: {self.high_score} "
        self.screen.draw_text(GAME_WIDTH - len(high_score_text) - 2, 1, high_score_text, Color.MAGENTA)
        
        # Draw separator
        self.screen.draw_hline(1, 2, GAME_WIDTH - 2, '-', Color.CYAN)
        
        # Draw play area border (inner)
        for x in range(PLAY_AREA_X - 1, PLAY_AREA_X + PLAY_WIDTH + 1):
            self.screen.draw_char(x, PLAY_AREA_Y - 1, '.', Color.BLUE)
            self.screen.draw_char(x, PLAY_AREA_Y + PLAY_HEIGHT, '.', Color.BLUE)
        for y in range(PLAY_AREA_Y, PLAY_AREA_Y + PLAY_HEIGHT):
            self.screen.draw_char(PLAY_AREA_X - 1, y, '.', Color.BLUE)
            self.screen.draw_char(PLAY_AREA_X + PLAY_WIDTH, y, '.', Color.BLUE)
        
        # Draw food
        self.screen.draw_char(self.food[0], self.food[1], FOOD, Color.RED)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                # Head - brighter color
                self.screen.draw_char(x, y, SNAKE_HEAD, Color.GREEN)
            else:
                # Body
                self.screen.draw_char(x, y, SNAKE_BODY, Color.GREEN)
        
        # Draw controls hint
        controls = "WASD:Move | SPACE:Boost | P:Pause | Q:Quit"
        self.screen.draw_text(
            (GAME_WIDTH - len(controls)) // 2,
            GAME_HEIGHT - 1,
            controls,
            Color.WHITE
        )
        
        # Draw boost indicator
        can_boost = len(self.snake) > self.MIN_SNAKE_LENGTH
        if self.boosting:
            boost_text = " BOOST! "
            self.screen.draw_text(GAME_WIDTH // 2 - 4, 1, boost_text, Color.RED)
        elif not can_boost:
            boost_text = " [NO BOOST] "
            self.screen.draw_text(GAME_WIDTH // 2 - 6, 1, boost_text, Color.BLUE)
        
        # Draw overlays
        if self.game_over:
            self._draw_game_over()
        elif self.paused:
            self._draw_paused()
            
    def _draw_game_over(self):
        """Draw game over overlay."""
        box_width = 28
        box_height = 7
        box_x = (GAME_WIDTH - box_width) // 2
        box_y = (GAME_HEIGHT - box_height) // 2
        
        # Clear area
        self.screen.fill_rect(box_x, box_y, box_width, box_height, ' ')
        
        # Draw box
        self.screen.draw_box(box_x, box_y, box_width, box_height, color=Color.RED)
        
        # Draw text
        self.screen.draw_text(box_x + 8, box_y + 2, "GAME OVER!", Color.RED)
        self.screen.draw_text(box_x + 4, box_y + 4, f"Final Score: {self.score}", Color.YELLOW)
        self.screen.draw_text(box_x + 3, box_y + 5, "Press R to Restart", Color.WHITE)
        
    def _draw_paused(self):
        """Draw pause overlay."""
        box_width = 22
        box_height = 5
        box_x = (GAME_WIDTH - box_width) // 2
        box_y = (GAME_HEIGHT - box_height) // 2
        
        self.screen.fill_rect(box_x, box_y, box_width, box_height, ' ')
        self.screen.draw_box(box_x, box_y, box_width, box_height, color=Color.YELLOW)
        self.screen.draw_text(box_x + 7, box_y + 2, "PAUSED", Color.YELLOW)
        self.screen.draw_text(box_x + 2, box_y + 3, "Press P to Resume", Color.WHITE)
        
    def on_quit(self) -> bool:
        """Handle quit - ask for confirmation if in game."""
        if self.game_over:
            return True
        return True


def main():
    """Entry point for the Snake game."""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

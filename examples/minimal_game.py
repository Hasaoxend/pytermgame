"""
Minimal example game using PyTermGame.

This shows the simplest possible game using the engine.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytermgame.engine import Game
from pytermgame.input import Keys
from pytermgame.utils import Color


class MinimalGame(Game):
    """A minimal game example - move a character around the screen."""
    
    def __init__(self):
        super().__init__(width=40, height=15, fps=15, title="Minimal Example")
        
    def setup(self):
        """Initialize player position."""
        self.player_x = self.width // 2
        self.player_y = self.height // 2
        
    def update(self, dt: float):
        """Handle input and move player."""
        key = self.get_key()
        
        if key == Keys.UP and self.player_y > 1:
            self.player_y -= 1
        elif key == Keys.DOWN and self.player_y < self.height - 2:
            self.player_y += 1
        elif key == Keys.LEFT and self.player_x > 1:
            self.player_x -= 1
        elif key == Keys.RIGHT and self.player_x < self.width - 2:
            self.player_x += 1
            
    def draw(self):
        """Draw the game."""
        # Draw border
        self.screen.draw_box(0, 0, self.width, self.height, 
                            title="Minimal Game", color=Color.CYAN)
        
        # Draw player
        self.screen.draw_char(self.player_x, self.player_y, '@', Color.GREEN)
        
        # Draw instructions
        self.screen.draw_text(2, self.height - 2, "Arrow keys to move, Q to quit", Color.WHITE)


if __name__ == "__main__":
    MinimalGame().run()

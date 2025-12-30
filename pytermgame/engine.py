"""
Engine module - Core game engine and game loop

Supports both curses (if available) and ANSI fallback mode.
"""

import time
import sys
import os
from typing import Callable, Optional, Dict, Any
from abc import ABC, abstractmethod

from .screen import Screen
from .input import InputHandler, Keys

# Try to import curses
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False

# Windows keyboard input fallback
try:
    import msvcrt
    MSVCRT_AVAILABLE = True
except ImportError:
    MSVCRT_AVAILABLE = False


class Game(ABC):
    """
    Abstract base class for games.
    
    Subclass this and implement the abstract methods to create a game.
    
    Example:
        class MyGame(Game):
            def setup(self):
                self.player_x = 10
                
            def update(self, dt):
                if self.is_key_pressed(Keys.RIGHT):
                    self.player_x += 1
                    
            def draw(self):
                self.screen.draw_char(self.player_x, 5, '@')
        
        if __name__ == "__main__":
            MyGame(width=80, height=24).run()
    """
    
    def __init__(
        self,
        width: int = 80,
        height: int = 24,
        fps: int = 15,
        title: str = "PyTermGame"
    ):
        """
        Initialize the game engine.
        
        Args:
            width: Screen width in characters
            height: Screen height in characters
            fps: Target frames per second (lower = slower)
            title: Game window title (for future use)
        """
        self.width = width
        self.height = height
        self.target_fps = fps
        self.title = title
        
        self.screen = Screen(width, height)
        self.input = InputHandler(use_wasd=True)
        
        self._running = False
        self._current_key: Optional[int] = None
        self._frame_count = 0
        self._start_time = 0.0
        self._dt = 0.0
        
        # Game state storage
        self.state: Dict[str, Any] = {}
    
    def run(self):
        """
        Start the game loop.
        
        Uses curses if available, otherwise falls back to ANSI mode.
        """
        if CURSES_AVAILABLE:
            curses.wrapper(self._main_loop_curses)
        else:
            self._main_loop_ansi()
    
    def _main_loop_curses(self, stdscr):
        """Main game loop using curses"""
        # Initialize screen with curses
        self.screen.init_curses(stdscr)
        self._run_loop()
    
    def _main_loop_ansi(self):
        """Main game loop using ANSI escape codes (fallback)"""
        # Hide cursor and clear screen
        sys.stdout.write("\033[?25l")  # Hide cursor
        sys.stdout.write("\033[2J")    # Clear screen
        sys.stdout.flush()
        
        try:
            self._run_loop()
        finally:
            # Show cursor again
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
    
    def _run_loop(self):
        """Common game loop logic"""
        self._running = True
        self._start_time = time.time()
        
        # Call user setup
        self.setup()
        
        frame_time = 1.0 / self.target_fps
        last_time = time.time()
        
        while self._running:
            current_time = time.time()
            self._dt = current_time - last_time
            
            # Process input
            raw_key = self._get_input()
            self._current_key = self.input.process_key(raw_key)
            
            # Check for quit
            if self._current_key == Keys.Q or self._current_key == Keys.ESCAPE:
                if self.on_quit():
                    break
            
            # Update game state
            self.update(self._dt)
            
            # Clear and draw
            self.screen.clear()
            self.draw()
            
            # Refresh screen
            self.screen.refresh()
            
            # Update input state
            self.input.update()
            self._current_key = None
            
            # Frame timing
            elapsed = time.time() - current_time
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)
            
            last_time = current_time
            self._frame_count += 1
    
    def _get_input(self) -> Optional[int]:
        """Get keyboard input based on available backend"""
        # Try curses first
        key = self.screen.get_input()
        if key is not None:
            return key
        
        # Fall back to msvcrt on Windows
        if MSVCRT_AVAILABLE and msvcrt.kbhit():
            ch = msvcrt.getch()
            # Handle arrow keys (they send 2 bytes)
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                arrow_map = {
                    b'H': Keys.UP,
                    b'P': Keys.DOWN,
                    b'K': Keys.LEFT,
                    b'M': Keys.RIGHT,
                }
                return arrow_map.get(ch2)
            return ord(ch)
        
        return None
    
    def quit(self):
        """Exit the game loop"""
        self._running = False
    
    def on_quit(self) -> bool:
        """
        Called when user presses Q or ESC.
        
        Override to customize quit behavior.
        
        Returns:
            True to quit, False to cancel
        """
        return True
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a specific key was pressed this frame"""
        return self._current_key == key
    
    def get_key(self) -> Optional[int]:
        """Get the current key press (or None)"""
        return self._current_key
    
    @property
    def frame_count(self) -> int:
        """Get current frame number"""
        return self._frame_count
    
    @property
    def elapsed_time(self) -> float:
        """Get elapsed time since game start"""
        return time.time() - self._start_time
    
    @property
    def delta_time(self) -> float:
        """Get time since last frame"""
        return self._dt
    
    # Abstract methods - must be implemented by subclasses
    
    @abstractmethod
    def setup(self):
        """
        Initialize game state.
        
        Called once before the game loop starts.
        Override to set up your game.
        """
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """
        Update game logic.
        
        Called every frame.
        
        Args:
            dt: Time since last frame in seconds
        """
        pass
    
    @abstractmethod
    def draw(self):
        """
        Draw the game.
        
        Called every frame after update.
        Use self.screen to draw.
        """
        pass


class SimpleGame(Game):
    """
    A simplified game class using callbacks instead of subclassing.
    
    Example:
        game = SimpleGame(width=80, height=24)
        
        @game.on_setup
        def setup():
            game.state['x'] = 10
        
        @game.on_update
        def update(dt):
            if game.is_key_pressed(Keys.RIGHT):
                game.state['x'] += 1
        
        @game.on_draw
        def draw():
            game.screen.draw_char(game.state['x'], 5, '@')
        
        game.run()
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_fn: Optional[Callable] = None
        self._update_fn: Optional[Callable] = None
        self._draw_fn: Optional[Callable] = None
    
    def on_setup(self, fn: Callable):
        """Decorator to set the setup function"""
        self._setup_fn = fn
        return fn
    
    def on_update(self, fn: Callable):
        """Decorator to set the update function"""
        self._update_fn = fn
        return fn
    
    def on_draw(self, fn: Callable):
        """Decorator to set the draw function"""
        self._draw_fn = fn
        return fn
    
    def setup(self):
        if self._setup_fn:
            self._setup_fn()
    
    def update(self, dt: float):
        if self._update_fn:
            self._update_fn(dt)
    
    def draw(self):
        if self._draw_fn:
            self._draw_fn()

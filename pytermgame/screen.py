"""
Screen module - Terminal rendering and buffer management

Supports both curses and ANSI escape codes.
"""

import os
import sys
from typing import Optional

# Try to import curses (works on Windows with windows-curses)
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False
    curses = None  # type: ignore


# ANSI color codes
class ANSIColors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    COLORS = [
        "",           # 0 - default
        "\033[91m",   # 1 - red
        "\033[92m",   # 2 - green
        "\033[93m",   # 3 - yellow
        "\033[94m",   # 4 - blue
        "\033[95m",   # 5 - magenta
        "\033[96m",   # 6 - cyan
        "\033[97m",   # 7 - white
    ]


class Screen:
    """
    Screen class for terminal rendering.
    
    Manages a character buffer and handles drawing operations.
    Uses curses when available, falls back to ANSI escape codes.
    """
    
    def __init__(self, width: int = 80, height: int = 24):
        """
        Initialize a new screen.
        
        Args:
            width: Screen width in characters
            height: Screen height in characters
        """
        self.width = width
        self.height = height
        self._buffer: list[list[str]] = []
        self._color_buffer: list[list[int]] = []
        self._stdscr = None
        self._curses_mode = False
        self._clear_buffer()
        
    def _clear_buffer(self):
        """Clear the internal buffer"""
        self._buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self._color_buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
    
    def init_curses(self, stdscr) -> 'Screen':
        """
        Initialize curses mode with the given screen.
        
        Args:
            stdscr: curses screen object
            
        Returns:
            self for chaining
        """
        if not CURSES_AVAILABLE:
            return self
            
        self._stdscr = stdscr
        self._curses_mode = True
        
        # Setup curses
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True)  # Non-blocking input
        stdscr.keypad(True)  # Enable special keys
        
        # Initialize color pairs
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            # Define color pairs: pair_number, foreground, background
            curses.init_pair(1, curses.COLOR_RED, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            curses.init_pair(4, curses.COLOR_BLUE, -1)
            curses.init_pair(5, curses.COLOR_MAGENTA, -1)
            curses.init_pair(6, curses.COLOR_CYAN, -1)
            curses.init_pair(7, curses.COLOR_WHITE, -1)
        
        return self
    
    def clear(self):
        """Clear the screen buffer"""
        self._clear_buffer()
        if self._curses_mode and self._stdscr:
            self._stdscr.clear()
    
    def draw_char(self, x: int, y: int, char: str, color: int = 0):
        """
        Draw a single character at the specified position.
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            char: Character to draw
            color: Color pair number (0-7)
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self._buffer[y][x] = char[0] if char else ' '
            self._color_buffer[y][x] = color
    
    def draw_text(self, x: int, y: int, text: str, color: int = 0):
        """
        Draw a text string at the specified position.
        
        Args:
            x: Starting X coordinate
            y: Y coordinate
            text: Text to draw
            color: Color pair number
        """
        for i, char in enumerate(text):
            if x + i < self.width:
                self.draw_char(x + i, y, char, color)
    
    def draw_box(self, x: int, y: int, width: int, height: int, 
                 title: str = "", color: int = 0):
        """
        Draw a bordered box.
        
        Args:
            x: Top-left X coordinate
            y: Top-left Y coordinate
            width: Box width
            height: Box height
            title: Optional title for the box
            color: Color pair number
        """
        # Box drawing characters (ASCII fallback for compatibility)
        TOP_LEFT = '+'
        TOP_RIGHT = '+'
        BOTTOM_LEFT = '+'
        BOTTOM_RIGHT = '+'
        HORIZONTAL = '-'
        VERTICAL = '|'
        
        # Draw corners
        self.draw_char(x, y, TOP_LEFT, color)
        self.draw_char(x + width - 1, y, TOP_RIGHT, color)
        self.draw_char(x, y + height - 1, BOTTOM_LEFT, color)
        self.draw_char(x + width - 1, y + height - 1, BOTTOM_RIGHT, color)
        
        # Draw horizontal lines
        for i in range(1, width - 1):
            self.draw_char(x + i, y, HORIZONTAL, color)
            self.draw_char(x + i, y + height - 1, HORIZONTAL, color)
        
        # Draw vertical lines
        for i in range(1, height - 1):
            self.draw_char(x, y + i, VERTICAL, color)
            self.draw_char(x + width - 1, y + i, VERTICAL, color)
        
        # Draw title if provided
        if title:
            title_text = f" {title} "
            title_x = x + (width - len(title_text)) // 2
            self.draw_text(title_x, y, title_text, color)
    
    def draw_hline(self, x: int, y: int, length: int, char: str = '-', color: int = 0):
        """Draw a horizontal line"""
        for i in range(length):
            self.draw_char(x + i, y, char, color)
    
    def draw_vline(self, x: int, y: int, length: int, char: str = '|', color: int = 0):
        """Draw a vertical line"""
        for i in range(length):
            self.draw_char(x, y + i, char, color)
    
    def fill_rect(self, x: int, y: int, width: int, height: int, 
                  char: str = ' ', color: int = 0):
        """Fill a rectangular area with a character"""
        for row in range(height):
            for col in range(width):
                self.draw_char(x + col, y + row, char, color)
    
    def refresh(self):
        """Push the buffer to the terminal"""
        if self._curses_mode and self._stdscr:
            self._refresh_curses()
        else:
            self._refresh_ansi()
    
    def _refresh_curses(self):
        """Refresh using curses"""
        if not CURSES_AVAILABLE:
            return
        for y in range(self.height):
            for x in range(self.width):
                char = self._buffer[y][x]
                color = self._color_buffer[y][x]
                try:
                    if color > 0:
                        self._stdscr.addch(y, x, char, curses.color_pair(color))
                    else:
                        self._stdscr.addch(y, x, char)
                except:
                    # Ignore errors when writing to last cell
                    pass
        self._stdscr.refresh()
    
    def _refresh_ansi(self):
        """Refresh using ANSI escape codes (fallback)"""
        # Move cursor to home position
        sys.stdout.write("\033[H")
        
        output = []
        for y, row in enumerate(self._buffer):
            line_parts = []
            current_color = -1
            
            for x, char in enumerate(row):
                color = self._color_buffer[y][x]
                if color != current_color:
                    if color > 0 and color < len(ANSIColors.COLORS):
                        line_parts.append(ANSIColors.COLORS[color])
                    else:
                        line_parts.append(ANSIColors.RESET)
                    current_color = color
                line_parts.append(char)
            
            line_parts.append(ANSIColors.RESET)
            output.append(''.join(line_parts))
        
        sys.stdout.write('\n'.join(output))
        sys.stdout.flush()
    
    def get_input(self) -> Optional[int]:
        """
        Get keyboard input (non-blocking).
        
        Returns:
            Key code or None if no input
        """
        if self._curses_mode and self._stdscr:
            try:
                key = self._stdscr.getch()
                return key if key != -1 else None
            except:
                return None
        return None
    
    @property
    def center_x(self) -> int:
        """Get X coordinate of screen center"""
        return self.width // 2
    
    @property
    def center_y(self) -> int:
        """Get Y coordinate of screen center"""
        return self.height // 2

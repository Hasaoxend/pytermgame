# 🐍 PyTermGame

<div align="center">

**A lightweight Python ASCII game engine for terminal**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Create retro ASCII games that run directly in your terminal!*

</div>

---

## ✨ Features

- 🎮 **Simple Game Loop** - Easy update/draw cycle
- ⌨️ **Input Handling** - Arrow keys, WASD support
- 🎨 **ANSI Colors** - Works without curses on Windows
- 📦 **Entity System** - Sprites, entities, collision
- 🚀 **No Dependencies** - Pure Python 3.10+

---

## 🎮 Demo: Snake Game

```
+----------------------- SNAKE GAME -----------------------+
|  Score: 50     BOOST!                      High: 120     |
|..........................................................|
|.                                                        .|
|.       OOOO#                                            .|
|.                                      *                 .|
+--WASD:Move | SPACE:Boost | P:Pause | Q:Quit-------------+
```

### Controls
- `W/A/S/D` or Arrow keys - Move
- `SPACE` - **Boost** (2x speed, shrinks snake!)
- `P` - Pause
- `Q` - Quit
- `R` - Restart (after game over)

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/yourusername/pytermgame.git
cd pytermgame

# Run Snake game (no install needed!)
python -m games.snake
```

---

## 📖 Create Your Own Game

```python
from pytermgame.engine import Game
from pytermgame.input import Keys
from pytermgame.utils import Color

class MyGame(Game):
    def setup(self):
        self.x = self.width // 2
        self.y = self.height // 2
        
    def update(self, dt):
        key = self.get_key()
        if key == Keys.UP: self.y -= 1
        if key == Keys.DOWN: self.y += 1
        if key == Keys.LEFT: self.x -= 1
        if key == Keys.RIGHT: self.x += 1
            
    def draw(self):
        self.screen.draw_box(0, 0, self.width, self.height, "My Game")
        self.screen.draw_char(self.x, self.y, '@', Color.GREEN)

if __name__ == "__main__":
    MyGame(width=40, height=20, fps=15).run()
```

---

## 📁 Project Structure

```
pytermgame/
├── pytermgame/      # Core engine
│   ├── engine.py    # Game loop
│   ├── screen.py    # Rendering
│   ├── input.py     # Keyboard
│   ├── entities.py  # Sprites
│   └── collision.py # Physics
├── games/snake/     # Snake demo
├── examples/        # Code samples
└── tests/           # Unit tests
```

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ and Python**

</div>

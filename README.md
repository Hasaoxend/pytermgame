# 🐍 PyTermGame - ASCII Game Engine

<div align="center">

**Build retro terminal games with pure Python!**  
*Tạo game terminal retro với Python thuần!*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey?style=for-the-badge)](/)

</div>

---

## 📋 Table of Contents / Mục lục

1. [About / Giới thiệu](#-about--giới-thiệu)
2. [Technology / Công nghệ](#️-technology--công-nghệ)
3. [Installation / Cài đặt](#-installation--cài-đặt)
4. [Demo](#-demo)

---

## 🎯 About / Giới thiệu

**EN:** PyTermGame is a lightweight game engine for creating ASCII games that run directly in the terminal. Designed to be simple, dependency-free, and cross-platform.

**VI:** PyTermGame là một game engine nhẹ để tạo các game ASCII chạy trực tiếp trong terminal. Được thiết kế đơn giản, không phụ thuộc, và đa nền tảng.

### Features / Tính năng

| Feature | Description / Mô tả |
|---------|---------------------|
| 🎮 **Game Loop** | Adjustable FPS game loop / Vòng lặp game với FPS tùy chỉnh |
| ⌨️ **Input** | Arrow keys, WASD support / Hỗ trợ Arrow keys, WASD |
| 🎨 **Colors** | ANSI terminal colors / Màu sắc ANSI terminal |
| 📦 **Entities** | Entity/Sprite system / Hệ thống Entity/Sprite |
| 💥 **Collision** | AABB collision detection / Phát hiện va chạm AABB |
| 🖥️ **No Dependencies** | Pure Python 3.10+ / Python thuần 3.10+ |

---

## 🛠️ Technology / Công nghệ

### Architecture / Kiến trúc

```
┌─────────────────────────────────────────┐
│              Game (Abstract)            │
│  ┌─────────┬──────────┬──────────────┐  │
│  │ setup() │ update() │    draw()    │  │
│  └────┬────┴────┬─────┴───────┬──────┘  │
│       │         │             │         │
│  ┌────▼─────────▼─────────────▼──────┐  │
│  │           Game Loop               │  │
│  │  while running:                   │  │
│  │    input → update → draw → sleep  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
           │           │           │
    ┌──────▼───┐ ┌─────▼────┐ ┌────▼─────┐
    │  Screen  │ │  Input   │ │ Entities │
    └──────────┘ └──────────┘ └──────────┘
```

### Core Modules / Các module chính

| Module | Description / Mô tả |
|--------|---------------------|
| `engine.py` | Game loop, lifecycle / Vòng lặp game |
| `screen.py` | Terminal rendering / Hiển thị terminal |
| `input.py` | Keyboard input / Đầu vào bàn phím |
| `entities.py` | Sprites, entities / Đối tượng game |
| `collision.py` | Collision detection / Phát hiện va chạm |

### Tech Stack

- **Language:** Python 3.10+
- **Rendering:** ANSI Escape Codes
- **Input:** `msvcrt` (Windows) / `curses` (Unix)
- **Dependencies:** None / Không có

---

## 📦 Installation / Cài đặt

### Requirements / Yêu cầu
- Python 3.10+
- ANSI-compatible terminal

### Setup / Thiết lập

```bash
# Clone repository
git clone https://github.com/Hasaoxend/pytermgame.git
cd pytermgame

# Run Snake game / Chạy game Snake
python -m games.snake
```

### Controls / Điều khiển

| Key / Phím | Function / Chức năng |
|------------|----------------------|
| `W` `A` `S` `D` / `↑` `←` `↓` `→` | Move / Di chuyển |
| `SPACE` | Boost 2x speed (shrinks snake) / Tăng tốc 2x (rắn ngắn dần) |
| `P` | Pause / Tạm dừng |
| `R` | Restart / Chơi lại |
| `Q` | Quit / Thoát |

### Create Your Own Game / Tạo game riêng

```python
from pytermgame.engine import Game
from pytermgame.input import Keys
from pytermgame.utils import Color

class MyGame(Game):
    def setup(self):
        self.x, self.y = self.width // 2, self.height // 2
        
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

## 🎮 Demo

### Snake Game

```
+----------------------- SNAKE GAME -----------------------+
|  Score: 120            BOOST!                 High: 250  |
|..........................................................|
|.                                                        .|
|.       OOOOOOO                                          .|
|.             O                                          .|
|.             OOOOO#                         *           .|
|.                                                        .|
+---WASD:Move | SPACE:Boost | P:Pause | Q:Quit------------+
```

### Game Over

```
+----------------------- SNAKE GAME -----------------------+
|                 +----------------------------+           |
|                 |        GAME OVER!          |           |
|                 |    Final Score: 180        |           |
|                 |   Press R to Restart       |           |
|                 +----------------------------+           |
+----------------------------------------------------------+
```

### Gameplay

- 🐍 **Classic Snake** - Move, eat, avoid collision / Di chuyển, ăn, tránh va chạm
- 🚀 **Boost Mode** - 2x speed, snake shrinks / Tốc độ 2x, rắn ngắn dần
- 📊 **High Score** - Saved per session / Lưu trong phiên

---

## 📁 Project Structure / Cấu trúc

```
pytermgame/
├── pytermgame/       # Core engine
├── games/snake/      # Snake demo
├── examples/         # Code samples
└── tests/            # Unit tests
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

<div align="center">

**Made with ❤️ and Python**

⭐ Star if you like it! / ⭐ Star nếu thấy hay!

</div>

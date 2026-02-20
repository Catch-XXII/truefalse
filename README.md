# TrueFalse - A Fun Math True/False Game

A fast-paced CLI game that tests your quick thinking with math equations. Answer whether each equation is true or false, compete on the leaderboard, and challenge yourself with three difficulty levels.

## 🎮 Features

- **Multi-difficulty gameplay**: Easy (5 Q's), Medium (9 Q's), Hard (15 Q's)
- **Persistent scoring**: Leaderboard and game history tracked in SQLite
- **Player profiles**: Create profiles or login to track your stats
- **Colored output**: Beautiful terminal UI with colorama
- **Smart menu system**: Easy navigation with multiple game modes
- **Session persistence**: Your progress is saved automatically

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd truefalse

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"  # Full install with dev tools
# OR just the base dependencies:
pip install colorama
```

### Playing the Game

```bash
python main.py
```

## 📋 How to Play

1. **Create or login** to your player profile
2. **Select difficulty**: Easy, Medium, or Hard
3. **Answer questions**: You'll see equations like `45<67` - answer True or False
4. **Get points**: 
   - Correct answers award points (varies by difficulty)
   - Wrong answers deduct points (minimum 0)
5. **Check leaderboard**: See how you rank against other players
6. **View stats**: Track your personal game history

### Scoring

| Difficulty | Questions | Points/Correct | Penalty/Wrong |
|-----------|-----------|----------------|--------------|
| Easy      | 5         | 10             | 5            |
| Medium    | 9         | 5              | 5            |
| Hard      | 15        | 3              | 2            |

## 📊 Project Structure

```
truefalse/
├── config.py              # Game configuration and difficulty levels
├── const.py               # Constants (regex patterns, DB name)
├── main.py                # Main entry point and game loop
├── player.py              # Player model (moved to models/player.py)
├── game/
│   ├── __init__.py
│   ├── question.py        # Question generation and validation
│   └── engine.py          # GameEngine class - core game logic
├── models/
│   ├── __init__.py
│   ├── player.py          # Player data model
│   └── game_result.py     # GameResult model for tracking games
├── db/
│   ├── __init__.py        # Database initialization and setup
│   └── operations.py      # PlayerRepository and GameResultRepository
├── ui/
│   ├── __init__.py
│   ├── display.py         # Colored output functions
│   └── prompts.py         # User input prompts and validation
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures
│   ├── test_game_engine.py
│   ├── test_player.py
│   ├── test_db_operations.py
│   └── test_integration.py
├── game.db                # SQLite database (auto-created on first run)
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html

# Run specific test file
python -m pytest tests/test_game_engine.py -v
```

## 💻 Development

### Type Checking

```bash
mypy . --ignore-missing-imports
```

### Code Formatting

```bash
# Format code
black .

# Sort imports
isort .
```

### Add New Features

See `docs/DEVELOPER_GUIDE.md` for architectural patterns and guidelines.

## 📚 Documentation

- **USER_GUIDE.md** - Detailed gameplay rules and tips
- **ARCHITECTURE.md** - System design and module relationships
- **DEVELOPER_GUIDE.md** - Contributing and development setup

## 🗄️ Database

The game uses SQLite with two main tables:

### `player` table
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `email` (TEXT UNIQUE)
- `age` (INTEGER)
- `phone` (TEXT UNIQUE)
- `score` (INTEGER)
- `duration` (REAL)
- `date` (TIMESTAMP)

### `game_session` table
- `id` (INTEGER PRIMARY KEY)
- `player_id` (INTEGER FK)
- `difficulty` (TEXT)
- `score` (INTEGER)
- `max_score` (INTEGER)
- `duration` (REAL)
- `created_at` (TIMESTAMP)

The database is created automatically on first run.

## 🐛 Troubleshooting

**Q: Game crashes on start**
- A: Ensure you have Python 3.13+
- Try: `python --version`

**Q: "No module named colorama"**
- A: Install dependencies: `pip install colorama`

**Q: Database errors**
- A: Delete `game.db` and restart to rebuild it

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! See DEVELOPER_GUIDE.md for setup instructions.

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-20  
**Python Version:** 3.13+


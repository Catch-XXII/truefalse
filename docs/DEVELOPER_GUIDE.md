# TrueFalse Developer Guide

## Architecture Overview

TrueFalse follows a clean architecture with separation of concerns:

### Layers

1. **UI Layer** (`ui/`)
   - `display.py`: Colored output and formatting
   - `prompts.py`: User input and validation
   - Responsibility: All user interaction

2. **Business Logic** (`game/`)
   - `engine.py`: Game state and scoring
   - `question.py`: Question generation
   - Responsibility: Game mechanics

3. **Data Models** (`models/`)
   - `player.py`: Player information
   - `game_result.py`: Game outcome tracking
   - Responsibility: Data representation

4. **Data Access** (`db/`)
   - `operations.py`: Repositories for data access
   - `__init__.py`: Database initialization
   - Responsibility: Persistence and queries

5. **Configuration** (`config.py`, `const.py`)
   - Centralized settings and constants
   - Responsibility: Configuration management

6. **Entry Point** (`main.py`)
   - `GameApp`: Orchestrates all layers
   - Responsibility: Application flow

### Design Patterns Used

- **Repository Pattern**: `PlayerRepository`, `GameResultRepository` isolate data access
- **Dependency Injection**: Dependencies passed to constructors, not hard-coded
- **Factory Pattern**: `GameEngine` factory for creating game sessions
- **Strategy Pattern**: Different difficulty levels implement scoring strategies
- **MVC-inspired**: Models (Player, GameResult), Views (UI), Controllers (GameApp)

## Setting Up Development Environment

### Prerequisites

- Python 3.13+
- pip or uv package manager

### Installation

```bash
# Clone repository
git clone <url>
cd truefalse

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
# OR with uv:
uv add pytest pytest-cov mypy black isort --dev
```

## Running Tests

### Basic Test Run

```bash
python -m pytest tests/ -v
```

### With Coverage Report

```bash
python -m pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

### Run Specific Tests

```bash
# Test a specific file
python -m pytest tests/test_game_engine.py -v

# Test a specific class
python -m pytest tests/test_game_engine.py::TestQuestion -v

# Test a specific function
python -m pytest tests/test_game_engine.py::TestQuestion::test_question_string_representation -v
```

### Test Markers

```bash
# Run only unit tests
python -m pytest -m unit

# Run only integration tests
python -m pytest -m integration
```

## Code Quality

### Type Checking

```bash
mypy . --ignore-missing-imports
```

Fix type errors before committing:

```bash
# Check types
mypy .

# Fix obvious issues
mypy . --warn-unused-ignores
```

### Code Formatting

```bash
# Format all code
black .

# Check what would be formatted
black . --check

# Sort imports
isort .
```

### Linting

```bash
# Format and check
black . --check
isort . --check-only
```

## Adding New Features

### Feature Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Add tests first** (TDD approach)
   - Add test file in `tests/test_your_feature.py`
   - Write failing tests

3. **Implement feature**
   - Write code to pass tests
   - Follow SOLID principles

4. **Type check and format**
   ```bash
   mypy .
   black .
   isort .
   ```

5. **Run full test suite**
   ```bash
   pytest tests/ -v
   ```

6. **Commit with clear message**
   ```bash
   git commit -m "feat: add your feature description"
   ```

### Code Style Guidelines

- **Type Hints**: All functions should have type hints
- **Docstrings**: All public classes/functions should have docstrings
- **Comments**: Comment *why*, not *what* the code does
- **Line Length**: Max 100 characters (black default)
- **Imports**: Use absolute imports, organize with isort

### Example: Adding a New Difficulty Level

1. **Update config.py**
   ```python
   EXTREME: Final[DifficultyLevel] = DifficultyLevel(
       name="Extreme",
       num_questions=20,
       score_per_correct=2,
       score_penalty=1,
   )
   ```

2. **Update DIFFICULTY_LEVELS dict**
   ```python
   DIFFICULTY_LEVELS["extreme"] = EXTREME
   ```

3. **Update ui/prompts.py**
   ```python
   options = ["Easy", "Medium", "Hard", "Extreme"]
   difficulties = ["easy", "medium", "hard", "extreme"]
   ```

4. **Write tests** in `tests/test_game_engine.py`
5. **Run full test suite** to ensure nothing breaks

## Database Operations

### Schema Overview

#### player table
```sql
CREATE TABLE player(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    score INTEGER NOT NULL,
    duration REAL NOT NULL,
    date TIMESTAMP NOT NULL
);
```

#### game_session table
```sql
CREATE TABLE game_session(
    id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    difficulty TEXT NOT NULL,
    score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,
    duration REAL NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY(player_id) REFERENCES player(id)
);
```

### Using Repositories

```python
from db import create_sqlite_database
from db.operations import PlayerRepository, GameResultRepository

# Create connection
conn = create_sqlite_database("game.db")

# Use player repository
player_repo = PlayerRepository(conn)
player_id = player_repo.insert_player(
    name="John", 
    email="john@example.com",
    age=30,
    phone="555-1234",
    date=datetime.now()
)

# Use game result repository
result_repo = GameResultRepository(conn)
results = result_repo.get_leaderboard(limit=10)
```

## Troubleshooting Development Issues

### Import Errors

If you get import errors, ensure:
1. You're in the project root: `pwd` should show `truefalse`
2. Virtual environment is activated
3. Package is installed: `pip install -e .`

### Type Errors

```bash
# See all type errors
mypy .

# Ignore specific errors (last resort)
# Add comment: # type: ignore
```

### Database Lock Errors

```python
# Ensure connections are closed
from db import close_connection
close_connection(conn)
```

## Continuous Integration

When you push to main, tests run automatically. Ensure:
1. All tests pass: `pytest tests/ -v`
2. No type errors: `mypy .`
3. Code is formatted: `black . --check`
4. Imports sorted: `isort . --check-only`

## Deployment

### Version Management

Update version in `pyproject.toml`:

```toml
[project]
version = "1.0.0"
```

Create a git tag:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Release Checklist

- [ ] All tests passing
- [ ] Type check clean
- [ ] Code formatted
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] Tests run on target Python version (3.13+)

## Getting Help

- Check existing issues: `git log --oneline | head -20`
- Review test examples: `tests/test_*.py`
- Check ARCHITECTURE.md for design details

---

**Happy coding!**

# System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   main.py (GameApp)                     │
│              Orchestrates entire application             │
└─────────────────────┬───────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   UI Layer   │ │Game Logic    │ │   Models     │
│ (ui/)        │ │  (game/)     │ │ (models/)    │
├──────────────┤ ├──────────────┤ ├──────────────┤
│ display.py   │ │ engine.py    │ │ player.py    │
│ prompts.py   │ │ question.py  │ │game_result.py│
└──────────────┘ └──────────────┘ └──────────────┘
      │                                  │
      └──────────────────┬───────────────┘
                         │
                    ┌────▼────────┐
                    │ Data Access │
                    │   (db/)     │
                    ├─────────────┤
                    │operations.py│
                    │repositories │
                    └─────────────┘
                         │
                    ┌────▼────────┐
                    │  SQLite DB  │
                    │  game.db    │
                    └─────────────┘
```

## Module Dependencies

```
config.py (top-level config)
    ↓
const.py (constants)
    ↓
game/
  ├─ question.py
  └─ engine.py
         ↓
    models/
      ├─ player.py
      └─ game_result.py
         ↓
db/
  ├─ __init__.py (db setup)
  └─ operations.py (repos)
     ↓
ui/
  ├─ display.py
  └─ prompts.py
     ↓
main.py (entry point)
```

## Class Hierarchy

### Models

```
Player (models/player.py)
├─ Properties with validation
│  ├─ name: str
│  ├─ email: str (unique)
│  ├─ age: int (1-150)
│  ├─ phone: str (unique)
│  ├─ score: int
│  └─ date: datetime

GameResult (models/game_result.py)
├─ player_id: int
├─ difficulty: str
├─ score: int
├─ max_score: int
├─ duration: float
├─ created_at: datetime
└─ accuracy: float (calculated property)
```

### Business Logic

```
GameEngine (game/engine.py)
├─ __init__(player, difficulty)
├─ play_round(answer) → bool
├─ get_score() → int
├─ get_max_possible_score() → int
├─ is_game_finished() → bool
├─ get_progress() → tuple
└─ _parse_answer(str) → bool

Question (game/question.py)
├─ left: int
├─ operator: str ("<", "=", ">")
├─ right: int
├─ is_correct(answer) → bool
└─ __str__() → str
```

### Data Access

```
PlayerRepository (db/operations.py)
├─ insert_player() → int
├─ find_player_by_email() → dict
└─ find_player_by_id() → dict

GameResultRepository (db/operations.py)
├─ insert_game_result() → int
├─ get_leaderboard(limit) → list[dict]
└─ get_player_game_history() → list[dict]
```

## Data Flow

### New Player Flow
```
User Input → prompts.py
    ↓
validate (email format, age range, etc)
    ↓
Player(name, email, age, phone)
    ↓
PlayerRepository.insert_player()
    ↓
SQLite INSERT
    ↓
Store player_id in session
```

### Game Flow
```
Player selects difficulty
    ↓
GameEngine(player, difficulty)
    ↓
LOOP:
  generate_question()
    ↓
  display question
    ↓
  get user answer
    ↓
  engine.play_round(answer)
    ↓
  update score
    ↓
  display result
    ↓
END LOOP
    ↓
GameResult(player_id, difficulty, score, max_score, duration)
    ↓
GameResultRepository.insert_game_result()
    ↓
SQLite INSERT
```

### Leaderboard Flow
```
GameResultRepository.get_leaderboard()
    ↓
SQL GROUP BY player_id, aggregate scores
    ↓
Sort by best_score DESC
    ↓
Return top 20
    ↓
display.print_leaderboard()
```

## Configuration System

### Difficulty Levels (config.py)

```python
EASY = DifficultyLevel(
    name="Easy",
    num_questions=5,
    score_per_correct=10,
    score_penalty=5
)

MEDIUM = DifficultyLevel(...)
HARD = DifficultyLevel(...)

DIFFICULTY_LEVELS = {
    "easy": EASY,
    "medium": MEDIUM,
    "hard": HARD
}
```

### Game Constants (config.py)

```python
MIN_NUMBER = 1
MAX_NUMBER = 100
OPERATORS = ["<", "=", ">"]
```

### Database Constants (const.py)

```python
DB_NAME = "game.db"
RE_EMAIL = r"..."  # Email validation regex
RE_PHONE = r"..."  # Phone validation regex
```

## Error Handling Strategy

### Input Validation
1. **UI Layer**: `prompts.py` catches user input errors
2. **Model Layer**: Properties validate on assignment
3. **Game Layer**: GameEngine validates answers

Example:
```
User enters age "abc"
    ↓ caught in get_player_age()
    ↓ print error, retry
User enters age "25"
    ↓ Player(age=25) passes validation
    ↓ age property converts and validates
```

### Database Errors
1. Caught in repositories with try/except
2. Proper rollback on transaction errors
3. Meaningful error messages to user

Example:
```
Duplicate email insertion
    ↓ caught in insert_player()
    ↓ sqlite3.IntegrityError raised
    ↓ caught in GameApp._create_new_player()
    ↓ offer to login instead
```

## Testing Strategy

### Unit Tests (isolated components)
- `test_game_engine.py`: Question generation, scoring logic
- `test_player.py`: GameEngine state management
- `test_db_operations.py`: Repository operations

### Integration Tests (end-to-end workflows)
- `test_integration.py`: Full game flows, persistence

### Test Fixtures (conftest.py)
- `temp_db`: Temporary test database
- `sample_player`: Standard test player object

## Performance Considerations

1. **Question Generation**: O(1) - just random choices
2. **Score Calculation**: O(1) - simple arithmetic
3. **Leaderboard Query**: O(n log n) - uses GROUP BY and sorting
4. **Database**: SQLite suitable for single-user local app

## Security Considerations

1. **Input Validation**: All user inputs validated before use
2. **SQL Injection**: Parameterized queries prevent injection
3. **Data Validation**: Email/phone regex patterns prevent invalid data
4. **Type Safety**: Type hints catch many potential errors

## Scalability Notes

Current design suitable for:
- Single-player local games
- ~1000+ players (SQLite limitation)
- Local file storage only

For scaling:
- Replace SQLite with PostgreSQL
- Add API server (FastAPI/Flask)
- Implement authentication/authorization
- Add caching layer for leaderboard

---

**Last Updated:** 2026-02-20  
**Version:** 1.0.0

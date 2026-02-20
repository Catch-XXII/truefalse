# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-20

### Added

#### Core Features
- Multi-difficulty game modes (Easy, Medium, Hard)
- Player profile system with email and phone validation
- Persistent player database with SQLite
- Leaderboard showing top 20 players
- Game history and personal statistics
- Auto-generated math equations with <, =, > operators
- Scoring system with difficulty-based point values
- Game timing and accuracy calculation

#### User Interface
- Colored terminal output using colorama
- Menu-driven navigation system
- Input validation with helpful error messages
- Game progress display (current question / total)
- Game summary with accuracy percentage
- Leaderboard display with formatted table
- Player statistics view

#### Architecture
- Clean modular architecture with separation of concerns
- Repository pattern for data access
- GameEngine class for game logic
- Question class for equation representation
- Player and GameResult models
- Dependency injection throughout
- Type hints on all functions

#### Testing
- Comprehensive unit test suite
- Integration tests for end-to-end workflows
- Pytest configuration with fixtures
- Test utilities in conftest.py
- ~50+ test cases covering happy paths and error cases
- Database testing with temporary test databases

#### Documentation
- Comprehensive README with installation and quick start
- USER_GUIDE.md with gameplay instructions and tips
- DEVELOPER_GUIDE.md with development setup and contribution guidelines
- ARCHITECTURE.md with system design and data flow diagrams
- Inline docstrings for all public classes and functions

#### Developer Tools
- setup.sh script for easy environment setup
- Support for mypy type checking
- Code formatting support (black, isort)
- Pytest configuration
- Development dependencies in pyproject.toml

### Technical Details

#### Database Schema
- `player` table: Stores player profiles with unique email/phone
- `game_session` table: Tracks individual game results with foreign key to player

#### Game Mechanics
- Question generation from configurable difficulty levels
- Dynamic scoring based on difficulty
- Answer validation and feedback
- Progress tracking during games
- Accuracy calculation (score / max_score × 100%)

#### Configuration
- DifficultyLevel dataclass for easy difficulty management
- Configurable game constants (number ranges, operators)
- Email and phone regex validation patterns

### Performance
- O(1) question generation and scoring
- O(n log n) leaderboard queries
- Suitable for 1000+ players on SQLite
- <100ms per question operation

### Known Limitations
- Single-player local-only (no networking)
- SQLite limited to ~1000 concurrent connections
- No game pause/resume functionality
- No player profile editing
- No profile deletion

---

## Future Roadmap

### v1.1.0 (Planned)
- [ ] Game pause and resume
- [ ] Player profile editing
- [ ] Multiple game modes (timed, survival, etc)
- [ ] Achievements/badges system
- [ ] Game statistics dashboard

### v2.0.0 (Future)
- [ ] Network multiplayer
- [ ] Web interface
- [ ] API backend (FastAPI)
- [ ] PostgreSQL support
- [ ] User authentication
- [ ] Mobile companion app

---

**For installation and usage, see README.md**
**For development, see docs/DEVELOPER_GUIDE.md**

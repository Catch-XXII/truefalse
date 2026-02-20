# TrueFalse User Guide

## Getting Started

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd truefalse
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install colorama
   ```

4. **Run the game**
   ```bash
   python main.py
   ```

## Game Rules

### The Basics

TrueFalse presents you with math equations and asks: **Is this true or false?**

**Example:**
```
45 < 67    →  True (45 is less than 67)
50 > 100   →  False (50 is NOT greater than 100)
42 = 42    →  True (42 equals 42)
```

### Three Difficulty Levels

Choose your challenge level before each game:

| Level  | Questions | Points for Correct | Penalty for Wrong | Difficulty |
|--------|-----------|-------------------|-------------------|------------|
| Easy   | 5         | +10 points        | -5 points         | ⭐        |
| Medium | 9         | +5 points         | -5 points         | ⭐⭐      |
| Hard   | 15        | +3 points         | -2 points         | ⭐⭐⭐    |

### Scoring System

- **Minimum Score**: Never goes below 0
- **Maximum Score**: Varies by difficulty level
- **Accuracy**: Calculated as (Your Score / Max Possible Score) × 100%

**Example:**
```
Easy game (max 50 points):
- Get all 5 correct: 50 points (100% accuracy)
- Get 3 correct, 2 wrong: 30 - 10 = 20 points (40% accuracy)
- Get 1 correct, 4 wrong: 10 - 20 = 0 points (0% accuracy, can't go negative)
```

## How to Play

### Step 1: Create or Login

When you start, you'll see:
```
Select option:
1. New Player
2. Returning Player
3. Exit
```

**New Player:**
- Enter your name
- Enter your email (must be unique)
- Enter your age (1-150)
- Enter your phone number

**Returning Player:**
- Enter your email to login
- Your stats will be loaded

### Step 2: Main Menu

Once logged in:
```
Main Menu - John

Select option:
1. Play Game
2. View Leaderboard
3. View Your Stats
4. View Rules
5. Change Player
6. Exit
```

### Step 3: Select Difficulty

```
Select option:
1. Easy (5 questions)
2. Medium (9 questions)
3. Hard (15 questions)
```

### Step 4: Play!

For each equation, answer:
- **T** or **True** for true
- **F** or **False** for false

```
[1/5] 45<67
Your answer (T/F): T
✓ Correct!
Score: 10
```

### Step 5: View Results

After completing a game:
```
==================================================
                    Game Summary
==================================================

Difficulty: easy
Score: 45/50
Accuracy: 90.0%
Time: 2m 34s

✓ Great job!
```

## Menu Features

### Play Game

Start a new game with your chosen difficulty level.

**Tips:**
- Answer quickly - there's no timer, but speed helps!
- Focus on accuracy over guessing
- Each wrong answer costs you points
- Minimum score is always 0

### View Leaderboard

See the top 20 players and compare your scores.

```
==================================================
                   LEADERBOARD
==================================================
Rank   Name                   Best Score   Avg Score   Games
───────────────────────────────────────────────────────────
#1     Alice                  50           48.5        20
#2     Bob                    45           40.2        15
#3     Charlie                40           35.1        10
```

**Sorted by:**
- Best score (highest first)
- Shows average score across all games
- Shows total games played

### View Your Stats

See your personal game history.

```
Recent Games (10):

#    Difficulty    Score          Accuracy    Time
─────────────────────────────────────────────────────────
1    Medium        45/50          90.0%       3m 45s
2    Hard          35/45          77.8%       5m 12s
3    Easy          50/50          100.0%      2m 30s
```

### View Rules

Review the game rules and scoring information.

## Tips for Success

### Quick Wins
1. **Start Easy**: Build confidence with Easy mode
2. **Mental Math**: Practice quick mental comparison
3. **Rhythm**: Develop a pattern - read, think, answer
4. **Accuracy > Speed**: One correct is better than two guesses

### Strategy by Difficulty

**Easy Mode Tips:**
- Higher points per correct (+10)
- Lower penalty per wrong (-5)
- Good for learning and warm-up
- Easier to get perfect score

**Medium Mode Tips:**
- Balanced challenge
- 9 questions tests endurance
- More focus needed than Easy
- Good practice for Hard mode

**Hard Mode Tips:**
- Lower points (+3) but 15 questions
- Harsh penalty (-2) on mistakes
- Requires concentration
- Shows true skill level

### Accuracy Targets
- **Expert**: 90%+ accuracy
- **Proficient**: 75-90% accuracy
- **Learning**: 60-75% accuracy
- **Beginner**: <60% accuracy

## Keyboard Shortcuts

| Keys      | Action |
|-----------|--------|
| T or t    | Answer True |
| F or f    | Answer False |
| Y or N    | Confirm/Decline |
| CTRL+C    | Quit game (gracefully) |
| Enter     | Proceed/Confirm |

## Troubleshooting

### Q: I got an error when starting
**A:** Make sure:
- Python 3.13+ is installed: `python --version`
- You're in the project directory: `cd truefalse`
- You've activated the venv: `source .venv/bin/activate`

### Q: "Email already registered!"
**A:** That email is already used. Options:
- Use a different email for a new account
- Select "Returning Player" to login with that email

### Q: Can I change my profile information?
**A:** Current version doesn't support edits. To change:
- Create a new player with different email
- Your old stats remain in leaderboard

### Q: How is the leaderboard calculated?
**A:** Sorted by highest score from a single game, showing:
- Best score achieved
- Average score across all games
- Total games played

### Q: Can I play offline?
**A:** Yes! The game uses a local SQLite database. No internet needed.

### Q: Where is my data stored?
**A:** In `game.db` in the project folder. This file contains:
- Player profiles
- All your game results
- Leaderboard data

### Q: Can I delete my data?
**A:** Delete `game.db` and restart the game to start fresh.

## Game Statistics Explained

### Accuracy
```
Accuracy = (Your Score / Maximum Possible Score) × 100%

Example:
Game: Easy (max 50 points)
You scored: 45 points
Accuracy = (45 / 50) × 100% = 90%
```

### Duration
Time taken to complete the game, from start of first question to final answer.

### Best Score
Your highest score achieved across all games at any difficulty.

### Average Score
Average of all your games across all difficulties.

## Frequently Asked Questions

**Q: What's the maximum possible score?**
```
Easy:   5 × 10 = 50 points
Medium: 9 × 5  = 45 points
Hard:   15 × 3 = 45 points
```

**Q: Do I earn points for speed?**
A: No, only accuracy matters. Answer at your own pace!

**Q: Can scores go negative?**
A: No, minimum score is always 0.

**Q: Are questions repeated?**
A: Randomly generated each time - unlikely to see exact duplicates.

**Q: Can I play the same game twice?**
A: Yes! Each game is independent. Play as many times as you like.

---

## Have Fun! 🎮

TrueFalse is meant to be fun and challenging. Whether you're training your mental math or just looking for a quick game, enjoy!

**Pro Tip:** Share your scores with friends and compete on the leaderboard!

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-20

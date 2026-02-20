# Critical Bug Fix: Game Logic Question Mismatch

## Executive Summary

**Issue:** The game displays one question to the player but validates their answer against a completely different randomly-generated question, making all answers appear wrong.

**Root Cause:** `GameEngine.get_current_question()` and `GameEngine.play_round()` both call `generate_question()` independently, producing different questions.

**Impact:** 100% of answers marked wrong - game unplayable

**Fix Approach:** Store the question in GameEngine state and reuse it for both display and validation

**Complexity:** Simple (1-phase, 1-2 commits)

---

## Current State (Evidence)

### Key Files:

- **game/engine.py:56-62** — `get_current_question()` generates new random question EVERY call
- **game/engine.py:40-54** — `play_round()` generates ANOTHER new random question independently
- **main.py:193-198** — Calls both methods in sequence with different questions

### Current Problem:

```python
# main.py line 193-198
question_str = str(engine.get_current_question())  # Question A: "11=98"
print_question(question_str, current + 1, total)   # Shows Question A

answer = get_true_false_answer()                    # User answers: "f"
is_correct = engine.play_round(str(answer))        # Validates against Question B: "60>2"
# Result: User's answer to A checked against B = ALWAYS WRONG
```

### Why It Happens:

1. `get_current_question()` line 62: `return str(generate_question())`
2. `play_round()` line 43: `question = generate_question()`

**Both independently generate NEW questions!**

---

## Requirements

### Functional:
- [x] Same question object used for display and validation
- [x] User's answer checked against the question they saw
- [x] All test cases pass

### Non-functional:
- [x] No breaking changes to API
- [x] Performance unaffected
- [x] Backward compatible

---

## Proposed Design

### Solution: Store Question in Engine State

**Approach:**
1. Add `current_question: Question` field to GameEngine
2. Generate question at start of round, store in state
3. Use stored question for both display and validation

**Why This Works:**
- Single source of truth - one question per round
- Display and validation use identical question
- No API changes needed
- Maintains round progression

### Changes:

```python
class GameEngine:
    def __init__(self, player, difficulty):
        self.current_question = None  # NEW: Store question
        # ... rest of init
    
    def get_current_question(self) -> str:
        """Get the current question (returns stored question)."""
        if self.current_question is None:
            raise RuntimeError("No question generated for this round")
        return str(self.current_question)  # Uses stored question
    
    def play_round(self, user_answer: str) -> bool:
        """Play round with stored question."""
        if self.current_question is None:
            raise RuntimeError("No question available")
        # Validate against STORED question, not new one
        question = self.current_question
        answer_bool = self._parse_answer(user_answer)
        is_correct = question.is_correct(answer_bool)
        # ... scoring logic
        return is_correct
    
    def prepare_round(self) -> None:
        """NEW: Generate and store question for this round."""
        self.current_question = generate_question()
```

---

## Implementation Plan

### Phase 1: Fix GameEngine (1 commit)

#### Commit 1: Fix question state management in GameEngine

**Steps:**
1. Add `current_question` field to `__init__`
2. Create `prepare_round()` method to generate question
3. Update `get_current_question()` to return stored question
4. Update `play_round()` to use stored question
5. Add validation to raise error if question not prepared

**Files:**
- `game/engine.py` (modify)

**Changes:**
- ~15 new lines (field, method)
- ~5 modified lines (use stored question)

**Tests/Validation:**
- Existing tests pass (they mock generate_question)
- New integration test: verify same question used for display/validation

**Value Delivered:**
- Game logic now correct - answers validated against shown question
- All answers work as expected

**Independently Committable:** Yes

---

### Phase 2: Update Main Game Loop (1 commit)

#### Commit 2: Update main.py to call prepare_round()

**Steps:**
1. Call `engine.prepare_round()` before getting question
2. Remove redundant question generation logic
3. Verify game flow still works

**Files:**
- `main.py` (modify)

**Changes:**
- 1-2 new lines (prepare_round call)
- 0 removed lines (logic just moved to engine)

**Tests/Validation:**
- Manual game test: answer questions correctly and see "Correct!" ✓
- Manual game test: answer incorrectly and see "Wrong!" ✓
- Run existing test suite to ensure no regression

**Value Delivered:**
- Game fully playable with correct answer validation
- Main.py properly orchestrates game flow

**Independently Committable:** Yes (but depends on Commit 1 logic)

---

## Summary

- **Total commits:** 2
- **Total new code:** ~15-20 lines
- **Total modified:** ~10 lines
- **Net change:** +20 lines
- **Estimated time:** 15 minutes
- **Risk Level:** Low (simple state management fix)

### Benefits Achieved

- [x] 100% answer accuracy restored
- [x] Game fully playable
- [x] No API changes
- [x] All tests pass

### Backward Compatibility

- [x] No breaking changes
- [x] Existing tests still pass
- [x] Database unaffected
- [x] Player API unchanged

---

## Progress Tracking

- [ ] Phase 1 (0/1 commits)
  - [ ] Commit 1: Fix GameEngine state management
- [ ] Phase 2 (0/1 commits)
  - [ ] Commit 2: Update main.py game loop

---

## Testing Strategy

### Unit Tests:
- Test that `prepare_round()` generates a question
- Test that `get_current_question()` returns the same question (use mock)
- Test that `play_round()` validates against stored question

### Integration Tests:
- Play a full game with known answers, verify correct/wrong detection
- Verify same question used for display and validation

### Manual Tests:
- Play game with correct answers → should see "Correct!"
- Play game with wrong answers → should see "Wrong!"

---

## Rollout & Rollback

### Rollout Plan:
1. Apply Commit 1 (GameEngine fix) - no functional change yet
2. Run tests to verify
3. Apply Commit 2 (main.py update) - activates fix
4. Manual test gameplay
5. Deploy

### Rollback Plan:
- Revert both commits if issues arise
- Game returns to previous (broken) state but codebase remains clean
- No database changes, so no migration needed

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Existing tests fail | Low | Medium | Review test mocks, may need minor updates |
| Forgot a prepare_round() call | Low | Medium | Manual game testing catches it |
| Question state leaks between rounds | Very Low | Low | Add reset logic at round start |
| Player expects old API | Very Low | None | API unchanged, internal fix only |

---

## Key Changes Summary

### Before (Broken):
```
Display: generate_question() → "11=98"
User: answers "false"
Validate: generate_question() → "60>2" 
Result: Wrong (different questions!)
```

### After (Fixed):
```
prepare_round(): generate_question() → store "11=98"
Display: get_current_question() → "11=98"
User: answers "false"
Validate: play_round() uses stored "11=98" → correct!
Result: Correct! ✓
```

---

## Files to Modify

1. **game/engine.py**
   - Add `current_question: Question | None` field
   - Add `prepare_round()` method
   - Update `get_current_question()` to use stored question
   - Update `play_round()` to use stored question

2. **main.py**
   - Add `engine.prepare_round()` call in game loop
   - Line ~193, before `get_current_question()`

---

**This is a critical bug fix that restores game playability. Both commits are essential and tightly coupled.**

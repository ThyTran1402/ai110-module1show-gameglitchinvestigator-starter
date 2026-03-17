# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game where the player picks a difficulty, then tries to guess a randomly chosen secret number within a limited number of attempts. Correct guesses earn points; wrong guesses cost points.

**Bugs found:**
1. **Backwards hints**: `check_guess` returned "Go HIGHER!" when the guess was too high and "Go LOWER!" when too low; the directions were swapped.
2. **String comparison on even attempts**: `app.py` cast the secret to a string every other attempt, breaking numeric comparison and producing random wrong hints.
3. **Hard difficulty easier than Normal**: Hard used range 1–50 while Normal used 1–100; the difficulty labels were misleading.
4. **Score rewarded wrong guesses**: "Too High" on even attempt numbers gave +5 points instead of deducting them.
5. **Attempts off-by-one**: Initial attempts was set to 1 (should be 0), making the "Attempts left" counter wrong from the start.
6. **Hardcoded range in UI**: The info banner always said "1 and 100" regardless of difficulty setting.
7. **Tests compared tuple to string**: `check_guess` returns `(outcome, message)` but tests asserted `result == "Win"`.
8. **`logic_utils.py` was all stubs**: All four game-logic functions needed to be moved from `app.py` into `logic_utils.py`.

**Fixes applied:**
- Moved all logic functions into `logic_utils.py` and updated `app.py` to import from it.
- Swapped the hint messages in `check_guess` so directions are correct.
- Removed the string-conversion block so `secret` is always passed as an integer.
- Corrected Hard difficulty range to 1–200.
- Simplified `update_score` so wrong guesses always deduct 5 points.
- Set initial attempts to 0 and made `new_game` consistent.
- Updated the info banner to use dynamic `low`/`high` values.
- Fixed tests to unpack the tuple and added 6 new targeted tests.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]

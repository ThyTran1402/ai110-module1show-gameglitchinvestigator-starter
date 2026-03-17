# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the hints were backwards").

When I first ran the game, it appeared to work on the surface — I could enter a number and see a hint — but the hints were consistently wrong. If I guessed too high, the game told me to "Go HIGHER!" instead of lower, which meant following the hints actually moved me further from the answer. A second bug I noticed was that the info banner always said "Guess a number between 1 and 100" even when I switched to Easy mode (which should be 1–20) or Hard mode. A third issue was that the "Hard" difficulty actually had the smallest range (1–50), making it easier than Normal (1–100) — the opposite of what the label promised. After digging into the code, I also found that on every even-numbered attempt the secret was silently cast to a string before comparison, which broke numeric hints in unpredictable ways.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code (Anthropic's CLI) as my AI pair programmer throughout this project. For the refactoring step, the AI correctly identified that all four functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) needed to move from `app.py` into `logic_utils.py`, and it generated the correct import line in `app.py`; I verified this by running `pytest` and confirming the tests still found the functions. One misleading suggestion came when I first asked the AI to "fix the score bug" without specifying which one — it initially proposed adding a flag to track whether points had already been awarded that round, which added unnecessary state. I rejected this and instead asked it to simplify: wrong guesses should always deduct 5 points with no special cases, which is cleaner and easier to test.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I used a two-step verification approach: first I ran `pytest` to check correctness at the function level, then I ran the Streamlit app manually to confirm the UI behaved as expected. The most useful test was `test_too_high_hint_says_go_lower`, which directly encoded the backwards-hint bug — before the fix it would have failed because the message contained "HIGHER" instead of "LOWER". After my fix it passed, giving me confidence the logic was corrected rather than just the text. The AI suggested checking the message content (not just the outcome string) for the hint tests, which was a good insight because it caught the label/direction mismatch that a simple outcome check would have missed. I also added `test_wrong_guess_never_awards_points` after the AI pointed out that the score deduction bug was testable with a single assertion comparing score before and after a wrong guess.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-executes your entire Python script from top to bottom every time a user interacts with the page — clicking a button, typing in an input, or changing a dropdown all trigger a full rerun. This means ordinary Python variables reset to their initial values on every interaction, so Streamlit provides `st.session_state` as a dictionary that persists across reruns. You check "if the key isn't in session_state yet, set it" at the top of the script, and then read/write to it freely. The bug where `attempts` started at 1 instead of 0 was subtle precisely because of this pattern: the initial `= 1` only runs once (when the key is first missing), so it looked harmless but caused an off-by-one error in the "Attempts left" display from the very first guess.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is writing tests that encode the specific bug, not just the happy path. A test like `test_too_high_hint_says_go_lower` would have caught the backwards-hint bug immediately if it had existed before the bug was introduced — that's the value of test-driven thinking even in debugging. Next time I work with AI on a coding task, I would give it a narrower scope per prompt: asking it to fix one specific function at a time produced cleaner, reviewable diffs, whereas broader prompts like "fix all the bugs" generated large changes that were harder to verify. This project reinforced that AI-generated code must be treated as a first draft written by a fast but careless colleague — it can be 90% right while hiding a subtle logic inversion that completely breaks the user experience.

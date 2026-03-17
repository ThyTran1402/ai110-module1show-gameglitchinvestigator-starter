from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

# FIX: Tests now unpack the (outcome, message) tuple that check_guess returns.
# Original tests compared the full tuple to a string (e.g. result == "Win"), which always failed.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# New test: verify hint direction is correct (was backwards before the fix)
def test_too_high_hint_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

# New test: wrong guesses must never award points
def test_wrong_guess_never_awards_points():
    score_before = 100
    score_after_high = update_score(score_before, "Too High", 2)
    score_after_low = update_score(score_before, "Too Low", 3)
    assert score_after_high < score_before, "Too High should deduct points, not award them"
    assert score_after_low < score_before

# New test: parse_guess handles invalid input
def test_parse_guess_invalid():
    ok, _, _ = parse_guess("abc")
    assert not ok

def test_parse_guess_valid():
    ok, value, _ = parse_guess("42")
    assert ok
    assert value == 42

# New test: Hard difficulty range is larger than Normal
def test_hard_range_larger_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard should have a larger range than Normal"

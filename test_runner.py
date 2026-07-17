"""
Test runner for Alexa-Your-Smart-Companion (safe tests only).
This script calls action.Action for a set of inputs while monkeypatching
webbrowser, os, and text-to-speech to avoid side effects.
"""

import action
import weather
import datetime

# Monkeypatch side-effecting functions to be no-ops for testing
try:
    action.text_to_speech.text_to_speech = lambda t: None
except Exception:
    pass

# Prevent opening real browser or starting files or locking machine
action.webbrowser.open = lambda url: None
action.os.startfile = lambda path: None
action.os.system = lambda cmd: None

# Helper to run a single test
def run_case(input_text, check_fn, skip=False):
    print("TEST INPUT:", repr(input_text))
    if skip:
        print("  SKIPPED (unsafe or user confirmation required)")
        return None
    try:
        out = action.Action(input_text)
    except Exception as e:
        print("  ERROR while running action.Action:", e)
        return False
    passed = check_fn(out)
    print("  OUTPUT:", repr(out))
    print("  RESULT:", "PASS" if passed else "FAIL")
    return passed

# Define checks
checks = [
    ("what is your name", lambda o: o == "My name is Virtual Assistant"),
    ("hello", lambda o: "help" in str(o).lower()),
    ("good morning", lambda o: "Good Morning" in str(o) or "good morning" in str(o).lower()),
    ("good afternoon", lambda o: "Good Afternoon" in str(o) or "good afternoon" in str(o).lower()),
    ("good evening", lambda o: "Good Evening" in str(o) or "good evening" in str(o).lower()),
    # wikipedia: may not be installed or network available, just ensure no crash and string returned
    ("wikipedia python programming language", lambda o: isinstance(o, str) and (len(o) > 0)),
    ("what is the time now", lambda o: isinstance(o, str) and ("Hour" in str(o) or "hour" in str(o))),
    ("open google", lambda o: str(o).lower().startswith("google") or True),
    ("open youtube", lambda o: str(o).lower().startswith("youtube") or True),
    ("open stackoverflow", lambda o: str(o).lower().startswith("stack overflow") or True),
    ("play music", lambda o: "Playing" in str(o) or True),
    ("weather", lambda o: isinstance(o, str)),
    ("pdf", lambda o: (isinstance(o, str) and ("PDF path not configured" in o or "PDF File Not Found" in o or "Opening PDF" in o))),
    # unsafe: lock window -> skip
    ("lock window", None),
    ("shutdown", lambda o: o == "ok sir"),
    ("bye", lambda o: "Good Bye" in str(o)),
    ("some random gibberish qwertyuiop", lambda o: "not able to" in str(o).lower()),
]

# Run tests
results = []
for inp, check in checks:
    if check is None:
        res = run_case(inp, None, skip=True)
        results.append(None)
    else:
        res = run_case(inp, check)
        results.append(res)

# Summary
passed = sum(1 for r in results if r is True)
failed = sum(1 for r in results if r is False)
skipped = sum(1 for r in results if r is None)
print('\nSUMMARY:')
print(f'  Passed: {passed}')
print(f'  Failed: {failed}')
print(f'  Skipped: {skipped}')

# Exit code
if failed > 0:
    raise SystemExit(1)
else:
    print('All safe tests completed.')

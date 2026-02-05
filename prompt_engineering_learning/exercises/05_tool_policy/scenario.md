# Exercise 05: Tool Policy (Action vs Suggestion)

## The Scenario

You're using Claude Code (or any agentic Claude setup with tools) to work on a codebase. You want Claude to:

1. Find a bug in the authentication module
2. Fix the bug
3. Run the tests to verify

Here's the context: You have a file `auth.py` that you suspect has a bug, and a test file `test_auth.py`.

**The problem**: Without explicit tool policy, Claude often:
- SUGGESTS changes instead of MAKING them
- Asks "would you like me to..." instead of just doing it
- Reads some files but not others
- Forgets to run tests after making changes

## Your Task

Write prompts that control Claude's tool-use behavior.

---

## Step 1: Write the Naive Prompt

Open `naive_prompt.txt`.

Write a simple request: "Find and fix the bug in auth.py, then run tests."

---

## Step 2: Test Your Naive Prompt

Observe:
- Does Claude edit the file or just suggest edits?
- Does Claude read the file before editing?
- Does Claude run tests after editing?
- How many "would you like me to..." questions?

---

## Step 3: Read the Guidance

Open `guidance.md` for tool policy patterns.

---

## Step 4: Write the Optimized Prompt

Add explicit tool policy that tells Claude WHEN to act vs WHEN to ask.

---

## Success Criteria

- [ ] Claude reads the file BEFORE proposing changes
- [ ] Claude MAKES the edit (doesn't just suggest)
- [ ] Claude runs tests AFTER the edit
- [ ] No unnecessary "permission asking" for routine operations
- [ ] Claude cleans up any temporary files it creates

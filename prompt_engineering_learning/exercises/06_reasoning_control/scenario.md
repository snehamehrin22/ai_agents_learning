# Exercise 06: Reasoning Control

## The Scenario

You need Claude to help with two very different tasks:

### Task A: Simple (Should be quick)
"What's the git command to undo the last commit but keep the changes staged?"

### Task B: Complex (Should show reasoning)
"We're seeing 504 timeout errors on our /api/reports endpoint when users request
large date ranges (>30 days). The endpoint queries our PostgreSQL database,
aggregates data, and returns JSON. Production logs show the query itself is fast
(~200ms) but the total request time exceeds our 30-second timeout. What could
be causing this, and how should we investigate?"

## Your Task

Write prompts that control HOW MUCH reasoning Claude shows based on task complexity.

---

## The Problem

Many prompts include blanket "think step by step" instructions that:
- Make simple answers unnecessarily verbose
- Slow down latency on trivial tasks
- In some Claude configurations, trigger extended thinking modes unexpectedly

But removing ALL reasoning guidance makes complex tasks worse:
- Claude may miss nuances
- Answers lack structure
- No clear problem-solving approach

---

## Step 1: Test with Generic "Think Step by Step"

Write a prompt with generic reasoning instructions and test on BOTH tasks.

Record:
- Task A: Was the simple answer bloated?
- Task B: Was the complex answer well-structured?

---

## Step 2: Read the Guidance

Open `guidance.md` for task-scoped reasoning patterns.

---

## Step 3: Write Task-Appropriate Prompts

Write two versions:
1. For simple tasks (direct answer)
2. For complex tasks (structured reasoning)

Or write ONE prompt that adapts based on complexity.

---

## Success Criteria

- [ ] Simple tasks get concise, direct answers
- [ ] Complex tasks get structured reasoning
- [ ] No unnecessary "Let me think about this..." on trivial questions
- [ ] Complex analysis follows a clear problem-solving structure

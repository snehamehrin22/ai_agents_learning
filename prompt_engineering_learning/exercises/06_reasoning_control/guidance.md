# Exercise 06: Guidance

## Why "Think Step by Step" is Problematic for Claude

Anthropic notes that Claude 4.5 (especially Opus without extended thinking) is "sensitive to the word 'think' and its variants."

**Problems with blanket CoT:**
1. **Latency**: Forces reasoning even on trivial tasks
2. **Verbosity**: Simple questions get essay-length answers
3. **Mode interaction**: Can trigger extended thinking unexpectedly
4. **Token waste**: You pay for reasoning you don't need

---

## The Fix: Task-Scoped Reasoning

Instead of "always think step by step," tell Claude WHEN to reason deeply vs WHEN to answer directly.

---

## Pattern 1: Complexity-Adaptive

```xml
<reasoning_style>
Adapt your reasoning depth to the question:

SIMPLE questions (factual, single-step, well-defined):
→ Answer directly in 1-2 sentences
→ No preamble, no "let me think about this"
→ Examples: syntax questions, command lookups, definitions

COMPLEX questions (multi-factor, ambiguous, require analysis):
→ First, briefly restate what you understand the problem to be
→ Outline your approach in 3-7 steps
→ Work through each step
→ Summarize findings and recommendations
→ Examples: debugging, architecture decisions, trade-off analysis

When uncertain about complexity, err toward concise.
</reasoning_style>
```

---

## Pattern 2: Explicit Triggers

```xml
<reasoning_style>
DEFAULT: Answer directly and concisely.

USE STRUCTURED REASONING when:
- The question involves trade-offs with no clear "right" answer
- Multiple factors need to be weighed
- Debugging or root cause analysis is required
- The answer depends on assumptions you need to state

STRUCTURE for complex questions:
1. Problem restatement (1-2 sentences)
2. Key factors/constraints
3. Analysis of options
4. Recommendation with rationale
</reasoning_style>
```

---

## Pattern 3: Word Substitution

Anthropic recommends avoiding "think" and using alternatives:
- "consider" instead of "think about"
- "evaluate" instead of "think through"
- "analyze" instead of "think step by step"

**Before:**
```
Think step by step about this problem.
```

**After:**
```
Analyze this problem systematically. Consider the key factors before recommending a solution.
```

---

## Anti-Pattern: Always-On CoT

**Bad:**
```
You are an expert engineer. ALWAYS think step by step. For every question,
reason through it carefully before answering. Show your work.
```

This turns a simple "what's the command for X" into a 500-word essay.

---

## For This Exercise

### For Simple Tasks (Task A)
Your prompt should encourage:
- Direct answers
- No preamble
- No unnecessary explanation

### For Complex Tasks (Task B)
Your prompt should encourage:
- Problem restatement
- Systematic analysis
- Clear structure
- Actionable recommendations

### Bonus: One Adaptive Prompt
Write a single prompt that handles BOTH appropriately.

---

## What You Should Notice

### With generic "think step by step":
- Task A: "Let me think about this... The git command... actually there are several ways... [continues for 3 paragraphs]"
- Task B: May or may not be well-structured

### With task-scoped reasoning:
- Task A: "Use `git reset --soft HEAD~1`"
- Task B: "**Problem**: 504s on large date ranges despite fast queries...
  **Likely causes**: 1) Data serialization... 2) Memory pressure... 3) Network...
  **Investigation steps**: 1) Add timing logs... 2) Profile memory...
  **Recommendation**: Start with..."

---

## Real Examples

### Generic CoT on Simple Question:
```
User: How do I reverse a list in Python?

Claude: Let me think through this step by step.

First, I need to consider what "reversing a list" means. When we reverse a list,
we want the elements to appear in the opposite order...

[continues for 200 more words]

The answer is: list[::-1] or list.reverse()
```

### Task-Scoped on Same Question:
```
User: How do I reverse a list in Python?

Claude: Use `list[::-1]` for a new reversed list, or `list.reverse()` to reverse in place.
```

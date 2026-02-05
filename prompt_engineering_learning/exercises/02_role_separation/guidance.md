# Exercise 02: Guidance

## Why System vs User Separation Matters

Anthropic explicitly recommends using the `system` parameter for role/persona and keeping task-specific details in the `user` message.

**Why this works:**
- System prompts are treated as persistent context
- User messages are treated as ephemeral tasks
- Mixing them creates confusion about what's stable vs what's per-request

Claude 4.x (especially Sonnet 4.5) is MORE responsive to system prompts than earlier models. This means:
- Well-structured system prompts have higher impact
- Overloading system prompts with task details can create conflicts

---

## The Pattern

### System Prompt (role, values, style)
```
You are a [seniority] [role] at [context].
You value [A, B, C] and avoid [X, Y].
Your communication style is [description].
```

### User Message (task, context, constraints)
```xml
<context>
[The specific code/document/data to work with]
</context>

<task>
[What to do with it]
</task>

<constraints>
[Any specific rules for this task]
</constraints>
```

---

## What Goes Where

### In System:
- Role identity ("You are a senior staff engineer")
- Core values ("You prioritize correctness over cleverness")
- Communication style ("You're direct and pragmatic")
- Persistent behaviors ("You always explain the 'why'")

### In User:
- The specific input (code, document, data)
- The specific task ("Review this code")
- Task-specific constraints ("Focus on security issues")
- Output format requirements

---

## Common Mistakes

### 1. Entire role in user message
**Bad (user message):**
```
You are a senior engineer. You have 15 years of experience.
You value clean code. You're pragmatic. You focus on real issues.
Now review this code: [code]
```

**Good (system):**
```
You are a senior staff engineer with deep Python expertise.
You're pragmatic—you focus on issues that matter, not style nitpicks.
You explain the "why" behind suggestions.
```

**Good (user):**
```xml
<code>
[code here]
</code>

<task>
Review this code. Identify bugs, significant style issues, and suggest improvements.
</task>
```

### 2. Task details in system
**Bad (system):**
```
You are a code reviewer. When reviewing code, first check for bugs,
then check for style, then suggest three improvements, and format
your response with headers Bug, Style, Improvements.
```

This mixes persistent identity with ephemeral task instructions.

### 3. Repeating system context in user
If your system says "You are a senior engineer," don't start your user message with "As a senior engineer, please..."

---

## For This Exercise

### System Prompt Should Include:
- Senior engineer identity
- Values: pragmatism, real issues over nitpicks, actionable feedback
- Style: direct, explains reasoning, not pedantic

### User Message Should Include:
- The code to review (in a clear section)
- The specific review task
- Any constraints (e.g., "focus on the most impactful 3 issues")

---

## What You Should Notice

After proper separation:
- Claude "is" the senior engineer rather than "playing" one
- No wasted tokens on role explanation in response
- More consistent persona across runs
- Cleaner prompt that's easier to modify

---

## Bonus: Testing System Prompt Impact

Try this experiment:
1. Run your task with NO system prompt
2. Run with a minimal system prompt ("You are a senior engineer.")
3. Run with your full optimized system prompt

Notice how the depth and quality of feedback changes.

# Exercise 08: Guidance

## Integration Strategy

Don't just concatenate all the techniques. Instead, think about how they COMPOSE:

---

## Layer 1: Foundation (System Prompt)

This is your **stable anchor**. It should include:

```
ROLE:
- Who Claude is for this task
- Core values and priorities
- Communication style

TOOL POLICY (if applicable):
- When to read files vs work from provided code
- Default behaviors

REASONING STYLE:
- How much analysis to show
- When to be thorough vs concise
```

---

## Layer 2: Task Structure (User Message)

This is your **per-request configuration**:

```xml
<context>
[The code to analyze]
</context>

<instructions>
[What to do - numbered steps]
</instructions>

<constraints>
[Prioritized list]
</constraints>

<output_format>
[Strict schema with enforcement rules]
</output_format>
```

---

## How Techniques Compose

### XML Structure + Schema Enforcement
The `<output_format>` section IS your schema enforcement. Use XML to separate it clearly from instructions.

### Role Separation + Explicit Intent
Put the WHY in both places:
- System: WHY this role exists, what it values
- User: WHY this specific analysis matters

### Constraint Priority + Reasoning Control
Your constraints should INCLUDE how to reason:
```xml
<constraints>
Priority 1: Find all security vulnerabilities (critical)
Priority 2: Identify bugs that could cause runtime errors
Priority 3: Note performance issues
Priority 4: Style issues (lowest priority)

For each issue, provide a brief description. Do not over-explain obvious problems.
</constraints>
```

---

## Template Structure

```
=== SYSTEM PROMPT ===

You are [role description].

You value:
- [priority 1]
- [priority 2]
- [priority 3]

[Tool policy if applicable]

[Reasoning style guidance]


=== USER MESSAGE ===

<context>
[Code to analyze]
</context>

<instructions>
1. [First step]
2. [Second step]
3. [Third step]
</instructions>

<constraints>
Priority 1: [Most important]
Priority 2: [Second most important]
...
If priorities conflict, follow the lower number.
</constraints>

<output_format>
Return ONLY valid JSON matching this schema:
{
  [exact schema]
}

RULES:
- [enforcement rules]
</output_format>
```

---

## Checklist Before Testing

Before running your prompt, verify:

### XML Structure
- [ ] Clear section separation with tags
- [ ] Context separate from instructions
- [ ] Output format isolated

### Role Separation
- [ ] System prompt has role, values, style
- [ ] User message has task, context, constraints

### Explicit Intent
- [ ] WHY behind the analysis is clear
- [ ] What "good output" means is defined

### Constraint Priority
- [ ] All constraints are numbered or tiered
- [ ] Conflict resolution rule exists

### Tool Policy
- [ ] Default behaviors defined (if using tools)
- [ ] What NOT to do is specified

### Reasoning Control
- [ ] Appropriate depth for task (this is analytical, needs structure)
- [ ] Not over-verbose

### Schema Enforcement
- [ ] Exact schema specified
- [ ] Types defined
- [ ] No markdown rule
- [ ] Start/end chars specified

---

## Expected Issues to Find

Your prompt should enable Claude to find:

### Critical (Security)
1. `eval(query)` - arbitrary code execution
2. `pickle.load()` - unsafe deserialization
3. Hardcoded password

### High (Bugs)
4. `transform()` returns None (missing implementation)

### Medium (Style/Bugs)
5. `!= None` instead of `is not None`
6. `range(len())` anti-pattern

### Low (Style)
7. TODO comment (incomplete code)
8. Potential path traversal in `load_user_data`

---

## Common Integration Failures

### Over-specification
Too many rules, contradictory constraints, 500-line prompts. Keep it focused.

### Under-specification
Missing one of the 7 elements, leading to inconsistent behavior.

### Wrong layer
Putting ephemeral task details in system prompt, or role identity in user message.

### Priority conflicts
Having rules like "be thorough" and "be concise" without resolution.

---

## Self-Evaluation Rubric

Score your final prompt:

| Element | Missing (0) | Partial (1) | Complete (2) |
|---------|-------------|-------------|--------------|
| XML structure | | | |
| Role separation | | | |
| Explicit intent | | | |
| Constraint priority | | | |
| Tool policy | | | |
| Reasoning control | | | |
| Schema enforcement | | | |

**12-14**: Excellent integration
**9-11**: Good, minor gaps
**6-8**: Needs work on integration
**<6**: Review exercises 01-07

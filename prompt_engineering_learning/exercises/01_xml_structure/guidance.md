# Exercise 01: Guidance

## Why XML Structure Matters for Claude

Claude was fine-tuned with heavy use of XML-like tags in training. When you use tags like `<context>`, `<instructions>`, `<output_format>`, Claude recognizes these as structural boundaries, not just text decoration.

**Without tags**: Claude must infer where context ends and instructions begin. This creates ambiguity and inconsistency.

**With tags**: Claude knows exactly what each section is for and treats them appropriately.

---

## The Pattern

```xml
<context>
[Background information, data to process]
</context>

<instructions>
[What Claude should do - numbered for clarity]
</instructions>

<constraints>
[Rules and limitations]
</constraints>

<output_format>
[Exact structure you want back]
</output_format>
```

---

## Common Mistakes to Avoid

### 1. Nesting instructions inside context
**Bad:**
```xml
<context>
Here's a ticket. Analyze it and categorize it.
[ticket text]
</context>
```

**Good:**
```xml
<context>
[ticket text only]
</context>

<instructions>
Analyze and categorize the ticket.
</instructions>
```

### 2. Vague output format
**Bad:**
```
Return as JSON.
```

**Good:**
```xml
<output_format>
Return ONLY valid JSON matching this schema:
{
  "category": "bug" | "feature" | "billing" | "general",
  "entities": {
    "product": string | null,
    "urgency": "low" | "medium" | "high" | "critical",
    "customer_tier": string | null
  },
  "suggested_template": string
}
No markdown, no explanation, just the JSON.
</output_format>
```

### 3. Missing explicit "no extra text" instruction
Claude likes to be helpful and explain itself. If you want ONLY JSON, you must say so explicitly.

---

## Your Optimized Prompt Should Have

1. **`<context>`** - The ticket text, clearly separated
2. **`<instructions>`** - Numbered steps for what to do
3. **`<constraints>`** - Any rules (e.g., must use specific categories)
4. **`<output_format>`** - Exact JSON schema with "no extra text" instruction

---

## Example Structure (Don't Copy - Write Your Own)

```xml
<context>
[TICKET TEXT HERE]
</context>

<instructions>
1. Categorize the ticket into one of the allowed categories
2. Extract key entities from the text
3. Generate an appropriate response template
</instructions>

<constraints>
- Categories must be one of: bug, feature, billing, general
- Urgency must be inferred from language and stated deadlines
- If an entity cannot be determined, use null
</constraints>

<output_format>
Return ONLY valid JSON with this structure:
{
  "category": string,
  "entities": {
    "product": string | null,
    "urgency": "low" | "medium" | "high" | "critical",
    "customer_tier": string | null
  },
  "suggested_template": string
}
No markdown code blocks. No explanatory text. Just the JSON object.
</output_format>
```

---

## What You Should Notice

After switching to XML structure:
- JSON is valid every time (no markdown wrappers)
- Same entities extracted across runs
- No preamble like "Here's my analysis..."
- Faster mental processing when reading the prompt yourself

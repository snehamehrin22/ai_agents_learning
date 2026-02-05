# Exercise 07: Output Schema Enforcement

## The Scenario

You're building a pipeline that processes Claude's output programmatically. You need Claude to return data that:
1. Is valid JSON (parseable by `json.loads()`)
2. Matches a specific schema
3. Has NO extra text around it
4. Is consistent across runs

### The Task

Analyze this product review and extract structured data:

```
Review: "I bought this laptop 3 months ago and it's been mostly great.
The display is stunning - 4K resolution and the colors are accurate.
Battery life is solid at around 8 hours of real use. My only complaint
is the fan noise when doing heavy tasks like video editing. It gets
pretty loud. Also, the price at $1499 felt steep but the quality
justifies it. Would recommend for creative professionals."
```

### Required Schema

```json
{
  "sentiment": "positive" | "negative" | "mixed",
  "rating_estimate": 1-5,
  "pros": ["string"],
  "cons": ["string"],
  "price_mentioned": number | null,
  "would_recommend": boolean,
  "target_audience": "string"
}
```

---

## Step 1: Write the Naive Prompt

Open `naive_prompt.txt`.

Write a simple "return as JSON" instruction.

---

## Step 2: Test Your Naive Prompt

Run 3 times and check:
- Is the JSON valid every time?
- Any markdown code blocks around it?
- Any explanatory text before/after?
- Does it match the exact schema?
- Any extra fields added?

---

## Step 3: Read the Guidance

Open `guidance.md` for schema enforcement patterns.

---

## Step 4: Write the Optimized Prompt

Apply strict schema enforcement.

---

## Success Criteria

- [ ] Valid JSON on all 3 runs
- [ ] NO markdown code fences (` ```json `)
- [ ] NO explanatory text before or after
- [ ] Exact schema match (no extra fields, no missing fields)
- [ ] Correct types (number for price, boolean for recommend, array for pros/cons)

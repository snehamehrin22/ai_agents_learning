# Exercise 07: Guidance

## Why Schema Enforcement is Hard (and Necessary)

Claude WANTS to be helpful, which means it often:
- Wraps JSON in markdown code blocks
- Adds "Here's the extracted data:" before the JSON
- Explains its reasoning after the JSON
- Adds extra fields it thinks might be useful

All of these break programmatic parsing.

---

## The Problem

**Naive prompt:**
```
Analyze this review and return JSON with sentiment, pros, cons, and rating.
```

**Claude's response:**
```
I've analyzed the review. Here's the structured data:

```json
{
  "sentiment": "positive",
  "pros": ["stunning display", "good battery"],
  "cons": ["fan noise"],
  "rating": 4,
  "additional_notes": "The reviewer seems satisfied overall"
}
```

The reviewer clearly appreciates the product quality despite the price point.
```

**Problems:**
1. Markdown code block (` ```json `) breaks parsing
2. Text before JSON
3. Text after JSON
4. Extra field "additional_notes" not in schema
5. "rating" instead of "rating_estimate"

---

## The Solution: Explicit Schema Enforcement

```xml
<output_format>
Return ONLY valid JSON matching this EXACT schema:
{
  "sentiment": "positive" | "negative" | "mixed",
  "rating_estimate": 1-5,
  "pros": ["string"],
  "cons": ["string"],
  "price_mentioned": number | null,
  "would_recommend": boolean,
  "target_audience": "string"
}

CRITICAL RULES:
- NO markdown code blocks (no ```)
- NO text before the JSON
- NO text after the JSON
- NO extra fields beyond the schema
- Use null for missing values, not "unknown" or omission
- Response must start with { and end with }
</output_format>
```

---

## Key Enforcement Patterns

### 1. Explicit "ONLY"
```
Return ONLY valid JSON.
```
The word "ONLY" is crucial. It signals exclusivity.

### 2. Forbid markdown explicitly
```
NO markdown code blocks. Do not wrap in ```.
```
Claude defaults to markdown formatting. You must explicitly forbid it.

### 3. Specify start/end
```
Your response must start with { and end with }
```
This catches both preamble and postamble text.

### 4. Define null behavior
```
Use null for missing values. Do not omit fields or use placeholder strings.
```
Without this, Claude might use "unknown" or "N/A" or skip fields entirely.

### 5. Forbid extra fields
```
Do not add any fields beyond those specified in the schema.
```
Claude tries to be helpful by adding context. You must stop this.

---

## Complete Template

```xml
<output_format>
Return ONLY valid JSON matching this schema:

{
  "field1": type,
  "field2": type,
  "field3": type
}

RULES:
1. Response must start with { and end with }
2. No markdown formatting (no ```)
3. No explanatory text before or after
4. No extra fields beyond the schema
5. Use null for values that cannot be determined
6. Use exact field names as specified (case-sensitive)
</output_format>
```

---

## Testing Your Schema Enforcement

After getting a response, verify:

```python
import json

response = claude_response.strip()

# Should start and end correctly
assert response.startswith('{'), "Response has preamble text"
assert response.endswith('}'), "Response has postamble text"

# Should parse
data = json.loads(response)

# Should have exact keys
expected_keys = {"sentiment", "rating_estimate", "pros", "cons",
                 "price_mentioned", "would_recommend", "target_audience"}
assert set(data.keys()) == expected_keys, f"Wrong keys: {set(data.keys())}"

# Should have correct types
assert data["sentiment"] in ["positive", "negative", "mixed"]
assert isinstance(data["rating_estimate"], int) and 1 <= data["rating_estimate"] <= 5
assert isinstance(data["pros"], list)
assert isinstance(data["cons"], list)
assert data["price_mentioned"] is None or isinstance(data["price_mentioned"], (int, float))
assert isinstance(data["would_recommend"], bool)
assert isinstance(data["target_audience"], str)
```

---

## Common Failures to Watch For

1. **Markdown wrapper**: Response is ` ```json\n{...}\n``` `
2. **Preamble**: "Here's the analysis:\n{...}"
3. **Postamble**: "{...}\nLet me know if you need more details."
4. **Schema drift**: Uses "rating" instead of "rating_estimate"
5. **Type errors**: `"would_recommend": "yes"` instead of `true`
6. **Extra helpfulness**: Adds "confidence_score" or "reasoning" fields

---

## For This Exercise

Your optimized prompt should:
1. Show the exact schema with types
2. Use "ONLY" and "CRITICAL" language
3. Explicitly forbid markdown
4. Specify start/end characters
5. Forbid extra fields
6. Define null behavior

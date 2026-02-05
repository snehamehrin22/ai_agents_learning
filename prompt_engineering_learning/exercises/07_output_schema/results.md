# Exercise 07: Results

## Naive Prompt Results

### Run 1
- Valid JSON?
- Markdown code blocks?
- Text before JSON?
- Text after JSON?
- Extra fields?
- Correct field names?
- Correct types?
- Raw response (first 200 chars):

### Run 2
- Valid JSON?
- Issues:

### Run 3
- Valid JSON?
- Issues:

### Naive Summary
- Parse success rate: /3
- Schema compliance rate: /3
- Main issues:

---

## Optimized Prompt Results

### Run 1
- Valid JSON?
- Starts with {?
- Ends with }?
- No markdown?
- No extra text?
- Schema match?
- Raw response (first 200 chars):

### Run 2
- Valid JSON?
- Schema match?

### Run 3
- Valid JSON?
- Schema match?

### Optimized Summary
- Parse success rate: /3
- Schema compliance rate: /3

---

## Comparison

| Check | Naive | Optimized |
|-------|-------|-----------|
| Valid JSON | /3 | /3 |
| No markdown | /3 | /3 |
| No preamble | /3 | /3 |
| No postamble | /3 | /3 |
| Exact schema | /3 | /3 |
| Correct types | /3 | /3 |

## Parsing Test Code Results

```python
# Paste your test results here
```

## Key Learnings

1.
2.
3.

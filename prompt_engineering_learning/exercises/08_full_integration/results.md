# Exercise 08: Results

## Pre-Test Self-Evaluation

Score your prompt before testing:

| Element | Score (0-2) | Notes |
|---------|-------------|-------|
| XML structure | | |
| Role separation | | |
| Explicit intent | | |
| Constraint priority | | |
| Tool policy | | |
| Reasoning control | | |
| Schema enforcement | | |
| **TOTAL** | /14 | |

---

## Test Results

### Run 1
- Valid JSON?
- Issues found:
  - Critical:
  - High:
  - Medium:
  - Low:
- All security issues caught?
- Notes:

### Run 2
- Valid JSON?
- Same issues as Run 1?
- Differences:

### Run 3
- Valid JSON?
- Same issues?
- Differences:

### Run 4
- Valid JSON?
- Same issues?
- Differences:

### Run 5
- Valid JSON?
- Same issues?
- Differences:

---

## Consistency Analysis

### Issues Found Across Runs

| Issue | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Rate |
|-------|-------|-------|-------|-------|-------|------|
| eval() security | | | | | | /5 |
| pickle security | | | | | | /5 |
| hardcoded password | | | | | | /5 |
| transform() bug | | | | | | /5 |
| != None style | | | | | | /5 |
| range(len()) | | | | | | /5 |
| path traversal | | | | | | /5 |

### Schema Compliance

| Check | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 |
|-------|-------|-------|-------|-------|-------|
| Valid JSON | | | | | |
| No markdown | | | | | |
| No extra text | | | | | |
| Exact schema | | | | | |

---

## Summary Metrics

- **JSON validity rate**: /5
- **Schema compliance rate**: /5
- **Critical issue detection rate**: /5
- **Consistency score** (same issues 4+ times): /5

---

## Technique Integration Assessment

For each technique, did it measurably improve the output?

| Technique | Impact Observed | Notes |
|-----------|-----------------|-------|
| XML structure | | |
| Role separation | | |
| Explicit intent | | |
| Constraint priority | | |
| Tool policy | | |
| Reasoning control | | |
| Schema enforcement | | |

---

## Final Reflection

### What worked well?


### What would you change?


### Key learnings from the full integration?

1.
2.
3.

### How does this compare to your Exercise 01 naive prompt?


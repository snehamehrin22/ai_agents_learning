# Exercise 03: Guidance

## Why Explaining "Why" Matters

Anthropic's docs explicitly state: giving Claude the MOTIVATION behind instructions improves outputs. Claude is "smart enough to generalize from the explanation."

**Without why**: Claude does the minimum to satisfy the literal request.
**With why**: Claude understands the intent and makes intelligent decisions about edge cases, coverage, and depth.

---

## The Pattern

Instead of:
```
Write tests for this code.
```

Write:
```
Write tests for this code.

Context: This project treats tests as the single source of truth for behavior.
Production bugs have been costly, so:
- Test coverage matters more than test count
- Edge cases must be covered
- Tests should catch regressions if behavior changes
```

---

## Why It Works for Claude Specifically

Claude's constitution emphasizes understanding user's:
1. **Immediate desires** - "write tests"
2. **Background desiderata** - tests should be useful, not just exist
3. **Deeper goals** - prevent bugs, maintain quality
4. **Autonomy** - let the user trust the output

When you explain WHY, you're giving Claude access to levels 2-4, not just level 1.

---

## Examples: What to What + Why

### Example 1: Code Review
**What only:**
```
Review this code.
```

**What + Why:**
```
Review this code.

This is going into a payment processing pipeline where:
- Bugs mean lost revenue or incorrect charges
- The code will be maintained by junior developers
- We prioritize correctness > readability > performance
```

### Example 2: Writing Documentation
**What only:**
```
Write documentation for this API.
```

**What + Why:**
```
Write documentation for this API.

Our users are:
- External developers integrating with our platform
- Often working under time pressure
- They need to know: what it does, how to call it, what errors to expect
- They DON'T need: internal implementation details
```

### Example 3: Refactoring
**What only:**
```
Refactor this function.
```

**What + Why:**
```
Refactor this function.

Goals:
- Make it easier for new team members to understand
- Reduce cyclomatic complexity (currently 15, want < 10)
- Don't change external behavior—tests must still pass

Why this matters: This function is modified monthly and current complexity
is causing bugs during routine changes.
```

---

## For This Exercise

Your optimized prompt should explain:

1. **Why tests matter for this project**
   - Tests are source of truth
   - Bugs in discount calculation = revenue loss

2. **What "good tests" means here**
   - Cover all tiers
   - Cover stacking behavior (multiplicative, not additive!)
   - Cover invalid inputs
   - Cover edge cases (zero price, etc.)

3. **What you DON'T want**
   - Tests that just verify "it runs"
   - Missing the multiplicative stacking edge case
   - Skipping error handling tests

---

## What You Should Notice

After adding intent:
- Claude tests the multiplicative stacking explicitly (because you explained it matters)
- More edge cases covered
- Test names reflect purpose, not just "test_1, test_2"
- Claude may even add comments explaining what each test validates

---

## Bonus: The "Unacceptable" Pattern

A powerful addition is explicitly stating what's unacceptable:

```
<unacceptable>
- Tests that only check happy path
- Missing coverage for the stacking discount calculation
- Tests that would pass even if the function was buggy
</unacceptable>
```

This gives Claude a clear "floor" to stay above.

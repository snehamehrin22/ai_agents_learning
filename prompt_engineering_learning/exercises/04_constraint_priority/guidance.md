# Exercise 04: Guidance

## Why Priority Ordering Matters

This is one of the MOST important Claude-specific behaviors to understand:

**Claude 4.x (especially Sonnet 4.5) does NOT blindly obey every "MUST" and "ALWAYS".**

When constraints conflict, Claude uses its own judgment to make tradeoffs. If you pile on many competing rules without priorities, you get:
- Inconsistent behavior across runs
- Claude picking arbitrary winners
- Frustration when it "ignores" your instructions

The fix: **Explicit priority ordering**.

---

## The Problem with Flat Constraints

**Bad prompt:**
```
ALWAYS maintain backward compatibility.
ALWAYS keep the diff minimal.
ALWAYS improve performance.
ALWAYS make the code more readable.
ALWAYS follow security best practices.
```

What happens when:
- Improving performance requires changing the API (breaks compatibility)?
- Making code readable requires renaming methods (increases diff)?
- Security requires adding validation (increases complexity)?

Claude has to choose. Without guidance, it improvises.

---

## The Solution: Numbered Priorities

**Good prompt:**
```xml
<constraints>
When these constraints conflict, follow the lower number:

Priority 1 (CRITICAL): Do not introduce security vulnerabilities
Priority 2 (HIGH): Maintain backward compatibility - existing code must still work
Priority 3 (MEDIUM): Keep the diff as small as possible
Priority 4 (LOW): Improve performance where possible without violating above
Priority 5 (NICE-TO-HAVE): Improve readability if it doesn't conflict with above

If you must violate a lower-priority constraint to satisfy a higher one,
explain the tradeoff briefly.
</constraints>
```

---

## How Claude Processes This

Claude's constitution says it should prioritize:
1. Broad safety
2. Broad ethics
3. Anthropic guidelines
4. User helpfulness

Your priority ordering slots into #4 (user helpfulness). Claude will:
- Respect your ordering within that category
- Apply judgment when your ordering is ambiguous
- Explain tradeoffs when it recognizes conflicts

---

## Common Patterns

### Pattern 1: Explicit numbered list
```xml
<constraints>
Priority 1: ...
Priority 2: ...
Priority 3: ...
If priorities conflict, follow the lower number.
</constraints>
```

### Pattern 2: Tiered categories
```xml
<constraints>
CRITICAL (never violate):
- Security
- Data integrity

IMPORTANT (avoid violating):
- Backward compatibility
- Minimal diff

NICE-TO-HAVE (if possible):
- Performance
- Readability
</constraints>
```

### Pattern 3: "When X conflicts with Y, prefer X"
```xml
<constraints>
- Maintain backward compatibility
- Keep diff minimal
- Improve readability

When backward compatibility conflicts with readability, prefer compatibility.
When minimal diff conflicts with meaningful improvements, prefer improvements
that fix actual problems over cosmetic changes.
</constraints>
```

---

## For This Exercise

Your optimized prompt should:

1. **List all 5 constraints**
2. **Assign clear priority numbers**
3. **Include a tie-breaker rule**: "If priorities conflict, follow the lower number"
4. **Optionally**: Ask Claude to note any tradeoffs it made

Suggested priority order for this scenario:
1. Security (never introduce vulnerabilities)
2. Backward compatibility (existing code must work)
3. Minimal diff (don't change things unnecessarily)
4. Performance (improve if possible)
5. Readability (nice to have)

---

## What You Should Notice

After adding priorities:
- Consistent decisions across runs
- Claude explains tradeoffs when they occur
- No surprise API changes
- No gratuitous renaming just for "readability"

---

## Red Flags in Naive Prompt Results

Watch for:
- Claude renaming methods "for clarity" (breaks compatibility, violates minimal diff)
- Adding new parameters to methods (breaks compatibility)
- Complete rewrite instead of targeted changes (violates minimal diff)
- Different decisions on run 1 vs run 3 (inconsistency from ambiguous constraints)

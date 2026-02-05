# Exercise 05: Guidance

## Why Tool Policy Matters

Claude 4.x is *steerable* but *conservative* by default on tool use. This means:
- It often SUGGESTS instead of DOES
- It asks permission even for routine operations
- It may not chain actions (read → edit → test) without explicit instruction

Anthropic provides canonical patterns like `<default_to_action>` and `<do_not_act_before_instructions>` to control this.

---

## The Core Problem

**Without tool policy:**
```
User: Fix the bug in auth.py and run tests.

Claude: I can see there's likely a bug in auth.py. Would you like me to:
1. Read the file to understand the issue?
2. Propose a fix?
3. Run the tests?

Please let me know how you'd like to proceed.
```

**With tool policy:**
```
User: Fix the bug in auth.py and run tests.

Claude: [Reads auth.py]
[Identifies bug at line 42]
[Edits file to fix bug]
[Runs tests]
All tests pass. The bug was a missing null check on line 42.
```

---

## Anthropic's Recommended Patterns

### Pattern 1: Default to Action
```xml
<tool_policy>
By default, IMPLEMENT changes rather than only suggesting them.
If you can take an action that directly accomplishes the user's goal, do it.
Only ask for confirmation on:
- Destructive operations (deleting files, dropping tables)
- Operations with side effects outside this session
- Ambiguous requests where multiple interpretations exist
</tool_policy>
```

### Pattern 2: Read Before Write
```xml
<tool_policy>
ALWAYS read and understand relevant files BEFORE proposing changes.
NEVER speculate about the contents of files you have not opened.
If you need to understand code, read it first—don't guess based on names.
</tool_policy>
```

### Pattern 3: Verification Loop
```xml
<tool_policy>
After making changes:
1. Run relevant tests if they exist
2. Report any failures
3. Iterate until tests pass or explain what's blocking
</tool_policy>
```

### Pattern 4: Parallel Tool Calls
```xml
<tool_policy>
When multiple independent operations are needed, run them in parallel.
Example: If you need to read 3 files, read all 3 at once rather than sequentially.
</tool_policy>
```

### Pattern 5: Cleanup
```xml
<tool_policy>
If you create temporary files or scripts during your work, delete them when done.
Do not leave debugging artifacts in the codebase.
</tool_policy>
```

---

## Complete Tool Policy Template

```xml
<tool_policy>
DEFAULT BEHAVIOR:
- IMPLEMENT changes directly rather than suggesting them
- Read files before editing them—never speculate about contents
- Run tests after making changes to verify correctness
- Clean up temporary files when done

WHEN TO ASK:
- Before destructive operations (delete, drop, truncate)
- When the request is ambiguous and has multiple valid interpretations
- Before operations that affect external systems (APIs, databases, deployments)

EFFICIENCY:
- Use parallel tool calls when operations are independent
- Don't read the same file multiple times unnecessarily
- Batch related operations together
</tool_policy>
```

---

## For This Exercise

Your optimized prompt should include:

1. **Default to action**: Make Claude edit directly
2. **Read before write**: Ensure Claude reads auth.py first
3. **Verification**: Run tests after editing
4. **No unnecessary permission asking**: Routine dev operations shouldn't require confirmation

---

## What You Should Notice

After adding tool policy:
- Claude takes action immediately
- Reads file → edits → tests in one flow
- No "would you like me to..." for routine operations
- Clear, confident output

---

## Real-World Tool Policy Examples

### For Code Review Agent:
```xml
<tool_policy>
- Read all files mentioned in the PR diff before commenting
- Use grep/search to find related code when reviewing for consistency
- Do NOT make edits during review—only suggest changes
</tool_policy>
```

### For Debugging Agent:
```xml
<tool_policy>
- Read error logs, stack traces, and relevant source files
- Make diagnostic edits (add logging) without asking
- Run tests to verify hypotheses
- Clean up diagnostic changes after finding the bug
</tool_policy>
```

### For Documentation Agent:
```xml
<tool_policy>
- Read source code before writing documentation
- NEVER speculate about function behavior—always verify by reading
- Create documentation files directly (don't just suggest content)
- Run any doc generation tools after writing
</tool_policy>
```

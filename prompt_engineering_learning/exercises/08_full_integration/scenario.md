# Exercise 08: Full Integration

## The Challenge

Combine ALL techniques from exercises 01-07 into a single, production-quality prompt.

### The Scenario

You're building a "Code Health Analyzer" that:
1. Takes a Python file as input
2. Analyzes it for issues (bugs, style, security, performance)
3. Returns structured JSON with findings
4. Provides severity levels and fix suggestions

### Sample Input

```python
import os
import pickle

def load_user_data(user_id):
    filename = f"/data/users/{user_id}.pkl"
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
    return None

def process_query(query):
    result = eval(query)  # Execute user query
    return str(result)

def get_config():
    password = "admin123"  # Default password
    return {"host": "localhost", "port": 5432, "password": password}

class DataProcessor:
    def __init__(self):
        self.cache = {}

    def process(self, items):
        results = []
        for i in range(len(items)):
            item = items[i]
            if item != None:
                processed = self.transform(item)
                results.append(processed)
        return results

    def transform(self, item):
        # TODO: implement this
        pass
```

### Required Output Schema

```json
{
  "file_summary": {
    "total_issues": number,
    "critical": number,
    "high": number,
    "medium": number,
    "low": number
  },
  "issues": [
    {
      "line": number,
      "severity": "critical" | "high" | "medium" | "low",
      "category": "security" | "bug" | "style" | "performance",
      "title": "string (max 50 chars)",
      "description": "string",
      "suggestion": "string"
    }
  ],
  "top_priority_fix": "string (which issue to fix first and why)"
}
```

---

## Your Task

Write a complete prompt that:

1. **Uses XML structure** (Exercise 01)
2. **Separates system and user roles** (Exercise 02)
3. **Explains the WHY** (Exercise 03)
4. **Has prioritized constraints** (Exercise 04)
5. **Includes tool policy** (Exercise 05) - if applicable
6. **Controls reasoning appropriately** (Exercise 06)
7. **Enforces output schema strictly** (Exercise 07)

---

## Step 1: Plan Your Prompt

Before writing, outline:
- What goes in System vs User?
- What are your constraint priorities?
- What reasoning level is appropriate?
- What schema enforcement rules do you need?

---

## Step 2: Write Your Prompt

Open `full_prompt.txt` and write your complete, integrated prompt.

---

## Step 3: Test Thoroughly

Run at least 5 times and verify:
- [ ] All security issues found (eval, pickle, hardcoded password)
- [ ] All style issues found (range(len()), != None)
- [ ] Severity levels are consistent
- [ ] JSON is valid and matches schema every time
- [ ] No extra text around JSON
- [ ] Consistent results across runs

---

## Step 4: Evaluate

Fill out `results.md` with your findings.

---

## Success Criteria

This exercise is complete when:
- [ ] You have a single, coherent prompt using all 7 techniques
- [ ] 5/5 runs produce valid, parseable JSON
- [ ] 5/5 runs find the critical security issues
- [ ] Consistency score: same issues found in at least 4/5 runs
- [ ] You can explain WHY each part of your prompt exists

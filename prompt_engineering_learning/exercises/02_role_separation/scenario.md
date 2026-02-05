# Exercise 02: Role Separation (System vs User)

## The Scenario

You're building a code review assistant that:
1. Reviews Python code for bugs and style issues
2. Suggests improvements
3. Maintains a senior engineer's perspective (pragmatic, not pedantic)

You'll review this code:

```python
def process_users(users):
    result = []
    for i in range(len(users)):
        user = users[i]
        if user['status'] == 'active':
            if user['age'] >= 18:
                if user['email'] != None:
                    result.append({
                        'name': user['name'],
                        'email': user['email'],
                        'type': 'adult'
                    })
    return result
```

## Your Task

Write a prompt that reviews this code with the persona of a senior engineer who:
- Focuses on real issues, not nitpicks
- Explains the "why" behind suggestions
- Keeps feedback actionable

---

## Step 1: Write the Naive Prompt

Open `naive_prompt.txt` and write your first attempt.

Common naive approaches:
- Put the role description in the user message
- Mix persona with task instructions
- Long role descriptions that bury the actual task

---

## Step 2: Test Your Naive Prompt

1. Paste your naive prompt into Claude
2. Include the code
3. Run it 3 times
4. Record in `results.md`:
   - Does it maintain consistent persona across runs?
   - Does it focus on real issues or nitpick?
   - Is the tone consistent (senior engineer vs generic assistant)?
   - Does it over-explain the role vs just BE the role?

---

## Step 3: Read the Guidance

Open `guidance.md` after testing.

---

## Step 4: Write the Optimized Prompt

Open `optimized_prompt.txt` and apply system/user separation.

---

## Success Criteria

- [ ] Consistent senior engineer tone across all runs
- [ ] Focuses on substantive issues (the nested ifs, None comparison)
- [ ] Doesn't waste tokens re-explaining its role
- [ ] Feedback is actionable, not academic

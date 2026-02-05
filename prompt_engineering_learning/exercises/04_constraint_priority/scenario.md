# Exercise 04: Constraint Priority

## The Scenario

You need Claude to refactor a piece of code with multiple competing constraints:

```python
# Current code - handles user session management
class SessionManager:
    def __init__(self):
        self.sessions = {}  # user_id -> session_data
        self.MAX_SESSIONS = 1000

    def create_session(self, user_id, data):
        if len(self.sessions) >= self.MAX_SESSIONS:
            # Remove oldest session
            oldest = min(self.sessions.items(), key=lambda x: x[1]['created_at'])
            del self.sessions[oldest[0]]
        self.sessions[user_id] = {
            'data': data,
            'created_at': time.time(),
            'last_access': time.time()
        }
        return True

    def get_session(self, user_id):
        if user_id in self.sessions:
            self.sessions[user_id]['last_access'] = time.time()
            return self.sessions[user_id]['data']
        return None

    def cleanup_expired(self, max_age=3600):
        now = time.time()
        expired = [uid for uid, s in self.sessions.items()
                   if now - s['last_access'] > max_age]
        for uid in expired:
            del self.sessions[uid]
```

Your constraints are:
1. **Security**: Don't introduce vulnerabilities
2. **Backward compatibility**: Existing code using this class must still work
3. **Performance**: Improve efficiency where possible
4. **Readability**: Make the code clearer
5. **Minimal diff**: Keep changes small

These constraints WILL conflict. What happens when Claude has to choose?

## Your Task

Write a prompt with multiple constraints and observe how Claude handles conflicts.

---

## Step 1: Write the Naive Prompt

Open `naive_prompt.txt`.

Include all 5 constraints without priority ordering. Use strong language like "MUST" and "ALWAYS" for each.

---

## Step 2: Test Your Naive Prompt

Run 3 times and observe:
- Does Claude make consistent choices when constraints conflict?
- Does it break backward compatibility for readability?
- Does it make unnecessary changes (large diff)?
- Does it explain its tradeoffs or just pick arbitrarily?

---

## Step 3: Read the Guidance

Open `guidance.md` to understand constraint prioritization.

---

## Step 4: Write the Optimized Prompt

Add explicit priority ordering.

---

## Success Criteria

- [ ] Claude respects the priority order consistently
- [ ] When tradeoffs are necessary, Claude chooses correctly
- [ ] Diff is minimal (no gratuitous renaming or restructuring)
- [ ] Backward compatibility is maintained

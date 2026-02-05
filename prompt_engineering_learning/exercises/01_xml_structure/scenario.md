# Exercise 01: XML Structure

## The Scenario

You're building a feature that analyzes customer support tickets and:
1. Categorizes them (bug, feature request, billing, general inquiry)
2. Extracts key entities (product mentioned, urgency level, customer tier)
3. Suggests a response template

You have this sample ticket:

```
Subject: URGENT - App crashes when I try to export

Hi,

I've been a Pro subscriber for 2 years and I'm extremely frustrated.
Every time I click the export button in the dashboard, the app freezes
and then crashes. I've tried Chrome and Firefox. This is blocking my
quarterly report which is due tomorrow!

Please help ASAP.

- Sarah
```

## Your Task

Write a prompt that processes this ticket and returns structured analysis.

---

## Step 1: Write the Naive Prompt

Open `naive_prompt.txt` and write your first attempt.

Common naive approaches:
- Put everything in one paragraph
- Mix instructions with context
- Use vague formatting requests like "return as JSON"

Don't overthink it - write what feels natural.

---

## Step 2: Test Your Naive Prompt

1. Paste your naive prompt into Claude
2. Include the ticket text
3. Run it 3 times
4. Record results in `results.md`:
   - Did it categorize correctly all 3 times?
   - Was the JSON valid and parseable?
   - Did it extract all entities?
   - How verbose was the response?

---

## Step 3: Read the Guidance

Open `guidance.md` after you've tested your naive prompt.

---

## Step 4: Write the Optimized Prompt

Open `optimized_prompt.txt` and apply the guidance.

---

## Step 5: Compare

Test your optimized prompt 3 times and compare results.

---

## Success Criteria

You've succeeded when:
- [ ] Optimized prompt produces valid JSON every time
- [ ] All three runs extract the same entities
- [ ] No extra explanatory text around the JSON
- [ ] You understand WHY the structure helped

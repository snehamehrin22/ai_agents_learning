# Exercise 03: Explicit Intent (Why vs What)

## The Scenario

You're asking Claude to write tests for a function. Here's the function:

```python
def calculate_discount(price: float, user_tier: str, promo_code: str | None = None) -> float:
    """
    Calculate final price after applying discounts.

    Tiers: 'basic' (0%), 'silver' (5%), 'gold' (10%), 'platinum' (15%)
    Promo codes: 'SAVE10' (10% off), 'SAVE20' (20% off)
    Discounts stack multiplicatively.
    """
    tier_discounts = {'basic': 0, 'silver': 0.05, 'gold': 0.10, 'platinum': 0.15}
    promo_discounts = {'SAVE10': 0.10, 'SAVE20': 0.20}

    if user_tier not in tier_discounts:
        raise ValueError(f"Invalid tier: {user_tier}")

    discount = tier_discounts[user_tier]
    if promo_code and promo_code in promo_discounts:
        # Stack multiplicatively
        discount = 1 - (1 - discount) * (1 - promo_discounts[promo_code])

    return round(price * (1 - discount), 2)
```

## Your Task

Write a prompt that generates comprehensive tests for this function.

---

## Step 1: Write the Naive Prompt

Open `naive_prompt.txt`.

Common naive approaches:
- "Write tests for this code"
- "Create unit tests"
- Focus on WHAT (tests) without explaining WHY they matter

---

## Step 2: Test Your Naive Prompt

Run it 3 times and record:
- How many test cases?
- Does it cover edge cases?
- Does it test the stacking behavior?
- Does it test error handling?
- Are tests useful or just checking "it runs"?

---

## Step 3: Read the Guidance

Open `guidance.md` after testing.

---

## Step 4: Write the Optimized Prompt

Apply the "explain the why" principle.

---

## Success Criteria

- [ ] Tests cover all tiers
- [ ] Tests cover promo code stacking
- [ ] Tests cover invalid inputs
- [ ] Tests check boundary conditions (price = 0, negative?)
- [ ] Claude understands tests are "source of truth" and doesn't skip edge cases

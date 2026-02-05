# Claude Prompt Engineering Exercise Lab

**Core Philosophy**: You don't understand a technique until you feel the pain of not using it.

Each exercise has you write the same prompt two ways:
1. **The Naive Way** - common GPT-style or unstructured approach
2. **The Claude Way** - optimized for how Claude actually works

Then you compare: quality, consistency, token usage, and your own frustration level.

---

## Lab Structure

```
prompt_engineering_learning/
├── README.md                    # This file
├── exercises/
│   ├── 01_xml_structure/        # XML tags vs unstructured
│   ├── 02_role_separation/      # System vs user placement
│   ├── 03_explicit_intent/      # Why vs what
│   ├── 04_constraint_priority/  # Conflicting rules
│   ├── 05_tool_policy/          # Action vs suggestion
│   ├── 06_reasoning_control/    # CoT spam vs scoped reasoning
│   ├── 07_output_schema/        # Loose vs strict formatting
│   └── 08_full_integration/     # Combine all techniques
├── templates/
│   └── comparison_template.md   # For recording results
└── measurement/
    └── metrics.md               # Track your improvements
```

---

## How to Use This Lab

### For Each Exercise:

1. **Read the scenario** in `scenario.md`
2. **Write your naive prompt** in `naive_prompt.txt`
3. **Test it** by pasting into Claude and recording results
4. **Read the guidance** in `guidance.md`
5. **Write your optimized prompt** in `optimized_prompt.txt`
6. **Test again** and compare
7. **Record measurements** in `results.md`

### What to Measure:

- **Quality**: Did it do what you wanted? (1-5 scale)
- **Consistency**: Run 3 times - same results? (1-5 scale)
- **Conciseness**: Did it over-explain or stay focused?
- **Correctness**: Any hallucinations or wrong assumptions?
- **Tokens**: Rough estimate of input/output length

---

## Exercise Progression

| Exercise | Concept | Difficulty | Time |
|----------|---------|------------|------|
| 01 | XML Structure | Easy | 15 min |
| 02 | Role Separation | Easy | 15 min |
| 03 | Explicit Intent | Medium | 20 min |
| 04 | Constraint Priority | Medium | 25 min |
| 05 | Tool Policy | Medium | 20 min |
| 06 | Reasoning Control | Medium | 20 min |
| 07 | Output Schema | Medium | 20 min |
| 08 | Full Integration | Hard | 45 min |

**Total**: ~3 hours for the complete lab

---

## Key Mental Model Shifts

Before starting, internalize these Claude-specific behaviors:

1. **Claude follows instructions literally** - it won't "read between the lines"
2. **Claude uses judgment on conflicts** - it won't blindly obey contradictory MUSTs
3. **Claude mirrors your style** - terse prompts get terse outputs
4. **Claude responds to structure** - XML tags aren't decoration, they're signals
5. **Claude asks when ambiguous** - it prefers clarification over guessing

---

## Getting Started

Start with Exercise 01. Don't skip ahead - each exercise builds on previous learnings.

```bash
cd exercises/01_xml_structure
cat scenario.md
```

Good luck! Remember: the goal isn't to "get it right" immediately. The goal is to FEEL the difference between approaches.

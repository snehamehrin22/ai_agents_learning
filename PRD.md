# PRD: NotesAgent
## Notion Note Categorizer & Pattern Detector

---

## 1. Product Summary

A system that reads your daily notes from a Notion database, categorizes each note's content into dynamic tags, flags items worth exploring, detects patterns across notes over time, and outputs a weekly digest to Obsidian.

Built incrementally across 11 phases to teach AI agent patterns from first principles — simple workflow → orchestrated workflow → single agent → agent with tools → agent with memory → MCP → multi-LLM patterns → production system.

---

## 2. User (You)

- Writes sporadic, free-form stream-of-consciousness notes in Notion ("Daily Notes" database)
- Mixed media: text, links, code blocks, raw thoughts
- Wants to learn agent patterns by building something real
- Prefers raw SDK understanding over abstraction libraries

---

## 3. Requirements

### 3.1 Input
| Requirement | Detail |
|---|---|
| Source | Notion database: "Daily Notes" |
| Format | Free-form, mixed media, stream of consciousness |
| Write frequency | Sporadic, assessed end-of-day |
| Trigger | Scheduled daily poll (end of day) + manual trigger |

### 3.2 Processing
| Requirement | Detail |
|---|---|
| Categorization | Hybrid: seed categories + LLM discovers new ones |
| Seed categories | `personal/health`, `productivity/tools`, `action_items`, `research/learning`, `observations`, `self_reflection` |
| Flagging | Binary: worth_exploring (yes/no) + reason |
| Worth exploring | Business/product observations, questions, actionable insights |
| Not worth exploring | Pure personal venting, one-off annoyances, no pattern |
| Pattern detection | Weekly: recurring themes, contradictions, unresolved action items, topic drift, tone shifts |
| Deduplication | Already-explored topics are skipped (requires memory) |

### 3.3 Output
| Requirement | Detail |
|---|---|
| Destination | Obsidian markdown files (for now) |
| Content | Categories + tags + worth_exploring flag + weekly pattern digest |
| Format | Clean markdown |
| Observability | Logging of what was processed + token usage tracking |

### 3.4 Constraints
- Raw Anthropic SDK only (no LangChain/CrewAI)
- Python, intermediate level
- LLM: Claude (Anthropic)
- API keys: Bitwarden (no .env files)
- Notion integration: notion-client SDK
- Cost: not a concern

---

## 4. Phase Breakdown

### Phase 1 — Simple Workflow
**Concept:** Linear pipeline. Prompt in → LLM → structured output out.
**Build:** Hardcoded sample notes → Claude categorizes → print to terminal.
**No tools, no memory, no loops. Just raw SDK.**
- File: `phases/phase1_workflow.py`

### Phase 2 — Workflow with Orchestration
**Concept:** Conditional branching, loops, error handling.
**Build:** Multiple notes → loop through each → branch on worth_exploring → retry on failure → output to markdown file.
- File: `phases/phase2_orchestrated_workflow.py`

### Phase 3 — Simple Agent
**Concept:** Agent loop — LLM decides what to do next, not just executes.
**Build:** Agent receives notes, decides: categorize, flag, or ask for clarification. Loops until done.
- File: `phases/phase3_simple_agent.py`

### Phase 4 — Simple Agent + Tools
**Concept:** Function calling / tool use.
**Build:** Agent has callable tools: `categorize_note()`, `flag_note()`, `save_to_obsidian()`. Agent decides which tool to call and when.
- File: `phases/phase4_agent_with_tools.py`

### Phase 5 — Simple Agent + Memory
**Concept:** Conversation history + persistent store for deduplication.
**Build:** Agent remembers past runs. Skips already-explored topics. Maintains running knowledge base (JSON/SQLite).
- File: `phases/phase5_agent_with_memory.py`

### Phase 6 — Simple Agent + Memory + Tools + Context
**Concept:** Full-featured single agent.
**Build:** Everything combined. Tools + memory + context window management (summarize old data to fit).
- File: `phases/phase6_full_single_agent.py`

### Phase 7 — Simple Agent + MCP
**Concept:** Model Context Protocol — external tool servers.
**Build:** Notion integration becomes an MCP server. Agent connects dynamically instead of hardcoded tools.
- Files: `phases/phase7_agent_with_mcp.py`, `mcp_notion_server.py`

### Phase 8 — Multi-LLM: Orchestrator/Worker
**Concept:** Two models with defined roles.
**Build:** Orchestrator (Claude) reads note and decides what analysis to run. Worker (cheaper model) executes categorization and flagging.
- File: `phases/phase8_multi_llm_orchestrator.py`

### Phase 9 — Multi-LLM: Pipeline
**Concept:** Chained specialization.
**Build:** Model 1 categorizes → Model 2 detects patterns → Model 3 synthesizes weekly digest.
- File: `phases/phase9_multi_llm_pipeline.py`

### Phase 10 — Multi-LLM: Debate/Critique
**Concept:** Adversarial refinement.
**Build:** Categorizer tags the note → Critic challenges the tags → Judge resolves and outputs final.
- File: `phases/phase10_multi_llm_debate.py`

### Phase 11 — Production System
**Concept:** Everything combined into a real product.
**Build:** Notion poll (scheduled) → multi-LLM pipeline categorization → pattern detection → weekly digest to Obsidian → logging + token tracking.
- File: `phases/phase11_production_system.py`

---

## 5. File Structure

```
ai_agents_learning/
├── CLAUDE.md                         # Project instructions for Claude
├── PRD.md                            # This file
├── requirements.txt                  # All dependencies
├── # API keys managed via Bitwarden (no .env)
├── phases/
│   ├── phase1_workflow.py
│   ├── phase2_orchestrated_workflow.py
│   ├── phase3_simple_agent.py
│   ├── phase4_agent_with_tools.py
│   ├── phase5_agent_with_memory.py
│   ├── phase6_full_single_agent.py
│   ├── phase7_agent_with_mcp.py
│   ├── phase8_multi_llm_orchestrator.py
│   ├── phase9_multi_llm_pipeline.py
│   ├── phase10_multi_llm_debate.py
│   └── phase11_production_system.py
├── mcp_notion_server.py              # MCP server for Notion (Phase 7+)
├── sample_notes/                     # Test data
│   └── sample_note_1.txt
└── obsidian_output/
    └── digests/                      # Weekly digest output
```

---

## 6. Dependencies

```
anthropic>=0.40.0        # Claude SDK (raw)
notion-client>=2.22.0    # Notion API
```

---

## 7. Day-by-Day Execution Plan

**Assumptions:** 8 hours/day available. Each phase includes build + test + verify it works before moving on.

| Day | Date | Hours | What Gets Done |
|---|---|---|---|
| **Day 1** | Jan 28 | 8h | **Setup + Phase 1 + Phase 2** |
| | | | - Project setup: requirements.txt, folder structure, Bitwarden keys (1h) |
| | | | - Phase 1: Simple workflow — hardcoded notes → Claude categorizes → print output (3h) |
| | | | - Phase 2: Orchestrated workflow — loop, branching, error handling, markdown output (4h) |
| **Day 2** | Jan 29 | 8h | **Phase 3 + Phase 4** |
| | | | - Phase 3: Simple agent loop — LLM decides next action (3h) |
| | | | - Phase 4: Agent + tools — function calling, tool definitions, Obsidian save tool (5h) |
| **Day 3** | Jan 30 | 8h | **Phase 5 + Phase 6** |
| | | | - Phase 5: Agent + memory — persistent store, deduplication logic (4h) |
| | | | - Phase 6: Full single agent — combine memory + tools + context management (4h) |
| **Day 4** | Jan 31 | 8h | **Phase 7 (MCP) + Notion integration** |
| | | | - Build MCP server for Notion (3h) |
| | | | - Phase 7: Agent connects to MCP server, reads real Notion notes (5h) |
| **Day 5** | Feb 1 | 8h | **Phase 8 + Phase 9** |
| | | | - Phase 8: Multi-LLM orchestrator/worker pattern (4h) |
| | | | - Phase 9: Multi-LLM pipeline — chained specialization (4h) |
| **Day 6** | Feb 2 | 8h | **Phase 10 + Phase 11 (start)** |
| | | | - Phase 10: Debate/critique pattern (3h) |
| | | | - Phase 11: Begin production system assembly (5h) |
| **Day 7** | Feb 3 | 8h | **Phase 11 (finish) + Polish** |
| | | | - Finish production system: scheduling, full Notion → Obsidian pipeline (4h) |
| | | | - Add logging + token usage tracking (2h) |
| | | | - End-to-end test with real notes, fix issues (2h) |

### Total: 7 days (Jan 28 – Feb 3)

### Daily Rhythm Suggestion
```
Morning (2-3h)  — Build the phase, write the code
Midday (2-3h)   — Test it, debug, verify output looks right
Afternoon (2-3h) — Polish, add comments, prep for next phase
```

---

## 8. Success Criteria

| Phase | "Done" means |
|---|---|
| Phase 1 | Run script → see categorized notes printed to terminal |
| Phase 2 | Run script → see markdown file with categories + flags |
| Phase 3 | Agent loops through notes without manual intervention |
| Phase 4 | Agent calls tools correctly, saves to Obsidian |
| Phase 5 | Deduplication works — re-run skips already-seen topics |
| Phase 6 | Full agent handles 10+ notes without context overflow |
| Phase 7 | Agent reads live Notion data via MCP |
| Phase 8 | Two models collaborate, output is better than single model |
| Phase 9 | Pipeline produces weekly digest from raw notes |
| Phase 10 | Debate improves categorization accuracy |
| Phase 11 | End-to-end: Notion → categorize → patterns → Obsidian digest, scheduled |

---

## 9. What We Learn at Each Phase

| Phase | Key Concept | Why It Matters |
|---|---|---|
| 1 | Raw SDK calls, prompt engineering | Foundation — how LLMs actually work |
| 2 | Control flow around LLMs | Real pipelines aren't just one call |
| 3 | Agent loops | When LLMs need to think, not just execute |
| 4 | Tool use / function calling | How agents interact with the world |
| 5 | Persistence & memory | Agents need to remember |
| 6 | Context management | Fitting everything into a finite window |
| 7 | MCP protocol | Industry standard for tool servers |
| 8 | Orchestrator/Worker | Dividing labor between models |
| 9 | Pipeline specialization | Each model does one thing well |
| 10 | Adversarial refinement | Self-correction via debate |
| 11 | Production systems | Scheduling, logging, reliability |

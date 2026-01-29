# NotesAgent — Project Instructions for Claude

## Project Purpose
Learning-driven project that teaches AI agent patterns by building a real product:
reads Notion daily notes → categorizes them → flags items worth exploring → detects patterns → outputs weekly digest to Obsidian.

## Build Rules
- All dependencies go in `requirements.txt` at project root
- Each phase is a standalone runnable script in `phases/`
- When refactoring or moving to a new phase, delete scripts that are no longer needed
- Use raw Anthropic SDK — no LangChain, no CrewAI, no abstractions (learning from first principles)
- API keys are managed via Bitwarden (no .env files)
- Sample/test notes live in `sample_notes/`
- Obsidian output goes to `obsidian_output/digests/`

## Coding Style
- Python, clean and well-commented (this is a learning project — comments explain WHY, not just what)
- Type hints on all functions
- Each phase script is self-contained and runnable with `python phases/phaseN_*.py`
- Print clear section headers when running so the user can follow the logic

## Phase Progression
Phase 1 → 2 → 3 → ... → 11. Each builds on the last. See PRD.md for full breakdown.
Current phase: **Phase 1**

## Key Decisions
- Output destination: Obsidian (markdown files) for now
- Memory store: SQLite or JSON (raw, educational — no vector DB until needed)
- LLM: Claude via Anthropic SDK
- Notion client: notion-client SDK
- Categorization: Hybrid (seed categories + LLM discovers new ones)
- Deduplication: Yes, skip already-explored topics
- Observability: Logging + token usage tracking

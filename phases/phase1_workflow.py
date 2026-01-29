"""
Phase 1 — Simple Workflow (Per-Note Classification → Full-Table Sensemaking)
-----------------------------------------------------------------------------
Concept: Linear pipeline. Prompt in → LLM → structured markdown out.
No tools, no memory, no loops. Just raw Anthropic SDK calls.

THIS SCRIPT:
  1. Fetches all notes from Notion (live)
  2. Runs each note individually through Pass 1 (classification) — cheap per-note calls
  3. Accumulates all classified rows into one Obsidian file
  4. Feeds the full classification table through Pass 2 (sensemaking) — single call
  5. Appends sensemaking output to the same Obsidian file

Prompts are stored in prompts.txt (not hardcoded here).

Usage:
    python phases/phase1_workflow.py
"""

import os
import sys
from datetime import datetime
import anthropic
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Add phases/ to path so we can import the connector
sys.path.insert(0, os.path.dirname(__file__))
from notion_connector import get_secrets, fetch_notion_notes

# Paths
OBSIDIAN_PATH = "/Users/snehamehrin/Desktop/obsidian_vaults/App Analysis/AI Agent Learning"
PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "prompts.txt")


def load_prompts() -> dict:
    """
    Loads prompts from prompts.txt.
    Parses by key markers (================... KEY: ... ================).
    Returns dict with prompt text keyed by name.
    """
    with open(PROMPTS_PATH, "r") as f:
        content = f.read()

    prompts = {}
    sections = content.split("=" * 80)

    current_key = None

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Look for "Key: PROMPT_NAME" lines
        for line in section.split("\n"):
            if line.strip().startswith("Key:"):
                current_key = line.strip().replace("Key:", "").strip()
                break
        else:
            # This section doesn't have a Key line — it's prompt body
            if current_key and section:
                if "––––––––––––––––\nINPUT\n––––––––––––––––" in section:
                    prompt_body = section.split("––––––––––––––––\nINPUT\n––––––––––––––––")[0]
                    prompt_body += "\n––––––––––––––––\nINPUT\n––––––––––––––––\n\n"
                    prompts[current_key] = prompt_body
                else:
                    prompts[current_key] = section + "\n\n"
                current_key = None

    return prompts


def format_single_note(note: dict) -> str:
    """Formats a single note for the classification prompt."""
    return f"**{note['title']}:**\n{note['content']}"


def run_classification_single(client: anthropic.Anthropic, note: dict, prompt: str) -> dict:
    """
    Pass 1: Classify a single note. Returns the markdown table rows.
    """
    note_text = format_single_note(note)
    full_prompt = prompt + note_text

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )

    return {
        "markdown_output": message.content[0].text,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
    }


def run_sensemaking(client: anthropic.Anthropic, classification_table: str, prompt: str) -> dict:
    """
    Pass 2: Per-note thinking mode annotation over the full classification table.
    """
    full_prompt = prompt + classification_table

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        messages=[
            {"role": "user", "content": full_prompt}
        ]
    )

    return {
        "markdown_output": message.content[0].text,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
    }


def extract_table_rows(markdown_output: str) -> list[str]:
    """
    Extracts table rows (excluding header and separator) from a markdown table.
    Returns list of row strings like "| note | category | tags |"
    """
    lines = markdown_output.strip().split("\n")
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue
        # Skip header row and separator row
        if "---|" in line or "---" == line.replace("|", "").replace(" ", "").replace("-", ""):
            continue
        # Skip if it looks like a header (contains "Original Note" or "Primary Category")
        if "Original Note" in line and "Primary Category" in line:
            continue
        rows.append(line)
    return rows


def main():
    print("=" * 60)
    print("  PHASE 1 — PER-NOTE CLASSIFICATION → FULL-TABLE SENSEMAKING")
    print("=" * 60)

    # Initialize Anthropic client
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY in .env")
    client = anthropic.Anthropic(api_key=anthropic_key)

    # Load prompts from prompts.txt
    print("\n  Loading prompts...")
    prompts = load_prompts()
    print(f"  Loaded: {list(prompts.keys())}\n")

    # --- Fetch live notes from Notion ---
    print("  Fetching notes from Notion...")
    notion_key, database_id = get_secrets()
    notes = fetch_notion_notes(notion_key, database_id)

    # Filter out empty or untitled notes
    notes = [n for n in notes if n.get("title") and n.get("content", "").strip()]
    print(f"  Got {len(notes)} notes with content\n")

    if not notes:
        print("  No notes to process. Exiting.")
        return

    # --- Pass 1: Classify each note individually ---
    all_rows = []
    total_p1_in = 0
    total_p1_out = 0

    for i, note in enumerate(notes, 1):
        print(f"  [Pass 1 - {i}/{len(notes)}] Classifying: {note['title']}...")
        result = run_classification_single(client, note, prompts["CLASSIFICATION_PROMPT"])
        total_p1_in += result["input_tokens"]
        total_p1_out += result["output_tokens"]
        print(f"    {result['input_tokens']} in / {result['output_tokens']} out")

        # Extract just the table rows (no header)
        rows = extract_table_rows(result["markdown_output"])
        all_rows.extend(rows)

    # Build full classification table with header
    header = "| Original Note (verbatim chunk) | Primary Category | Secondary Categories (comma-separated) |"
    separator = "|---|---|---|"
    full_classification_table = "\n".join([header, separator] + all_rows)

    print(f"\n  Pass 1 complete. {len(all_rows)} total rows.")
    print(f"  Tokens: {total_p1_in} in / {total_p1_out} out\n")

    # --- Pass 2: Sensemaking over the full table ---
    print("  [Pass 2] Sensemaking over full classification table...")
    sensemaking = run_sensemaking(client, full_classification_table, prompts["SECOND_ORDER_PROMPT"])
    print(f"  Done. {sensemaking['input_tokens']} in / {sensemaking['output_tokens']} out\n")

    # --- Save to Obsidian ---
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_titles = ", ".join(n["title"] for n in notes)
    filename = f"Phase1 - Sensemaking [{timestamp}].md"
    filepath = os.path.join(OBSIDIAN_PATH, filename)

    total_in = total_p1_in + sensemaking["input_tokens"]
    total_out = total_p1_out + sensemaking["output_tokens"]

    md = f"""# Phase 1 — Two-Pass Sensemaking

**Processed:** {timestamp}
**Model:** claude-sonnet-4-5-20250929
**Total tokens:** {total_in} in / {total_out} out
**Notes processed:** {note_titles}

---

## Pass 1 — Classification (per-note, structural indexing)
*Tokens: {total_p1_in} in / {total_p1_out} out*

{full_classification_table}

---

## Pass 2 — Sensemaking (thinking mode annotation)
*Tokens: {sensemaking['input_tokens']} in / {sensemaking['output_tokens']} out*

{sensemaking['markdown_output']}

---

## Raw Input Notes

"""
    for note in notes:
        md += f"""### {note['title']}
> {note['content']}

"""

    with open(filepath, "w") as f:
        f.write(md)

    print(f"  Saved: {filename}")
    print(f"\n  Total: {total_in} in / {total_out} out")
    print("  Done.")


if __name__ == "__main__":
    main()

"""
Export All Notion Notes to One Markdown File
---------------------------------------------
Fetches all notes from Notion and combines them into a single markdown file.

Usage:
    python experiments/export_all_notes.py
"""

import os
import sys
from datetime import datetime

# Add phases/ to path so we can import the connector
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phases"))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
from notion_connector import get_secrets, fetch_notion_notes

# Output path
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "all_notes.md")


def main():
    print("=" * 60)
    print("  EXPORT ALL NOTES TO MARKDOWN")
    print("=" * 60)

    # Fetch notes from Notion
    print("\n  Fetching notes from Notion...")
    notion_key, database_id = get_secrets()
    notes = fetch_notion_notes(notion_key, database_id)

    # Filter out empty or untitled notes
    notes = [n for n in notes if n.get("title") and n.get("content", "").strip()]
    print(f"  Got {len(notes)} notes with content\n")

    if not notes:
        print("  No notes to export. Exiting.")
        return

    # Build combined markdown
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    md = f"""# All Daily Notes

**Exported:** {timestamp}
**Total notes:** {len(notes)}

---

"""

    for i, note in enumerate(notes, 1):
        md += f"""## {note['title']}

**Created:** {note.get('created', 'unknown')[:10]}

{note['content']}

---

"""

    # Save to file
    with open(OUTPUT_PATH, "w") as f:
        f.write(md)

    print(f"  Saved: {OUTPUT_PATH}")
    print(f"  Total: {len(notes)} notes\n")
    print("  Done.")


if __name__ == "__main__":
    main()

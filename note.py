#!/usr/bin/env python3
"""
Simple note-taking CLI app
"""
import json
import sys
from pathlib import Path
from datetime import datetime


NOTES_FILE = Path.home() / ".notes.json"


def load_notes():
    """Load notes from JSON file."""
    if not NOTES_FILE.exists():
        return []

    with open(NOTES_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    """Save notes to JSON file."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def add_note(text):
    """Add a new note."""
    notes = load_notes()

    note = {
        "id": len(notes) + 1,
        "text": text,
        "created": datetime.now().isoformat(),
        "done": False
    }

    notes.append(note)
    save_notes(notes)

    print(f"✓ Added note #{note['id']}: {text}")


def list_notes():
    """List all notes."""
    notes = load_notes()

    if not notes:
        print("No notes yet. Add one with: note add \"your note\"")
        return

    print(f"\n{'ID':<4} {'Status':<8} {'Note':<50} {'Created':<20}")
    print("-" * 82)

    for note in notes:
        status = "✓ Done" if note["done"] else "○ Todo"
        created = note["created"][:10]  # Just the date
        print(f"{note['id']:<4} {status:<8} {note['text']:<50} {created:<20}")

    print()


def search_notes(query):
    """Search notes by text content (case-insensitive)."""
    notes = load_notes()

    if not notes:
        print("No notes to search. Add one with: note add \"your note\"")
        return

    query_lower = query.lower()
    matches = [note for note in notes if query_lower in note["text"].lower()]

    if not matches:
        print(f"No notes found matching '{query}'")
        return

    print(f"\nFound {len(matches)} note(s) matching '{query}':\n")
    print(f"{'ID':<4} {'Note':<50} {'Created':<20}")
    print("-" * 74)

    for note in matches:
        # Highlight matching text by showing it with >>> <<<
        text = note["text"]
        text_lower = text.lower()

        # Find the position of the match
        match_start = text_lower.find(query_lower)
        if match_start != -1:
            match_end = match_start + len(query)
            highlighted = (
                text[:match_start] +
                ">>>" + text[match_start:match_end] + "<<<" +
                text[match_end:]
            )
        else:
            highlighted = text

        created = note["created"][:10]  # Just the date
        print(f"{note['id']:<4} {highlighted:<50} {created:<20}")

    print()


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  note add <text>     - Add a new note")
        print("  note list           - List all notes")
        print("  note search <query> - Search notes by text content")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide note text")
            sys.exit(1)
        text = " ".join(sys.argv[2:])
        add_note(text)

    elif command == "list":
        list_notes()

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Please provide search query")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        search_notes(query)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

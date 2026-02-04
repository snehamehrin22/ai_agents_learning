#!/usr/bin/env python3
"""
Simple note-taking CLI app with search, tags, and export features
"""
import json
import sys
import csv
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


def add_note(text, tags=None):
    """Add a new note with optional tags."""
    notes = load_notes()

    note = {
        "id": len(notes) + 1,
        "text": text,
        "created": datetime.now().isoformat(),
        "done": False,
        "tags": tags if tags else []
    }

    notes.append(note)
    save_notes(notes)

    tags_display = f" [tags: {', '.join(tags)}]" if tags else ""
    print(f"✓ Added note #{note['id']}: {text}{tags_display}")


def list_notes():
    """List all notes."""
    notes = load_notes()

    if not notes:
        print("No notes yet. Add one with: note add \"your note\"")
        return

    print(f"\n{'ID':<4} {'Status':<8} {'Note':<35} {'Tags':<20} {'Created':<12}")
    print("-" * 80)

    for note in notes:
        status = "✓ Done" if note["done"] else "○ Todo"
        created = note["created"][:10]  # Just the date
        tags = ", ".join(note.get("tags", [])) if note.get("tags") else ""
        print(f"{note['id']:<4} {status:<8} {note['text']:<35} {tags:<20} {created:<12}")

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


def list_tags():
    """List all tags with their counts."""
    notes = load_notes()

    if not notes:
        print("No notes yet. Add one with: note add \"your note\"")
        return

    # Count tags
    tag_counts = {}
    for note in notes:
        for tag in note.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    if not tag_counts:
        print("No tags found. Add tags with: note add \"text\" --tags tag1,tag2")
        return

    print(f"\n{'Tag':<30} {'Count':<10}")
    print("-" * 40)

    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{tag:<30} {count:<10}")

    print()


def filter_by_tag(tag):
    """Show notes filtered by a specific tag."""
    notes = load_notes()

    if not notes:
        print("No notes yet. Add one with: note add \"your note\"")
        return

    # Filter notes by tag
    filtered_notes = [note for note in notes if tag in note.get("tags", [])]

    if not filtered_notes:
        print(f"No notes found with tag: {tag}")
        return

    print(f"\nNotes with tag '{tag}':")
    print(f"\n{'ID':<4} {'Status':<8} {'Note':<35} {'Tags':<20} {'Created':<12}")
    print("-" * 80)

    for note in filtered_notes:
        status = "✓ Done" if note["done"] else "○ Todo"
        created = note["created"][:10]  # Just the date
        tags = ", ".join(note.get("tags", []))
        print(f"{note['id']:<4} {status:<8} {note['text']:<35} {tags:<20} {created:<12}")

    print()


def export_markdown(notes, filename):
    """Export notes to Markdown format."""
    with open(filename, "w") as f:
        f.write("# Notes Export\n\n")
        f.write(f"*Exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")

        for note in notes:
            status = "Done" if note["done"] else "Todo"
            created_date = note["created"][:10]
            tags = note.get("tags", [])
            tags_str = f"Tags: {', '.join(tags)}" if tags else "No tags"

            f.write(f"## Note #{note['id']}\n\n")
            f.write(f"**Status:** {status}  \n")
            f.write(f"**Created:** {created_date}  \n")
            f.write(f"**{tags_str}**  \n")
            f.write(f"**Content:** {note['text']}\n\n")
            f.write("---\n\n")

    print(f"✓ Exported {len(notes)} notes to {filename}")


def export_csv(notes, filename):
    """Export notes to CSV format."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "text", "created", "done", "tags"])

        for note in notes:
            tags_str = ", ".join(note.get("tags", []))
            writer.writerow([
                note["id"],
                note["text"],
                note["created"],
                note["done"],
                tags_str
            ])

    print(f"✓ Exported {len(notes)} notes to {filename}")


def export_txt(notes, filename):
    """Export notes to plain text format."""
    with open(filename, "w") as f:
        f.write(f"Notes Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for note in notes:
            status = "[✓]" if note["done"] else "[ ]"
            created_date = note["created"][:10]
            tags = note.get("tags", [])
            tags_str = f" [{', '.join(tags)}]" if tags else ""
            f.write(f"{status} #{note['id']} ({created_date}): {note['text']}{tags_str}\n")

    print(f"✓ Exported {len(notes)} notes to {filename}")


def export_notes(format_type):
    """Export all notes to the specified format."""
    notes = load_notes()

    if not notes:
        print("No notes to export. Add some notes first!")
        return

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"notes_export_{timestamp}.{format_type}"

    # Export based on format
    if format_type == "markdown" or format_type == "md":
        export_markdown(notes, filename)
    elif format_type == "csv":
        export_csv(notes, filename)
    elif format_type == "txt":
        export_txt(notes, filename)
    else:
        print(f"Error: Unsupported format '{format_type}'")
        print("Supported formats: markdown, csv, txt")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  note add <text> [--tags tag1,tag2]  - Add a new note with optional tags")
        print("  note list                            - List all notes")
        print("  note search <query>                  - Search notes by text content")
        print("  note tags                            - List all tags with counts")
        print("  note filter <tag>                    - Show notes with a specific tag")
        print("  note export <format>                 - Export notes (formats: markdown, csv, txt)")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide note text")
            sys.exit(1)

        # Parse arguments for --tags option
        args = sys.argv[2:]
        tags = None
        text_parts = []

        i = 0
        while i < len(args):
            if args[i] == "--tags":
                if i + 1 < len(args):
                    # Split tags by comma and strip whitespace
                    tags = [tag.strip() for tag in args[i + 1].split(",")]
                    i += 2
                else:
                    print("Error: --tags requires a value (e.g., --tags work,personal)")
                    sys.exit(1)
            else:
                text_parts.append(args[i])
                i += 1

        if not text_parts:
            print("Error: Please provide note text")
            sys.exit(1)

        text = " ".join(text_parts)
        add_note(text, tags)

    elif command == "list":
        list_notes()

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: Please provide search query")
            sys.exit(1)
        query = " ".join(sys.argv[2:])
        search_notes(query)

    elif command == "tags":
        list_tags()

    elif command == "filter":
        if len(sys.argv) < 3:
            print("Error: Please provide a tag to filter by")
            sys.exit(1)
        tag = sys.argv[2]
        filter_by_tag(tag)

    elif command == "export":
        if len(sys.argv) < 3:
            print("Error: Please specify export format (markdown, csv, or txt)")
            sys.exit(1)
        format_type = sys.argv[2].lower()
        export_notes(format_type)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

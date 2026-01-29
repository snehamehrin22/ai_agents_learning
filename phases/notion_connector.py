"""
Notion Connector
----------------
Reads API key and database ID from .env file,
then fetches all notes from the "Daily Notes" database.

Uses raw httpx calls to the Notion API (no notion-client library).
This is intentional — we want to understand the API from first principles.

Usage:
    python phases/notion_connector.py

Requires:
    - .env file at project root with NOTION_API_KEY and NOTION_DATABASE_ID
    - httpx installed (comes with anthropic)
"""

import os
import httpx
from dotenv import load_dotenv

# Load .env from project root (one level up from phases/)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Notion API base URL and required version header
NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def get_secrets() -> tuple[str, str]:
    """
    Reads NOTION_API_KEY and NOTION_DATABASE_ID from .env.
    Returns (api_key, database_id).
    """
    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not api_key or not database_id:
        raise RuntimeError(
            "Missing env vars. Create a .env file at project root with:\n"
            "  NOTION_API_KEY=secret_xxx\n"
            "  NOTION_DATABASE_ID=xxx\n"
        )

    # Notion API expects UUID format with dashes
    # Auto-convert if it's a raw 32-char hex string
    if len(database_id) == 32 and "-" not in database_id:
        database_id = (
            f"{database_id[:8]}-{database_id[8:12]}-{database_id[12:16]}"
            f"-{database_id[16:20]}-{database_id[20:]}"
        )

    return api_key, database_id


def get_headers(api_key: str) -> dict:
    """Standard headers for all Notion API calls."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def query_database(api_key: str, database_id: str) -> list[dict]:
    """
    Queries a Notion database and returns all pages.
    Uses POST /databases/{id}/query endpoint.
    """
    resp = httpx.post(
        f"{NOTION_BASE_URL}/databases/{database_id}/query",
        headers=get_headers(api_key),
        json={},  # empty body = no filters, return all
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def get_page_content(api_key: str, page_id: str) -> str:
    """
    Retrieves all blocks from a Notion page and concatenates them
    into a single plain-text string.
    Uses GET /blocks/{id}/children endpoint.
    """
    resp = httpx.get(
        f"{NOTION_BASE_URL}/blocks/{page_id}/children",
        headers=get_headers(api_key),
        timeout=30.0,
    )
    resp.raise_for_status()
    block_list = resp.json().get("results", [])

    text_parts = []
    for block in block_list:
        block_type = block.get("type", "")
        block_data = block.get(block_type, {})

        # Handle the most common block types
        if block_type in (
            "paragraph", "heading_1", "heading_2", "heading_3",
            "bulleted_list_item", "numbered_list_item"
        ):
            rich_text = block_data.get("rich_text", [])
            line = "".join(rt.get("plain_text", "") for rt in rich_text)
            text_parts.append(line)

        elif block_type == "code":
            rich_text = block_data.get("rich_text", [])
            code = "".join(rt.get("plain_text", "") for rt in rich_text)
            language = block_data.get("language", "")
            text_parts.append(f"```{language}\n{code}\n```")

        elif block_type == "quote":
            rich_text = block_data.get("rich_text", [])
            quote = "".join(rt.get("plain_text", "") for rt in rich_text)
            text_parts.append(f"> {quote}")

        elif block_type == "divider":
            text_parts.append("---")

        elif block_type == "toggle":
            rich_text = block_data.get("rich_text", [])
            toggle_title = "".join(rt.get("plain_text", "") for rt in rich_text)
            text_parts.append(f"[Toggle] {toggle_title}")

        # Skip unsupported types (images, files, etc.) silently

    return "\n".join(text_parts)


def fetch_notion_notes(api_key: str, database_id: str) -> list[dict]:
    """
    Fetches all pages from a Notion database.
    Returns a list of dicts, each with:
        - id: page ID
        - title: page title (from the Name property)
        - content: full page content as plain text
        - created: creation timestamp
    """
    pages = query_database(api_key, database_id)

    notes = []
    for page in pages:
        # Extract title from the Name property
        title = ""
        name_prop = page.get("properties", {}).get("Name", {})
        if name_prop.get("title"):
            title = name_prop["title"][0].get("plain_text", "")

        # Fetch the full page content (blocks)
        content = get_page_content(api_key, page["id"])

        notes.append({
            "id": page["id"],
            "title": title,
            "content": content,
            "created": page.get("created_time", ""),
        })

    return notes


def main():
    print("=" * 60)
    print("  NOTION CONNECTOR")
    print("=" * 60)

    # Step 1: Load secrets from .env
    print("\n[1/3] Loading secrets from .env...")
    api_key, database_id = get_secrets()
    print(f"      API key: {api_key[:12]}...")
    print(f"      Database ID: {database_id}")

    # Step 2: Fetch notes from Notion
    print("\n[2/3] Fetching notes from Notion database...")
    notes = fetch_notion_notes(api_key, database_id)
    print(f"      Found {len(notes)} notes")

    # Step 3: Display results
    print("\n[3/3] Notes summary:")
    print("-" * 60)
    for i, note in enumerate(notes, 1):
        print(f"\n  Note {i}: {note['title'] or '(untitled)'}")
        print(f"  Created: {note['created']}")
        preview = note['content'][:150].replace('\n', ' ')
        print(f"  Preview: {preview}...")
        print()

    print("=" * 60)
    print(f"  Done. {len(notes)} notes fetched successfully.")
    print("=" * 60)

    return notes


if __name__ == "__main__":
    main()

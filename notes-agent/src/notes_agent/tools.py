"""
Tools for external I/O: Notion and Supabase.
This module ONLY does I/O - no business logic.
"""
import os
from typing import List, Optional
from datetime import datetime
from notion_client import Client as NotionClient
from supabase import create_client, Client as SupabaseClient

from .schemas import NotionEntry, BlockClassification


def get_notion_client() -> NotionClient:
    """Get configured Notion client."""
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        raise ValueError("NOTION_API_KEY not set in environment")
    return NotionClient(auth=api_key)


def get_supabase_client() -> SupabaseClient:
    """Get configured Supabase client."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

    from supabase.lib.client_options import SyncClientOptions
    return create_client(url, key, options=SyncClientOptions(schema="raw"))


def fetch_latest_notion_entries(limit: int = 10) -> List[NotionEntry]:
    """
    Fetch the latest journal entries from Notion.

    Args:
        limit: Maximum number of entries to fetch

    Returns:
        List of NotionEntry objects

    Raises:
        ValueError: If Notion credentials are missing
        Exception: If Notion API call fails
    """
    notion = get_notion_client()
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not database_id:
        raise ValueError("NOTION_DATABASE_ID not set in environment")

    # Query Notion database - get latest entries
    # Use direct HTTP request since notion-client doesn't expose query method properly
    import httpx

    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        'Authorization': f'Bearer {notion.options.auth}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    body = {
        'page_size': limit,
        'sorts': [{'timestamp': 'created_time', 'direction': 'descending'}]
    }

    http_response = httpx.post(url, headers=headers, json=body)
    http_response.raise_for_status()
    response = http_response.json()

    entries = []
    for page in response.get("results", []):
        page_id = page["id"]
        created_time = datetime.fromisoformat(page["created_time"].replace("Z", "+00:00"))

        # Fetch page blocks to get actual content
        blocks_url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        blocks_response = httpx.get(blocks_url, headers=headers)
        blocks_response.raise_for_status()
        blocks_data = blocks_response.json()

        # Extract text from all blocks
        content_parts = []
        for block in blocks_data.get("results", []):
            block_type = block.get("type")
            if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "to_do", "quote", "callout"]:
                # Get rich_text from the block
                rich_text = block.get(block_type, {}).get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    content_parts.append(text)

        content = "\n".join(content_parts)

        if content.strip():  # Only include non-empty entries
            entries.append(NotionEntry(
                id=page_id,
                created_time=created_time,
                content=content
            ))

    return entries


def check_already_processed(notion_entry_id: str) -> bool:
    """
    Check if a Notion entry has already been processed.

    Args:
        notion_entry_id: Notion page ID

    Returns:
        True if already processed, False otherwise
    """
    supabase = get_supabase_client()

    result = supabase.table("processed_entries").select("notion_entry_id").eq(
        "notion_entry_id", notion_entry_id
    ).execute()

    return len(result.data) > 0


def write_classification_to_supabase(
    notion_entry_id: str,
    block_name: str,
    classification: BlockClassification
) -> bool:
    """
    Write a classified block to Supabase.

    Args:
        notion_entry_id: Notion page ID
        block_name: Human-readable block name
        classification: Validated BlockClassification object

    Returns:
        True if write succeeded, False otherwise

    Note:
        Uses ON CONFLICT DO NOTHING (via UNIQUE constraint) for idempotency
    """
    supabase = get_supabase_client()

    # Extract block number from block_id (e.g., "b1" -> 1)
    block_number = int(classification.block_id.replace("b", ""))

    data = {
        "notion_page_id": notion_entry_id,
        "block_number": block_number,
        "block_text": classification.block_text,
        "themes": classification.themes,
        "core_emotion": classification.core_emotion,
        "nervous_system_state": classification.nervous_system_state,
        "behavioral_response": classification.behavioral_response,
        "fear_underneath": classification.fear_underneath,
        "self_concept_gap": classification.self_concept_gap,
        "action_signal": classification.action_signal,
        "action_note": classification.action_note
        # Note: confidence field not in schema, skip it
    }

    try:
        supabase.table("journal_blocks").insert(data).execute()
        return True
    except Exception as e:
        # UNIQUE constraint violations are expected (duplicate blocks) - ignore them
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            return True  # Already exists, that's fine
        raise  # Re-raise other errors


def mark_entry_as_processed(notion_entry_id: str, block_count: int) -> None:
    """
    Mark a Notion entry as fully processed.

    Args:
        notion_entry_id: Notion page ID
        block_count: Number of blocks processed
    """
    supabase = get_supabase_client()

    data = {
        "notion_entry_id": notion_entry_id,
        "block_count": block_count
    }

    supabase.table("processed_entries").insert(data).execute()

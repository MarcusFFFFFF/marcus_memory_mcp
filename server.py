"""
marcus_memory_mcp/server.py — MCP-server för marcus_memory.

Exponerar marcus_memory:s sökning, add, get-by-ids, och thread-context som
MCP-tools så Claude Code / Desktop / andra MCP-klienter kan ansluta.

Status: skiss 2026-06-07. Kräver `pip3 install --user mcp` för att köra.

Tools:
    recall(query, k=5, min_score=0.30, source_contains=None, since=None)
        → list of {id, text, source, ts, score}

    remember(text, source)
        → {inserted: int}

    get_by_ids(ids)
        → list of {id, text, source, ts}

    thread_context(memory_id, before=1, after=1)
        → list of {id, text, source, ts, position} or null

Köra:
    python3 server.py
    # eller via MCP-klient-config med 'command: python3', 'args: [server.py]'
"""

import sys
import os
from pathlib import Path

# Lägg till marcus_memory på path
MARCUS_MEMORY_PATH = Path.home() / "marcus_memory"
if str(MARCUS_MEMORY_PATH) not in sys.path:
    sys.path.insert(0, str(MARCUS_MEMORY_PATH))

try:
    import memory_core
except ImportError as e:
    print(f"FEL: kan inte importera memory_core från {MARCUS_MEMORY_PATH}: {e}", file=sys.stderr)
    sys.exit(1)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("FEL: mcp SDK saknas. Installera: pip3 install --user mcp", file=sys.stderr)
    sys.exit(1)


mcp = FastMCP("marcus-memory")


@mcp.tool()
def recall(
    query: str,
    k: int = 5,
    min_score: float = 0.30,
    source_contains: str | None = None,
    since: str | None = None,
) -> list[dict]:
    """
    Sök i marcus_memory med embedding-similarity + optional source/since-filter.

    Args:
        query: söktext (embeddas och jämförs mot lagrade vektorer)
        k: max antal träffar
        min_score: minsta cosine similarity (default 0.30; sätt lägre om ni vill ha brett)
        source_contains: SQL LIKE %X% mot source-fältet
        since: ISO-timestamp; bara poster med ts >= since
    """
    results = memory_core.search(
        query=query,
        k=k,
        min_score=min_score,
        source_contains=source_contains,
        since=since,
    )
    return [r for r in results if isinstance(r, dict)]


@mcp.tool()
def remember(text: str, source: str) -> dict:
    """
    Skriv ny post i marcus_memory.

    Args:
        text: innehållet
        source: namespace (t.ex. 'workshop-code-out', 'manual', etc.)

    Returns:
        {inserted: int} — 1 vid framgång, 0 vid duplicat (samma hash)
    """
    inserted = memory_core.add_memories([(text, source)])
    return {"inserted": inserted, "source": source, "bytes": len(text)}


@mcp.tool()
def get_by_ids(ids: list[int]) -> list[dict]:
    """
    Hämta exakta poster på ID. Bevarar ordning av input-listan.
    """
    return memory_core.get_by_ids(ids)


@mcp.tool()
def thread_context(memory_id: int, before: int = 1, after: int = 1) -> list[dict] | None:
    """
    Hämta intilliggande rader i samma tråd. None om posten saknar thread-metadata.

    Args:
        memory_id: ID på centerposten
        before: antal poster innan
        after: antal poster efter
    """
    return memory_core.get_context(memory_id, before=before, after=after)


def main():
    # Default: stdio transport (vad MCP-klienter förväntar sig)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

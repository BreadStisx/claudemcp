"""Markdown notes plugin. Read/write/list/search notes."""
from pathlib import Path
from datetime import datetime
from claudemcp.config import get_notes_dir


def list_notes() -> list[dict]:
    notes_dir = get_notes_dir()
    notes = []
    for f in sorted(notes_dir.glob("*.md")):
        stat = f.stat()
        notes.append({
            "name": f.stem,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })
    return notes


def read_note(name: str) -> str:
    path = get_notes_dir() / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"note '{name}' not found")
    return path.read_text(encoding="utf-8")


def write_note(name: str, content: str) -> str:
    path = get_notes_dir() / f"{name}.md"
    path.write_text(content, encoding="utf-8")
    return f"saved note '{name}' ({len(content)} bytes)"


def delete_note(name: str) -> str:
    path = get_notes_dir() / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"note '{name}' not found")
    path.unlink()
    return f"deleted note '{name}'"


def search_notes(query: str) -> list[dict]:
    results = []
    query_lower = query.lower()
    for f in get_notes_dir().glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if query_lower in content.lower():
            lines = content.split("\n")
            matching = [l.strip() for l in lines if query_lower in l.lower()]
            results.append({"name": f.stem, "matches": matching[:5]})
    return results

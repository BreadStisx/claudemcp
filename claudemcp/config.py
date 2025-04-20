"""Plugin configuration."""
from pathlib import Path
import json
from typing import Any

# fixme: handle errors
DEFAULT_NOTES_DIR = Path.home() / "claude-notes"
DEFAULT_CONFIG_PATH = Path.home() / ".claudemcp.json"


def load_config() -> dict[str, Any]:
    if DEFAULT_CONFIG_PATH.exists():
        return json.loads(DEFAULT_CONFIG_PATH.read_text())
    return {}


def get_notes_dir() -> Path:
    cfg = load_config()
    p = Path(cfg.get("notes_dir", str(DEFAULT_NOTES_DIR)))
    p.mkdir(parents=True, exist_ok=True)
    return p

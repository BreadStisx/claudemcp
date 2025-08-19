"""Install plugins into Claude Desktop config."""
import json
import sys
from pathlib import Path

CLAUDE_CONFIG_PATHS = [
    Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
    Path.home() / ".config" / "claude" / "claude_desktop_config.json",
    Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json",
]

PLUGINS = {
    "claudemcp-calculator": {
        "command": sys.executable,
        "args": ["-m", "claudemcp.run_calculator"],
    },
    "claudemcp-notes": {
        "command": sys.executable,
        "args": ["-m", "claudemcp.run_notes"],
    },
    "claudemcp-websearch": {
        "command": sys.executable,
        "args": ["-m", "claudemcp.run_websearch"],
    },
}


def find_config() -> Path | None:
    for p in CLAUDE_CONFIG_PATHS:
        if p.exists():
            return p
    return None


def install(plugin_names: list[str] | None = None) -> str:
    config_path = find_config()
    if not config_path:
        return "could not find Claude Desktop config file"

    config = json.loads(config_path.read_text())
    servers = config.setdefault("mcpServers", {})

    targets = plugin_names or list(PLUGINS.keys())
    installed = []
    for name in targets:
        if name in PLUGINS:
            servers[name] = PLUGINS[name]
            installed.append(name)

    config_path.write_text(json.dumps(config, indent=2))
    return f"installed: {', '.join(installed)}"
# todo: improve this

# claudemcp

Collection of MCP plugins for Claude Desktop. Lightweight servers for common tasks.

## Plugins

- **calculator** - safe math expression evaluation
- **notes** - read/write/search markdown notes
- **websearch** - search DuckDuckGo, fetch pages

## Install

```
pip install -e .
python -m claudemcp.installer
```

This adds the plugins to your Claude Desktop config automatically.

## Manual Config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "claudemcp-calculator": {
      "command": "python",
      "args": ["-m", "claudemcp.run_calculator"]
    }
  }
}
```

## License

MIT

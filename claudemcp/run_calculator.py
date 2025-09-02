"""Entry point for calculator MCP server."""
import json
import sys


def main():
    from claudemcp.calculator_plugin import safe_eval

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method", "")
            params = req.get("params", {})
            result = None

            if method == "tools/list":
                result = {"tools": [{
                    "name": "calculate",
                    "description": "Evaluate a math expression safely",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"],
                    },
                }]}
            elif method == "tools/call":
                expr = params.get("arguments", {}).get("expression", "")
                try:
                    val = safe_eval(expr)
                    result = {"content": [{"type": "text", "text": str(val)}]}
                except Exception as e:
                    result = {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True}

            resp = {"jsonrpc": "2.0", "id": req.get("id"), "result": result}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()

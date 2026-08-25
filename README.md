# API Client → Business Logic → MCP Tools

Small Python example showing how to reuse an API client and business logic from both
normal application code and MCP tools.

## Structure

```text
src/example/
├── api/
│   └── api_client.py
├── business/
│   └── service.py
├── mcp/
│   └── server.py
└── main.py
```

The example exposes 5 operations:

1. `get_user`
2. `list_users`
3. `create_user`
4. `update_user`
5. `delete_user`

The MCP layer is deliberately thin: it validates MCP inputs and delegates to the
business service. The business service delegates HTTP work to the API client.

## Install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the MCP server

```bash
python -m src.example.mcp.server
```

Or configure the MCP client to launch:

```text
python -m src.example.mcp.server
```

## Use MCP server
Via terminal

```
{"jsonrpc":"2.0","method":"tools/list","id":1}
```

Or Claude

```mcp_config.json:
{
  "mcpServers": {
    "example-users": {
      "command": "python",
      "args": ["-m", "src.example.mcp.server"]
    }
  }
}
```

Or vía WebSocket (Railway deployment)

**Live on Railway:**
```
wss://claude-ia-mcp-tools-staging.up.railway.app
```

**Connect with Python:**
```python
import asyncio
import json
import websockets

async def call_mcp():
    uri = "wss://claude-ia-mcp-tools-staging.up.railway.app"
    async with websockets.connect(uri) as ws:
        # Call get_user
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_user",
                "arguments": {"user_id": 1}
            },
            "id": 1
        }
        await ws.send(json.dumps(request))
        response = await ws.recv()
        print(json.loads(response))

asyncio.run(call_mcp())
```

**Configure in Claude Desktop:**
```json
{
  "mcpServers": {
    "claude-ia-mcp-tools": {
      "command": "uvx",
      "args": ["mcp-websocket-client", "wss://claude-ia-mcp-tools-staging.up.railway.app"]
    }
  }
}
```

**Available Tools:**
- `get_user` - Get one user by ID
- `list_users` - List all users
- `create_user` - Create a new user
- `update_user` - Update user name/email
- `delete_user` - Delete a user

## Important

This is a self-contained architectural example. The API client uses
`https://jsonplaceholder.typicode.com` as a public demo API.

For a real API, replace `ApiClient` implementation and keep the business/MCP
interfaces essentially unchanged.
# Test workflow execution

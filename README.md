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

## Important

This is a self-contained architectural example. The API client uses
`https://jsonplaceholder.typicode.com` as a public demo API.

For a real API, replace `ApiClient` implementation and keep the business/MCP
interfaces essentially unchanged.
# Test workflow execution

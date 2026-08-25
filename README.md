# claude-ia-mcp-tools

```

Arquitectura basada en orchestrator + agentes + procesos batch.

                     Claude / MCP Client
                           │
                           ▼
                    ┌─────────────┐
                    │ MCP Tools   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ UserService │
                    │  Business   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ ApiClient   │
                    └──────┬──────┘
                           │ HTTP
                           ▼
                    External API

UserService no depende de MCP, por lo que se puede utilizar exactamente la misma lógica desde un batch                  

service = UserService(ApiClient())
for item in batch:
    service.create_user(...)

mientras Claude puede utilizar:

create_user(...)

a través de MCP.
```


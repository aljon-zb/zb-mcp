# ZenMCP + MCP-Peltier merged project

This project uses the working `mcp-peltier` OAuth/security/runtime as the base and adds the dynamic deployment/tool-loading concepts from `zenmcp-main`.

## Retained from mcp-peltier

- Odoo JSON-2 client
- Odoo username/password authorization page and OAuth provider
- Dynamic OAuth client registration for Claude
- Per-principal tool permissions via `config/permissions.yaml`
- Audit logging, branding, prompts, security tests
- Existing Odoo tools: connection, users, projects, CRM, sales, accounting, inventory, contacts
- Docker/deployment files

## Added/adapted from zenmcp-main

- Dynamic identity through environment variables:
  - `CLIENT_ID`
  - `CLIENT_NAME`
  - `PROVIDER_NAME`
  - `SERVICE_NAME`
  - `WEBSITE_URL`
  - `ICON_URL`
  - `ACCESS_MODE`
- Dynamic addon loading through `ADDONS_PATH`
- Automatic discovery of all `app.tools`, `app.addons`, and `app.custom_addons` registration modules
- Generic dependency injection for addon registration functions
- Dynamic service/client/provider values in root/health/prompt/login responses

## Dynamic addon contract

Create a Python file inside `app/custom_addons/` or a directory listed in `ADDONS_PATH`.

Preferred form:

```python
def register_tools(mcp, odoo, settings, failed):
    @mcp.tool()
    async def my_tool():
        return {"client": settings.client_name}
```

Also supported: any function named `register_*_tools`.

Supported injected argument names:

- `mcp`, `server`, `mcp_server`
- `odoo`, `client`, `odoo_client`
- `settings`, `config`
- `failed`

## Why this project does not directly use zenmcp-main's FastMCP 4 registry

The two uploaded projects target different MCP/FastMCP generations. The Peltier authorization implementation is built around the MCP 1.x server/provider APIs, while zenmcp-main uses FastMCP 4 / MCP 2.x APIs. Combining those dependency trees directly would make the already-working OAuth implementation unstable.

Instead, the dynamic behavior was ported into the Peltier-compatible runtime so both goals work together: dynamic modules/configuration plus the current Odoo OAuth and permissions.

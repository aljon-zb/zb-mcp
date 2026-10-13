# ZenMCP Odoo Connector — merged runtime

A dynamic Odoo MCP connector that combines configurable multi-client deployment and addon discovery with the Peltier Odoo tools, Odoo-backed OAuth authorization, and per-user tool permissions.

## Setup

```bash
cp .env.example .env
# edit .env
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m app.server
```

For Docker:

```bash
docker build -t zenmcp-odoo .
docker run --env-file .env -p 8000:8000 zenmcp-odoo
```

## Core architecture

- `app/server.py` — MCP server, OAuth routes, permissions, health/root endpoints
- `app/config.py` — dynamic instance/Odoo/security configuration
- `app/tool_loader.py` — automatic tool/addon discovery
- `app/tools/` — existing Peltier Odoo tools
- `app/addons/` — bundled optional dynamic addons
- `app/custom_addons/` — client-specific addons
- `app/odoo_oauth.py` — Odoo-backed authorization provider
- `app/permissions.py` — per-user tool visibility/execution permissions
- `config/permissions.yaml` — permission mapping

See `MERGE_NOTES.md` for the exact merge design and addon contract.
# zb-mcp

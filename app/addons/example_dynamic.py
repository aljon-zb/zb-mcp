"""Example dynamic addon. Disabled unless EXAMPLE_DYNAMIC_TOOL=true."""
import os


def register_tools(mcp, settings):
    if os.getenv("EXAMPLE_DYNAMIC_TOOL", "false").strip().lower() not in {"1", "true", "yes", "on"}:
        return

    @mcp.tool()
    async def get_mcp_identity():
        """Return the configured identity of this MCP instance."""
        return {
            "service": settings.service_name,
            "client_id": settings.client_id,
            "client": settings.client_name,
            "provider": settings.provider_name,
        }

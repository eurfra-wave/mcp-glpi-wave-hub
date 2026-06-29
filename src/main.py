"""Entry point del MCP Server GLPI Hub.

Orquestador principal: inicializa configuración, cliente GLPI,
registra todas las tools y levanta el servidor (SSE o stdio).
"""

import sys
import json
from mcp.server.fastmcp import FastMCP

from src.config import settings
from src.client import GLPIClient
from src.tools import register_all_tools


# Instancia global del cliente GLPI
glpi_client = GLPIClient()

# Servidor MCP
mcp = FastMCP("Hermes-GLPI-Wave-Hub")

# Registrar todas las tools
register_all_tools(mcp, glpi_client)


# Health check endpoint
@mcp.tool(name="glpi_health_check")
async def health_check() -> str:
    """Verifica conectividad con GLPI y estado de la sesión."""
    try:
        # Intentar una petición simple
        await glpi_client.ensure_session()
        # Si llegamos aquí, la sesión es válida
        return json.dumps({
            "status": "healthy",
            "glpi_connected": True,
            "session_active": glpi_client._session_token is not None,
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "unhealthy",
            "glpi_connected": False,
            "error": str(e),
        }, indent=2)


if __name__ == "__main__":
    if "--sse" in sys.argv:
        # Modo producción: SSE para Hermes Agent
        mcp.run(transport="sse", port=settings.mcp_port, host=settings.mcp_host)
    else:
        # Modo desarrollo: stdio para debugging
        mcp.run(transport="stdio")
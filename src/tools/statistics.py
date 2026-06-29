"""Tools MCP para Estadísticas / Dashboard."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_error


def register_statistics_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_get_ticket_stats",
        description="Obtiene estadísticas de tickets (contadores por estado)"
    )
    async def glpi_get_ticket_stats() -> str:
        try:
            stats = await client.get_ticket_stats()
            return format_json(stats)
        except Exception as e:
            return format_error(f"Error obteniendo estadísticas de tickets: {e}")

    @mcp.tool(
        name="glpi_get_asset_stats",
        description="Obtiene estadísticas de inventario de activos"
    )
    async def glpi_get_asset_stats() -> str:
        try:
            stats = await client.get_asset_stats()
            return format_json(stats)
        except Exception as e:
            return format_error(f"Error obteniendo estadísticas de activos: {e}")
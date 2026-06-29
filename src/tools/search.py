"""Tools MCP para Búsqueda Avanzada."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_search_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_search",
        description="Búsqueda avanzada multi-criterio en GLPI. Permite buscar cualquier tipo de item con criterios complejos."
    )
    async def glpi_search(
        itemtype: str,
        criteria: list[dict],
    ) -> str:
        """
        Búsqueda avanzada en GLPI.

        Args:
            itemtype: Tipo de item a buscar (ej: "Ticket", "Computer", "User", "Problem", "Change", "Software", etc.)
            criteria: Lista de criterios de búsqueda, cada uno con:
                - field: ID del campo (ej: 1=nombre, 2=estado, etc.)
                - searchtype: "contains" | "equals" | "notequals" | "lessthan" | "morethan" | "under" | "notunder"
                - value: Valor a buscar
                - link (opcional): "AND" | "OR" para combinar criterios (desde el segundo)

        Ejemplo:
            criteria=[
                {"field": 1, "searchtype": "contains", "value": "impresora"},
                {"field": 2, "searchtype": "equals", "value": "1", "link": "AND"}
            ]
        """
        try:
            results = await client.search(itemtype, criteria)
            return format_list_response(results)
        except Exception as e:
            return format_error(f"Error en búsqueda avanzada: {e}")
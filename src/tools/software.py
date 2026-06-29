"""Tools MCP para Software."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_software_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_softwares",
        description="Lista software del inventario"
    )
    async def glpi_list_softwares(limit: int = 50) -> str:
        try:
            softwares = await client.get_softwares(range_=f"0-{limit - 1}")
            return format_list_response(
                softwares,
                key_fields=["id", "name", "softwarecategories_id", "manufacturers_id", "is_deleted"]
            )
        except Exception as e:
            return format_error(f"Error listando software: {e}")

    @mcp.tool(
        name="glpi_get_software",
        description="Obtiene detalle de un software"
    )
    async def glpi_get_software(id: int) -> str:
        try:
            software = await client.get_software(id)
            return format_json(software)
        except Exception as e:
            return format_error(f"Error obteniendo software {id}: {e}")

    @mcp.tool(
        name="glpi_create_software",
        description="Crea un nuevo software en el inventario"
    )
    async def glpi_create_software(
        name: str,
        comment: str | None = None,
        manufacturers_id: int | None = None,
        softwarecategories_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if comment:
                data["comment"] = comment
            if manufacturers_id:
                data["manufacturers_id"] = manufacturers_id
            if softwarecategories_id:
                data["softwarecategories_id"] = softwarecategories_id

            result = await client.create_software(data)
            return format_json({
                "success": True,
                "message": f"Software creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando software: {e}")
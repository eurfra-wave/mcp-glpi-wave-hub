"""Tools MCP para ITIL Changes."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_change_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_changes",
        description="Lista cambios ITIL de GLPI"
    )
    async def glpi_list_changes(limit: int = 50, order: str = "DESC") -> str:
        try:
            changes = await client.get_changes(range_=f"0-{limit - 1}", order=order)
            return format_list_response(
                changes,
                key_fields=["id", "name", "status", "urgency", "priority", "date"]
            )
        except Exception as e:
            return format_error(f"Error listando cambios: {e}")

    @mcp.tool(
        name="glpi_get_change",
        description="Obtiene detalle completo de un cambio"
    )
    async def glpi_get_change(id: int) -> str:
        try:
            change = await client.get_change(id)
            return format_json(change)
        except Exception as e:
            return format_error(f"Error obteniendo cambio {id}: {e}")

    @mcp.tool(
        name="glpi_create_change",
        description="Crea una nueva solicitud de cambio ITIL"
    )
    async def glpi_create_change(
        name: str,
        content: str,
        urgency: int = 3,
        impact: int = 3,
        priority: int = 3,
        itilcategories_id: int | None = None,
    ) -> str:
        try:
            data = {
                "name": name,
                "content": content,
                "urgency": urgency,
                "impact": impact,
                "priority": priority,
            }
            if itilcategories_id:
                data["itilcategories_id"] = itilcategories_id

            result = await client.create_change(data)
            return format_json({
                "success": True,
                "message": f"Cambio creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando cambio: {e}")

    @mcp.tool(
        name="glpi_update_change",
        description="Actualiza un cambio existente"
    )
    async def glpi_update_change(
        id: int,
        name: str | None = None,
        content: str | None = None,
        status: int | None = None,
    ) -> str:
        try:
            updates = {}
            if name is not None:
                updates["name"] = name
            if content is not None:
                updates["content"] = content
            if status is not None:
                updates["status"] = status

            await client.update_change(id, updates)
            return format_json({
                "success": True,
                "message": f"Cambio {id} actualizado",
            })
        except Exception as e:
            return format_error(f"Error actualizando cambio: {e}")
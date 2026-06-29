"""Tools MCP para ITIL Problems."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_problem_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_problems",
        description="Lista problemas ITIL de GLPI"
    )
    async def glpi_list_problems(limit: int = 50, order: str = "DESC") -> str:
        try:
            problems = await client.get_problems(range_=f"0-{limit - 1}", order=order)
            return format_list_response(
                problems,
                key_fields=["id", "name", "status", "urgency", "priority", "date"]
            )
        except Exception as e:
            return format_error(f"Error listando problemas: {e}")

    @mcp.tool(
        name="glpi_get_problem",
        description="Obtiene detalle completo de un problema"
    )
    async def glpi_get_problem(id: int) -> str:
        try:
            problem = await client.get_problem(id)
            return format_json(problem)
        except Exception as e:
            return format_error(f"Error obteniendo problema {id}: {e}")

    @mcp.tool(
        name="glpi_create_problem",
        description="Crea un nuevo problema ITIL"
    )
    async def glpi_create_problem(
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

            result = await client.create_problem(data)
            return format_json({
                "success": True,
                "message": f"Problema creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando problema: {e}")

    @mcp.tool(
        name="glpi_update_problem",
        description="Actualiza un problema existente"
    )
    async def glpi_update_problem(
        id: int,
        name: str | None = None,
        content: str | None = None,
        status: int | None = None,
        urgency: int | None = None,
        impact: int | None = None,
        priority: int | None = None,
    ) -> str:
        try:
            updates = {}
            if name is not None:
                updates["name"] = name
            if content is not None:
                updates["content"] = content
            if status is not None:
                updates["status"] = status
            if urgency is not None:
                updates["urgency"] = urgency
            if impact is not None:
                updates["impact"] = impact
            if priority is not None:
                updates["priority"] = priority

            await client.update_problem(id, updates)
            return format_json({
                "success": True,
                "message": f"Problema {id} actualizado",
            })
        except Exception as e:
            return format_error(f"Error actualizando problema: {e}")
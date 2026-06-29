"""Tools MCP para Proyectos."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_project_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_projects",
        description="Lista proyectos de GLPI"
    )
    async def glpi_list_projects(limit: int = 50) -> str:
        try:
            projects = await client.get_projects(range_=f"0-{limit - 1}")
            return format_list_response(
                projects,
                key_fields=["id", "name", "code", "percent_done", "projectstates_id", "plan_start_date", "plan_end_date"]
            )
        except Exception as e:
            return format_error(f"Error listando proyectos: {e}")

    @mcp.tool(
        name="glpi_get_project",
        description="Obtiene detalle completo de un proyecto"
    )
    async def glpi_get_project(id: int) -> str:
        try:
            project = await client.get_project(id)
            return format_json(project)
        except Exception as e:
            return format_error(f"Error obteniendo proyecto {id}: {e}")

    @mcp.tool(
        name="glpi_create_project",
        description="Crea un nuevo proyecto"
    )
    async def glpi_create_project(
        name: str,
        code: str | None = None,
        content: str | None = None,
        priority: int = 3,
        plan_start_date: str | None = None,
        plan_end_date: str | None = None,
        users_id: int | None = None,
        groups_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name, "priority": priority}
            if code:
                data["code"] = code
            if content:
                data["content"] = content
            if plan_start_date:
                data["plan_start_date"] = plan_start_date
            if plan_end_date:
                data["plan_end_date"] = plan_end_date
            if users_id:
                data["users_id"] = users_id
            if groups_id:
                data["groups_id"] = groups_id

            result = await client.create_project(data)
            return format_json({
                "success": True,
                "message": f"Proyecto creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando proyecto: {e}")

    @mcp.tool(
        name="glpi_update_project",
        description="Actualiza un proyecto existente"
    )
    async def glpi_update_project(
        id: int,
        name: str | None = None,
        content: str | None = None,
        percent_done: float | None = None,
        real_start_date: str | None = None,
        real_end_date: str | None = None,
    ) -> str:
        try:
            updates = {}
            if name is not None:
                updates["name"] = name
            if content is not None:
                updates["content"] = content
            if percent_done is not None:
                updates["percent_done"] = percent_done
            if real_start_date is not None:
                updates["real_start_date"] = real_start_date
            if real_end_date is not None:
                updates["real_end_date"] = real_end_date

            await client.update_project(id, updates)
            return format_json({
                "success": True,
                "message": f"Proyecto {id} actualizado",
            })
        except Exception as e:
            return format_error(f"Error actualizando proyecto: {e}")
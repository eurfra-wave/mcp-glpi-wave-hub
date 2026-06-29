"""Tools MCP para Tickets — CRUD + Followups + Tasks + Solutions."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_ticket_response, format_list_response, format_error
from src.utils.status_maps import get_ticket_status, get_ticket_urgency


def register_ticket_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_tickets",
        description="Lista tickets de GLPI con filtros opcionales (estado, límite, orden)"
    )
    async def glpi_list_tickets(
        limit: int = 50,
        status: int | None = None,
        order: str = "DESC",
    ) -> str:
        """Retorna lista de tickets formateada."""
        try:
            search_text = None
            if status:
                search_text = {"status": str(status)}

            tickets = await client.get_tickets(
                range_=f"0-{limit - 1}",
                order=order,
                search_text=search_text,
            )
            return format_list_response(
                tickets,
                key_fields=["id", "name", "status", "urgency", "date_creation", "date_modification"]
            )
        except Exception as e:
            return format_error(f"Error listando tickets: {e}")

    @mcp.tool(
        name="glpi_get_ticket",
        description="Obtiene detalle completo de un ticket incluyendo seguimientos, tareas y soluciones"
    )
    async def glpi_get_ticket(id: int) -> str:
        """Retorna ticket con todos sus detalles."""
        try:
            ticket = await client.get_ticket(id)
            followups = await client.get_ticket_followups(id)
            tasks = await client.get_ticket_tasks(id)

            # Añadir detalles al ticket
            ticket["followups"] = followups
            ticket["tasks"] = tasks
            ticket["solutions"] = []  # GLPI no tiene endpoint directo para solutions en ticket

            return format_ticket_response(ticket)
        except Exception as e:
            return format_error(f"Error obteniendo ticket {id}: {e}")

    @mcp.tool(
        name="glpi_create_ticket",
        description="Crea un nuevo ticket en GLPI"
    )
    async def glpi_create_ticket(
        name: str,
        content: str,
        urgency: int = 3,
        priority: int = 3,
        impact: int = 3,
        type: int = 1,
        itilcategories_id: int | None = None,
        entities_id: int | None = None,
        users_id_assign: int | None = None,
        groups_id_assign: int | None = None,
    ) -> str:
        """Crea ticket y retorna el ID creado."""
        try:
            data = {
                "name": name,
                "content": content,
                "urgency": urgency,
                "priority": priority,
                "impact": impact,
                "type": type,
            }
            if itilcategories_id:
                data["itilcategories_id"] = itilcategories_id
            if entities_id:
                data["entities_id"] = entities_id
            if users_id_assign:
                data["_users_id_assign"] = users_id_assign
            if groups_id_assign:
                data["_groups_id_assign"] = groups_id_assign

            result = await client.create_ticket(data)
            return format_json({
                "success": True,
                "message": f"Ticket creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando ticket: {e}")

    @mcp.tool(
        name="glpi_update_ticket",
        description="Actualiza un ticket existente"
    )
    async def glpi_update_ticket(
        id: int,
        name: str | None = None,
        content: str | None = None,
        status: int | None = None,
        urgency: int | None = None,
        priority: int | None = None,
        impact: int | None = None,
    ) -> str:
        """Actualiza campos del ticket."""
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
            if priority is not None:
                updates["priority"] = priority
            if impact is not None:
                updates["impact"] = impact

            await client.update_ticket(id, updates)
            return format_json({
                "success": True,
                "message": f"Ticket {id} actualizado correctamente",
            })
        except Exception as e:
            return format_error(f"Error actualizando ticket {id}: {e}")

    @mcp.tool(
        name="glpi_delete_ticket",
        description="Elimina un ticket (mueve a papelera o purga definitivamente)"
    )
    async def glpi_delete_ticket(id: int, force: bool = False) -> str:
        """Elimina ticket. force=True = purga definitiva."""
        try:
            await client.delete_ticket(id, force=force)
            action = "purgado definitivamente" if force else "movido a papelera"
            return format_json({
                "success": True,
                "message": f"Ticket {id} {action}",
            })
        except Exception as e:
            return format_error(f"Error eliminando ticket {id}: {e}")

    @mcp.tool(
        name="glpi_add_followup",
        description="Añade un seguimiento/comentario a un ticket"
    )
    async def glpi_add_followup(ticket_id: int, content: str, is_private: bool = False) -> str:
        """Añade followup al ticket."""
        try:
            result = await client.add_ticket_followup(ticket_id, content, is_private)
            return format_json({
                "success": True,
                "message": f"Seguimiento añadido al ticket {ticket_id}",
                "followup_id": result.get("id"),
            })
        except Exception as e:
            return format_error(f"Error añadiendo seguimiento: {e}")

    @mcp.tool(
        name="glpi_add_task",
        description="Añade una tarea a un ticket con tiempo y estado"
    )
    async def glpi_add_task(
        ticket_id: int,
        content: str,
        is_private: bool = False,
        actiontime: int = 0,
        state: int = 1,
        users_id_tech: int | None = None,
    ) -> str:
        """Añade tarea al ticket. state: 0=Info, 1=Por hacer, 2=Hecho."""
        try:
            result = await client.add_ticket_task(
                ticket_id, content, is_private, actiontime, state, users_id_tech
            )
            return format_json({
                "success": True,
                "message": f"Tarea añadida al ticket {ticket_id}",
                "task_id": result.get("id"),
            })
        except Exception as e:
            return format_error(f"Error añadiendo tarea: {e}")

    @mcp.tool(
        name="glpi_add_solution",
        description="Añade una solución para cerrar un ticket"
    )
    async def glpi_add_solution(ticket_id: int, content: str, solutiontypes_id: int = 0) -> str:
        """Añade solución al ticket."""
        try:
            result = await client.add_ticket_solution(ticket_id, content, solutiontypes_id)
            return format_json({
                "success": True,
                "message": f"Solución añadida al ticket {ticket_id}",
                "solution_id": result.get("id"),
            })
        except Exception as e:
            return format_error(f"Error añadiendo solución: {e}")

    @mcp.tool(
        name="glpi_assign_ticket",
        description="Asigna un ticket a un usuario o grupo"
    )
    async def glpi_assign_ticket(ticket_id: int, user_id: int, assign_type: int = 2) -> str:
        """Asigna ticket. assign_type: 1=Solicitante, 2=Asignado, 3=Observador."""
        try:
            result = await client.assign_ticket(ticket_id, user_id, assign_type)
            return format_json({
                "success": True,
                "message": f"Ticket {ticket_id} asignado a usuario {user_id}",
                "assignment_id": result.get("id"),
            })
        except Exception as e:
            return format_error(f"Error asignando ticket: {e}")

    @mcp.tool(
        name="glpi_get_ticket_tasks",
        description="Obtiene todas las tareas de un ticket"
    )
    async def glpi_get_ticket_tasks(ticket_id: int) -> str:
        """Lista tareas del ticket."""
        try:
            tasks = await client.get_ticket_tasks(ticket_id)
            return format_list_response(tasks)
        except Exception as e:
            return format_error(f"Error obteniendo tareas: {e}")

    @mcp.tool(
        name="glpi_get_ticket_followups",
        description="Obtiene todos los seguimientos/comentarios de un ticket"
    )
    async def glpi_get_ticket_followups(ticket_id: int) -> str:
        """Lista followups del ticket."""
        try:
            followups = await client.get_ticket_followups(ticket_id)
            return format_list_response(followups)
        except Exception as e:
            return format_error(f"Error obteniendo seguimientos: {e}")
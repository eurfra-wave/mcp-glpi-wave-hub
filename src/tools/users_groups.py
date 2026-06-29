"""Tools MCP para Usuarios y Grupos."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_user_tools(mcp: FastMCP, client: GLPIClient) -> None:

    # ==================== USUARIOS ====================

    @mcp.tool(
        name="glpi_list_users",
        description="Lista usuarios de GLPI"
    )
    async def glpi_list_users(limit: int = 50, active_only: bool = True) -> str:
        try:
            users = await client.get_users(range_=f"0-{limit - 1}", is_active=active_only)
            return format_list_response(
                users,
                key_fields=["id", "name", "realname", "firstname", "email", "is_active", "profiles_id"]
            )
        except Exception as e:
            return format_error(f"Error listando usuarios: {e}")

    @mcp.tool(
        name="glpi_get_user",
        description="Obtiene detalle completo de un usuario"
    )
    async def glpi_get_user(id: int) -> str:
        try:
            user = await client.get_user(id)
            return format_json(user)
        except Exception as e:
            return format_error(f"Error obteniendo usuario {id}: {e}")

    @mcp.tool(
        name="glpi_search_user",
        description="Busca un usuario por nombre"
    )
    async def glpi_search_user(name: str) -> str:
        try:
            users = await client.search_user(name)
            return format_list_response(users)
        except Exception as e:
            return format_error(f"Error buscando usuario: {e}")

    @mcp.tool(
        name="glpi_create_user",
        description="Crea un nuevo usuario en GLPI"
    )
    async def glpi_create_user(
        name: str,
        password: str | None = None,
        realname: str | None = None,
        firstname: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        mobile: str | None = None,
        profiles_id: int | None = None,
        entities_id: int | None = None,
        is_active: int = 1,
    ) -> str:
        try:
            data = {"name": name, "is_active": is_active}
            if password:
                data["password"] = password
            if realname:
                data["realname"] = realname
            if firstname:
                data["firstname"] = firstname
            if email:
                data["email"] = email
            if phone:
                data["phone"] = phone
            if mobile:
                data["mobile"] = mobile
            if profiles_id:
                data["profiles_id"] = profiles_id
            if entities_id:
                data["entities_id"] = entities_id

            result = await client.create_user(data)
            return format_json({
                "success": True,
                "message": f"Usuario creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando usuario: {e}")

    # ==================== GRUPOS ====================

    @mcp.tool(
        name="glpi_list_groups",
        description="Lista grupos de GLPI"
    )
    async def glpi_list_groups(limit: int = 50) -> str:
        try:
            groups = await client.get_groups(range_=f"0-{limit - 1}")
            return format_list_response(
                groups,
                key_fields=["id", "name", "completename", "entities_id", "is_assign", "is_requester"]
            )
        except Exception as e:
            return format_error(f"Error listando grupos: {e}")

    @mcp.tool(
        name="glpi_get_group",
        description="Obtiene detalle de un grupo"
    )
    async def glpi_get_group(id: int) -> str:
        try:
            group = await client.get_group(id)
            return format_json(group)
        except Exception as e:
            return format_error(f"Error obteniendo grupo {id}: {e}")

    @mcp.tool(
        name="glpi_create_group",
        description="Crea un nuevo grupo"
    )
    async def glpi_create_group(
        name: str,
        comment: str | None = None,
        entities_id: int | None = None,
        is_recursive: int = 0,
        is_requester: int = 1,
        is_assign: int = 1,
        is_notify: int = 0,
    ) -> str:
        try:
            data = {
                "name": name,
                "is_recursive": is_recursive,
                "is_requester": is_requester,
                "is_assign": is_assign,
                "is_notify": is_notify,
            }
            if comment:
                data["comment"] = comment
            if entities_id:
                data["entities_id"] = entities_id

            result = await client.create_group(data)
            return format_json({
                "success": True,
                "message": f"Grupo creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando grupo: {e}")

    @mcp.tool(
        name="glpi_add_user_to_group",
        description="Añade un usuario a un grupo"
    )
    async def glpi_add_user_to_group(user_id: int, group_id: int, is_manager: int = 0) -> str:
        try:
            result = await client.add_user_to_group(user_id, group_id, is_manager)
            return format_json({
                "success": True,
                "message": f"Usuario {user_id} añadido al grupo {group_id}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error añadiendo usuario a grupo: {e}")
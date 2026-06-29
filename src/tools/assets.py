"""Tools MCP para Activos — Computadoras, Impresoras, Monitores, Teléfonos, Equipos de Red."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_asset_tools(mcp: FastMCP, client: GLPIClient) -> None:

    # ==================== COMPUTADORAS ====================

    @mcp.tool(
        name="glpi_list_computers",
        description="Lista computadoras/estaciones de trabajo del inventario"
    )
    async def glpi_list_computers(
        limit: int = 50,
        include_deleted: bool = False,
    ) -> str:
        try:
            computers = await client.get_computers(
                range_=f"0-{limit - 1}",
                is_deleted=include_deleted,
            )
            return format_list_response(
                computers,
                key_fields=["id", "name", "serial", "locations_id", "states_id", "date_modification"]
            )
        except Exception as e:
            return format_error(f"Error listando computadoras: {e}")

    @mcp.tool(
        name="glpi_get_computer",
        description="Obtiene detalle de una computadora con software y conexiones opcionales"
    )
    async def glpi_get_computer(
        id: int,
        with_softwares: bool = True,
        with_connections: bool = True,
        with_networkports: bool = False,
    ) -> str:
        try:
            computer = await client.get_computer(
                id,
                with_softwares=with_softwares,
                with_connections=with_connections,
                with_networkports=with_networkports,
            )
            return format_json(computer)
        except Exception as e:
            return format_error(f"Error obteniendo computadora {id}: {e}")

    @mcp.tool(
        name="glpi_create_computer",
        description="Crea una nueva computadora en el inventario"
    )
    async def glpi_create_computer(
        name: str,
        serial: str | None = None,
        otherserial: str | None = None,
        contact: str | None = None,
        comment: str | None = None,
        locations_id: int | None = None,
        states_id: int | None = None,
        computertypes_id: int | None = None,
        manufacturers_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if serial:
                data["serial"] = serial
            if otherserial:
                data["otherserial"] = otherserial
            if contact:
                data["contact"] = contact
            if comment:
                data["comment"] = comment
            if locations_id:
                data["locations_id"] = locations_id
            if states_id:
                data["states_id"] = states_id
            if computertypes_id:
                data["computertypes_id"] = computertypes_id
            if manufacturers_id:
                data["manufacturers_id"] = manufacturers_id

            result = await client.create_computer(data)
            return format_json({
                "success": True,
                "message": f"Computadora creada con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando computadora: {e}")

    @mcp.tool(
        name="glpi_update_computer",
        description="Actualiza una computadora existente"
    )
    async def glpi_update_computer(
        id: int,
        name: str | None = None,
        serial: str | None = None,
        comment: str | None = None,
        locations_id: int | None = None,
        states_id: int | None = None,
    ) -> str:
        try:
            updates = {}
            if name is not None:
                updates["name"] = name
            if serial is not None:
                updates["serial"] = serial
            if comment is not None:
                updates["comment"] = comment
            if locations_id is not None:
                updates["locations_id"] = locations_id
            if states_id is not None:
                updates["states_id"] = states_id

            await client.update_computer(id, updates)
            return format_json({
                "success": True,
                "message": f"Computadora {id} actualizada",
            })
        except Exception as e:
            return format_error(f"Error actualizando computadora: {e}")

    @mcp.tool(
        name="glpi_delete_computer",
        description="Elimina una computadora del inventario"
    )
    async def glpi_delete_computer(id: int, force: bool = False) -> str:
        try:
            await client.delete_computer(id, force=force)
            action = "purgada" if force else "movida a papelera"
            return format_json({
                "success": True,
                "message": f"Computadora {id} {action}",
            })
        except Exception as e:
            return format_error(f"Error eliminando computadora: {e}")

    # ==================== IMPRESORAS ====================

    @mcp.tool(
        name="glpi_list_printers",
        description="Lista impresoras del inventario"
    )
    async def glpi_list_printers(limit: int = 50) -> str:
        try:
            printers = await client.get_printers(range_=f"0-{limit - 1}")
            return format_list_response(
                printers,
                key_fields=["id", "name", "serial", "locations_id", "date_modification"]
            )
        except Exception as e:
            return format_error(f"Error listando impresoras: {e}")

    @mcp.tool(
        name="glpi_get_printer",
        description="Obtiene detalle de una impresora"
    )
    async def glpi_get_printer(id: int) -> str:
        try:
            printer = await client.get_printer(id)
            return format_json(printer)
        except Exception as e:
            return format_error(f"Error obteniendo impresora {id}: {e}")

    @mcp.tool(
        name="glpi_create_printer",
        description="Crea una nueva impresora en el inventario"
    )
    async def glpi_create_printer(
        name: str,
        serial: str | None = None,
        locations_id: int | None = None,
        printertypes_id: int | None = None,
        manufacturers_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if serial:
                data["serial"] = serial
            if locations_id:
                data["locations_id"] = locations_id
            if printertypes_id:
                data["printertypes_id"] = printertypes_id
            if manufacturers_id:
                data["manufacturers_id"] = manufacturers_id

            result = await client.create_printer(data)
            return format_json({
                "success": True,
                "message": f"Impresora creada con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando impresora: {e}")

    # ==================== MONITORES ====================

    @mcp.tool(
        name="glpi_list_monitors",
        description="Lista monitores del inventario"
    )
    async def glpi_list_monitors(limit: int = 50) -> str:
        try:
            monitors = await client.get_monitors(range_=f"0-{limit - 1}")
            return format_list_response(
                monitors,
                key_fields=["id", "name", "serial", "size", "locations_id"]
            )
        except Exception as e:
            return format_error(f"Error listando monitores: {e}")

    @mcp.tool(
        name="glpi_get_monitor",
        description="Obtiene detalle de un monitor"
    )
    async def glpi_get_monitor(id: int) -> str:
        try:
            monitor = await client.get_monitor(id)
            return format_json(monitor)
        except Exception as e:
            return format_error(f"Error obteniendo monitor {id}: {e}")

    # ==================== TELÉFONOS ====================

    @mcp.tool(
        name="glpi_list_phones",
        description="Lista teléfonos del inventario"
    )
    async def glpi_list_phones(limit: int = 50) -> str:
        try:
            phones = await client.get_phones(range_=f"0-{limit - 1}")
            return format_list_response(
                phones,
                key_fields=["id", "name", "serial", "locations_id", "number_line"]
            )
        except Exception as e:
            return format_error(f"Error listando teléfonos: {e}")

    @mcp.tool(
        name="glpi_get_phone",
        description="Obtiene detalle de un teléfono"
    )
    async def glpi_get_phone(id: int) -> str:
        try:
            phone = await client.get_phone(id)
            return format_json(phone)
        except Exception as e:
            return format_error(f"Error obteniendo teléfono {id}: {e}")

    # ==================== EQUIPOS DE RED ====================

    @mcp.tool(
        name="glpi_list_network_equipments",
        description="Lista equipos de red (switches, routers, etc.)"
    )
    async def glpi_list_network_equipments(limit: int = 50) -> str:
        try:
            equipments = await client.get_network_equipments(range_=f"0-{limit - 1}")
            return format_list_response(
                equipments,
                key_fields=["id", "name", "serial", "locations_id", "networkequipmenttypes_id"]
            )
        except Exception as e:
            return format_error(f"Error listando equipos de red: {e}")

    @mcp.tool(
        name="glpi_get_network_equipment",
        description="Obtiene detalle de un equipo de red con puertos opcionales"
    )
    async def glpi_get_network_equipment(
        id: int,
        with_networkports: bool = True,
    ) -> str:
        try:
            equipment = await client.get_network_equipment(id, with_networkports=with_networkports)
            return format_json(equipment)
        except Exception as e:
            return format_error(f"Error obteniendo equipo de red {id}: {e}")

    @mcp.tool(
        name="glpi_create_network_equipment",
        description="Crea un nuevo equipo de red en el inventario"
    )
    async def glpi_create_network_equipment(
        name: str,
        serial: str | None = None,
        otherserial: str | None = None,
        locations_id: int | None = None,
        networkequipmenttypes_id: int | None = None,
        manufacturers_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if serial:
                data["serial"] = serial
            if otherserial:
                data["otherserial"] = otherserial
            if locations_id:
                data["locations_id"] = locations_id
            if networkequipmenttypes_id:
                data["networkequipmenttypes_id"] = networkequipmenttypes_id
            if manufacturers_id:
                data["manufacturers_id"] = manufacturers_id

            result = await client.create_network_equipment(data)
            return format_json({
                "success": True,
                "message": f"Equipo de red creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando equipo de red: {e}")
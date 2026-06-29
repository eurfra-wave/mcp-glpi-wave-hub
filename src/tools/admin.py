"""Tools MCP administrativas — Localizaciones, Entidades, Categorías, Contratos, Proveedores."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_admin_tools(mcp: FastMCP, client: GLPIClient) -> None:

    # ==================== LOCALIZACIONES ====================

    @mcp.tool(
        name="glpi_list_locations",
        description="Lista localizaciones (ubicaciones) de GLPI"
    )
    async def glpi_list_locations(limit: int = 50) -> str:
        try:
            locations = await client.get_locations(range_=f"0-{limit - 1}")
            return format_list_response(
                locations,
                key_fields=["id", "name", "completename", "town", "building", "room", "locations_id"]
            )
        except Exception as e:
            return format_error(f"Error listando localizaciones: {e}")

    @mcp.tool(
        name="glpi_get_location",
        description="Obtiene detalle de una localización"
    )
    async def glpi_get_location(id: int) -> str:
        try:
            location = await client.get_location(id)
            return format_json(location)
        except Exception as e:
            return format_error(f"Error obteniendo localización {id}: {e}")

    @mcp.tool(
        name="glpi_create_location",
        description="Crea una nueva localización"
    )
    async def glpi_create_location(
        name: str,
        address: str | None = None,
        postcode: str | None = None,
        town: str | None = None,
        country: str | None = None,
        building: str | None = None,
        room: str | None = None,
        locations_id: int | None = None,
        entities_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if address:
                data["address"] = address
            if postcode:
                data["postcode"] = postcode
            if town:
                data["town"] = town
            if country:
                data["country"] = country
            if building:
                data["building"] = building
            if room:
                data["room"] = room
            if locations_id:
                data["locations_id"] = locations_id
            if entities_id:
                data["entities_id"] = entities_id

            result = await client.create_location(data)
            return format_json({
                "success": True,
                "message": f"Localización creada con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando localización: {e}")

    # ==================== ENTIDADES ====================

    @mcp.tool(
        name="glpi_list_entities",
        description="Lista entidades de GLPI"
    )
    async def glpi_list_entities(limit: int = 50) -> str:
        try:
            entities = await client.get_entities(range_=f"0-{limit - 1}")
            return format_list_response(
                entities,
                key_fields=["id", "name", "completename", "level", "entities_id"]
            )
        except Exception as e:
            return format_error(f"Error listando entidades: {e}")

    @mcp.tool(
        name="glpi_get_entity",
        description="Obtiene detalle de una entidad"
    )
    async def glpi_get_entity(id: int) -> str:
        try:
            entity = await client.get_entity(id)
            return format_json(entity)
        except Exception as e:
            return format_error(f"Error obteniendo entidad {id}: {e}")

    # ==================== CATEGORÍAS ITIL ====================

    @mcp.tool(
        name="glpi_list_categories",
        description="Lista categorías ITIL (para tickets, problemas, cambios)"
    )
    async def glpi_list_categories(limit: int = 50) -> str:
        try:
            categories = await client.get_categories(range_=f"0-{limit - 1}")
            return format_list_response(
                categories,
                key_fields=["id", "name", "completename", "level", "is_helpdesk_visible"]
            )
        except Exception as e:
            return format_error(f"Error listando categorías: {e}")

    # ==================== CONTRATOS ====================

    @mcp.tool(
        name="glpi_list_contracts",
        description="Lista contratos de GLPI"
    )
    async def glpi_list_contracts(limit: int = 50) -> str:
        try:
            contracts = await client.get_contracts(range_=f"0-{limit - 1}")
            return format_list_response(
                contracts,
                key_fields=["id", "name", "num", "contracttypes_id", "begin_date", "duration", "entities_id"]
            )
        except Exception as e:
            return format_error(f"Error listando contratos: {e}")

    @mcp.tool(
        name="glpi_get_contract",
        description="Obtiene detalle de un contrato"
    )
    async def glpi_get_contract(id: int) -> str:
        try:
            contract = await client.get_contract(id)
            return format_json(contract)
        except Exception as e:
            return format_error(f"Error obteniendo contrato {id}: {e}")

    @mcp.tool(
        name="glpi_create_contract",
        description="Crea un nuevo contrato"
    )
    async def glpi_create_contract(
        name: str,
        num: str | None = None,
        contracttypes_id: int | None = None,
        begin_date: str | None = None,
        duration: int | None = None,
        notice: int | None = None,
        comment: str | None = None,
        entities_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if num:
                data["num"] = num
            if contracttypes_id:
                data["contracttypes_id"] = contracttypes_id
            if begin_date:
                data["begin_date"] = begin_date
            if duration:
                data["duration"] = duration
            if notice:
                data["notice"] = notice
            if comment:
                data["comment"] = comment
            if entities_id:
                data["entities_id"] = entities_id

            result = await client.create_contract(data)
            return format_json({
                "success": True,
                "message": f"Contrato creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando contrato: {e}")

    # ==================== PROVEEDORES ====================

    @mcp.tool(
        name="glpi_list_suppliers",
        description="Lista proveedores de GLPI"
    )
    async def glpi_list_suppliers(limit: int = 50) -> str:
        try:
            suppliers = await client.get_suppliers(range_=f"0-{limit - 1}")
            return format_list_response(
                suppliers,
                key_fields=["id", "name", "suppliertypes_id", "email", "phonenumber", "town", "website"]
            )
        except Exception as e:
            return format_error(f"Error listando proveedores: {e}")

    @mcp.tool(
        name="glpi_get_supplier",
        description="Obtiene detalle de un proveedor"
    )
    async def glpi_get_supplier(id: int) -> str:
        try:
            supplier = await client.get_supplier(id)
            return format_json(supplier)
        except Exception as e:
            return format_error(f"Error obteniendo proveedor {id}: {e}")

    @mcp.tool(
        name="glpi_create_supplier",
        description="Crea un nuevo proveedor"
    )
    async def glpi_create_supplier(
        name: str,
        address: str | None = None,
        postcode: str | None = None,
        town: str | None = None,
        state: str | None = None,
        country: str | None = None,
        website: str | None = None,
        phonenumber: str | None = None,
        email: str | None = None,
        entities_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name}
            if address:
                data["address"] = address
            if postcode:
                data["postcode"] = postcode
            if town:
                data["town"] = town
            if state:
                data["state"] = state
            if country:
                data["country"] = country
            if website:
                data["website"] = website
            if phonenumber:
                data["phonenumber"] = phonenumber
            if email:
                data["email"] = email
            if entities_id:
                data["entities_id"] = entities_id

            result = await client.create_supplier(data)
            return format_json({
                "success": True,
                "message": f"Proveedor creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando proveedor: {e}")
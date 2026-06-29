"""Tools MCP para Base de Conocimiento."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_kb_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_knowbase",
        description="Lista artículos de la base de conocimiento"
    )
    async def glpi_list_knowbase(limit: int = 50) -> str:
        try:
            items = await client.get_knowbase_items(range_=f"0-{limit - 1}")
            return format_list_response(
                items,
                key_fields=["id", "name", "is_faq", "knowbaseitemcategories_id", "date_modification"]
            )
        except Exception as e:
            return format_error(f"Error listando KB: {e}")

    @mcp.tool(
        name="glpi_get_knowbase_item",
        description="Obtiene un artículo específico de la base de conocimiento"
    )
    async def glpi_get_knowbase_item(id: int) -> str:
        try:
            item = await client.get_knowbase_item(id)
            return format_json(item)
        except Exception as e:
            return format_error(f"Error obteniendo artículo {id}: {e}")

    @mcp.tool(
        name="glpi_search_knowbase",
        description="Busca en la base de conocimiento por término"
    )
    async def glpi_search_knowbase(query: str) -> str:
        try:
            items = await client.search_knowbase(query)
            return format_list_response(
                items,
                key_fields=["id", "name", "is_faq", "knowbaseitemcategories_id"]
            )
        except Exception as e:
            return format_error(f"Error buscando en KB: {e}")

    @mcp.tool(
        name="glpi_create_knowbase_item",
        description="Crea un nuevo artículo en la base de conocimiento"
    )
    async def glpi_create_knowbase_item(
        name: str,
        answer: str,
        is_faq: int = 0,
        knowbaseitemcategories_id: int | None = None,
    ) -> str:
        try:
            data = {"name": name, "answer": answer, "is_faq": is_faq}
            if knowbaseitemcategories_id:
                data["knowbaseitemcategories_id"] = knowbaseitemcategories_id

            result = await client.create_knowbase_item(data)
            return format_json({
                "success": True,
                "message": f"Artículo KB creado con ID {result.get('id')}",
                "data": result,
            })
        except Exception as e:
            return format_error(f"Error creando artículo KB: {e}")
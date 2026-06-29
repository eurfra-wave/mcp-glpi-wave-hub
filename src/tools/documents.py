"""Tools MCP para Documentos."""

import json
from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient
from src.utils.formatters import format_json, format_list_response, format_error


def register_document_tools(mcp: FastMCP, client: GLPIClient) -> None:

    @mcp.tool(
        name="glpi_list_documents",
        description="Lista documentos de GLPI"
    )
    async def glpi_list_documents(limit: int = 50) -> str:
        try:
            documents = await client.get_documents(range_=f"0-{limit - 1}")
            return format_list_response(
                documents,
                key_fields=["id", "name", "filename", "mime", "date_modification", "documentcategories_id"]
            )
        except Exception as e:
            return format_error(f"Error listando documentos: {e}")

    @mcp.tool(
        name="glpi_get_document",
        description="Obtiene detalle de un documento"
    )
    async def glpi_get_document(id: int) -> str:
        try:
            document = await client.get_document(id)
            return format_json(document)
        except Exception as e:
            return format_error(f"Error obteniendo documento {id}: {e}")
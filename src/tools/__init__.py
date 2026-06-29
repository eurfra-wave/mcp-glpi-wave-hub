"""Orquestador de Tools — Registra todos los módulos en el servidor MCP."""

from mcp.server.fastmcp import FastMCP
from src.client import GLPIClient


def register_all_tools(mcp: FastMCP, client: GLPIClient) -> None:
    """Registra todas las tools del hub en el servidor MCP.

    Args:
        mcp: Instancia del servidor FastMCP
        client: Instancia del cliente GLPI configurada
    """
    from .tickets import register_ticket_tools
    from .assets import register_asset_tools
    from .software import register_software_tools
    from .problems import register_problem_tools
    from .changes import register_change_tools
    from .knowledgebase import register_kb_tools
    from .projects import register_project_tools
    from .users_groups import register_user_tools
    from .admin import register_admin_tools
    from .documents import register_document_tools
    from .search import register_search_tools
    from .statistics import register_statistics_tools

    # Registro ordenado por dominio
    register_ticket_tools(mcp, client)
    register_asset_tools(mcp, client)
    register_software_tools(mcp, client)
    register_problem_tools(mcp, client)
    register_change_tools(mcp, client)
    register_kb_tools(mcp, client)
    register_project_tools(mcp, client)
    register_user_tools(mcp, client)
    register_admin_tools(mcp, client)
    register_document_tools(mcp, client)
    register_search_tools(mcp, client)
    register_statistics_tools(mcp, client)
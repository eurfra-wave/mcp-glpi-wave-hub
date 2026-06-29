"""Configuración del GLPI Hub usando Pydantic Settings.

Toda la configuración se carga desde variables de entorno (.env).
Nada está hardcodeado.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configuración desde variables de entorno."""

    # ==================== GLPI ====================
    glpi_url: str = Field(..., alias="GLPI_URL", description="URL base de la API REST de GLPI")
    glpi_app_token: str = Field(..., alias="GLPI_APP_TOKEN", description="App Token de GLPI")
    glpi_user_token: str = Field(default="", alias="GLPI_USER_TOKEN", description="User Token de GLPI")
    glpi_username: str = Field(default="", alias="GLPI_USERNAME", description="Username para Basic Auth")
    glpi_password: str = Field(default="", alias="GLPI_PASSWORD", description="Password para Basic Auth")

    # ==================== MCP Server ====================
    mcp_host: str = Field(default="0.0.0.0", alias="MCP_HOST", description="Host para el servidor SSE")
    mcp_port: int = Field(default=8080, alias="MCP_PORT", description="Puerto para el servidor SSE")

    # ==================== Red Proxmox (LXCs) ====================
    # IPs internas de los LXCs en Proxmox — obligatorias en .env
    glpi_internal_host: str = Field(..., alias="GLPI_INTERNAL_HOST", description="IP interna de la VPS GLPI en Proxmox")
    hub_internal_host: str = Field(..., alias="HUB_INTERNAL_HOST", description="IP interna de este Hub en Proxmox")
    hermes_agent_internal_host: str = Field(..., alias="HERMES_AGENT_INTERNAL_HOST", description="IP interna del Hermes Agent en Proxmox")
    proxmox_network_subnet: str = Field(..., alias="PROXMOX_NETWORK_SUBNET", description="Subred de la red interna Proxmox")

    # ==================== Hermes Agent (opcional) ====================
    hermes_agent_url: str = Field(default="", alias="HERMES_AGENT_URL", description="URL completa del agente Hermes para callbacks")

    # ==================== Logging ====================
    log_level: str = Field(default="INFO", alias="LOG_LEVEL", description="Nivel de logging")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
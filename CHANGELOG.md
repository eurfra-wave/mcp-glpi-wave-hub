# Changelog - mcp-glpi-wave-hub

## [Unreleased] - 2026-06-28

### Iniciado
- Creado repositorio `mcp-glpi-wave-hub` en `C:\Users\Eurfran M\Documents\Proyectos\mcp-glpi-wave-hub`
- Establecida arquitectura: MCP Server con transporte SSE para comunicación entre LXCs en Proxmox
- Definidos tres componentes en Proxmox:
  - Hermes Agent (LXC 1): Agente WhatsApp con cerebro OpenRouter
  - GLPI Hub (LXC 2): Este servidor MCP (puerto 8080)
  - GLPI VPS (LXC 3): Instancia GLPI con API REST

### Planificado
- Estructura modular con responsabilidad única:
  - `config.py`: Configuración Pydantic desde .env
  - `client.py`: Cliente HTTP genérico para API GLPI con gestión de sesión
  - `models/`: 14 archivos Pydantic (uno por dominio)
  - `tools/`: 13 módulos de tools (uno por dominio funcional)
  - `utils/`: Mapeos de estado y formateadores
  - `main.py`: Orquestador principal (SSE + stdio)
- ~65 tools MCP organizadas por dominio
- Dockerfile multi-stage Alpine + uv para imagen ligera
- docker-compose con red Proxmox interna
- CHANGELOG.md en lenguaje natural para trazabilidad completa
# Changelog - mcp-glpi-wave-hub

## [1.0.0] - 2026-06-28

### Estructura completada
- Repositorio `mcp-glpi-wave-hub` con 44 archivos, git inicializado
- Arquitectura MCP Server con transporte SSE para comunicación entre LXCs en Proxmox
- Tres componentes en Proxmox:
  - Hermes Agent (LXC 1): Agente WhatsApp con cerebro OpenRouter
  - GLPI Hub (LXC 2): Este servidor MCP (puerto configurable)
  - GLPI VPS (LXC 3): Instancia GLPI con API REST

### Código fuente
- `config.py`: Configuración Pydantic desde .env — todas las IPs/URLs/tokens son variables de entorno
- `client.py`: GLPIClient con autenticación multi-modo, sesión lazy + auto-refresh en 401, CRUD genéricos
- `main.py`: Entry point con FastMCP, health check, registro de 71 tools
- `models/`: 11 archivos Pydantic (ticket, asset, software, problem, change, user, project, kb, contract, location, document)
- `tools/`: 12 módulos de tools MCP:
  - tickets.py (11), assets.py (15), software.py (3), problems.py (4), changes.py (4)
  - knowledgebase.py (4), projects.py (4), users_groups.py (8), admin.py (12)
  - documents.py (2), search.py (1), statistics.py (2)
- `utils/`: formatters.py (format_json, format_error, format_ticket_response) + status_maps.py

### Infraestructura
- Dockerfile multi-stage Alpine + Python 3.12, puerto configurable via MCP_PORT
- docker-compose.yml con red Proxmox, IPs desde .env
- Makefile con comandos: build, up, down, lint, test, deploy
- requirements.txt y pyproject.toml con dependencias

### Testing
- 8 tests unitarios pasando (config + GLPIClient)
- Tests cubren: carga de settings, auth, sesión lazy, refresh en 401, params HTTP

### Correcciones aplicadas
- Dockerfile: puerto 8080 hardcodeado → MCP_PORT configurable
- docker-compose.yml: HUB_INTERNAL_IP → HUB_INTERNAL_HOST, PROXMOX_SUBNET → PROXMOX_NETWORK_SUBNET
- config.py: IPs Proxmox con defaults hardcodeados → campos requeridos (sin defaults)
- client.py: import asyncio movido al tope del archivo
- Tests: env vars requeridas incluidas en fixtures
- Documentación: CONTEXT.md y README.md actualizados con tool counts reales (71)

# Hermes GLPI Wave Hub

MCP Server para GLPI — Hub de herramientas para el agente Hermes (WhatsApp + OpenRouter).

## Arquitectura

```
┌─────────────────┐     SSE (8080)      ┌──────────────────┐     REST      ┌────────┐
│  Hermes Agent   │ ◀──────────────────▶ │  GLPI Hub (LXC)  │ ────────────▶ │  GLPI  │
│  (LXC separada) │                      │  mcp-glpi-wave-  │               │  (VPS) │
│  OpenRouter     │                      │  hub             │               │        │
└─────────────────┘                      └──────────────────┘               └────────┘
```

## Inicio rápido

```bash
# 1. Configurar entorno
cp .env.example .env
# Editar .env con credenciales GLPI

# 2. Levantar con Docker
docker-compose up -d --build

# 3. Verificar salud
curl http://localhost:8080/health
```

## Herramientas disponibles (70)

- **Tickets** (11): list, get, create, update, delete, followup, task, solution, assign, get_tasks, get_followups
- **Assets** (15): computers (CRUD + delete), printers (list, get, create), monitors (list, get), phones (list, get), network equipment (list, get, create)
- **Software** (3): list, get, create
- **ITIL Problems** (4): list, get, create, update
- **ITIL Changes** (4): list, get, create, update
- **Knowledge Base** (4): list, get, search, create
- **Projects** (4): list, get, create, update
- **Users & Groups** (8): list users, get user, search user, create user, list groups, get group, create group, add user to group
- **Admin** (12): locations (list, get, create), entities (list, get), categories (list), contracts (list, get, create), suppliers (list, get, create)
- **Documents** (2): list, get
- **Search** (1): búsqueda avanzada multi-criterio
- **Statistics** (2): ticket stats, asset stats
- **Health** (1): verificar conexión con GLPI

## Desarrollo local

```bash
# Instalar dependencias
uv sync --dev

# Ejecutar en modo stdio (para debug)
python -m src.main

# Ejecutar en modo SSE (producción)
python -m src.main --sse
```

## Configuración

Toda la configuración se realiza via variables de entorno (`.env`). Ver `.env.example` para la plantilla completa.

```env
GLPI_URL=http://your-glpi-host/apirest.php
GLPI_APP_TOKEN=your-app-token
GLPI_USER_TOKEN=your-user-token
GLPI_INTERNAL_HOST=10.0.0.20
HUB_INTERNAL_HOST=10.0.0.10
HERMES_AGENT_INTERNAL_HOST=10.0.0.5
PROXMOX_NETWORK_SUBNET=10.0.0.0/24
MCP_PORT=8080
```

## Testing

```bash
# Ejecutar tests
uv run pytest -v

# Tests con cobertura
uv run pytest --cov=src --cov-report=term-missing
```

## Code Quality

```bash
# Linter
uv run ruff check src/

# Formatear
uv run ruff format src/

# Type check
uv run mypy src/
```

## Licencia

MIT

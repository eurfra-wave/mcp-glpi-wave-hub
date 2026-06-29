# Hermes GLPI Wave Hub — Contexto para el Agente

## Arquitectura de Red (Proxmox)

```
┌─────────────────────────────────────────────────────────────┐
│                        PROXMOX                                │
│                                                              │
│  ┌─────────────────┐    SSE (8080)     ┌──────────────────┐  │
│  │  Hermes Agent   │ ◀────────────────▶ │  GLPI Hub        │  │
│  │  (LXC 1)        │                    │  (LXC 2)         │  │
│  │  IP: 10.0.0.5   │                    │  IP: 10.0.0.10   │  │
│  │  OpenRouter     │                    │  mcp-glpi-wave-  │  │
│  │  WhatsApp bot   │                    │  hub             │  │
│  └─────────────────┘                    └────────┬─────────┘  │
│                                                   │            │
│                                                   │ GLPI REST  │
│                                                   ▼            │
│                                        ┌──────────────────┐  │
│                                        │  GLPI VPS        │  │
│                                        │  (LXC 3 / VPS)   │  │
│                                        │  IP: 10.0.0.20   │  │
│                                        │  /apirest.php    │  │
│                                        └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Variables de Entorno Clave

| Variable | Requerida | Descripción | Ejemplo |
|----------|-----------|-------------|---------|
| `GLPI_URL` | ✅ | URL base de la API REST de GLPI | `http://10.0.0.20/apirest.php` |
| `GLPI_APP_TOKEN` | ✅ | App Token de GLPI (Setup > General > API) | `abc123...` |
| `GLPI_USER_TOKEN` | | User Token del usuario API (o usar Basic Auth) | `xyz789...` |
| `GLPI_USERNAME` | | Username para Basic Auth (alternativa a User Token) | `admin` |
| `GLPI_PASSWORD` | | Password para Basic Auth (alternativa a User Token) | `***` |
| `MCP_HOST` | | Host para el servidor SSE | `0.0.0.0` |
| `MCP_PORT` | | Puerto para el servidor SSE | `8080` |
| `GLPI_INTERNAL_HOST` | ✅ | IP interna de la VPS GLPI en Proxmox | `10.0.0.20` |
| `HUB_INTERNAL_HOST` | ✅ | IP interna de este Hub en Proxmox | `10.0.0.10` |
| `HERMES_AGENT_INTERNAL_HOST` | ✅ | IP interna del Hermes Agent en Proxmox | `10.0.0.5` |
| `PROXMOX_NETWORK_SUBNET` | ✅ | Subred de la red interna Proxmox | `10.0.0.0/24` |
| `HERMES_AGENT_URL` | | URL completa del agente Hermes para callbacks | `http://10.0.0.5:9090` |
| `LOG_LEVEL` | | Nivel de logging | `INFO` |

## Estructura del Código

```
src/
├── main.py              # Orquestador principal (entry point)
├── config.py            # Configuración Pydantic desde .env
├── client.py            # GLPIClient — HTTP + sesión + CRUD genérico
├── models/              # 11 archivos Pydantic (1 por dominio)
│   ├── ticket.py       # TicketBase, TicketFollowup, TicketTask, TicketSolution
│   ├── asset.py        # ComputerBase, PrinterBase, MonitorBase, PhoneBase, NetworkEquipmentBase
│   ├── software.py     # SoftwareBase
│   ├── problem.py      # ProblemBase
│   ├── change.py       # ChangeBase
│   ├── user.py         # UserBase, GroupBase
│   ├── project.py      # ProjectBase
│   ├── kb.py           # KnowbaseItemBase
│   ├── contract.py     # ContractBase, SupplierBase
│   ├── location.py     # LocationBase, EntityBase, CategoryBase
│   ├── document.py     # DocumentBase
│   └── __init__.py     # Exports explícitos
├── tools/               # 12 módulos de tools MCP (70 tools totales)
│   ├── __init__.py      # Orquestador: register_all_tools()
│   ├── tickets.py       # 11 tools (list, get, create, update, delete, followup, task, solution, assign, tasks, followups)
│   ├── assets.py        # 15 tools (computers CRUD, printers, monitors, phones, network equipment)
│   ├── software.py      # 3 tools (list, get, create)
│   ├── problems.py      # 4 tools (list, get, create, update)
│   ├── changes.py       # 4 tools (list, get, create, update)
│   ├── knowledgebase.py # 4 tools (list, get, search, create)
│   ├── projects.py      # 4 tools (list, get, create, update)
│   ├── users_groups.py  # 8 tools (users, groups, search, add to group)
│   ├── admin.py         # 12 tools (locations, entities, categories, contracts, suppliers)
│   ├── documents.py     # 2 tools (list, get)
│   ├── search.py        # 1 tool (búsqueda avanzada multi-criterio)
│   └── statistics.py    # 2 tools (ticket stats, asset stats)
└── utils/
    ├── __init__.py
    ├── status_maps.py   # Diccionarios de estados GLPI
    └── formatters.py    # Helpers de formato (format_json, format_error, format_ticket_response)
```

## Flujo de una Tool

1. **Hermes Agent** (OpenRouter) recibe mensaje en WhatsApp
2. OpenRouter pide `list_tools` al Hub vía SSE (`http://10.0.0.10:8080/mcp`)
3. OpenRouter decide qué tool llamar según el lenguaje natural
4. Hub ejecuta: `GLPIClient` → REST a `http://10.0.0.20/apirest.php`
5. Hub retorna JSON formateado → OpenRouter → Respuesta en WhatsApp

## Convenciones de Tools

- Nomenclatura: `glpi_{acción}_{entidad}` (ej: `glpi_list_tickets`)
- Todas las tools son `async` y retornan `str` (JSON con indent=2)
- Parámetros con tipos Python + descripción para schema MCP

## Despliegue

```bash
# En el LXC del Hub (10.0.0.10)
cp .env.example .env
# Editar .env con tokens reales
docker-compose up -d --build

# Verificar
curl http://10.0.0.10:8080/health
```

## Health Check

Endpoint: `GET /health` (puerto configurable, default 8080)
Respuesta: `{"status": "healthy", "glpi_connected": true/false}`

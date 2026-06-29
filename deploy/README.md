# Deploy en Proxmox LXC

## Opción 1: Script completo (recomendado)

Ejecuta desde el **host de Proxmox**:

```bash
# Copiar el script al host
scp deploy/deploy-proxmox.sh root@PROXMOX_IP:/tmp/

# Ejecutar
ssh root@PROXMOX_IP
bash /tmp/deploy-proxmox.sh
```

Este script:
1. Crea un LXC Debian 12 (ID 200)
2. Instala Docker dentro del LXC
3. Clona el repositorio
4. Levanta el servicio

## Opción 2: Setup manual

Si ya tienes el LXC creado:

```bash
# Entrar al LXC
pct enter 200

# Copiar y ejecutar el setup
bash /opt/mcp-glpi-wave-hub/deploy/setup-lxc.sh
```

## Después del despliegue

1. **Editar `.env`** con tus credenciales GLPI:
```bash
pct exec 200 -- nano /opt/mcp-glpi-wave-hub/.env
```

2. **Reiniciar después de editar `.env`:**
```bash
pct exec 200 -- bash -c 'cd /opt/mcp-glpi-wave-hub && docker compose restart'
```

3. **Verificar:**
```bash
curl http://10.0.0.10:8080/health
```

4. **Ver logs:**
```bash
pct exec 200 -- bash -c 'cd /opt/mcp-glpi-wave-hub && docker compose logs -f'
```

## Parámetros del LXC

| Parámetro | Valor |
|-----------|-------|
| ID | 200 |
| Hostname | mcp-glpi-hub |
| IP | 10.0.0.10/24 |
| Gateway | 10.0.0.1 |
| RAM | 2048 MB |
| Disco | 8 GB |
| Cores | 2 |
| Password | mcp-glpi-hub |
| Features | nesting=1, keyctl=1 |

## Variables del `.env`

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `GLPI_URL` | URL API REST GLPI | `http://10.0.0.20/apirest.php` |
| `GLPI_APP_TOKEN` | App Token de GLPI | `abc123...` |
| `GLPI_USER_TOKEN` | User Token de GLPI | `xyz789...` |
| `GLPI_INTERNAL_HOST` | IP de GLPI | `10.0.0.20` |
| `HUB_INTERNAL_HOST` | IP de este Hub | `10.0.0.10` |
| `HERMES_AGENT_INTERNAL_HOST` | IP del Hermes Agent | `10.0.0.5` |
| `PROXMOX_NETWORK_SUBNET` | Subred | `10.0.0.0/24` |

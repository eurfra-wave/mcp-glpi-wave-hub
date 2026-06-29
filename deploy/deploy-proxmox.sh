#!/usr/bin/bash
# ============================================================
# deploy-proxmox.sh — Crea el LXC Alpine + Docker y despliega mcp-glpi-wave-hub
#
# Ejecutar desde el HOST de Proxmox (no desde dentro del LXC)
# Uso: bash deploy/deploy-proxmox.sh
# ============================================================

set -euo pipefail

# ===================== CONFIGURACIÓN =====================
LXC_ID=200
LXC_HOSTNAME="mcp-glpi-hub"
LXC_IP="10.0.0.10/24"
LXC_GW="10.0.0.1"
LXC_BRIDGE="vmbr0"
LXC_DISK="8"
LXC_RAM="2048"
LXC_SWAP="1024"
LXC_CORES="2"
LXC_PASSWORD="mcp-glpi-hub"
LXC_TEMPLATE="local:vztmpl/alpine-3.21-standard_3.21.3-x86_64.tar.zst"

REPO_URL="https://github.com/eurfra-wave/mcp-glpi-wave-hub.git"
INSTALL_PATH="/opt/mcp-glpi-wave-hub"
# ============================================================

echo "============================================="
echo "  MCP GLPI Wave Hub — Deploy en Proxmox"
echo "============================================="
echo ""

# Verificar que estamos en Proxmox
if ! command -v pct &> /dev/null; then
    echo "ERROR: Este script debe ejecutarse en el host de Proxmox"
    exit 1
fi

# Verificar si el LXC ya existe
if pct status "$LXC_ID" &> /dev/null; then
    echo "AVISO: El LXC $LXC_ID ya existe"
    read -p "Eliminarlo y recrearlo? (s/N): " CONFIRM
    if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
        echo "Cancelado."
        exit 0
    fi
    echo "Deteniendo LXC $LXC_ID..."
    pct stop "$LXC_ID"
    sleep 2
    pct destroy "$LXC_ID" --purge
    echo "LXC $LXC_ID eliminado"
fi

# Descargar template Alpine si no existe
echo "Verificando template Alpine 3.21..."
pveam update
if ! pveam available | grep -q "alpine-3.21"; then
    echo "Descargando template Alpine 3.21..."
    pveam install 3.21
fi

# Crear LXC
echo "Creando LXC $LXC_ID ($LXC_HOSTNAME)..."
pct create "$LXC_ID" "$LXC_TEMPLATE" \
    --hostname "$LXC_HOSTNAME" \
    --memory "$LXC_RAM" \
    --swap "$LXC_SWAP" \
    --cores "$LXC_CORES" \
    --net0 "name=eth0,bridge=$LXC_BRIDGE,ip=$LXC_IP,gw=$LXC_GW,type=veth" \
    --rootfs "${LXC_ID}:local-lvm:${LXC_DISK},size=${LXC_DISK}G" \
    --password "$LXC_PASSWORD" \
    --ostype alpine \
    --unprivileged 0 \
    --features "nesting=1,keyctl=1" \
    --onboot 1 \
    --startup "order=2"

# Iniciar LXC
echo "Iniciando LXC..."
pct start "$LXC_ID"
sleep 5

# Esperar a que el LXC esté listo
echo "Esperando que el LXC este listo..."
for i in {1..30}; do
    if pct exec "$LXC_ID" -- test -f /etc/os-release 2>/dev/null; then
        break
    fi
    sleep 2
done

# Ejecutar setup dentro del LXC
echo "Ejecutando setup dentro del LXC..."
pct exec "$LXC_ID" -- bash -c "
set -euo pipefail

# Actualizar sistema
apk update
apk upgrade

# Instalar dependencias
apk add bash curl git docker docker-compose

# Habilitar e iniciar Docker
rc-update add docker boot
service docker start

echo 'Docker instalado correctamente'
"

# Clonar repositorio
echo "Clonando repositorio..."
pct exec "$LXC_ID" -- bash -c "
if [ -d '$INSTALL_PATH' ]; then
    cd '$INSTALL_PATH' && git pull
else
    git clone '$REPO_URL' '$INSTALL_PATH'
fi
"

# Crear .env
echo "Creando archivo .env..."
pct exec "$LXC_ID" -- bash -c "
if [ ! -f '$INSTALL_PATH/.env' ]; then
    cp '$INSTALL_PATH/.env.example' '$INSTALL_PATH/.env'
    echo ''
    echo 'Edita el archivo .env con tus credenciales reales:'
    echo '    nano $INSTALL_PATH/.env'
    echo ''
fi
"

# Construir y levantar
echo "Construyendo y levantando el servicio..."
pct exec "$LXC_ID" -- bash -c "
cd '$INSTALL_PATH'
docker compose up -d --build
"

echo ""
echo "============================================="
echo "  DESPLIEGUE COMPLETADO"
echo "============================================="
echo ""
echo "  LXC ID:     $LXC_ID"
echo "  Hostname:   $LXC_HOSTNAME"
echo "  IP:         ${LXC_IP%/*}"
echo "  Puerto:     8080"
echo "  Password:   $LXC_PASSWORD"
echo "  OS:         Alpine 3.21"
echo ""
echo "  Siguientes pasos:"
echo "  1. Editar .env con credenciales GLPI:"
echo "     pct exec $LXC_ID -- nano $INSTALL_PATH/.env"
echo ""
echo "  2. Reiniciar el servicio despues de editar .env:"
echo "     pct exec $LXC_ID -- bash -c 'cd $INSTALL_PATH && docker compose restart'"
echo ""
echo "  3. Verificar salud:"
echo "     curl http://${LXC_IP%/*}:8080/health"
echo ""
echo "  4. Ver logs:"
echo "     pct exec $LXC_ID -- bash -c 'cd $INSTALL_PATH && docker compose logs -f'"
echo "============================================="

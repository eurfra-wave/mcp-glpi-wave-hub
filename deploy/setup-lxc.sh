#!/usr/bin/bash
# ============================================================
# setup-lxc.sh — Instala Docker Alpine y despliega el Hub
#
# Ejecutar DENTRO del LXC (no desde Proxmox host)
# Si ya tienes el LXC creado, ejecuta esto dentro:
#   bash /opt/mcp-glpi-wave-hub/deploy/setup-lxc.sh
# ============================================================

set -euo pipefail

REPO_URL="https://github.com/eurfra-wave/mcp-glpi-wave-hub.git"
INSTALL_PATH="/opt/mcp-glpi-wave-hub"

echo "============================================="
echo "  MCP GLPI Wave Hub — Setup LXC (Alpine)"
echo "============================================="

# Instalar Docker si no existe
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    apk update
    apk add bash curl git docker docker-compose
    rc-update add docker boot
    service docker start
    echo "Docker instalado"
else
    echo "Docker ya instalado"
fi

# Clonar repositorio
echo "Clonando repositorio..."
if [ -d "$INSTALL_PATH" ]; then
    cd "$INSTALL_PATH" && git pull
else
    git clone "$REPO_URL" "$INSTALL_PATH"
fi

# Crear .env si no existe
if [ ! -f "$INSTALL_PATH/.env" ]; then
    cp "$INSTALL_PATH/.env.example" "$INSTALL_PATH/.env"
    echo ""
    echo "Edita el archivo .env con tus credenciales:"
    echo "    nano $INSTALL_PATH/.env"
    echo ""
    read -p "Presiona Enter cuando hayas editado el .env..."
fi

# Levantar servicio
echo "Construyendo y levantando..."
cd "$INSTALL_PATH"
docker compose up -d --build

# Verificar
echo ""
echo "Verificando salud..."
sleep 5
curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || echo "Endpoint no disponible aun, espera unos segundos"

echo ""
echo "============================================="
echo "  LISTO"
echo "  URL: http://$(hostname -I | awk '{print $1}'):8080/health"
echo "============================================="

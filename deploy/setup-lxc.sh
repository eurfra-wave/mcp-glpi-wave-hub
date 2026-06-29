#!/usr/bin/bash
# ============================================================
# setup-lxc.sh — Instala Docker y despliega el Hub
#
# Ejecutar DENTRO del LXC (no desde Proxmox host)
# Si ya tienes el LXC creado, ejecuta esto dentro:
#   bash setup-lxc.sh
# ============================================================

set -euo pipefail

REPO_URL="https://github.com/TU_USUARIO/mcp-glpi-wave-hub.git"
INSTALL_PATH="/opt/mcp-glpi-wave-hub"

echo "============================================="
echo "  MCP GLPI Wave Hub — Setup LXC"
echo "============================================="

# Instalar Docker si no existe
if ! command -v docker &> /dev/null; then
    echo "🐳 Instalando Docker..."
    apt-get update
    apt-get install -y ca-certificates curl gnupg lsb-release

    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list

    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    systemctl enable docker
    systemctl start docker
    echo "✅ Docker instalado"
else
    echo "✅ Docker ya instalado"
fi

# Clonar repositorio
echo "📥 Clonando repositorio..."
if [ -d "$INSTALL_PATH" ]; then
    cd "$INSTALL_PATH" && git pull
else
    git clone "$REPO_URL" "$INSTALL_PATH"
fi

# Crear .env si no existe
if [ ! -f "$INSTALL_PATH/.env" ]; then
    cp "$INSTALL_PATH/.env.example" "$INSTALL_PATH/.env"
    echo ""
    echo "⚠️  Edita el archivo .env con tus credenciales:"
    echo "    nano $INSTALL_PATH/.env"
    echo ""
    read -p "Presiona Enter cuando hayas editado el .env..."
fi

# Levantar servicio
echo "🔨 Construyendo y levantando..."
cd "$INSTALL_PATH"
docker compose up -d --build

# Verificar
echo ""
echo "⏳ Verificando salud..."
sleep 5
curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || echo "⚠️  Endpoint no disponible aún, espera unos segundos"

echo ""
echo "============================================="
echo "  ✅ LISTO"
echo "  URL: http://$(hostname -I | awk '{print $1}'):8080/health"
echo "============================================="

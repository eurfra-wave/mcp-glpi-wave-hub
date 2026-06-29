.PHONY: help build up down logs shell test lint format clean deploy

# Variables
PROJECT_NAME := mcp-glpi-wave-hub
COMPOSE_FILE := docker-compose.yml
ENV_FILE := .env
LXC_HOST := root@10.0.0.10
LXC_PATH := /opt/mcp-glpi-wave-hub

help: ## Mostrar esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ==========================================
# Desarrollo local
# ==========================================

install: ## Instalar dependencias con uv
	uv sync --dev

shell: ## Entrar al contenedor
	docker-compose exec mcp-glpi-wave-hub sh

logs: ## Ver logs en tiempo real
	docker-compose logs -f

# ==========================================
# Docker
# ==========================================

build: ## Construir imagen
	docker-compose build --no-cache

up: ## Levantar servicios
	docker-compose up -d

down: ## Bajar servicios
	docker-compose down

restart: ## Reiniciar servicios
	docker-compose restart

# ==========================================
# Calidad de código
# ==========================================

lint: ## Linter (ruff)
	uv run ruff check src/

format: ## Formatear código
	uv run ruff format src/

typecheck: ## Verificar tipos (mypy)
	uv run mypy src/

check: lint typecheck ## Ejecutar todos los checks

# ==========================================
# Testing
# ==========================================

test: ## Ejecutar tests
	uv run pytest -v

test-cov: ## Tests con cobertura
	uv run pytest --cov=src --cov-report=term-missing

# ==========================================
# Despliegue en Proxmox LXC
# ==========================================

deploy: ## Desplegar en LXC Proxmox (requiere SSH)
	@echo "🚀 Desplegando en $(LXC_HOST)..."
	ssh $(LXC_HOST) "mkdir -p $(LXC_PATH)"
	scp -r . $(LXC_HOST):$(LXC_PATH)/
	ssh $(LXC_HOST) "cd $(LXC_PATH) && docker-compose -f $(COMPOSE_FILE) up -d --build"
	@echo "✅ Despliegue completado"

deploy-logs: ## Ver logs en LXC remoto
	ssh $(LXC_HOST) "cd $(LXC_PATH) && docker-compose logs -f"

# ==========================================
# Utilidades
# ==========================================

clean: ## Limpiar artefactos
	docker-compose down -v
	rm -rf .venv __pycache__ .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info

health: ## Verificar salud del servicio
	curl -f http://localhost:8080/health || echo "❌ Health check failed"
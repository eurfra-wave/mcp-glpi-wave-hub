"""GLPI Client — Cliente HTTP para la API REST de GLPI.

Responsabilidad única: comunicación HTTP con GLPI, gestión de sesión,
y métodos CRUD genéricos.
"""

import asyncio
import json
from typing import Any, Optional
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from src.config import settings


class GLPIError(Exception):
    """Excepción base para errores de GLPI."""
    def __init__(self, message: str, status_code: int = 0):
        self.status_code = status_code
        super().__init__(message)


class GLPIAuthError(GLPIError):
    """Error de autenticación con GLPI."""
    pass


class GLPIClient:
    """Cliente para la API REST de GLPI.

    Maneja:
    - Autenticación multi-modo (User Token, Basic Auth)
    - Gestión de sesión (init/kill/refresh)
    - Métodos CRUD genéricos
    - Métodos específicos por entidad
    """

    def __init__(self) -> None:
        self.base_url = settings.glpi_url.rstrip("/")
        self.app_token = settings.glpi_app_token
        self.user_token = settings.glpi_user_token
        self.username = settings.glpi_username
        self.password = settings.glpi_password

        self._session_token: Optional[str] = None
        self._client = httpx.AsyncClient(timeout=30.0)

    # ==================== Sesión ====================

    def _get_headers(self, include_session: bool = True) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "App-Token": self.app_token,
        }
        if include_session and self._session_token:
            headers["Session-Token"] = self._session_token
        return headers

    async def init_session(self) -> str:
        """Inicializa sesión con GLPI."""
        headers = self._get_headers(include_session=False)

        if self.user_token:
            headers["Authorization"] = f"user_token {self.user_token}"
        elif self.username and self.password:
            import base64
            credentials = base64.b64encode(
                f"{self.username}:{self.password}".encode()
            ).decode()
            headers["Authorization"] = f"Basic {credentials}"
        else:
            raise GLPIAuthError("No hay método de autenticación configurado")

        response = await self._client.get(
            urljoin(self.base_url, "/initSession"),
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()
        self._session_token = data["session_token"]
        return self._session_token

    async def kill_session(self) -> None:
        """Cierra la sesión actual."""
        if not self._session_token:
            return
        try:
            await self._client.get(
                urljoin(self.base_url, "/killSession"),
                headers=self._get_headers(),
            )
        finally:
            self._session_token = None

    async def ensure_session(self) -> None:
        """Asegura que hay una sesión válida."""
        if not self._session_token:
            await self.init_session()

    # ==================== Métodos Genéricos ====================

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Any:
        """Ejecuta una petición HTTP genérica."""
        await self.ensure_session()

        url = urljoin(self.base_url, endpoint)
        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
            )
            response.raise_for_status()
            if response.status_code == 204:
                return None
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Sesión expirada, forzar renovación
                self._session_token = None
                await self.ensure_session()
                # Reintentar una vez
                response = await self._client.request(
                    method=method,
                    url=url,
                    headers=self._get_headers(),
                    json=data,
                    params=params,
                )
                response.raise_for_status()
                return response.json()
            raise GLPIError(f"HTTP {e.response.status_code}: {e.response.text}", e.response.status_code)

    async def get_items(
        self,
        itemtype: str,
        range_: Optional[str] = None,
        sort: Optional[int] = None,
        order: str = "DESC",
        search_text: Optional[dict] = None,
        is_deleted: Optional[bool] = None,
        **extra_params: Any,
    ) -> list[dict]:
        """Obtiene una lista de items de un tipo."""
        params = {}
        if range_:
            params["range"] = range_
        if sort:
            params["sort"] = str(sort)
        if order:
            params["order"] = order
        if is_deleted is not None:
            params["is_deleted"] = "1" if is_deleted else "0"
        if search_text:
            for key, value in search_text.items():
                params[f"searchText[{key}]"] = value
        params.update(extra_params)

        result = await self._request("GET", f"/{itemtype}", params=params)
        return result if isinstance(result, list) else []

    async def get_item(
        self,
        itemtype: str,
        item_id: int,
        **extra_params: Any,
    ) -> dict:
        """Obtiene un item específico por ID."""
        params = extra_params
        result = await self._request("GET", f"/{itemtype}/{item_id}", params=params)
        return result

    async def create_item(self, itemtype: str, data: dict) -> dict:
        """Crea un nuevo item."""
        result = await self._request("POST", f"/{itemtype}", data={"input": data})
        return result

    async def update_item(self, itemtype: str, item_id: int, data: dict) -> bool:
        """Actualiza un item existente."""
        await self._request("PUT", f"/{itemtype}/{item_id}", data={"input": data})
        return True

    async def delete_item(
        self,
        itemtype: str,
        item_id: int,
        force: bool = False,
        history: bool = True,
    ) -> bool:
        """Elimina un item."""
        params = {}
        if force:
            params["force_purge"] = "1"
        if not history:
            params["history"] = "0"
        await self._request("DELETE", f"/{itemtype}/{item_id}", params=params)
        return True

    # ==================== Métodos Específicos: Tickets ====================

    async def get_tickets(self, **kwargs) -> list[dict]:
        return await self.get_items("Ticket", **kwargs)

    async def get_ticket(self, ticket_id: int, **kwargs) -> dict:
        return await self.get_item("Ticket", ticket_id, **kwargs)

    async def create_ticket(self, data: dict) -> dict:
        return await self.create_item("Ticket", data)

    async def update_ticket(self, ticket_id: int, data: dict) -> bool:
        return await self.update_item("Ticket", ticket_id, data)

    async def delete_ticket(self, ticket_id: int, force: bool = False) -> bool:
        return await self.delete_item("Ticket", ticket_id, force=force)

    async def add_ticket_followup(
        self, ticket_id: int, content: str, is_private: bool = False
    ) -> dict:
        return await self.create_item("ITILFollowup", {
            "itemtype": "Ticket",
            "items_id": ticket_id,
            "content": content,
            "is_private": 1 if is_private else 0,
        })

    async def add_ticket_task(
        self,
        ticket_id: int,
        content: str,
        is_private: bool = False,
        actiontime: int = 0,
        state: int = 1,
        users_id_tech: Optional[int] = None,
    ) -> dict:
        input_data = {
            "tickets_id": ticket_id,
            "content": content,
            "is_private": 1 if is_private else 0,
            "actiontime": actiontime,
            "state": state,
        }
        if users_id_tech:
            input_data["users_id_tech"] = users_id_tech
        return await self.create_item("TicketTask", input_data)

    async def add_ticket_solution(
        self, ticket_id: int, content: str, solutiontypes_id: int = 0
    ) -> dict:
        return await self.create_item("ITILSolution", {
            "itemtype": "Ticket",
            "items_id": ticket_id,
            "content": content,
            "solutiontypes_id": solutiontypes_id,
        })

    async def get_ticket_followups(self, ticket_id: int) -> list[dict]:
        return await self.get_items("Ticket", item_id=ticket_id, sub_type="ITILFollowup")

    async def get_ticket_tasks(self, ticket_id: int) -> list[dict]:
        return await self.get_items("Ticket", item_id=ticket_id, sub_type="TicketTask")

    async def assign_ticket(
        self, ticket_id: int, user_id: int, assign_type: int = 2
    ) -> dict:
        return await self.create_item("Ticket_User", {
            "tickets_id": ticket_id,
            "users_id": user_id,
            "type": assign_type,
        })

    # ==================== Métodos Específicos: Problemas ====================

    async def get_problems(self, **kwargs) -> list[dict]:
        return await self.get_items("Problem", **kwargs)

    async def get_problem(self, problem_id: int, **kwargs) -> dict:
        return await self.get_item("Problem", problem_id, **kwargs)

    async def create_problem(self, data: dict) -> dict:
        return await self.create_item("Problem", data)

    async def update_problem(self, problem_id: int, data: dict) -> bool:
        return await self.update_item("Problem", problem_id, data)

    # ==================== Métodos Específicos: Cambios ====================

    async def get_changes(self, **kwargs) -> list[dict]:
        return await self.get_items("Change", **kwargs)

    async def get_change(self, change_id: int, **kwargs) -> dict:
        return await self.get_item("Change", change_id, **kwargs)

    async def create_change(self, data: dict) -> dict:
        return await self.create_item("Change", data)

    async def update_change(self, change_id: int, data: dict) -> bool:
        return await self.update_item("Change", change_id, data)

    # ==================== Métodos Específicos: Usuarios ====================

    async def get_users(self, **kwargs) -> list[dict]:
        return await self.get_items("User", **kwargs)

    async def get_user(self, user_id: int, **kwargs) -> dict:
        return await self.get_item("User", user_id, **kwargs)

    async def search_user(self, name: str) -> list[dict]:
        return await self.get_items("User", search_text={"name": name})

    async def create_user(self, data: dict) -> dict:
        return await self.create_item("User", data)

    # ==================== Métodos Específicos: Grupos ====================

    async def get_groups(self, **kwargs) -> list[dict]:
        return await self.get_items("Group", **kwargs)

    async def get_group(self, group_id: int, **kwargs) -> dict:
        return await self.get_item("Group", group_id, **kwargs)

    async def create_group(self, data: dict) -> dict:
        return await self.create_item("Group", data)

    async def add_user_to_group(
        self, user_id: int, group_id: int, is_manager: bool = False
    ) -> dict:
        return await self.create_item("Group_User", {
            "users_id": user_id,
            "groups_id": group_id,
            "is_manager": 1 if is_manager else 0,
        })

    # ==================== Métodos Específicos: Computadoras ====================

    async def get_computers(self, **kwargs) -> list[dict]:
        return await self.get_items("Computer", **kwargs)

    async def get_computer(self, computer_id: int, **kwargs) -> dict:
        return await self.get_item("Computer", computer_id, **kwargs)

    async def create_computer(self, data: dict) -> dict:
        return await self.create_item("Computer", data)

    async def update_computer(self, computer_id: int, data: dict) -> bool:
        return await self.update_item("Computer", computer_id, data)

    async def delete_computer(self, computer_id: int, force: bool = False) -> bool:
        return await self.delete_item("Computer", computer_id, force=force)

    # ==================== Métodos Específicos: Software ====================

    async def get_softwares(self, **kwargs) -> list[dict]:
        return await self.get_items("Software", **kwargs)

    async def get_software(self, software_id: int, **kwargs) -> dict:
        return await self.get_item("Software", software_id, **kwargs)

    async def create_software(self, data: dict) -> dict:
        return await self.create_item("Software", data)

    # ==================== Métodos Específicos: Equipos de Red ====================

    async def get_network_equipments(self, **kwargs) -> list[dict]:
        return await self.get_items("NetworkEquipment", **kwargs)

    async def get_network_equipment(self, equipment_id: int, **kwargs) -> dict:
        return await self.get_item("NetworkEquipment", equipment_id, **kwargs)

    async def create_network_equipment(self, data: dict) -> dict:
        return await self.create_item("NetworkEquipment", data)

    # ==================== Métodos Específicos: Impresoras ====================

    async def get_printers(self, **kwargs) -> list[dict]:
        return await self.get_items("Printer", **kwargs)

    async def get_printer(self, printer_id: int, **kwargs) -> dict:
        return await self.get_item("Printer", printer_id, **kwargs)

    async def create_printer(self, data: dict) -> dict:
        return await self.create_item("Printer", data)

    # ==================== Métodos Específicos: Monitores ====================

    async def get_monitors(self, **kwargs) -> list[dict]:
        return await self.get_items("Monitor", **kwargs)

    async def get_monitor(self, monitor_id: int, **kwargs) -> dict:
        return await self.get_item("Monitor", monitor_id, **kwargs)

    # ==================== Métodos Específicos: Teléfonos ====================

    async def get_phones(self, **kwargs) -> list[dict]:
        return await self.get_items("Phone", **kwargs)

    async def get_phone(self, phone_id: int, **kwargs) -> dict:
        return await self.get_item("Phone", phone_id, **kwargs)

    # ==================== Métodos Específicos: Base de Conocimiento ====================

    async def get_knowbase_items(self, **kwargs) -> list[dict]:
        return await self.get_items("KnowbaseItem", **kwargs)

    async def get_knowbase_item(self, item_id: int, **kwargs) -> dict:
        return await self.get_item("KnowbaseItem", item_id, **kwargs)

    async def search_knowbase(self, query: str) -> list[dict]:
        return await self.get_items(
            "search/KnowbaseItem",
            criteria=[{"field": 6, "searchtype": "contains", "value": query}]
        )

    async def create_knowbase_item(self, data: dict) -> dict:
        return await self.create_item("KnowbaseItem", data)

    # ==================== Métodos Específicos: Proyectos ====================

    async def get_projects(self, **kwargs) -> list[dict]:
        return await self.get_items("Project", **kwargs)

    async def get_project(self, project_id: int, **kwargs) -> dict:
        return await self.get_item("Project", project_id, **kwargs)

    async def create_project(self, data: dict) -> dict:
        return await self.create_item("Project", data)

    async def update_project(self, project_id: int, data: dict) -> bool:
        return await self.update_item("Project", project_id, data)

    # ==================== Métodos Específicos: Contratos ====================

    async def get_contracts(self, **kwargs) -> list[dict]:
        return await self.get_items("Contract", **kwargs)

    async def get_contract(self, contract_id: int, **kwargs) -> dict:
        return await self.get_item("Contract", contract_id, **kwargs)

    async def create_contract(self, data: dict) -> dict:
        return await self.create_item("Contract", data)

    # ==================== Métodos Específicos: Proveedores ====================

    async def get_suppliers(self, **kwargs) -> list[dict]:
        return await self.get_items("Supplier", **kwargs)

    async def get_supplier(self, supplier_id: int, **kwargs) -> dict:
        return await self.get_item("Supplier", supplier_id, **kwargs)

    async def create_supplier(self, data: dict) -> dict:
        return await self.create_item("Supplier", data)

    # ==================== Métodos Específicos: Localizaciones ====================

    async def get_locations(self, **kwargs) -> list[dict]:
        return await self.get_items("Location", **kwargs)

    async def get_location(self, location_id: int, **kwargs) -> dict:
        return await self.get_item("Location", location_id, **kwargs)

    async def create_location(self, data: dict) -> dict:
        return await self.create_item("Location", data)

    # ==================== Métodos Específicos: Entidades ====================

    async def get_entities(self, **kwargs) -> list[dict]:
        return await self.get_items("Entity", **kwargs)

    async def get_entity(self, entity_id: int, **kwargs) -> dict:
        return await self.get_item("Entity", entity_id, **kwargs)

    # ==================== Métodos Específicos: Categorías ====================

    async def get_categories(self, **kwargs) -> list[dict]:
        return await self.get_items("ITILCategory", **kwargs)

    # ==================== Métodos Específicos: Documentos ====================

    async def get_documents(self, **kwargs) -> list[dict]:
        return await self.get_items("Document", **kwargs)

    async def get_document(self, document_id: int, **kwargs) -> dict:
        return await self.get_item("Document", document_id, **kwargs)

    # ==================== Búsqueda Avanzada ====================

    async def search(
        self,
        itemtype: str,
        criteria: list[dict],
    ) -> list[dict]:
        """Búsqueda avanzada multi-criterio."""
        params = {}
        for i, c in enumerate(criteria):
            params[f"criteria[{i}][field]"] = str(c["field"])
            params[f"criteria[{i}][searchtype]"] = c["searchtype"]
            params[f"criteria[{i}][value]"] = c["value"]
            if c.get("link") and i > 0:
                params[f"criteria[{i}][link]"] = c["link"]
        return await self._request("GET", f"/search/{itemtype}", params=params)

    # ==================== Estadísticas ====================

    async def get_ticket_stats(self) -> dict:
        """Estadísticas de tickets por estado."""
        tickets = await self.get_items("Ticket", range_="0-9999")
        return {
            "total": len(tickets),
            "new": sum(1 for t in tickets if t.get("status") == 1),
            "processing_assigned": sum(1 for t in tickets if t.get("status") == 2),
            "processing_planned": sum(1 for t in tickets if t.get("status") == 3),
            "pending": sum(1 for t in tickets if t.get("status") == 4),
            "solved": sum(1 for t in tickets if t.get("status") == 5),
            "closed": sum(1 for t in tickets if t.get("status") == 6),
        }

    async def get_asset_stats(self) -> dict:
        """Estadísticas de inventario de activos."""
        results = await asyncio.gather(
            self.get_items("Computer", range_="0-9999", is_deleted=False),
            self.get_items("Monitor", range_="0-9999", is_deleted=False),
            self.get_items("Printer", range_="0-9999", is_deleted=False),
            self.get_items("NetworkEquipment", range_="0-9999", is_deleted=False),
            self.get_items("Phone", range_="0-9999", is_deleted=False),
            self.get_items("Software", range_="0-9999", is_deleted=False),
        )
        return {
            "computers": len(results[0]),
            "monitors": len(results[1]),
            "printers": len(results[2]),
            "network_equipments": len(results[3]),
            "phones": len(results[4]),
            "softwares": len(results[5]),
        }

    # ==================== Cierre ====================

    async def close(self) -> None:
        """Cierra el cliente y la sesión."""
        await self.kill_session()
        await self._client.aclose()
"""Formateadores de respuestas para MCP — Helpers puros."""

import json
from datetime import datetime
from typing import Any


def format_json(data: Any, indent: int = 2) -> str:
    """Serializa a JSON con manejo de tipos especiales."""
    return json.dumps(data, indent=indent, default=_json_default, ensure_ascii=False)


def _json_default(obj: Any) -> Any:
    """Maneja tipos no serializables por defecto."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def format_ticket_response(ticket: dict, include_details: bool = True) -> str:
    """Formatea respuesta de ticket con etiquetas legibles."""
    from src.utils.status_maps import get_ticket_status, get_ticket_urgency, get_ticket_type

    result = {
        "id": ticket.get("id"),
        "name": ticket.get("name"),
        "content": ticket.get("content"),
        "status": {
            "id": ticket.get("status"),
            "label": get_ticket_status(ticket.get("status", 0)),
        },
        "urgency": {
            "id": ticket.get("urgency"),
            "label": get_ticket_urgency(ticket.get("urgency", 0)),
        },
        "type": {
            "id": ticket.get("type"),
            "label": get_ticket_type(ticket.get("type", 0)),
        },
        "date_creation": ticket.get("date_creation"),
        "date_modification": ticket.get("date_modification"),
        "users_id_recipient": ticket.get("users_id_recipient"),
        "itilcategories_id": ticket.get("itilcategories_id"),
    }

    if include_details:
        result["followups_count"] = len(ticket.get("followups", []))
        result["tasks_count"] = len(ticket.get("tasks", []))
        result["solutions_count"] = len(ticket.get("solutions", []))

    return format_json(result)


def format_list_response(items: list[dict], key_fields: list[str] = None) -> str:
    """Formatea lista de items para respuesta compacta."""
    if not items:
        return format_json([])

    if key_fields:
        simplified = []
        for item in items:
            simplified.append({k: item.get(k) for k in key_fields if k in item})
        return format_json(simplified)

    return format_json(items)


def format_error(message: str, code: str = "ERROR") -> str:
    """Formatea error estándar."""
    return format_json({"error": True, "code": code, "message": message})


def format_success(message: str, data: dict = None) -> str:
    """Formatea respuesta de éxito estándar."""
    result = {"success": True, "message": message}
    if data:
        result["data"] = data
    return format_json(result)
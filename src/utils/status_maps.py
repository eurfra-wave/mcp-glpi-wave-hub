"""Mapeos de estados de GLPI — Solo diccionarios, sin lógica de negocio."""

# ==================== Estados de Tickets ====================
TICKET_STATUS = {
    1: "Nuevo",
    2: "En curso (asignado)",
    3: "En curso (planificado)",
    4: "Pendiente",
    5: "Resuelto",
    6: "Cerrado",
}

# ==================== Urgencia / Prioridad ====================
TICKET_URGENCY = {
    1: "Muy baja",
    2: "Baja",
    3: "Media",
    4: "Alta",
    5: "Muy alta",
}

# ==================== Estados de Problemas (ITIL) ====================
PROBLEM_STATUS = {
    1: "Nuevo",
    2: "Aceptado",
    3: "Planificado",
    4: "Pendiente",
    5: "Resuelto",
    6: "Cerrado",
}

# ==================== Estados de Cambios (ITIL) ====================
CHANGE_STATUS = {
    1: "Nuevo",
    2: "Evaluación",
    3: "Aprobación",
    4: "Aceptado",
    5: "Pendiente",
    6: "Prueba",
    7: "Calificación",
    8: "Aplicado",
    9: "Revisión",
    10: "Cerrado",
    11: "Rechazado",
    12: "Cancelado",
}

# ==================== Tipos de Ticket ====================
TICKET_TYPE = {
    1: "Incidencia",
    2: "Petición",
}

# ==================== Estados de Activos ====================
ASSET_STATE = {
    0: "En stock",
    1: "En producción",
    2: "En mantenimiento",
    3: "En reserva",
    4: "Retirado",
    5: "Perdido",
    6: "Robado",
    7: "Prestado",
    8: "En préstamo",
    9: "En reparación",
    10: "En prueba",
}

# ==================== Tipos de Computadora ====================
COMPUTER_TYPE = {
    1: "Estación de trabajo",
    2: "Portátil",
    3: "Servidor",
    4: "Otro",
}

# ==================== Helper para obtener etiqueta ====================

def get_status_label(status_id: int, status_map: dict) -> str:
    """Obtiene la etiqueta legible de un estado."""
    return status_map.get(status_id, f"Desconocido ({status_id})")


def get_ticket_status(status_id: int) -> str:
    return get_status_label(status_id, TICKET_STATUS)


def get_ticket_urgency(urgency_id: int) -> str:
    return get_status_label(urgency_id, TICKET_URGENCY)


def get_problem_status(status_id: int) -> str:
    return get_status_label(status_id, PROBLEM_STATUS)


def get_change_status(status_id: int) -> str:
    return get_status_label(status_id, CHANGE_STATUS)


def get_ticket_type(type_id: int) -> str:
    return get_status_label(type_id, TICKET_TYPE)


def get_asset_state(state_id: int) -> str:
    return get_status_label(state_id, ASSET_STATE)


def get_computer_type(type_id: int) -> str:
    return get_status_label(type_id, COMPUTER_TYPE)
"""Modelos Pydantic para Tickets y entidades relacionadas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketBase(BaseModel):
    id: int
    name: str
    content: str
    status: int
    urgency: int
    priority: int = 3
    impact: int = 3
    type: int = 1
    date_creation: Optional[str] = None
    date_modification: Optional[str] = None
    date_solved: Optional[str] = None
    date_closed: Optional[str] = None
    users_id_recipient: Optional[int] = None
    users_id_lastupdater: Optional[int] = None
    itilcategories_id: Optional[int] = None
    entities_id: Optional[int] = None
    time_to_resolve: Optional[str] = None
    actiontime: Optional[int] = None


class TicketFollowup(BaseModel):
    id: int
    content: str
    is_private: int = 0
    date: str
    users_id: Optional[int] = None
    itemtype: str = "Ticket"
    items_id: int


class TicketTask(BaseModel):
    id: int
    content: str
    is_private: int = 0
    actiontime: int = 0
    state: int = 1
    begin: Optional[str] = None
    end: Optional[str] = None
    users_id_tech: Optional[int] = None
    groups_id_tech: Optional[int] = None
    tickets_id: int


class TicketSolution(BaseModel):
    id: int
    content: str
    solutiontypes_id: Optional[int] = None
    itemtype: str = "Ticket"
    items_id: int
    date: str
    users_id: Optional[int] = None


class TicketWithDetails(TicketBase):
    """Ticket con seguimientos, tareas y soluciones."""
    followups: list[TicketFollowup] = []
    tasks: list[TicketTask] = []
    solutions: list[TicketSolution] = []


class TicketCreateInput(BaseModel):
    name: str = Field(..., description="Título/asunto del ticket")
    content: str = Field(..., description="Descripción/contenido del ticket")
    urgency: int = Field(default=3, ge=1, le=5, description="Urgencia (1-5)")
    priority: int = Field(default=3, ge=1, le=6, description="Prioridad (1-6)")
    impact: int = Field(default=3, ge=1, le=5, description="Impacto (1-5)")
    type: int = Field(default=1, ge=1, le=2, description="Tipo: 1=Incidente, 2=Petición")
    itilcategories_id: Optional[int] = Field(default=None, description="ID de categoría ITIL")
    entities_id: Optional[int] = Field(default=None, description="ID de entidad")
    users_id_assign: Optional[int] = Field(default=None, description="ID de usuario asignado")
    groups_id_assign: Optional[int] = Field(default=None, description="ID de grupo asignado")


class TicketUpdateInput(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    status: Optional[int] = Field(default=None, ge=1, le=6)
    urgency: Optional[int] = Field(default=None, ge=1, le=5)
    priority: Optional[int] = Field(default=None, ge=1, le=6)
    impact: Optional[int] = Field(default=None, ge=1, le=5)
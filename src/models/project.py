"""Modelos Pydantic para Proyectos."""

from pydantic import BaseModel, Field
from typing import Optional


class ProjectBase(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    priority: int = 3
    content: Optional[str] = None
    comment: Optional[str] = None
    date_creation: Optional[str] = None
    date_modification: Optional[str] = None
    plan_start_date: Optional[str] = None
    plan_end_date: Optional[str] = None
    real_start_date: Optional[str] = None
    real_end_date: Optional[str] = None
    percent_done: float = 0.0
    projectstates_id: Optional[int] = None
    projecttypes_id: Optional[int] = None
    users_id: Optional[int] = None
    groups_id: Optional[int] = None
    entities_id: Optional[int] = None


class ProjectCreateInput(BaseModel):
    name: str = Field(..., description="Nombre del proyecto")
    code: Optional[str] = Field(default=None, description="Código del proyecto")
    content: Optional[str] = Field(default=None, description="Descripción")
    priority: Optional[int] = Field(default=3, ge=1, le=6)
    plan_start_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    plan_end_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    users_id: Optional[int] = Field(default=None, description="ID del responsable")
    groups_id: Optional[int] = Field(default=None, description="ID del grupo responsable")
    entities_id: Optional[int] = None


class ProjectUpdateInput(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    percent_done: Optional[float] = Field(default=None, ge=0, le=100)
    real_start_date: Optional[str] = None
    real_end_date: Optional[str] = None
    projectstates_id: Optional[int] = None
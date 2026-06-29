"""Modelos Pydantic para ITIL Changes."""

from pydantic import BaseModel, Field
from typing import Optional


class ChangeBase(BaseModel):
    id: int
    name: str
    content: str
    status: int
    urgency: int
    impact: int
    priority: int
    date: Optional[str] = None
    date_modification: Optional[str] = None
    date_solved: Optional[str] = None
    date_closed: Optional[str] = None
    users_id_recipient: Optional[int] = None
    itilcategories_id: Optional[int] = None
    entities_id: Optional[int] = None


class ChangeCreateInput(BaseModel):
    name: str = Field(..., description="Título del cambio")
    content: str = Field(..., description="Descripción del cambio")
    urgency: Optional[int] = Field(default=3, ge=1, le=5)
    impact: Optional[int] = Field(default=3, ge=1, le=5)
    priority: Optional[int] = Field(default=3, ge=1, le=6)
    itilcategories_id: Optional[int] = None
    entities_id: Optional[int] = None


class ChangeUpdateInput(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    status: Optional[int] = Field(default=None, ge=1, le=12)
    urgency: Optional[int] = Field(default=None, ge=1, le=5)
    impact: Optional[int] = Field(default=None, ge=1, le=5)
    priority: Optional[int] = Field(default=None, ge=1, le=6)
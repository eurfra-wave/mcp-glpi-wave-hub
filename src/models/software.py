"""Modelos Pydantic para Software."""

from pydantic import BaseModel
from typing import Optional


class SoftwareBase(BaseModel):
    id: int
    name: str
    comment: Optional[str] = None
    locations_id: Optional[int] = None
    users_id_tech: Optional[int] = None
    groups_id_tech: Optional[int] = None
    is_helpdesk_visible: int = 0
    manufacturers_id: Optional[int] = None
    softwarecategories_id: Optional[int] = None
    is_deleted: int = 0
    entities_id: Optional[int] = None


class SoftwareCreateInput(BaseModel):
    name: str
    comment: Optional[str] = None
    manufacturers_id: Optional[int] = None
    softwarecategories_id: Optional[int] = None
    locations_id: Optional[int] = None
    entities_id: Optional[int] = None
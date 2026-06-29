"""Modelos Pydantic para Localizaciones y Entidades."""

from pydantic import BaseModel, Field
from typing import Optional


class LocationBase(BaseModel):
    id: int
    name: str
    completename: Optional[str] = None
    locations_id: Optional[int] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    town: Optional[str] = None
    country: Optional[str] = None
    building: Optional[str] = None
    room: Optional[str] = None
    entities_id: Optional[int] = None


class LocationCreateInput(BaseModel):
    name: str = Field(..., description="Nombre de la localización")
    address: Optional[str] = None
    postcode: Optional[str] = None
    town: Optional[str] = None
    country: Optional[str] = None
    building: Optional[str] = None
    room: Optional[str] = None
    locations_id: Optional[int] = Field(default=None, description="Localización padre")
    entities_id: Optional[int] = None


class EntityBase(BaseModel):
    id: int
    name: str
    completename: Optional[str] = None
    entities_id: Optional[int] = None
    level: int = 0
    comment: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    town: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    phonenumber: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None


class CategoryBase(BaseModel):
    id: int
    name: str
    completename: Optional[str] = None
    itilcategories_id: Optional[int] = None
    level: int = 0
    entities_id: Optional[int] = None
    is_helpdesk_visible: int = 1
    is_incident: int = 1
    is_request: int = 1
    is_problem: int = 1
    is_change: int = 1
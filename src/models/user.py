"""Modelos Pydantic para Usuarios y Grupos."""

from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    id: int
    name: str
    realname: Optional[str] = None
    firstname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    is_active: int = 1
    locations_id: Optional[int] = None
    profiles_id: Optional[int] = None
    entities_id: Optional[int] = None
    is_deleted: int = 0
    lang: Optional[str] = None


class UserCreateInput(BaseModel):
    name: str = Field(..., description="Nombre de usuario (login)")
    password: Optional[str] = Field(default=None, description="Contraseña inicial")
    realname: Optional[str] = Field(default=None, description="Apellidos")
    firstname: Optional[str] = Field(default=None, description="Nombre")
    email: Optional[str] = Field(default=None, description="Email")
    phone: Optional[str] = Field(default=None, description="Teléfono")
    mobile: Optional[str] = Field(default=None, description="Móvil")
    profiles_id: Optional[int] = Field(default=None, description="ID de perfil")
    entities_id: Optional[int] = Field(default=None, description="ID de entidad")
    is_active: int = Field(default=1, description="1=Activo, 0=Inactivo")


class GroupBase(BaseModel):
    id: int
    name: str
    completename: Optional[str] = None
    comment: Optional[str] = None
    entities_id: Optional[int] = None
    is_recursive: int = 0
    is_requester: int = 1
    is_assign: int = 1
    is_notify: int = 0


class GroupCreateInput(BaseModel):
    name: str = Field(..., description="Nombre del grupo")
    comment: Optional[str] = None
    entities_id: Optional[int] = None
    is_recursive: int = Field(default=0, description="0=No, 1=Sí")
    is_requester: int = Field(default=1, description="Puede ser solicitante")
    is_assign: int = Field(default=1, description="Puede ser asignado")
    is_notify: int = Field(default=0, description="Recibe notificaciones")


class GroupUserInput(BaseModel):
    user_id: int
    group_id: int
    is_manager: int = Field(default=0, description="0=No, 1=Es manager del grupo")
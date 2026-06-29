"""Modelos Pydantic para Activos (Computadoras, Impresoras, Monitores, Teléfonos, Equipos de Red)."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ComputerBase(BaseModel):
    id: int
    name: str
    serial: Optional[str] = None
    otherserial: Optional[str] = None
    contact: Optional[str] = None
    contact_num: Optional[str] = None
    comment: Optional[str] = None
    date_modification: Optional[str] = None
    operatingsystems_id: Optional[int] = None
    locations_id: Optional[int] = None
    states_id: Optional[int] = None
    computertypes_id: Optional[int] = None
    manufacturers_id: Optional[int] = None
    computermodels_id: Optional[int] = None
    uuid: Optional[str] = None
    is_deleted: int = 0
    entities_id: Optional[int] = None


class ComputerWithDetails(ComputerBase):
    """Computadora con software instalado y conexiones."""
    softwares: list[dict] = []
    connections: list[dict] = []
    networkports: list[dict] = []
    disks: list[dict] = []


class PrinterBase(BaseModel):
    id: int
    name: str
    serial: Optional[str] = None
    otherserial: Optional[str] = None
    contact: Optional[str] = None
    contact_num: Optional[str] = None
    have_serial: int = 0
    have_parallel: int = 0
    have_usb: int = 0
    have_wifi: int = 0
    have_ethernet: int = 0
    comment: Optional[str] = None
    date_modification: Optional[str] = None
    locations_id: Optional[int] = None
    printertypes_id: Optional[int] = None
    printermodels_id: Optional[int] = None
    manufacturers_id: Optional[int] = None
    is_deleted: int = 0
    entities_id: Optional[int] = None


class MonitorBase(BaseModel):
    id: int
    name: str
    serial: Optional[str] = None
    otherserial: Optional[str] = None
    contact: Optional[str] = None
    contact_num: Optional[str] = None
    comment: Optional[str] = None
    date_modification: Optional[str] = None
    size: Optional[float] = None
    have_micro: int = 0
    have_speaker: int = 0
    have_subd: int = 0
    have_bnc: int = 0
    have_dvi: int = 0
    have_pivot: int = 0
    have_hdmi: int = 0
    have_displayport: int = 0
    locations_id: Optional[int] = None
    monitortypes_id: Optional[int] = None
    monitormodels_id: Optional[int] = None
    manufacturers_id: Optional[int] = None
    is_deleted: int = 0
    entities_id: Optional[int] = None


class PhoneBase(BaseModel):
    id: int
    name: str
    serial: Optional[str] = None
    otherserial: Optional[str] = None
    contact: Optional[str] = None
    contact_num: Optional[str] = None
    comment: Optional[str] = None
    date_modification: Optional[str] = None
    locations_id: Optional[int] = None
    phonetypes_id: Optional[int] = None
    phonemodels_id: Optional[int] = None
    manufacturers_id: Optional[int] = None
    is_deleted: int = 0
    entities_id: Optional[int] = None
    firmware: Optional[str] = None
    number_line: Optional[str] = None
    have_headset: int = 0
    have_hp: int = 0


class NetworkEquipmentBase(BaseModel):
    id: int
    name: str
    ram: Optional[str] = None
    serial: Optional[str] = None
    otherserial: Optional[str] = None
    contact: Optional[str] = None
    contact_num: Optional[str] = None
    comment: Optional[str] = None
    date_modification: Optional[str] = None
    locations_id: Optional[int] = None
    networks_id: Optional[int] = None
    networkequipmenttypes_id: Optional[int] = None
    networkequipmentmodels_id: Optional[int] = None
    manufacturers_id: Optional[int] = None
    is_deleted: int = 0
    entities_id: Optional[int] = None


class NetworkEquipmentWithPorts(NetworkEquipmentBase):
    """Equipo de red con puertos de red."""
    networkports: list[dict] = []


class AssetCreateInput(BaseModel):
    name: str = Field(..., description="Nombre del activo")
    serial: Optional[str] = Field(default=None, description="Número de serie")
    otherserial: Optional[str] = Field(default=None, description="Número de inventario")
    comment: Optional[str] = Field(default=None, description="Comentarios")
    locations_id: Optional[int] = Field(default=None, description="ID de localización")
    states_id: Optional[int] = Field(default=None, description="ID de estado")
    entities_id: Optional[int] = Field(default=None, description="ID de entidad")


class ComputerCreateInput(AssetCreateInput):
    computertypes_id: Optional[int] = Field(default=None, description="Tipo: 1=Workstation, 2=Laptop, 3=Server")
    manufacturers_id: Optional[int] = Field(default=None, description="ID de fabricante")
    computermodels_id: Optional[int] = Field(default=None, description="ID de modelo")
    contact: Optional[str] = Field(default=None, description="Persona de contacto")
    operatingsystems_id: Optional[int] = Field(default=None, description="ID de sistema operativo")


class PrinterCreateInput(AssetCreateInput):
    printertypes_id: Optional[int] = Field(default=None, description="ID de tipo de impresora")
    printermodels_id: Optional[int] = Field(default=None, description="ID de modelo de impresora")
    manufacturers_id: Optional[int] = Field(default=None, description="ID de fabricante")


class NetworkEquipmentCreateInput(AssetCreateInput):
    networkequipmenttypes_id: Optional[int] = Field(default=None, description="ID de tipo de equipo")
    networkequipmentmodels_id: Optional[int] = Field(default=None, description="ID de modelo")
    manufacturers_id: Optional[int] = Field(default=None, description="ID de fabricante")
    networks_id: Optional[int] = Field(default=None, description="ID de red")


class AssetUpdateInput(BaseModel):
    name: Optional[str] = None
    serial: Optional[str] = None
    otherserial: Optional[str] = None
    comment: Optional[str] = None
    locations_id: Optional[int] = None
    states_id: Optional[int] = None
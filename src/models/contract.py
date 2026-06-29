"""Modelos Pydantic para Contratos y Proveedores."""

from pydantic import BaseModel, Field
from typing import Optional


class ContractBase(BaseModel):
    id: int
    name: str
    num: Optional[str] = None
    contracttypes_id: Optional[int] = None
    begin_date: Optional[str] = None
    duration: Optional[int] = None
    notice: Optional[int] = None
    periodicity: Optional[int] = None
    billing: Optional[int] = None
    comment: Optional[str] = None
    renewal: int = 0
    entities_id: Optional[int] = None


class ContractCreateInput(BaseModel):
    name: str = Field(..., description="Nombre del contrato")
    num: Optional[str] = Field(default=None, description="Número de contrato")
    contracttypes_id: Optional[int] = None
    begin_date: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    duration: Optional[int] = Field(default=None, description="Duración en meses")
    notice: Optional[int] = Field(default=None, description="Aviso en meses")
    comment: Optional[str] = None
    entities_id: Optional[int] = None


class SupplierBase(BaseModel):
    id: int
    name: str
    suppliertypes_id: Optional[int] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    town: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    phonenumber: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    comment: Optional[str] = None
    entities_id: Optional[int] = None


class SupplierCreateInput(BaseModel):
    name: str = Field(..., description="Nombre del proveedor")
    suppliertypes_id: Optional[int] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    town: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    phonenumber: Optional[str] = None
    email: Optional[str] = None
    entities_id: Optional[int] = None
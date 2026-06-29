"""Modelos Pydantic para Base de Conocimiento."""

from pydantic import BaseModel, Field
from typing import Optional


class KnowbaseItemBase(BaseModel):
    id: int
    name: str
    answer: str
    is_faq: int = 0
    view_count: int = 0
    date_creation: Optional[str] = None
    date_modification: Optional[str] = None
    users_id: Optional[int] = None
    knowbaseitemcategories_id: Optional[int] = None
    entities_id: Optional[int] = None


class KnowbaseItemCreateInput(BaseModel):
    name: str = Field(..., description="Título del artículo")
    answer: str = Field(..., description="Contenido (HTML permitido)")
    is_faq: int = Field(default=0, description="0=No, 1=Añadir a FAQ")
    knowbaseitemcategories_id: Optional[int] = Field(default=None, description="ID de categoría KB")
    entities_id: Optional[int] = None
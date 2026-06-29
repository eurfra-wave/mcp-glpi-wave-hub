"""Modelos Pydantic para Documentos."""

from pydantic import BaseModel
from typing import Optional


class DocumentBase(BaseModel):
    id: int
    name: str
    filename: Optional[str] = None
    filepath: Optional[str] = None
    mime: Optional[str] = None
    date_modification: Optional[str] = None
    comment: Optional[str] = None
    sha1sum: Optional[str] = None
    documentcategories_id: Optional[int] = None
    users_id: Optional[int] = None
    entities_id: Optional[int] = None
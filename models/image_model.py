from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union


class ImageModel(BaseModel):
    programa: Optional[str] = None
    fecha_inscripcion: Optional[datetime] = None
    tipo_documento: str
    num_documento: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[int] = None
    vendedor: Optional[int] = None

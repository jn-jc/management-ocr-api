from pydantic import BaseModel
from typing import Optional

class GetDataModel(BaseModel):
  fecha_inscripcion: Optional[str] = None
  tipo_documento: Optional[str] = None
  num_documento: Optional[str] = None
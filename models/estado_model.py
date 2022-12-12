from pydantic import BaseModel
from typing import Optional

class EstadoModel(BaseModel):
  id_estado: int
  tipo_estado: Optional[str] = None
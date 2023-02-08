from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegistroModel(BaseModel):
  id_registro: Optional[int] = None
  no_doc_cliente: Optional[str] = None
  id_estado: int
  fecha_registro: datetime
  firma: int
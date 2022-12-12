from pydantic import BaseModel
from typing import Optional

class TipoDocModel(BaseModel):
  id_tipo_doc: int
  tipo_doc: Optional[str] = None
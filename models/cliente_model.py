from pydantic import BaseModel
from typing import Optional
from models.tipo_doc_model import TipoDocModel


class ClienteModel(BaseModel):
    id_cliente: Optional[int] = None
    id_tipo_doc: TipoDocModel
    num_documento: int
    nombre_cliente: str
    apellido_cliente: str
    email_cliente: str

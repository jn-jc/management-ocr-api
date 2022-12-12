from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.estado_model import EstadoModel
from models.tipo_doc_model import TipoDocModel


class ClienteModel(BaseModel):
    id_cliente: Optional[int] = None
    id_tipo_doc: Optional[TipoDocModel] = None
    num_documento: Optional[int] = None
    nombre_cliente: Optional[str] = None
    apellido_cliente: Optional[str] = None
    email_cliente: Optional[str] = None
    fecha_inscripcion: Optional[datetime] = None
    id_estado: EstadoModel

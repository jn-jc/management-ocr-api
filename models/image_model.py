from pydantic import BaseModel
from typing import Optional
from models.plan_cliente_model import PlanClienteModel
from models.cliente_model import ClienteModel


class ImageModel(BaseModel):
    id_imagen: Optional[int] = None
    id_usuario: int
    id_registro: int
    nombre_archivo: str
    path_archivo: str

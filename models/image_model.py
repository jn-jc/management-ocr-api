from pydantic import BaseModel
from typing import Optional
from models.plan_cliente_model import PlanClienteModel
from models.cliente_model import ClienteModel


class ImageModel(BaseModel):
    id_imagen: Optional[int] = None
    id_usuario: int
    id_plan_cliente: Optional[PlanClienteModel.id_plan_cliente] = None
    id_cliente: ClienteModel.id_cliente
    nombre_archivo: str
    path_archivo: str

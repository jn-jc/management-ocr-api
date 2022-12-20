from pydantic import BaseModel
from typing import Optional
from models.cliente_model import ClienteModel
from models.plan_model import PlanModel

class PlanClienteModel(BaseModel):
  id_plan_cliente: Optional[int] = None
  id_cliente: int
  id_plan: int
  fecha_inscripcion: str
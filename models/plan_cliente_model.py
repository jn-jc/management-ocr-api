from pydantic import BaseModel
from typing import Optional
from models.cliente_model import ClienteModel
from models.plan_model import PlanModel

class PlanClienteModel(BaseModel):
  id_plan_cliente: Optional[int] = None
  id_cliente: ClienteModel.id_cliente
  id_plan: PlanModel.id_plan
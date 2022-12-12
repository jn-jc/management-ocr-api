from pydantic import BaseModel
from typing import Optional

class PlanModel(BaseModel):
  id_plan: int
  tipo_plan: Optional[str] = None
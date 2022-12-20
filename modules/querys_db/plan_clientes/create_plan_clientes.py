from config.db import conn
from schemas.plan_clientes import plan_clientes

def create_plan_cliente(data: dict):
    result = conn.execute(plan_clientes.insert().values(data))
    id_plan_cliente = result.lastrowid
    return id_plan_cliente
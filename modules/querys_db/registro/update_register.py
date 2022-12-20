from config.db import conn
from schemas.registro import registro

def update_register(id_registro: int, data: dict):
    conn.execute(registro.update().values(data).where(registro.c.id_registro == id_registro))
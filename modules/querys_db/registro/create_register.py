from config.db import conn
from schemas.registro import registro
from models.registro_model import RegistroModel


def create_register():
    register: RegistroModel = {"id_estado": 2, "firma": 0}
    result = conn.execute(registro.insert().values(register))
    id_registro = result.lastrowid
    return(id_registro)

def delete_register(id_registro: int):
    conn.execute(registro.delete().where(registro.c.id_registro == id_registro))
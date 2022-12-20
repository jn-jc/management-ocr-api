from config.db import conn
from schemas.cliente import clientes


def create_customer(data: dict):
    result = conn.execute(clientes.insert().values(data))
    id_customer = result.lastrowid
    no_doc_customer = conn.execute(clientes.select().where(clientes.c.id_cliente == id_customer)).fetchone()
    return no_doc_customer[2]

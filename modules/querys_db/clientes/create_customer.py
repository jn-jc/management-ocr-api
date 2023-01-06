from sqlalchemy import select
from config.db import conn
from schemas.cliente import clientes


def create_customer(data: dict):
    validate_customer = conn.execute(select(clientes).where(clientes.c.num_documento == data["num_documento"])).first()
    if validate_customer == None:
      result = conn.execute(clientes.insert().values(data))
      id_customer = result.lastrowid
      no_doc_customer = conn.execute(clientes.select().where(clientes.c.id_cliente == id_customer)).fetchone()
      return no_doc_customer[2]
    else:
      return validate_customer[2]

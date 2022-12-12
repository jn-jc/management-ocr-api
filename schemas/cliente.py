from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer, DateTime
from config.db import meta

clientes = Table(
    "clientes",
    meta,
    Column("id_cliente", Integer, primary_key=True),
    Column("id_tipo_doc", Integer),
    Column("num_documento", Integer),
    Column("nombre_cliente", String(255)),
    Column("apellido_cliente", String(255)),
    Column("email_cliente", String(255)),
    Column("fecha_inscripcion", DateTime),
    Column("id_estado", Integer),
)

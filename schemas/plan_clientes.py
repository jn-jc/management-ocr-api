from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

plan_clientes = Table(
    "plan_clientes",
    meta,
    Column("id_plan_cliente", Integer, primary_key=True),
    Column("id_registro", Integer),
    Column("id_plan", Integer),
    Column("fecha_inscripcion", String(255)),
)

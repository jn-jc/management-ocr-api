from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

imagen = Table(
    "imagen",
    meta,
    Column("id_imagen", Integer, primary_key=True),
    Column("id_usuario", Integer),
    Column("id_plan_cliente", Integer),
    Column("id_cliente", Integer),
    Column("nombre_archivo", String(255)),
    Column("path_archivo", String(255)),
)

from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import meta

estado = Table(
    "estado",
    meta,
    Column("id_estado", Integer, primary_key=True),
    Column("tipo_estado", String(50)),
)

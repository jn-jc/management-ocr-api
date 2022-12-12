from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

tipo_doc = Table(
    "tipo_documento",
    meta,
    Column("id_tipo_doc", Integer, primary_key=True),
    Column("tipo_doc", String(50)),
)

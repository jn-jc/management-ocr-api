from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, TIMESTAMP
from config.db import meta

registro = Table(
    "registros",
    meta,
    Column("id_registro", Integer, primary_key=True),
    Column("no_doc_client", String(255)),
    Column("id_estado", Integer),
    Column("fecha_inscripcion", DateTime),
    Column("fecha_registro", TIMESTAMP),
)

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, DateTime, TIMESTAMP
from config.db import meta

registro = Table(
    "registros",
    meta,
    Column("id_registro", Integer, primary_key=True),
    Column("no_doc_cliente", String(255), ForeignKey('cliente.num_documento')),
    Column("id_estado", Integer, ForeignKey('estado.id_estado')),
    Column("fecha_registro", TIMESTAMP),
    Column("fecha_inscripcion", String(255)),
    Column("firma", Integer)
)

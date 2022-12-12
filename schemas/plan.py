from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta

plan = Table(
    "plan",
    meta,
    Column("id_plan", Integer, primary_key=True),
    Column("tipo_plan", String(255)),
)

from sqlalchemy import create_engine, MetaData

USER_DB: str = "root"
PASS_DB: str = "root123"
HOST_DB: str = "127.0.0.0"
PORT_DB: str = "3309"
DATABASE: str = "back_office_bd"

engine = create_engine(
    f"mysql+pymysql://{USER_DB}:{PASS_DB}@{HOST_DB}:{PORT_DB}/{DATABASE}"
)

meta = MetaData()

conn = engine.connect()

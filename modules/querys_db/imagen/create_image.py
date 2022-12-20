from config.db import conn
from schemas.imagen import imagen

def create_image(data: dict):
    result = conn.execute(imagen.insert().values(data))
    id_image = result.lastrowid
    return(id_image)
    
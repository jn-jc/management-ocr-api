# FastAPI
from fastapi import APIRouter, UploadFile
from fastapi import File

# Python
from os import getcwd

# Local
from modules.image import get_data, crear_registro
from modules.querys_db.registro.create_register import delete_register

image = APIRouter(prefix="/images", tags=["Images"])

@image.get(path="/load-images")
async def load_images():
    return get_data()

@image.post(path="/get-image")
async def get_image(image: UploadFile = File(...)):
  try:
    id_registro = crear_registro()
    with open(getcwd() + "/temp/" + f'{id_registro}-{image.filename}', "wb") as file:
        content = image.file.read()
        file.write(content)
        file.close()
    return {
            "message": f"La imagen con id {id_registro} se envío exitosamente, se encuentra en espera para ser procesada.",
            "status_code": 200,
        }
  except Exception as e:
    print(e)
    delete_register(id_registro)
    return {"message": f"Error: {e}", "status_code": 500}


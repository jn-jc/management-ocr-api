# FastAPI
from fastapi import APIRouter, UploadFile
from fastapi import File
from multiprocessing import Process

# Python
from os import getcwd

# Local
from modules.image import get_data

image = APIRouter(prefix="/images", tags=["Images"])

process = Process(target=get_data)

@image.post(path="/get-image")
async def get_image(image: UploadFile = File(...)):
    with open(getcwd() + "/temp/" + image.filename, "wb") as file:
        content = image.file.read()
        file.write(content)
        file.close()
    return get_data()


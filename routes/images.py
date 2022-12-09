# FastAPI
from fastapi import APIRouter, UploadFile
from fastapi import File

# Python
from os import getcwd

# Local
from modules.image import validate_data_loyalty

router = APIRouter(prefix="/images", tags=["Images"])


@router.get(path="/")
async def home_images():
    return {"message": "Hello world from api images"}


@router.post(path="/get-image")
async def get_image(image: UploadFile = File(...)):
    with open(getcwd() + "/temp/" + image.filename, "wb") as file:
        content = image.file.read()
        file.write(content)
        file.close()
    return {"message": "success"}
  
@router.get(path='/prueba')
def prueba():
   validate_data_loyalty()
  

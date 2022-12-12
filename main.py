#FastAPI packages
from fastapi import FastAPI

#Local packages
from routes.images import image

app = FastAPI()

app.include_router(prefix='/api', router=image)

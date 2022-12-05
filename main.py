#FastAPI packages
from fastapi import FastAPI

#Local packages
from routes import images

app = FastAPI()

app.include_router(prefix='/api', router=images.router)

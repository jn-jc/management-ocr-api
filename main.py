#FastAPI packages
from fastapi import FastAPI

import uvicorn
#Local packages
from routes.images import image

app = FastAPI()

app.include_router(prefix='/api', router=image)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=9000)

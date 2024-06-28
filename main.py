from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db import models
from db.database_definition import engine
from routers.api_router import router as api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
def index():
    return RedirectResponse(url="/docs")


models.Base.metadata.create_all(bind=engine)

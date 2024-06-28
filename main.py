from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from db import models
from db.database_definition import engine

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(url="/docs")


models.Base.metadata.create_all(bind=engine)

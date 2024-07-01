import warnings

# Ignore specific Pydantic warning about configuration key changes
warnings.filterwarnings(
    "ignore", category=UserWarning, message=r".*Valid config keys have changed in V2.*"
)

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routers.api_post import router as api_router

app = FastAPI()
app.include_router(api_router)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

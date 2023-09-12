from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import LOGGING_CONFIG
from .routers import maintenance, methodologies, publications

dictConfig(LOGGING_CONFIG)

app = FastAPI()

origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(maintenance.router)
app.include_router(methodologies.router)
app.include_router(publications.router)


@app.get("/")
async def root():
    return {"message": "EES support bot content ingestion"}

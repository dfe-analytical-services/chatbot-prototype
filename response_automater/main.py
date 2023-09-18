from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import LOGGING_CONFIG, settings
from .routers import message

dictConfig(LOGGING_CONFIG)

app = FastAPI()

origins = [settings.url_chat_ui]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def http_exception_handler(req: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(content=exc.detail, status_code=exc.status_code)


app.include_router(message.router)


@app.get("/")
async def root():
    return {"message": "Response automater"}
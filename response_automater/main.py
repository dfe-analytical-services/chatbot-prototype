import logging
from logging.config import dictConfig

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import LOGGING_CONFIG, settings
from .routers import message

dictConfig(LOGGING_CONFIG)

app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.api_allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.error(msg=f"Invalid request to {request.url}. Reason: {exc.__repr__()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


app.include_router(message.router)


@app.get("/")
async def root():
    return {"message": "Response automater"}

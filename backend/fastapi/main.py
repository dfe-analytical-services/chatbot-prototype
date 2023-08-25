import asyncio
import logging
from typing import AsyncIterable, Awaitable

import config
import openai
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document
from pydantic import BaseModel
from qdrant_client import QdrantClient
from utils import makechain

app = FastAPI()
router = APIRouter(prefix="/api")
settings = config.Settings()


origins = [settings.url_public_site]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    await fn
    event.set()


async def send_message(message: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    client = QdrantClient(settings.host, port=settings.qdrant_port)

    embeds = openai.Embedding.create(input=message, engine=settings.openai_embedding_model)

    chain = makechain(callback)

    # query the database
    resp = client.search(collection_name="ees", query_vector=embeds["data"][0]["embedding"], limit=4)

    logging.info(resp)

    documents = [Document(page_content=resp[i].payload["text"]) for i in range(len(resp))]
    list_urls = list(set(resp[i].payload["url"] for i in range(len(resp))))

    task = asyncio.create_task(
        wrap_done(chain.arun(input_documents=documents, question=message, links=str(list_urls)), callback.done),
    )

    # Logic to send the response to the frontend as an event stream
    async for token in callback.aiter():
        yield f"{token}"

    await task


@app.exception_handler(RequestValidationError)
async def http_exception_handler(req: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(content=exc.detail, status_code=exc.status_code)


# pydantic validation of the request
class StreamRequest(BaseModel):
    """Request body for streaming."""

    question: str


@router.post("/chat")
def stream(body: StreamRequest):
    if len(body.question.split(" ")) > 1000:
        raise HTTPException(status_code=412, detail="Question too long")
    try:
        openai.Embedding.create(input="Test input", engine=settings.openai_embedding_model)
    except openai.error.AuthenticationError:
        logging.error("Invalid openai api key")
        raise HTTPException(status_code=500)
    except openai.error.ApiConnectionError:
        logging.error("Issue connecting to open ai service. Check network and configuration settings")
        raise HTTPException(status_code=500)
    except openai.error.RateLimitError:
        logging.error("You have exceeded your predefined rate limits")
        raise HTTPException(status_code=500)
    except openai.error.ServiceUnavaiableError:
        logging.error("OpenAi service is down")
        raise HTTPException(status_code=500)

    return StreamingResponse(send_message(body.question), media_type="text/event-stream")


app.include_router(router)

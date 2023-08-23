import asyncio
import logging
from typing import AsyncIterable, Awaitable

import config
import openai
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document
from pydantic import BaseModel
from qdrant_client import QdrantClient
from starlette.exceptions import HTTPException
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


async def send_message(message: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    client = QdrantClient(settings.host, port=settings.qdrant_port)
    embeds = openai.Embedding.create(input=message, engine=settings.openai_embedding_model)

    chain = makechain(callback)

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
        try:
            await fn
        except Exception as e:
            # TODO: handle exception
            logging.error(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop.
            event.set()

    # query the database
    resp = client.search(collection_name="ees", query_vector=embeds["data"][0]["embedding"], limit=6)

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


# pydantic validation of the request
class StreamRequest(BaseModel):
    """Request body for streaming."""

    question: str


@router.post("/chat")
def stream(body: StreamRequest):
    print("Hello")
    try:
        return StreamingResponse(send_message(body.question), media_type="text/event-stream")
    except Exception as e:
        # ToDo: More specific error handling
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(router)

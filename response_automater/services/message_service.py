import asyncio
import logging
from typing import AsyncIterable, Awaitable

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document

from ..utils import makechain
from .openai_client import get_embedding
from .vector_db_client import search

logger = logging.getLogger(__name__)


async def wrap_done(fn: Awaitable, event: asyncio.Event):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    await fn
    event.set()


async def send_message(message: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()

    embedding = get_embedding(message)

    chain = makechain(callback)

    # query the database
    resp = search(query_vector=embedding, limit=6)

    documents = [Document(page_content=resp[i].payload["text"]) for i in range(len(resp))]
    list_urls = list(set(resp[i].payload["url"] for i in range(len(resp))))

    task = asyncio.create_task(
        wrap_done(chain.arun(input_documents=documents, question=message, links=str(list_urls)), callback.done),
    )

    # Logic to send the response to the frontend as an event stream
    async for token in callback.aiter():
        yield f"{token}"

    await task

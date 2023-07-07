from typing import Awaitable, AsyncIterable
import asyncio
import json
from bs4 import BeautifulSoup
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from utils import makechain
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
   "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
  allow_methods=["*"],
    allow_headers=["*"],
)

async def send_message(message: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    client = QdrantClient('localhost', port = 6333)
    embeds = openai.Embedding.create(input = message, engine = 'text-embedding-ada-002')
    
    chain = makechain(callback)

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
        try:
            await fn
        except Exception as e:
            # TODO: handle exception
            print(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop.
            event.set()
    
    resp = client.search(collection_name = 'ees', query_vector = embeds['data'][0]['embedding'],
                         limit = 6)
    

    documents = [Document(page_content = resp[i].payload['text']) for i in range(resp)]
    list_urls = list(set(resp[i].payload['url'] for i in range(len(resp))))
    
    task = asyncio.create_task(wrap_done(
        chain.arun(input_documents = documents, question = message, links = str(list_urls)),
        callback.done),
    )
    
    async for token in callback.aiter():
        yield f'{token}'

    yield json.dumps({'sourceDocuments': list_urls})

    await task


class StreamRequest(BaseModel):
    """Request body for streaming."""
    question: str


@app.post("/api")
def stream(body: StreamRequest):
    return StreamingResponse(send_message(body.question), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)

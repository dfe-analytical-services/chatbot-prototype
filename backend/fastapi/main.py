from typing import Awaitable, AsyncIterable
import asyncio
import json
from bs4 import BeautifulSoup
import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.docstore.document import Document
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from starlette.exceptions import HTTPException 
from utils import makechain
from fastapi.middleware.cors import CORSMiddleware
import logging

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
            logging.error(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop.
            event.set()
    
    #query the database
    resp = client.search(collection_name = 'ees', query_vector = embeds['data'][0]['embedding'],
                         limit = 6)
    
    logging.info(resp)

    documents = [Document(page_content = resp[i].payload['text']) for i in range(len(resp))]
    list_urls = list(set(resp[i].payload['url'] for i in range(len(resp))))
    
    task = asyncio.create_task(wrap_done(
        chain.arun(input_documents = documents, question = message, links = str(list_urls)),
        callback.done),
    )
    
    #Logic to send the response to the frontend as an event stream
    async for token in callback.aiter():
        yield f'{token}'

    #yield json.dumps({'sourceDocuments': list_urls})

    await task
    
@app.exception_handler(HTTPException)
async def http_exception_handler(exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={'error': exc.detail}) 


#pydantic validation of the request
class StreamRequest(BaseModel):
    """Request body for streaming."""
    question: str


@app.post("/api")
def stream(body: StreamRequest):
    try:
        return StreamingResponse(send_message(body.question), media_type="text/event-stream")
    except Exception as e:
        # ToDo: More specific error handling
        raise HTTPException(status_code = 500, detail = str(e))

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)

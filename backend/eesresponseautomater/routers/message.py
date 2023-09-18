import logging

import openai
from config import settings
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from services.message_service import send_message
from utils import StreamRequest

router = APIRouter(prefix="/api")


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

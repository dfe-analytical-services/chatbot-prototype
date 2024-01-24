import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..services.message_service import send_message
from ..types import StreamingRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")


@router.post("/chat")
def stream(body: StreamingRequest):
    return StreamingResponse(send_message(body.question), media_type="text/event-stream")

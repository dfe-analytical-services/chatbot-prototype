from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from ..config import settings


# The text-embedding-ada-002 model limits us to 8192 tokens. This includes the chat prompt and history.
# For now, limiting the word count is a close-enough effort to ensure we don't exceed this limit.
def within_accepted_token_count(v: str):
    assert (
        len(v.split(" ")) <= settings.chat_message_word_limit
    ), f"Message length exceeded - whilst the service is in prototype a user message must not exceed {settings.chat_message_word_limit} words"
    return v


Question = Annotated[
    str,
    Field(min_length=1),
    AfterValidator(within_accepted_token_count),
]


class StreamingRequest(BaseModel):
    """Request body for streaming."""

    question: Question

from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


# TODO: Do we need to keep this check? If so would it be better to just check string length rather than calling split() ?
def not_over_one_thousand_words(v: str):
    assert len(v.split(" ")) <= 1000, "Question exceeded 1000 words"
    return v


Question = Annotated[
    str,
    Field(min_length=1),
    AfterValidator(not_over_one_thousand_words),
]


class StreamingRequest(BaseModel):
    """Request body for streaming."""

    question: Question

from pydantic import ValidationError
from pytest import raises

from response_automater.types import StreamingRequest


def test_happy_path():
    valid_request = StreamingRequest(question="This is my question")

    assert valid_request.question == "This is my question"


def test_empty_string():
    with raises(ValidationError) as exc_info:
        StreamingRequest(question="")
    print(exc_info)
    assert "String should have at least 1 character" in str(object=exc_info.value)


def test_not_over_one_thousand_words():
    very_long_question = "".join(["Capybara "] * 1001)

    with raises(ValidationError) as exc_info:
        StreamingRequest(question=very_long_question)

    assert "Question exceeded 1000 words" in str(object=exc_info.value)

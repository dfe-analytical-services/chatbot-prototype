from fastapi.testclient import TestClient

from response_automater.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Response automater"}


def test_body_validation_when_question_is_missing():
    response = client.post("/api/chat", json={"not-the-right-key": "What is your name?"})
    assert response.status_code == 422

    response_details = response.json()["detail"]
    assert len(response_details) == 1

    response_detail = response_details[0]

    assert response_detail["type"] == "missing"
    assert response_detail["msg"] == "Field required"


def test_body_validation_when_question_is_empty_string():
    response = client.post("/api/chat", json={"question": ""})
    assert response.status_code == 422

    response_details = response.json()["detail"]
    assert len(response_details) == 1

    response_detail = response_details[0]

    assert response_detail["type"] == "string_too_short"
    assert response_detail["msg"] == "String should have at least 1 character"


def test_body_validation_when_question_is_an_invalid_value():
    very_long_question = "".join(["Capybara "] * 301)
    response = client.post("/api/chat", json={"question": very_long_question})
    assert response.status_code == 422

    response_details = response.json()["detail"]
    assert len(response_details) == 1

    response_detail = response_details[0]

    assert response_detail["type"] == "assertion_error"
    assert (
        response_detail["msg"]
        == "Assertion failed, Message length exceeded - whilst the service is in prototype a user message must not exceed 300 words"
    )


# TODO: Add a Happy Path / successful test. This requires mocking out the openai and qdrant services

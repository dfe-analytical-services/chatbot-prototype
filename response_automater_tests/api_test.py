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
    response = client.post("/api/chat", json={"question": "dessert"})
    assert response.status_code == 422

    response_details = response.json()["detail"]
    assert len(response_details) == 1

    response_detail = response_details[0]

    assert response_detail["type"] == "assertion_error"
    assert response_detail["msg"] == "Assertion failed, dessert is not allowed"


# TODO: Add a Happy Path / successful test. This requires mocking out the openai and qdrant services

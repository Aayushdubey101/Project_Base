from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_rejects_unsupported_file_type():
    response = client.post(
        "/predict",
        files={"file": ("note.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 400

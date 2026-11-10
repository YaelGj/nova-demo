from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_prix_margherita():
    assert client.get("/commandes").json()["Margherita"]["prix"] == 9

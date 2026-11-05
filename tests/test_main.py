from fastapi.testclient import TestClient
from app.main import app, prix_total

def test_prix_total_unitaire():
    assert prix_total([10, 5]) == 16

def test_route_commandes_integration():
    client = TestClient(app)
    reponse = client.get("/commandes")
    assert reponse.status_code == 200

"""TP 4 : la règle « une commande compte de 1 à 4 pizzas » (verifier_quantite).

Remplacez les ___ (modèle : slide « Un test unitaire et un test d'intégration »), puis renommez ce fichier en test_quantite.py :
    git mv tests/quantite_a_trous.py tests/test_quantite.py
Puis lancez pytest.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app, verifier_quantite


def test_quantite_trop_grande_refusee_unitaire():
    with pytest.raises(ValueError):
        verifier_quantite(___)


def test_quantite_trop_grande_refusee_integration():
    client = TestClient(app)
    reponse = client.post("/commandes", json={"pizza": "Margherita", "quantite": ___})
    assert reponse.status_code == ___

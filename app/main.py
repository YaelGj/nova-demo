"""API de la pizzeria Nova (cas fictif, exercice pédagogique)."""
from fastapi import FastAPI

app = FastAPI(title="Nova")

# Données en mémoire : pas de base de données dans cette démonstration.
COMMANDES = [
    {"id": 1, "pizza": "Margherita", "prix": 9.5},
    {"id": 2, "pizza": "Reine", "prix": 11.0},
    {"id": 3, "pizza": "Quatre fromages", "prix": 12.5},
]


def prix_total(prix: list[float]) -> float:
    """Additionne les prix d'un panier, arrondi au centime."""
    return round(sum(prix), 2)


@app.get("/commandes")
def lister_commandes():
    return COMMANDES

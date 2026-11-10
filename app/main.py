"""Nova, pizzeria en ligne (cas fictif, exercice pédagogique)."""
import asyncio
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

PIZZERIA = "Pizzeria Nova"
QUANTITE_MAX = 4
# Pizzas, en mémoire : prix en euros et stock.
PIZZAS = {
    "Margherita": {"prix": 9, "stock": 500},
    "Reine": {"prix": 11, "stock": 300},
    "Quatre fromages": {"prix": 12, "stock": 200},
}

app = FastAPI(title="Nova")

# TP 4 : décommentez les deux lignes suivantes pour exposer /metrics à Prometheus.
# from prometheus_fastapi_instrumentator import Instrumentator
# Instrumentator().instrument(app, latency_lowr_buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)).expose(app)


class Commande(BaseModel):
    pizza: str
    quantite: int


def verifier_quantite(quantite):
    """Règle métier : une commande compte de 1 à QUANTITE_MAX pizzas."""
    if not 1 <= quantite <= QUANTITE_MAX:
        raise ValueError(f"une commande compte de 1 à {QUANTITE_MAX} pizzas")
    return quantite


# Latence simulée : chaque requête en cours ajoute 20 ms d'attente (elle monte sous ./charge.sh rush).
en_cours = 0


async def latence_simulee():
    global en_cours
    en_cours += 1
    try:
        await asyncio.sleep(min(0.003 + 0.02 * (en_cours - 1), 0.9))
    finally:
        en_cours -= 1


@app.get("/", response_class=HTMLResponse)
def accueil():
    lignes = "".join(f"<li>{nom} : {p['prix']} €, {p['stock']} en stock</li>" for nom, p in PIZZAS.items())
    docker = "<p>Servie par un conteneur Docker</p>" if os.environ.get("SERVIE_PAR") == "docker" else ""
    return f"""<!doctype html><meta charset="utf-8"><title>Nova</title>
<h1>{PIZZERIA}</h1>
<p>Commande en ligne : jusqu'à {QUANTITE_MAX} pizzas par commande.</p>
<ul>{lignes}</ul>
{docker}"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/commandes")
async def lister_pizzas():
    await latence_simulee()
    return PIZZAS


@app.post("/commandes", status_code=201)
async def commander(commande: Commande):
    await latence_simulee()
    try:
        verifier_quantite(commande.quantite)
    except ValueError as erreur:
        raise HTTPException(status_code=422, detail=str(erreur))
    if commande.pizza not in PIZZAS:
        raise HTTPException(status_code=404, detail="pizza inconnue")
    PIZZAS[commande.pizza]["stock"] -= commande.quantite
    return commande

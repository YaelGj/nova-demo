# Nova — dépôt de démonstration

> Cas fictif, exercice pédagogique. La pizzeria Nova n'existe pas.

Petite API de la pizzeria Nova, utilisée par le formateur du cours DevOps pour ses démonstrations.

## Contenu

| Chemin | Rôle |
|---|---|
| `app/main.py` | API FastAPI : fonction `prix_total` et route `GET /commandes` |
| `tests/test_main.py` | Un test unitaire et un test d'intégration (pytest) |
| `.github/workflows/livraison.yml` | Crée la release GitHub quand un tag `v*` est poussé |
| `CHANGELOG.md` | Notes de version, reprises dans la release |
| `Dockerfile` | Image de l'API |
| `infra/vm/` | Réseau et « VM » en Terraform (image `vm/`, ports 8081 et 8082), configurées par Ansible : inventaire recette/production, `group_vars/`, modèle `vitrine.html.j2` |
| `infra/cloud/` | L'API derrière un répartiteur nginx, de 2 à 3 instances |
| `k8s/` | Deployment de 3 réplicas et Service (démonstration facultative) |
| `ruleset.json` | Règles de protection de `main`, désactivées (référence) |
| `DEMO.md` | Déroulé des démonstrations et rôle des branches |
| `.devcontainer/` | Environnement du codespace (`devcontainer.json`, `post-create.sh`) |

## Lancer en local (dans le codespace)

Le codespace installe tout à sa création (`.devcontainer/post-create.sh`).

```bash
pytest
pip-audit -r requirements.txt     # dépendances à faille connue
uvicorn app.main:app --reload
```

## Avec Docker

```bash
docker build -t nova .
docker run --rm -p 8000:8000 nova
```

Puis ouvrir <http://localhost:8000/commandes>. Ctrl+C arrête le conteneur.

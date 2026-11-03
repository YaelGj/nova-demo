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
| `infra/vm/` | Réseau et « VM » en Terraform, configurées par Ansible |
| `infra/cloud/` | L'API derrière un répartiteur nginx, de 2 à 3 instances |
| `k8s/` | Deployment de 3 réplicas et Service (démonstration facultative) |
| `ruleset.json` | Règles de protection de `main`, désactivées (référence) |
| `DEMO.md` | Déroulé des démonstrations et rôle des branches |

## Lancer en local (dans le codespace)

```bash
pytest
uvicorn app.main:app --reload
```

## Avec Docker

```bash
docker build -t nova .
docker run --rm -p 8000:8000 nova
```

Puis ouvrir <http://localhost:8000/commandes>. Ctrl+C arrête le conteneur.

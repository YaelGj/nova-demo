# Nova — pizzeria en ligne

> Cas fictif, exercice pédagogique.

Nova vend ses pizzas en ligne. Ce dépôt sert aux démonstrations du formateur : mêmes fichiers, mêmes commandes et mêmes ports que kelvia-api ; déroulé dans [DEMO.md](DEMO.md).

- `app/main.py` : l'API (page `/`, `/health`, `/commandes`) ; `tests/` : les tests pytest.
- `.devcontainer/` : l'environnement du codespace, décrit en code.
- `infra/` : Terraform et Ansible (TP 3) ; `Dockerfile`, `compose.yaml`, `monitoring/`, `charge.sh` : TP 4.
- `RENDU.md` : vos réponses (TP 1 et TP 4).

Bloqué 5 minutes : ouvrez le bloc **Indice** ; 5 minutes de plus : le bloc **Solution**. Une erreur : [Erreurs fréquentes](#erreurs-fréquentes).

## Livrer : commit et push

Un commit par livrable, avec le bouton **Source Control** (barre de gauche) : message, **Commit**, puis **Sync Changes**.
Depuis le TP 2, `main` est protégée : passez par une branche et une pull request.

<details><summary>Solution</summary>

```bash
git switch -c tp3                 # une branche par livrable (depuis le TP 2)
git add -A
git commit -m "TP 3 : inventaire"
git push -u origin tp3            # puis, sur GitHub : Compare & pull request, Create, Merge
git switch main && git pull       # revenir sur main à jour
```
</details>

## TP 0 — Votre pizzeria en ligne

### 1. Ouvrir le codespace, lancer l'API, ouvrir le port 8000.

```bash
uvicorn app.main:app --reload
```

**Vous devez voir** : la page de la pizzeria.

<details><summary>Indice</summary>

Page du dépôt : **Code → Codespaces**. Le port 8000 est dans l'onglet **Ports**, à côté du terminal (icône globe).
</details>

<details><summary>Solution</summary>

**Code → Codespaces → Create codespace on main** (ou ouvrir celui créé à J-2). Dans le terminal : `uvicorn app.main:app --reload`.
Onglet **Ports** → ligne 8000 → **Open in Browser**. Laissez la visibilité du port à **Private**.
</details>

### 2. Changer le nom de la pizzeria dans app/main.py.

**Vous devez voir** : le nouveau nom.

<details><summary>Indice</summary>

La variable `PIZZERIA`, en haut du fichier. Grâce à `--reload`, l'API redémarre seule : rechargez la page.
</details>

<details><summary>Solution</summary>

```python
PIZZERIA = "Pizzeria de Mon Binôme"
```
Enregistrez (Ctrl+S), puis rechargez la page du port 8000.
</details>

### 3. Inviter votre binôme, activer la protection au push.

**Vous devez voir** : la protection activée.

<details><summary>Indice</summary>

Tout est dans **Settings**, sur la page du dépôt.
</details>

<details><summary>Solution</summary>

**Settings → Collaborators → Add people** : le compte GitHub de votre binôme.
**Settings → Advanced Security** (ou **Code security**) **→ Push protection → Enable** : GitHub refusera un push qui contient un secret.
</details>

### 4. Commit et push avec le bouton Source Control.

**Vous devez voir** : le commit sur GitHub.

<details><summary>Indice</summary>

Barre de gauche, icône des branches : message du commit, **Commit**, puis **Sync Changes**.
</details>

<details><summary>Solution</summary>

```bash
git commit -am "TP 0 : nom de la pizzeria"
git push
```
Postez le lien de votre dépôt dans le chat.
</details>

## TP 1 — Étude de cas : diagnostic et rôles

En binôme, dans `RENDU.md` (partie TP 1) du dépôt de l'un des deux. Données : en tête de `RENDU.md`.
Remplacez seulement les `___`. Livrable : un commit de `RENDU.md`.

### 1. Compléter les calculs des 4 métriques (données en tête de `RENDU.md`).

**Vous devez voir** : 4 valeurs chiffrées.

<details><summary>Indice</summary>

Écrivez le calcul, pas seulement le résultat. Lead time : du jour du commit au jour du déploiement. Change fail rate : déploiements en échec / déploiements.
</details>

<details><summary>Solution</summary>

12 déploiements sur 1 mois, 12 par mois ; (10 + 8 + 3) / 3 = 7 jours ; 3 / 12 = 25 % ; (1 + 2 + 6) / 3 = 3 h.
</details>

### 2. Relier la friction de l'entretien à un enjeu métier.

**Vous devez voir** : 1 ligne complète.

<details><summary>Indice</summary>

Pour chaque citation : qu'est-ce que l'entreprise perd ? Du temps (délai), de l'argent (coût), la confiance des clients (image).
</details>

<details><summary>Solution</summary>

Karim : délai (ou coût).
</details>

### 3. Un seul rôle responsable par tâche (liste dans RENDU.md).

**Vous devez voir** : 8 responsables.

<details><summary>Indice</summary>

SysOps : serveurs, réseau, sauvegardes. DevOps : le chemin du code à la production. DevSecOps : la sécurité dans ce chemin.
</details>

<details><summary>Solution</summary>

1 DevOps, 2 SysOps, 3 DevSecOps, 4 DevOps, 5 SysOps, 6 SysOps, 7 DevSecOps, 8 DevSecOps. Toute réponse argumentée avec un seul responsable est acceptée.
</details>

### 4. Un contrôle de sécurité et son moment dans le cycle.

**Vous devez voir** : 1 ligne complète.

<details><summary>Indice</summary>

Le plus tôt possible dans le cycle, là où une correction coûte le moins cher (shift left).
</details>

<details><summary>Solution</summary>

| Contrôle | Moment du cycle |
|---|---|
| analyse des dépendances (pip-audit) | à chaque pull request |
</details>

## TP 2 — Votre pipeline protège main

### 1. Recopier ci.yml du README sur une branche, pull request, fusion.

Fichier `.github/workflows/ci.yml` :

```yaml
name: ci
on:
  push: {branches: [main]}
  pull_request:
# moindre privilège pour le jeton
permissions: {contents: read}
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with: {python-version: "3.12"}
      - run: pip install -r requirements.txt
      - run: pytest
```

**Vous devez voir** : la pastille verte.

<details><summary>Indice</summary>

Créez la branche avec le nom de branche en bas à gauche de l'éditeur (**Create new branch**). Après le push, GitHub propose **Compare & pull request**.
</details>

<details><summary>Solution</summary>

```bash
git switch -c ajout-ci
mkdir -p .github/workflows       # puis créer ci.yml dans ce dossier, avec le contenu ci-dessus
git add .github/workflows/ci.yml
git commit -m "TP 2 : pipeline d'intégration continue"
git push -u origin ajout-ci
```
Sur GitHub : **Compare & pull request → Create pull request**, attendre la pastille verte, **Merge pull request**. Puis `git switch main && git pull`.
</details>

### 2. Ajouter le badge d'état au README.

Ligne à coller en haut du `README.md` (remplacez `<votre-compte>` par votre compte GitHub) :

```markdown
![ci](https://github.com/<votre-compte>/nova-demo/actions/workflows/ci.yml/badge.svg)
```

**Vous devez voir** : le badge vert sur la page du dépôt.

<details><summary>Indice</summary>

Le badge affiche l'état du pipeline sur `main`. Commit et push, puis rechargez la page du dépôt.
</details>

<details><summary>Solution</summary>

Collez la ligne sous le titre, enregistrez, puis :

```bash
git commit -am "TP 2 : badge d'état"
git push
```
</details>

### 3. Ruleset (slide « Protéger main avec un ruleset »), changer un prix, pull request.

**Vous devez voir** : la fusion bloquée. Remettre le prix.

<details><summary>Indice</summary>

**Settings → Rules → Rulesets**. Le check à exiger est le nom du job : `tests`. Le test `test_prix_margherita` vérifie le prix de la Margherita.
</details>

<details><summary>Solution</summary>

1. **Settings → Rules → Rulesets → New ruleset → New branch ruleset** ; cible : **Include default branch** ; cocher **Require a pull request before merging** (0 approbation) et **Require status checks to pass before merging**, ajouter `tests` ; **Enforcement status : Active** ; **Create**.
2. Changer un prix :
   ```bash
   git switch -c prix                 # puis, dans app/main.py : "prix": 9 devient "prix": 10
   git commit -am "Nouveau prix de la Margherita"
   git push -u origin prix
   ```
   Ouvrir la pull request : pastille rouge, **Merge** grisé.
3. Remettre `9`, puis `git commit -am "Prix remis" && git push` : pastille verte, fusion.
</details>

## TP 3 — L'infrastructure de Nova en code

Dans `infra/` : `main.tf` (Terraform), `inventaire.yaml` et `site.yaml` (Ansible). Livrable : un commit de `infra/inventaire.yaml`.

### 1. Dans infra/ : terraform init, plan, apply.

```bash
cd infra
terraform init
terraform apply      # affiche le plan, puis répondez yes
```

**Vous devez voir** : deux pages, ports 8081 et 8082.

<details><summary>Indice</summary>

Lisez le plan avant de répondre `yes` : chaque `+` est une ressource créée. Les pages s'ouvrent dans l'onglet **Ports**, ou avec `curl localhost:8081`.
</details>

<details><summary>Solution</summary>

Plan : `Plan: 4 to add, 0 to change, 0 to destroy.` (image, réseau, vm-web-1, vm-web-2). Les ports 8081 et 8082 affichent « Directory listing for / » : le dossier `/srv` est encore vide.
</details>

### 2. Lancer le playbook.

```bash
ansible-playbook -i inventaire.yaml site.yaml
```

**Vous devez voir** : RECETTE sur 8081, PRODUCTION sur 8082.

<details><summary>Indice</summary>

Lancez la commande depuis `infra/`. Rechargez les deux pages.
</details>

<details><summary>Solution</summary>

`changed=1` pour vm-web-1 et vm-web-2. `curl localhost:8081` affiche `<h1>RECETTE</h1>`, `curl localhost:8082` affiche `<h1>PRODUCTION</h1>`.
</details>

### 3. maintenance: true pour la production (inventaire.yaml), relancer.

**Vous devez voir** : seule la production en maintenance.

<details><summary>Indice</summary>

Une seule valeur change, dans le groupe `production`. Relancez le playbook.
</details>

<details><summary>Solution</summary>

```yaml
  vars: {environnement: PRODUCTION,
         maintenance: true}
```
Puis `ansible-playbook -i inventaire.yaml site.yaml` : `changed=1` pour vm-web-2 seulement ; le port 8082 affiche « Maintenance en cours ».
</details>

### 4. Remettre false, tout relancer deux fois.

```bash
terraform apply
ansible-playbook -i inventaire.yaml site.yaml
```

**Vous devez voir** : « No changes » et changed=0.

<details><summary>Indice</summary>

Le premier passage remet la page de production ; le second ne trouve plus rien à changer : c'est l'idempotence.
</details>

<details><summary>Solution</summary>

Remettez `maintenance: false`. Premier passage : `No changes.` pour Terraform, `changed=1` pour vm-web-2. Second passage : `No changes.` et `changed=0` partout.
</details>

## TP 4 — Partie 1 : conteneuriser l'API

Livrable : un commit de `compose.yaml`.

### 1. Lire le Dockerfile, décommenter le service api de compose.yaml, docker compose up -d.

```bash
docker compose up -d
docker compose ps
```

**Vous devez voir** : api healthy.

<details><summary>Indice</summary>

Arrêtez d'abord uvicorn (Ctrl+C) : il occupe le port 8000. Pour décommenter : sélectionnez les lignes du service `api`, puis Ctrl+/. La vérification de santé a lieu toutes les 10 s.
</details>

<details><summary>Solution</summary>

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment: {SERVIE_PAR: docker}
    healthcheck:
      test: >-
        python -c "import urllib.request as u;
        u.urlopen('http://localhost:8000/health')"
      interval: 10s
```
`docker compose ps` : `Up … (healthy)` sur la ligne api (après « health: starting », 10 à 20 s).
</details>

### 2. Ouvrir le port 8000.

**Vous devez voir** : « Servie par un conteneur Docker ».

<details><summary>Indice</summary>

Onglet **Ports**, ligne 8000. La phrase s'affiche quand la variable `SERVIE_PAR` vaut `docker`.
</details>

<details><summary>Solution</summary>

Onglet **Ports** → 8000 → **Open in Browser** (ou `curl localhost:8000`). La variable vient de `environment` dans `compose.yaml`.
</details>

### 3. Changer un texte de la page, docker compose up -d --build.

```bash
docker compose up -d --build
```

**Vous devez voir** : la modification.

<details><summary>Indice</summary>

Sans `--build`, l'ancienne image tourne toujours.
</details>

<details><summary>Solution</summary>

Dans `app/main.py`, changez par exemple `PIZZERIA` ou la phrase « Commande en ligne… », puis `docker compose up -d --build` et rechargez la page.
</details>

## TP 4 — Observer Nova, provoquer une panne

Livrables : un commit pour l'instrumentation et `RENDU.md`, un commit pour le test des quantités.

### 1. Décommenter l'instrumentation, up -d --build, Grafana, ./charge.sh puis ./charge.sh rush.

```bash
docker compose up -d --build
./charge.sh          # Ctrl+C, puis ./charge.sh rush
```

**Vous devez voir** : les courbes monter.

<details><summary>Indice</summary>

Les deux lignes marquées « TP 4 » dans `app/main.py`. Grafana : port 3000, tableau de bord « Nova ». Les courbes se mettent à jour toutes les 5 s.
</details>

<details><summary>Solution</summary>

```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app, latency_lowr_buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)).expose(app)
```
`curl -s localhost:8000/metrics | head` affiche des mesures. Sous `./charge.sh`, environ 5 requêtes par seconde ; sous `./charge.sh rush`, le trafic et la latence montent pendant 60 s.
</details>

### 2. Partie SLO (Service Level Objective) de RENDU.md.

**Vous devez voir** : indicateur, cible, error budget.

<details><summary>Indice</summary>

Error budget = 100 % moins la cible, appliqué aux 43 200 minutes de 30 jours.
</details>

<details><summary>Solution</summary>

Panneau « Latence 95e centile /commandes » ; SLI sous 500 ms pendant 99,5 % du temps ; 0,5 % de 43 200 min = 216 min au-dessus de 500 ms ; budget épuisé : on fige les nouveautés et on fiabilise.
</details>

### 3. Compléter et renommer le test à trous (README), limite à 6.

Fichier `tests/quantite_a_trous.py` :

```bash
git mv tests/quantite_a_trous.py tests/test_quantite.py
pytest
```

**Vous devez voir** : le test rouge. Remettre 4.

<details><summary>Indice</summary>

Une quantité refusée est hors de 1 à 4 pizzas. Code HTTP d'une donnée refusée : 422. Puis `QUANTITE_MAX = 6` dans `app/main.py` et relancez `pytest`.
</details>

<details><summary>Solution</summary>

Trous : `verifier_quantite(5)`, `"quantite": 5`, `== 422`. `pytest` : vert. Avec `QUANTITE_MAX = 6`, 5 devient acceptée : `2 failed`. Remettez `QUANTITE_MAX = 4` : vert.
</details>

### 4. Partie chaos de RENDU.md, docker compose stop api 2 minutes, puis start.

```bash
docker compose stop api      # attendre 2 minutes
docker compose start api
```

**Vous devez voir** : la panne, puis le retour.

<details><summary>Indice</summary>

Remplissez « Avant l'expérience » avant d'arrêter quoi que ce soit. Gardez `./charge.sh` dans un autre terminal et le tableau de bord ouvert.
</details>

<details><summary>Solution</summary>

`./charge.sh` affiche `000` (pas de réponse) ; « API joignable » passe à 0 en une dizaine de secondes ; les panneaux de trafic et de latence montrent un trou. Après `start` : « API joignable » revient à 1, `200` revient.
</details>

## TP 5 — Atelier collectif : préparer la migration de Nova

En classe, sans dépôt : une stratégie 7 R par composant, le service cloud de l'API, un risque et sa mesure.

## En avance ?

- Ajoutez `pip install pip-audit` et `pip-audit -r requirements.txt` au pipeline.
- Passez `nombre_vm` à 3 dans `infra/main.tf`, puis `terraform apply` : une troisième page.
- Dans Grafana, une alerte sur « API joignable » à 0.

## Erreurs fréquentes

Copiez le message exact avant de demander de l'aide.

| Message ou symptôme | Cause et correction |
|---|---|
| `push declined due to repository rule violations` | `main` est protégée depuis le TP 2 : passez par une branche et une pull request. |
| `Interrupted: 1 error during collection` | `pytest.ini` a disparu de la racine : restaurez-le. |
| `StarletteDeprecationWarning` | Un avertissement sans effet : les tests passent. |
| Cible Prometheus en erreur (`no such host`), « API joignable » à 0 | Le service `api` est encore en commentaire dans `compose.yaml` (TP 4, partie 1). |
| Panneaux de requêtes et de latence vides pendant l'arrêt de l'API | Normal : une API arrêtée n'envoie plus de mesures. Seul « API joignable » (et `charge.sh`) voit la panne. |
| `port is already allocated` sur le port 8000 | Un conteneur ou uvicorn tourne encore : Ctrl+C, ou `docker ps` puis `docker stop`. |
| `timeout while waiting for state to become 'removed'` | Une ressource remplacée (`-/+` dans le plan) est encore utilisée par une autre. |
| `env: 'bash\r': No such file or directory` ou `detected dubious ownership` | Vous travaillez hors de Codespaces : repassez sur votre codespace. |

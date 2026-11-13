# Démonstrations du formateur (nova-demo)

> Cas fictif, exercice pédagogique. Mêmes fichiers, commandes et ports que kelvia-api.

`main` = état « avant » ; `solution` = état final (dont `livraison.yml` complété et `CHANGELOG.md` v1.0.0).
Aucun ruleset, aucun tag, aucune release : le ruleset se crée en direct (démonstration 2, étape 3).
Commandes lancées dans le codespace de `main`, à la racine du dépôt, sauf mention de `infra/`.

## La veille (J-1)

1. Codespace sur `main`, gardé jusqu'à la fin du jour 2, puis `docker compose pull`.
2. `gh release list` vide ; `git ls-remote --heads origin` : `main` et `solution` seulement ; Settings → Rules → Rulesets : vide.
3. Noter l'état « avant » pour l'après-séance : `git rev-parse HEAD`.

## 1. « On fait ensemble » avant le TP 0 — sur kelvia-formateur

Code → Codespaces ; ouvrir `.devcontainer/devcontainer.json` (image, outils, `post-create.sh`, ports), puis :

```bash
uvicorn app.main:app --reload
```

Onglet **Ports** → 8000 (visibilité **Private**) ; puis le bouton **Source Control**. Vote « fait » à chaque geste.

## 2. Un cycle complet, en direct (chapitre 3)

Après chaque fusion : **Delete branch** sur la pull request, puis `git switch main && git pull`.

1. ci.yml (copié du README) :
   ```bash
   git switch -c ajout-ci
   mkdir -p .github/workflows     # coller ci.yml du README dans .github/workflows/ci.yml
   git add .github && git commit -m "Pipeline d'intégration continue"
   git push -u origin ajout-ci
   ```
   **Compare & pull request → Create** : pastille verte ; **Merge pull request**.
2. Badge : coller `![ci](https://github.com/YaelGj/nova-demo/actions/workflows/ci.yml/badge.svg)` sous le titre du README.
   ```bash
   git switch -c badge
   git commit -am "Badge d'état" && git push -u origin badge
   ```
   Pull request, fusion : badge vert sur la page du dépôt (environ 30 s).
3. Ruleset (slide « Protéger main avec un ruleset ») : **Settings → Rules → Rulesets → New ruleset → New branch ruleset**, nom `proteger-main`, **Include default branch**, **Require a pull request before merging** (0 approbation), **Require status checks to pass before merging** + `tests`, **Enforcement status : Active**, **Create**.
   Puis, dans `app/main.py`, `"prix": 9` devient `"prix": 10` :
   ```bash
   git switch -c prix
   git commit -am "Margherita à 10 €" && git push -u origin prix
   ```
   Pull request : rouge, **Merge** bloqué. **Details** → journal du job `tests` : `assert 10 == 9`. Remettre `9` :
   ```bash
   git commit -am "Prix remis" && git push
   ```
   Vert ; fusion.
4. Livraison : livraison.yml complété et CHANGELOG v1.0.0, pris sur `solution` (lire à l'écran les réponses A à D) :
   ```bash
   git switch -c livraison
   git checkout origin/solution -- .github/workflows/livraison.yml CHANGELOG.md
   git commit -m "Livraison v1.0.0" && git push -u origin livraison
   ```
   Pull request, fusion, puis :
   ```bash
   git switch main
   git pull
   git tag v1.0.0
   git push origin v1.0.0
   ```
   Onglet **Actions** : `livraison` (environ 30 s) ; onglet **Releases** : v1.0.0, avec le texte du CHANGELOG.

## 3. TP 3 — dossier infra/

```bash
cd infra
terraform init
terraform plan                                  # lire les + : Plan: 4 to add
terraform apply                                 # yes ; ports 8081 et 8082 : dossier vide
ansible-playbook -i inventaire.yaml site.yaml   # 8081 RECETTE, 8082 PRODUCTION
```

`maintenance: true` dans le groupe `production` de `inventaire.yaml`, relancer le playbook : 8082 « Maintenance en cours », 8081 inchangé.
Remettre `false`, puis deux fois `terraform apply` et le playbook : « No changes. », `changed=0`. Ne pas détruire : la démonstration 6 réutilise l'infrastructure.

## 4. TP 4, partie 1 — conteneuriser

Arrêter uvicorn (Ctrl+C). Lire le `Dockerfile`. Décommenter le service `api` de `compose.yaml` (sélection, Ctrl+/) :

```bash
docker compose up -d
docker compose ps                # api : (healthy) après 10 à 20 s
```

Port 8000 : « Servie par un conteneur Docker ». Changer la phrase « Commande en ligne… » dans `app/main.py`, puis `docker compose up -d --build`.

## 5. Grafana ensemble et TP 4

1. Décommenter les deux lignes « TP 4 » de `app/main.py`, puis `docker compose up -d --build`.
2. Port 3000 : tableau de bord « Nova » (« Kelvia » chez les élèves). Vote « fait ». Puis `./charge.sh` (Ctrl+C) et `./charge.sh rush` : les courbes montent.
3. Test rouge : compléter `tests/quantite_a_trous.py` (`5`, `5`, `422`), puis :
   ```bash
   git mv tests/quantite_a_trous.py tests/test_quantite.py
   pytest                           # 4 passed
   ```
   `QUANTITE_MAX = 6` dans `app/main.py`, `pytest` : `2 failed`, lire `DID NOT RAISE` et `assert 201 == 422`. Remettre `4`, `pytest` : vert.
4. Faire voter l'hypothèse ; `./charge.sh` dans un second terminal, tableau de bord ouvert :
   ```bash
   docker compose stop api          # « API joignable » à 0 en 10 s environ ; charge.sh affiche 000
   docker compose start api         # retour à 1 en 5 s environ
   ```
   Partage d'écran seulement, jamais de port en Public.

## 6. Déployer comme sur un cloud — dossier infra/

Dans `infra/main.tf`, variable `nombre_vm` : `default = 2` devient `default = 3`.

```bash
terraform plan                   # Plan: 1 to add, 0 to change, 0 to destroy
terraform apply                  # yes ; troisième page sur le port 8083 (dossier vide : hors inventaire Ansible)
```

## Après la séance : revenir à l'état « avant »

```bash
cd infra && terraform destroy -auto-approve && cd .. && docker compose down
```

Supprimer le ruleset (**Settings → Rules → Rulesets → proteger-main → Delete ruleset**), puis, avec le commit noté la veille :

```bash
gh release delete v1.0.0 --cleanup-tag --yes      # supprime aussi le tag, distant et local
git switch main && git pull
git restore --source=<commit noté la veille> --staged --worktree .
git commit -m "Retour à l'état avant" && git push
```

## Répéter sur une copie (nova-repetition)

1. nova-demo, **Settings → General → Template repository** : cocher.
2. **Use this template → Create a new repository** : `nova-repetition`, public, **Include all branches** coché (l'étape 4 lit `origin/solution`).
3. Décocher **Template repository** sur nova-demo.
4. Dans un codespace de nova-repetition : démonstrations 2 à 6, en remplaçant `YaelGj/nova-demo` par `YaelGj/nova-repetition` dans la ligne du badge.
5. Rejouer la démonstration 2 : la section précédente ; ou supprimer nova-repetition (**Settings → Delete this repository**) et recommencer.

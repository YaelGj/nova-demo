# Démonstrations du formateur (nova-demo)

> Cas fictif, exercice pédagogique. Mêmes fichiers, commandes et ports que kelvia-api.

`main` = état « avant » ; `solution` = état final. Branches prêtes pour la démonstration 2, créées depuis `main`, une par fichier touché :
`demo-1-ci` (ci.yml), `demo-2-badge` (badge du README), `demo-3-prix` (Margherita à 10 €), `demo-4-livraison` (livraison.yml, CHANGELOG v1.0.0).
Aucun ruleset, aucun tag, aucune release à l'avance. Un seul codespace, sur `main`, créé à J-1 et gardé jusqu'à la fin du jour 2.
Commandes à la racine du dépôt, sauf mention de `infra/`. Ne jamais cliquer **Delete branch** : les branches `demo-*` servent à rejouer.

## La veille (J-1)

1. Codespace sur `main`, puis :
   ```bash
   docker compose pull
   cd infra && terraform init && cd ..
   git rev-parse HEAD               # noter ce commit : état « avant », pour l'après-séance
   ```
2. Vérifier : `gh release list` vide ; `git ls-remote --heads origin` : `main`, `solution` et les 4 `demo-*` ; **Settings → Rules → Rulesets** vide ; libellés de la slide « Protéger main avec un ruleset ».

## 1. « On fait ensemble » avant le TP 0 — sur nova-demo

1. Page du dépôt : **Code**, **Pull requests**, **Actions**, **Settings**. Vote « fait ».
2. Ouvrir le codespace ; ouvrir `.devcontainer/devcontainer.json` : image, outils, `post-create.sh`, ports. Vote « fait ».
3. Terminal :
   ```bash
   uvicorn app.main:app --reload
   ```
   Onglet **Ports** → 8000, visibilité **Private**. Vote « fait ». Ctrl+C ensuite.
4. Le bouton **Source Control**. Vote « fait ».

## 2. Un cycle complet, en direct (chapitre 3) — sur GitHub

Rien à taper : **Pull requests → New pull request**, base `main`, compare `demo-…`, **Create pull request**. Pendant chaque pipeline : « vert ou rouge ? » au chat.

1. `demo-1-ci` : pastille verte (environ 30 s) ; **Merge pull request**.
2. `demo-2-badge` : verte ; fusion ; page du dépôt : badge vert.
3. Ruleset (slide « Protéger main avec un ruleset ») : **Settings → Rules → Rulesets → New ruleset → New branch ruleset**, nom `proteger-main`, cible **Include default branch**, **Require a pull request before merging** (0 approbation), **Require status checks to pass before merging** + `tests`, **Enforcement status : Active**, **Create**.
   Puis `demo-3-prix` : rouge, **Merge** bloqué. **Details** → journal du job `tests` : `assert 10 == 9`. **Close pull request**, sans fusionner.
4. `demo-4-livraison` : onglet **Files changed**, montrer `livraison.yml` (A `tags`, B `write`, C `ubuntu-latest`, D `GH_TOKEN`) ; verte ; fusion. Puis, dans le codespace :
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
terraform plan                                  # lire les + : Plan: 4 to add
terraform apply                                 # yes ; ports 8081 et 8082 : dossier vide
ansible-playbook -i inventaire.yaml site.yaml   # 8081 RECETTE, 8082 PRODUCTION
```

`maintenance: true` dans le groupe `production` de `inventaire.yaml`, relancer le playbook : 8082 « Maintenance en cours », 8081 inchangé.
Remettre `false`, puis `terraform apply` et le playbook, deux fois : « No changes. », `changed=0`. Ne pas détruire : la démonstration 6 réutilise l'infrastructure.

## 4. TP 4, partie 1 — conteneuriser

Arrêter uvicorn (Ctrl+C). Lire le `Dockerfile`. Décommenter le service `api` de `compose.yaml` (sélection, Ctrl+/) :

```bash
docker compose up -d
docker compose ps                # api : (healthy) après 10 à 20 s
```

Port 8000 : « Servie par un conteneur Docker ». Changer la phrase « Commande en ligne… » dans `app/main.py`, puis `docker compose up -d --build` : la modification.

## 5. Grafana ensemble et TP 4

1. Décommenter les deux lignes « TP 4 » de `app/main.py`, puis `docker compose up -d --build`.
2. Port 3000 : tableau de bord « Nova » (« Kelvia » chez les élèves). Vote « fait ». Puis `./charge.sh` (Ctrl+C) et `./charge.sh rush` : les courbes montent.
3. Test rouge, comme les élèves : compléter `tests/quantite_a_trous.py` (`5`, `5`, `422`), puis :
   ```bash
   git mv tests/quantite_a_trous.py tests/test_quantite.py
   pytest                           # 4 passed
   ```
   Ligne 10 de `app/main.py` : `QUANTITE_MAX = 4` devient `QUANTITE_MAX = 6` ; `pytest` : `2 failed`, lire `DID NOT RAISE` et `assert 201 == 422`. Remettre `4`, `pytest` : vert.
4. Faire voter l'hypothèse ; `./charge.sh` dans un second terminal, tableau de bord ouvert :
   ```bash
   docker compose stop api          # « API joignable » à 0 en 10 s environ ; charge.sh affiche 000
   docker compose start api         # retour à 1 en 5 s environ, healthy en 11 s
   ```
   Partage d'écran seulement, jamais de port en Public.

## 6. Déployer comme sur un cloud — dossier infra/

Une seule modification : dans `infra/main.tf`, variable `nombre_vm`, `default = 2` devient `default = 3` (plutôt que `-var nombre_vm=3`, qu'un `apply` suivant sans l'option déferait).

```bash
terraform apply                  # lire le plan : Plan: 1 to add ; yes ; troisième page sur le port 8083
```

## Après la séance : revenir à l'état « avant » et rejouer

```bash
cd infra && terraform destroy -auto-approve && cd .. && docker compose down
git reset --hard                 # défait dans le codespace les démonstrations 4 à 6
```

Supprimer le ruleset (**Settings → Rules → Rulesets → proteger-main → Delete ruleset**), puis, avec le commit noté la veille :

```bash
gh release delete v1.0.0 --cleanup-tag --yes      # supprime la release et le tag, distant et local
git switch main
git push --force origin <commit noté la veille>:main   # main revient à l'état « avant », sans les fusions
git reset --hard <commit noté la veille>
```

Les branches `demo-*` n'ont pas bougé : la démonstration 2 se rejoue telle quelle, avec de nouvelles pull requests. Sans le `--force`, GitHub refuserait ces pull requests (« No commits between main and demo-1-ci »).

## Répéter sur une copie (nova-repetition)

1. Dans un terminal de votre machine où `gh` est connecté (le jeton d'un codespace ne crée pas de dépôt) :
   ```bash
   gh repo create YaelGj/nova-repetition --public
   git clone --bare https://github.com/YaelGj/nova-demo.git nova.git
   git -C nova.git push --all https://github.com/YaelGj/nova-repetition.git
   ```
   Pas de « Use this template » : les branches y perdent leur historique commun avec `main`, et GitHub refuse les pull requests des branches `demo-*`.
2. Démonstrations 1 à 6 sur nova-repetition (le badge de `demo-2-badge` affiche l'état de nova-demo : sans importance).
3. Rejouer : la section précédente ; ou supprimer nova-repetition (**Settings → Delete this repository**) et recommencer.

# Démonstrations du formateur (nova-demo)

> Cas fictif, exercice pédagogique. Mêmes fichiers, commandes et ports que kelvia-api.

`main` = état « avant » ; `solution` = état final, avec en plus `.github/workflows/livraison.yml` et `CHANGELOG.md` (livraison sur tag).
Ruleset `proteger-main` : créé, **désactivé**. Toutes les commandes se lancent dans un codespace de `main`, à la racine du dépôt.

## La veille

1. Codespace créé sur `main`, puis `docker compose pull` (images Prometheus et Grafana en cache).
2. Ruleset désactivé : `gh api repos/YaelGj/nova-demo/rulesets --jq '.[].enforcement'` affiche `disabled`.
3. Pas de tag ni de release : `gh release list` est vide.
4. Branches distantes : `main` et `solution` seulement (`git ls-remote --heads origin`). Une fois, avant la première séance :
   `gh pr close 2` puis `git push origin --delete ajout-ci test-casse` (restes de la version précédente).

## TP 0 (3 min) : le codespace

Montrer `.devcontainer/devcontainer.json` (image, outils, `post-create.sh`, ports), puis :

```bash
uvicorn app.main:app --reload
```

Onglet **Ports** → 8000 → **Open in Browser** (visibilité **Private**) : la page de la pizzeria. Changer `PIZZERIA` dans `app/main.py`, recharger. Ctrl+C.

## Chapitre 2 : pip-audit

```bash
pip install pip-audit==2.10.1
pip-audit -r requirements.txt; echo $?     # 0 : aucune faille connue
```

## TP 1 (2 min) : RENDU.md

Ouvrir `RENDU.md`, remplir en direct : `12 déploiements sur 1 mois | 12 par mois`, puis la friction de Karim : `délai`.
Ne pas commiter (Ctrl+Z, ou `git checkout RENDU.md`).

## Chapitre 3 : un cycle complet (25 min)

1. Branche `ajout-ci`, pull request : pastille verte, fusion.
   ```bash
   git switch -c ajout-ci
   git checkout origin/solution -- .github CHANGELOG.md
   git commit -m "Pipeline : ci.yml et livraison.yml"
   git push -u origin ajout-ci
   gh pr create --fill
   gh pr checks --watch
   gh pr merge --merge
   ```
2. Badge d'état : sur `main`, coller sous le titre du README
   `![ci](https://github.com/YaelGj/nova-demo/actions/workflows/ci.yml/badge.svg)`, puis :
   ```bash
   git switch main && git pull
   git commit -am "Badge d'état" && git push
   ```
   Page du dépôt : badge vert après le pipeline de `main` (environ 30 s).
3. Un test cassé : `"prix": 9` devient `"prix": 10` dans `app/main.py`.
   ```bash
   git switch -c casse-en-direct
   git commit -am "Margherita à 10 €" && git push -u origin casse-en-direct
   gh pr create --fill
   gh pr checks --watch                    # tests : fail
   gh run view --log-failed | grep -E "assert|FAILED"
   ```
   Lire `assert 10 == 9`, remettre `9`, puis `git commit -am "Prix remis" && git push`, `gh pr checks --watch` (pass), `gh pr merge --merge`.
4. Tag v1.0.0 : la release apparaît.
   ```bash
   git switch main && git pull
   git tag v1.0.0 && git push origin v1.0.0
   gh run watch $(gh run list -w livraison -L 1 --json databaseId -q '.[0].databaseId')
   gh release view v1.0.0
   ```

Pendant la pause qui suit : préparer la pull request rouge du ruleset (elle fait aussi apparaître le check `tests` dans le ruleset).

```bash
git switch main && git pull && git switch -c test-casse
sed -i 's/"prix": 9/"prix": 10/' app/main.py
git commit -am "Test cassé (démonstration du ruleset, ne pas fusionner)" && git push -u origin test-casse
gh pr create --fill
```

## Ruleset (avant le TP 2)

**Settings → Rules → Rulesets → proteger-main → Enforcement status : Active → Save** (ou `gh api -X PUT repos/YaelGj/nova-demo/rulesets/$(gh api repos/YaelGj/nova-demo/rulesets --jq '.[0].id') -f enforcement=active`).
Ouvrir la pull request `test-casse` : **Merge** est bloqué (`gh pr merge test-casse --merge` est refusé).

## TP 3 (4 min) : Terraform et Ansible

```bash
cd infra
terraform init
terraform apply                                   # Plan: 4 to add ; yes
ansible-playbook -i inventaire.yaml site.yaml     # changed=1 sur vm-web-1 et vm-web-2
```

Ports 8081 (RECETTE) et 8082 (PRODUCTION). Puis `maintenance: true` pour `production` dans `inventaire.yaml`, relancer le playbook :
8082 affiche « Maintenance en cours ». Remettre `false`, relancer deux fois `terraform apply` et le playbook : « No changes. », `changed=0`.

## TP 4 partie 1 (3 min) : conteneuriser

Lire le `Dockerfile`. Décommenter le service `api` de `compose.yaml` (sélection, Ctrl+/), puis :

```bash
docker compose up -d
docker compose ps        # api : (healthy) après 10 à 20 s
```

Port 8000 : « Servie par un conteneur Docker ». Changer la phrase « Commande en ligne… » dans `app/main.py`, puis `docker compose up -d --build`.

## Chapitre 6 : Prometheus et Grafana sous charge

Décommenter les deux lignes « TP 4 » de `app/main.py`, puis :

```bash
docker compose up -d --build
./charge.sh              # environ 5 requêtes par seconde ; Ctrl+C, puis :
./charge.sh rush         # 60 s, 20 clients : la latence monte vers 0,5 s
```

Port 3000 (Grafana, lecture sans connexion) : tableau de bord « Nova ». Partage d'écran seulement, jamais de port public.

## TP 4 (4 min) : test rouge et panne

1. Test à trous : `5`, `5`, `422`, puis :
   ```bash
   git mv tests/quantite_a_trous.py tests/test_quantite.py
   pytest                   # 4 passed ; avec QUANTITE_MAX = 6 : 2 failed (lire le test rouge) ; remettre 4
   ```
2. Panne, avec `./charge.sh` dans un second terminal et le tableau de bord ouvert :
   ```bash
   docker compose stop api      # « API joignable » à 0 en 10 s environ ; charge.sh affiche 000
   docker compose start api     # retour à 1 en 5 s environ
   ```

## Chapitre 8 : déployer comme sur un cloud (6 min)

Dans `infra/main.tf`, `default = 2` devient `default = 3` (variable `nombre_vm`), puis :

```bash
terraform apply          # Plan: 1 to add, 0 to change, 0 to destroy ; port 8083
```

## Après la séance

```bash
cd infra && terraform destroy -auto-approve && cd .. && docker compose down
```

Remettre `main` dans l'état « avant » (sans réécrire l'historique) et désactiver le ruleset :

```bash
gh api -X PUT repos/YaelGj/nova-demo/rulesets/$(gh api repos/YaelGj/nova-demo/rulesets --jq '.[0].id') -f enforcement=disabled
gh pr close test-casse --delete-branch
git switch main && git pull
git restore --source="$(git log --format=%H -1 --grep="^Pipeline : ci.yml")^" --staged --worktree .
git commit -m "Retour à l'état avant" && git push
gh release delete v1.0.0 --cleanup-tag --yes
```

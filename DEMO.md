# Déroulé des démonstrations

> Cas fictif, exercice pédagogique.

Tout se lance dans le codespace du dépôt (dev container : Python 3.12, Docker, Terraform 1.17.1, ansible-core 2.21.6
et la collection community.docker 5.4.0, installés par `.devcontainer/post-create.sh`).

## Les branches

| Branche | Contenu | Sert à |
|---|---|---|
| `main` | Tout, sauf `.github/workflows/ci.yml` | Point de départ |
| `ajout-ci` | `main` + `ci.yml` | Démonstration « un cycle complet » : première pull request |
| `test-casse` | `ajout-ci` + un test cassé | Pull request laissée au rouge pour montrer la fusion bloquée par le ruleset |

Les deux branches reçoivent les mises à jour de `main` par fusion (`git merge main`), jamais par rebase :
leur historique déjà poussé ne change pas.

`livraison.yml` est déjà sur `main` : il ne réagit qu'aux tags `v*`, il ne gêne donc pas les pull requests,
et il est présent sur le commit qui recevra le tag `v1.0.0`.

## La veille

1. Pousser `main`, `ajout-ci` et `test-casse`. Ne pas poser de tag.
2. Ouvrir la pull request `test-casse` → `main` : `ci.yml` est sur la branche, le job `tests` démarre et passe au rouge.
   Ne jamais la fusionner.
3. Préparer le ruleset désactivé : à la main dans Settings → Rules → Rulesets, ou avec `ruleset.json` :
   `gh api --method POST repos/<compte>/nova-demo/rulesets --input ruleset.json`.
   Le check `tests` n'est proposé dans l'interface qu'après une première exécution du job (étape 2).
4. Créer le codespace et lancer une fois `terraform init` dans `infra/vm` et `infra/cloud`.

## Chapitre 2 — Décaler les contrôles à gauche (pip-audit)

`pip-audit` est dans `requirements.txt` : il est déjà installé dans le codespace.

```bash
pip-audit -r requirements.txt
echo $?        # 0 : aucune faille connue ; 1 : au moins une faille, à lire avec la classe
```

Au 5/11/2026 : `No known vulnerabilities found`, code de sortie 0 (environ 7 s).

## Démonstration « un cycle complet »

1. Pull request `ajout-ci` → `main` : vert, puis fusion **par un commit de fusion** (« Create a merge commit »).
   Avec « Squash and merge », la pull request `test-casse` montrerait de nouveau `ci.yml` dans ses fichiers modifiés.
2. En direct : `git switch main && git pull`, `git switch -c casse-en-direct`, casser l'assertion de
   `test_prix_total_unitaire`, pousser, ouvrir la pull request : rouge.
3. Lire le journal du job `tests`, corriger, pousser : vert. Commenter une ligne, fusionner.
4. `git switch main && git pull`, puis `git tag v1.0.0` et `git push origin v1.0.0` :
   le workflow `livraison` crée la release avec `CHANGELOG.md`.

## Ruleset (slide « Protéger main avec un ruleset »)

Activer le ruleset (Enforcement status : Active), puis ouvrir la pull request `test-casse` : la fusion est bloquée.

## Chapitre 4 — Terraform et Ansible (démonstration de 3 à 4 minutes)

Dossier `infra/vm` : une image « VM » (`vm/Dockerfile`, Python qui sert `/srv` sur le port 8000),
le réseau `nova` et deux « VM » publiées sur les ports 8081 et 8082.

Avant la séance (pas pendant les 4 minutes) :

```bash
cd infra/vm
terraform init
terraform apply        # yes : image nova-vm, réseau nova, vm-web-1 (8081), vm-web-2 (8082)
curl -s localhost:8081 # « Nova — machine en attente de configuration »
```

En direct :

1. Montrer `inventaire.yaml` (groupes `recette` et `production`), puis `group_vars/recette.yml` et
   `group_vars/production.yml`.
2. `ansible-playbook -i inventaire.yaml site.yaml` : `changed` sur les deux machines.
   Ouvrir les ports 8081 (bandeau RECETTE, orange) et 8082 (bandeau PRODUCTION, vert) dans l'onglet Ports.
3. Question à la classe, puis `maintenance: true` dans `group_vars/production.yml` et relancer :
   `changed` sur vm-web-2 seulement ; la page 8082 affiche « Maintenance en cours ».
4. Remettre `maintenance: false`, relancer (`changed` sur vm-web-2), puis relancer encore : `changed=0` partout.

Preuve d'idempotence : un second `terraform apply` affiche « No changes » ; un second passage du playbook,
`changed=0` (sorties copiées dans `exemples/idempotence-nova.md` du dépôt Kelvia).

Après la séance : `terraform destroy`.

## Chapitre 4 — Exercice « lisez le plan Terraform » (préparé, non montré)

Pour retrouver le plan de la slide à partir de `infra/vm` (dans une copie, pas dans le dépôt) :

1. Configuration « avant » : `main.tf` sans le bloc `web_2`. `terraform apply`.
2. Configuration « après » : `internal = true` dans `docker_network.nova` (force le remplacement),
   `restart = "unless-stopped"` dans `web_1` (modifiable en place), bloc `web_2` remis.
3. `terraform plan` : web_1 `updated in-place`, web_2 `created`, réseau nova `must be replaced`,
   « Plan: 2 to add, 1 to change, 1 to destroy. »
4. `terraform apply` échoue au bout de 30 s : le réseau, encore utilisé par vm-web-1, ne peut pas être détruit
   (`Error: timeout while waiting for state to become 'removed' (last state: 'pending', timeout: 30s)`).
   `terraform destroy` pour finir.

## Chapitre 8 — Déployer comme sur un cloud

```bash
cd infra/cloud
terraform init
terraform apply                       # image Nova construite (environ 2 min), 2 instances, répartiteur sur le port 8080
curl -si localhost:8080/commandes     # l'en-tête X-Instance change à chaque requête
terraform apply -var instances=3      # Plan: 2 to add, 0 to change, 1 to destroy (répartiteur remplacé)
terraform destroy -var instances=3
```

## Kubernetes (facultatif, en cas d'avance)

Testé dans le dev container (en local, pas dans un codespace) avec kind v0.33.0 et kubectl v1.37.0
(environ 0,8 Gio de mémoire pour le cluster).

```bash
mkdir -p ~/bin && cd ~/bin
curl -fsSLo kind https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64
curl -fsSLo kubectl https://dl.k8s.io/release/v1.37.0/bin/linux/amd64/kubectl
chmod +x kind kubectl && export PATH=~/bin:$PATH && cd -
kind create cluster --name nova
docker build -t nova:1.0 . && kind load docker-image nova:1.0 --name nova
kubectl apply -f k8s/
kubectl get pods                       # 3 pods
kubectl delete pod <un des pods>       # un nouveau pod le remplace
kubectl port-forward service/nova 8080:80    # puis, dans un autre terminal : curl localhost:8080/commandes
kind delete cluster --name nova
```

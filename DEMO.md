# Déroulé des démonstrations

> Cas fictif, exercice pédagogique.

## Les branches

| Branche | Contenu | Sert à |
|---|---|---|
| `main` | Tout, sauf `.github/workflows/ci.yml` | Point de départ |
| `ajout-ci` | `main` + `ci.yml` (un commit) | Démonstration « un cycle complet » : première pull request |
| `test-casse` | `ajout-ci` + un test cassé (un commit) | Pull request laissée au rouge pour montrer la fusion bloquée par le ruleset |

`livraison.yml` est déjà sur `main` : il ne réagit qu'aux tags `v*`, il ne gêne donc pas les pull requests,
et il est présent sur le commit qui recevra le tag `v1.0.0`.

## La veille

1. Pousser `main`, `ajout-ci` et `test-casse`. Ne pas poser de tag.
2. Ouvrir la pull request `test-casse` → `main` : `ci.yml` est sur la branche, le job `tests` démarre et passe au rouge.
   Ne jamais la fusionner.
3. Préparer le ruleset désactivé : à la main dans Settings → Rules → Rulesets, ou avec `ruleset.json` :
   `gh api --method POST repos/<compte>/nova-demo/rulesets --input ruleset.json`.
   Le check `tests` n'est proposé dans l'interface qu'après une première exécution du job (étape 2).

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

## Infrastructure (dans le codespace)

```bash
cd infra/vm
terraform init
terraform apply                                   # réseau nova, vm-web-1, vm-web-2
terraform apply                                   # second passage : aucun changement
ansible-playbook -i inventaire.yaml site.yaml     # deux fois : changed=0 au second passage
terraform destroy
```

```bash
cd infra/cloud
terraform init
terraform apply                       # image Nova construite, 2 instances, répartiteur sur le port 8080
curl -si localhost:8080/commandes     # l'en-tête X-Instance change à chaque requête
terraform apply -var instances=3      # 3 instances : seule la variable change
terraform destroy
```

## Kubernetes (facultatif, en cas d'avance)

Testé dans le dev container avec kind v0.33.0 et kubectl v1.37.0 (environ 0,8 Gio de mémoire pour le cluster).

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

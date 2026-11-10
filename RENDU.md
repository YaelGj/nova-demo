# RENDU — Nova

Binôme (TP 1) : ___ et ___
Remplacez seulement les `___` : une valeur lue à l'écran, ou un mot de la liste proposée.

## TP 1 — Diagnostic

Données de Nova (mars 2026) : 12 déploiements ; 3 annulés en urgence, rétablis en 1 h, 2 h et 6 h ; changements commités les 2, 4 et 9 mars, tous déployés le 12 mars ; 1 déploiement non planifié après une panne du paiement.

### 1. Métriques DORA

| Métrique | Calcul | Résultat |
|---|---|---|
| Deployment frequency | ___ déploiements sur ___ mois | ___ par mois |
| Change lead time moyen | (___ + ___ + ___) / 3 jours | ___ jours |
| Change fail rate | ___ / ___ | ___ % |
| Failed deployment recovery time moyen | (___ + ___ + ___) / 3 heures | ___ h |

### 2. Friction et enjeu métier (1 ligne)

Choisissez l'enjeu : délai, coût ou image auprès des clients.

| Friction (citation) | Enjeu métier |
|---|---|
| Karim (cuisine) : « On découvre les nouvelles recettes sur le site le jour même. » | ___ |

### 3. Rôles : un seul responsable par tâche (SysOps, DevOps ou DevSecOps)

| Tâche | Responsable |
|---|---|
| 1 Écrire les tests de l'API | ___ |
| 2 Mettre à jour le système des serveurs | ___ |
| 3 Analyser les dépendances vulnérables | ___ |
| 4 Écrire le pipeline d'intégration continue | ___ |
| 5 Sauvegarder la base de données | ___ |
| 6 Définir l'alerte de disponibilité | ___ |
| 7 Stocker le mot de passe de la base | ___ |
| 8 Revoir les droits d'accès à la production | ___ |

### 4. Un contrôle de sécurité décalé à gauche

Contrôle, au choix : analyse des dépendances (pip-audit), protection au push des secrets, tests dans le pipeline.
Moment, au choix : à chaque push, à chaque pull request, avant la mise en production.

| Contrôle | Moment du cycle |
|---|---|
| ___ | ___ |

## TP 4 — SLO (Service Level Objective)

### SLI

Latence de /commandes au 95e centile, lue sur le panneau « ___ ».
Valeur relevée sous `./charge.sh` : ___ s. Valeur relevée sous `./charge.sh rush` : ___ s.

### SLO

SLI sous ___ ms pendant ___ % du temps, sur 30 jours glissants.

### Error budget sur 30 jours

30 jours = 43 200 min.
___ % de 43 200 min = ___ min au-dessus de ___ ms.

### Quand le budget est épuisé

Au choix : on livre plus vite, on fige les nouveautés et on fiabilise, on baisse la cible.
L'équipe : ___

## TP 4 — Expérience de chaos
Remplissez « Avant l'expérience » avant d'arrêter quoi que ce soit.

### Avant l'expérience

**Steady state** : /commandes répond à environ ___ requêtes par seconde, latence au 95e centile sous ___ ms (panneaux « ___ » et « ___ »).

**Hypothèse** : si l'API s'arrête 2 minutes, la page devient ___ (disponible ou indisponible) et la panne est visible sur le tableau de bord en moins de ___ secondes.

**Variable** : `docker compose stop api` pendant 2 minutes, puis `docker compose start api`.

**Critère d'arrêt** : si la panne dure plus de ___ minutes, relancer l'API (`docker compose start api`).

### Après l'expérience

**Ce qui s'est passé** : la page est devenue ___ (disponible ou indisponible) ; les panneaux de trafic et de latence ont montré ___ (un trou ou des erreurs) ; « API joignable » est passé à ___.

**Délai de détection** : ___ secondes, sur le panneau « ___ ».

**Écart avec l'hypothèse** : hypothèse ___ (confirmée ou infirmée).

**Action d'amélioration**, au choix : une alerte sur « API joignable », une deuxième copie de l'API, les deux.
Votre choix : ___

# Mode compagnon : protocole expérimental 0.2, **candidat**

**25 octobre 2026. Statut : revue scientifique avant sélection du modèle, non gelé, non exécutable.**
Ce document complète la [charte](CHARTE_RECHERCHE.md) et la
[roadmap](ROADMAP.md) ; il ne remplace ni l'une ni l'autre.
Aucun modèle, moteur, paramètre machine, seuil QoS ou logiciel n'a été choisi,
installé, mesuré ou exécuté lors de cette revue.

## Question précise

Sur **un modèle imposé et une machine fixée**, un contrôleur compagnon
simple D génère-t-il plus de tokens *acceptés* qu'une allocation statique
conservatrice B pour **la même limite de gêne mesurée** ?

- **H0 (utile)** : l'avantage de D n'est pas démontré ou D viole le budget
  QoS ; la stratégie adaptative n'est pas acceptée.
- **H1 (candidat)** : D respecte toutes les contraintes et dépasse B sur
  des traces non utilisées pour fixer ses seuils, sous des conditions
  thermiques et de charge comparables.
- **H2 (falsificateur)** : le gain disparaît si on inclut la surveillance,
  le temps de migration, les pauses, les préfill et les caches froids.
- **H3 (falsificateur)** : les canaris synthétiques sont satisfaits mais la
  réactivité utilisateur réelle se dégrade. Un canari seul ne prouve donc
  pas l'absence de gêne.

L'objectif reste « modèles imposés », **pas** « le plus petit modèle qui
tient sur la machine ».

## Paramètres bloquants à fixer AVANT une mesure

| Élément | Valeur décidée | Effet si absent |
| --- | --- | --- |
| Modèle original, licence et SHA-256 | **non choisi** | Pas de référence ni de tokens acceptés |
| Tokenizer / oracle déterministe E1 | **non choisi** | Pas de comparaison fidèle |
| Moteur, backend et versions | **non choisis** | Pas d'équité de calcul |
| Prompts publics, contextes et limites de sortie | **non gelés** (exemple dans `lab/config/experiment.example.json`) | Risque d'améliorer artificiellement le débit |
| Budget utilisateur : canari p95/p99, délai de pause, réserve RAM/VRAM | **non calibré** | Aucun droit de faire tourner D/B/C en fond |
| Témoin de réactivité hors instrumentation | **non mesuré** | Surcharge de l'observateur inconnue |
| Durée et scénarios de charge | **non fixés** | Comparaison non reproductible |
| Critère de succès numérique (gain minimal, incertitude) | **non fixé** | Pas de conclusion positive |

Il est interdit de convertir silencieusement ces « non choisis » en
constantes opportunistes après avoir regardé les résultats. La
proposition devra être archivée et gelée *avant* d'ouvrir les traces de test.

## Ordre des expériences, chacune avec porte de sortie

### Prétest T0 : admissibilité

Lire le modèle et moteur seulement après sélection explicite ; enregistrer
les empreintes et la licence. Démontrer sur un corpus construit que E1
peut reproduire token par token le même résultat dans le même régime de
décodage. Si la référence est nondéterministe, la question E1 n'est **pas**
résolue. Ne pas passer implicitement à E2 sans nouvelle décision.

### T1 : l'instrumentation ne doit pas créer son propre résultat

Comparer **A0** poste sans observateur à **A1** poste avec observateur,
sans inférence. Rester non privilégié ; collecter *structure uniquement*
(timestamps monotones, usages agrégés CPU/mémoire, canaris), jamais
touches, titres de fenêtres, applications ni contenu de documents.
Publier cadence, coût CPU, variation de p95/p99 et incertitude. Si
l'instrumentation ajoute un retard au-delà du budget, **s'arrêter**
avant l'inférence.

### T2 : calibration sur traces d'entraînement de la politique uniquement

Utiliser une charge **synthétique** annoncée et répétable :
repos, burst CPU, concurrence mémoire, reprise d'activité, transitions
charge/alimentation. Éviter d'imposer un test de stress invasif pendant
l'utilisation réelle. Estimer une enveloppe de non-gêne et fixer les
seuils **sur calibration**, pas sur les essais de confirmation.
Définir réactions à compteur indisponible, canari manquant, pression
mémoire incertaine et sortie d'hibernation.

### T3 : comparaison A/B/C/D sur les mêmes traces réservées

- **A** : sans inférence, avec observateur identique à B/C/D.
- **B** : allocation statique prudente, baseline de valeur.
- **C** : allocation statique agressive, baseline de violations ; le but
  n'est pas de la « battre » en débit en l'autorisant à gêner le poste.
- **D** : règle adaptative + temporisation / hystérésis documentée.

Pour éviter de confondre politique et chauffe de la machine :
répétitions par blocs, **ordre croisé / alterné** (par exemple rotation
ABCD, BCDA, CDAB, DABC), température initiale déclarée, temps
d'échauffement et récupération identiques. La rotation exacte est une
proposition à figer ; pas un tirage déjà effectué.

Comparer les quatre sur les *mêmes* graines, modèles, prompts, batchs,
contextes, durées et traces. Séparer cold-start et régime soutenu ; ne
pas exclure les temps de chargement du seul bras D.

### T4 : validation externe

Essayer au moins un scénario de charge **non utilisé dans les réglages**
et, si possible, une session humaine explicitement consentie.
Un gain sur la trace réglée ne valide pas une adaptation générale.
Reporter séparément les pertes selon charge et horizon, y compris
les cas où D est pire que B.

## Tableau des observables

| Résultat | Mesure et unité | Quand il rend D invalide |
| --- | --- | --- |
| Tokens acceptés | entier E1, même limite de temps de mur | Divergence de tokens ou de contexte |
| Gêne | variation canari p95/p99 vs A, ms/% ; occurrences et durée de dépassement | Budget ex ante dépassé |
| Temps d'arrêt | latence entre événement de pression et baisse/arrêt, ms | Au-delà du seuil de sécurité |
| Débit | TTFT, prefill/s, decode/s ; cumulé et soutenu | Gains uniquement instantanés/échauffement |
| Pression | RAM/VRAM libres, pagination, charge, E/S | Réserve inférieure au seuil |
| Énergie | Wh / token accepté *si capteur autorisé et calibré* | Données absentes = « non mesuré », jamais zéro |
| Coût de contrôle | CPU, mémoire, temps de réveil, migration | Gain net effacé |
| Fidélité | equality E1 sur prompts et pauses/reprises | Toute différence non expliquée |

**Résultat principal :** D > B en tokens E1 validés **ET** absence de
violation QoS sous mêmes charges et budget. Choisir *avant l'essai*
le plus petit gain intéressant et la méthode d'incertitude.
Le non-respect d'une seule contrainte majeure donne « échec de sûreté »,
même si le débit est supérieur.

## Dépendances et biais scientifiques

- **Couplage caché** : faible CPU% ≠ absence de contention mémoire, I/O
  ou puissance. Si un capteur manque, ne pas conclure « 0 gêne ».
- **Biais de sélection** : calibrer puis tester sur la même trace fausse
  l'estimation du contrôleur D.
- **Effet observateur** : le canari consomme lui-même des ressources.
- **Trace rejouée ≠ humain** : même si l'ordre des charges est identique,
  la cadence d'ordonnancement et les délais système changent.
- **Pseudo-réplications** : 1000 mesures de latence contiguës ne
  représentent pas 1000 répétitions indépendantes ; analyser par bloc/run
  et sous-groupes de régime.
- **Risques d'abstention** : une règle trop prudente peut gagner sur QoS
  simplement en ne produisant presque rien. Publier *à la fois*
  throughput et QoS, pas un score composite seul.
- **Échantillon matériel** : une première mesure sur i5/GTX 1070 n'établit
  pas le fonctionnement sur boîtiers TV/GPU récents.

## Décisions de recherche *proposées*, non adoptées

1. Avant toute allocation active, mener T1 (A0/A1) et refuser l'essai si
   le coût de mesure excède le seuil calibré.
2. Aucun modèle ni moteur choisi par le seul auteur de cette revue.
3. D devra être comparé à B **à gêne égale**, pas seulement en débit brut.
4. Conserver les résultats nuls et les traces de violations comme preuves
   négatives, sous forme agrégée publique sans contenu utilisateur.
5. Le premier **observateur exécutable** attend la spécification 0.1
   complète conformément à `PROJECT_STATE.md` et `docs/ROADMAP.md`.

## Références de méthode

- MLPerf Inference, implémentations et règles d'expérimentation
  (analogie méthodologique, **ce laboratoire ne prétend pas être MLPerf**) :
  https://github.com/mlcommons/inference
- Charte interne du projet : [CHARTE_RECHERCHE.md](CHARTE_RECHERCHE.md).

## Condition de sortie de cette phase

Un contrat expérimental **rempli**, des contrôles « refus de démarrer »
testables, un protocole d'instrumentation avec surcharge bornée et un
modèle/moteur décidés par le propriétaire. Cette note est seulement le
pré-enregistrement candidat ; **aucun gain n'a été mesuré**.

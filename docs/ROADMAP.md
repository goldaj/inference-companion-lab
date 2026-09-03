# Feuille de route de recherche

Version : 0.1
Principe directeur : chaque phase répond à une question mesurable et possède un critère de passage.

## Vue d’ensemble

| Phase | Question centrale | Livrable principal |
|---|---|---|
| 0 — Spécification | Mesurons-nous bien le même problème ? | Contrat expérimental v0.1 |
| 1 — Observation | Pouvons-nous expliquer le poste et le modèle sans les perturber ? | Observateur passif et baselines |
| 2 — Compagnon statique | Pouvons-nous fonctionner en fond de façon sûre ? | Exécution limitée, pause/reprise |
| 3 — Slack dynamique | Une adaptation simple bat-elle une limite statique ? | Contrôleur à règles A/B/C/D |
| 4 — Portefeuille | Plusieurs plans améliorent-ils le résultat cumulé ? | Plans validés et migrations |
| 5 — Dérivés exacts | La spécialisation locale apporte-t-elle un gain net ? | Cache compilé exact |
| 6 — Hétérogénéité | Plusieurs unités peuvent-elles contribuer positivement ? | Plan CPU/GPU/iGPU/NPU mesuré |
| 7 — Généralisation | L’abstraction survit-elle à d’autres machines et modèles ? | Graphe de capacités et adaptateurs |
| 8 — Recherche avancée | Quelles innovations dépassent les baselines établies ? | Kernels, certification, spéculation, thermique |

## Phase 0 — Spécification scientifique

### Objectif

Empêcher les faux gains et rendre l’expérience initiale reproductible.

### Sous-étapes

#### 0.1 Identifier le modèle

- chemin de l’original ;
- empreinte SHA-256 ;
- architecture ;
- tokenizer ;
- configuration ;
- licence et provenance ;
- espace disque ;
- code personnalisé éventuel.

#### 0.2 Choisir la référence

- moteur ;
- version ;
- backend ;
- commande ;
- paramètres ;
- raison du choix ;
- test de correction minimal.

#### 0.3 Définir E1

- génération déterministe ;
- seed ;
- température et sampling ;
- séquence de référence ;
- comparaison de tokens ;
- comportement après pause/reprise.

#### 0.4 Définir la charge

- batch 1 ;
- prompts publiés ;
- longueurs de contexte ;
- longueur de génération ;
- cache froid et chaud ;
- répétitions ;
- ordre des essais.

#### 0.5 Définir la qualité de service

- canari CPU ;
- pression mémoire ;
- pagination ;
- température ;
- première réserve RAM ;
- première politique de batterie ;
- valeur ou règle de tolérance \(\varepsilon\).

#### 0.6 Définir la conservation

- emplacement des traces ;
- durée de conservation ;
- données sensibles interdites ;
- taille maximale ;
- export des synthèses.

### Critère de passage

Une personne extérieure peut reproduire la baseline sans poser de question implicite et peut détecter un candidat qui triche sur la charge ou la fidélité.

## Phase 1 — Observateur passif

### Objectif

Mesurer sans contrôler ni modifier le poste.

### Sous-étapes

#### 1.1 Inventaire statique

- OS ;
- CPU et topologie ;
- RAM ;
- GPU/VRAM ;
- stockage ;
- pilotes ;
- profils d’alimentation ;
- capteurs ;
- capacités de télémétrie.

#### 1.2 Mesures actives légères

- surcharge de l’observateur ;
- latence de planification ;
- mémoire disponible et pression ;
- fréquence et température ;
- débit du moteur ;
- utilisation GPU si applicable.

#### 1.3 Canaris

- canari de réveil CPU ;
- canari mémoire ;
- canari GPU reporté à une sous-phase ultérieure si nécessaire ;
- métriques p50/p95/p99 ;
- calibration sans inférence.

#### 1.4 Baseline A

Mesurer le poste sans inférence sur la trace de charge.

#### 1.5 Baselines B et C

- B : limite statique conservatrice ;
- C : limite statique agressive.

#### 1.6 Modèle de données

- événement horodaté ;
- snapshot de ressources ;
- échantillon de débit ;
- événement utilisateur non sensible ;
- violation ;
- pause ;
- phase thermique.

### Critère de passage

- surcharge de l’observateur connue et acceptable ;
- mesures reproductibles ;
- A, B et C clairement différenciés ;
- aucun changement persistant ;
- aucune donnée personnelle capturée.

## Phase 2 — Compagnon statique sûr

### Objectif

Faire tourner le modèle en fond sous une enveloppe fixe, avec pause et reprise sûres.

### Sous-étapes

#### 2.1 Contrôle de charge

- priorité basse ;
- limite de workers ;
- affinité si exposée sans privilège ;
- intervalle d’échantillonnage ;
- pas de boucle active inutile.

#### 2.2 Garde mémoire

- réserve fixe ;
- seuil de pression ;
- détection de pagination ;
- interdiction d’augmenter l’engagement au-delà du plan ;
- arrêt propre avant effondrement.

#### 2.3 Pause et reprise

- frontière entre tokens ;
- état du tokenizer ;
- état du sampler ;
- seed ;
- cache KV ;
- comparaison E1 avant/après ;
- répétition de nombreux cycles.

#### 2.4 Surveillance prolongée

- fuite mémoire ;
- évolution thermique ;
- stabilité ;
- dérive des canaris ;
- récupération après arrêt du moteur.

### Critère de passage

Fonctionnement prolongé sans divergence, fuite, violation durable du budget ou modification persistante.

## Phase 3 — Estimation dynamique du slack

### Objectif

Démontrer la valeur du contrôle adaptatif.

### Sous-étapes

#### 3.1 Signaux rapides

- événement d’entrée récent sans contenu ;
- retard du canari ;
- pression mémoire ;
- charge CPU ;
- température ;
- état secteur/batterie.

#### 3.2 Enveloppe conservatrice

Produire un budget de ressources et un niveau de confiance.

#### 3.3 Politique à règles

- augmenter lentement ;
- réduire rapidement ;
- conserver une réserve ;
- suspendre en cas d’incertitude ;
- ne pas apprendre avant d’avoir une baseline stable.

#### 3.4 Hystérésis

- seuils d’entrée et de sortie distincts ;
- temporisation après activité ;
- durée minimale d’un état ;
- fréquence maximale de changement.

#### 3.5 Repli

- plan minimal ;
- pause ;
- détection de télémétrie incohérente ;
- journal de la cause.

#### 3.6 Expérience A/B/C/D

Appliquer la même trace à :

- A : aucune inférence ;
- B : compagnon statique conservateur ;
- C : compagnon statique agressif ;
- D : compagnon adaptatif à règles.

### Critère de passage

D produit plus de tokens conformes que B à budget de gêne équivalent et évite les violations significatives de C.

### Critère de reformulation

Si D ne gagne pas, mesurer séparément la surcharge de surveillance, le coût des transitions et la qualité de l’estimation. Ne pas ajouter d’apprentissage pour masquer l’échec.

## Phase 4 — Portefeuille de plans

### Objectif

Remplacer les simples quotas par des plans validés adaptés à différentes enveloppes.

### Sous-étapes

#### 4.1 Définir le manifeste de plan

- exigences ;
- plage de contexte ;
- débit ;
- impact ;
- température ;
- fidélité ;
- coût d’activation ;
- coût de sortie ;
- transitions compatibles.

#### 4.2 Construire une petite grille

- pause ;
- CPU minimal ;
- CPU discret ;
- CPU disponible ;
- accélérateur discret ;
- accélérateur disponible.

#### 4.3 Profiler et éliminer

- répétitions ;
- plans dominés ;
- stabilité ;
- conditions d’invalidation.

#### 4.4 Modéliser les migrations

- poids ;
- buffers ;
- cache KV ;
- état aléatoire ;
- durée d’amortissement ;
- retour arrière.

#### 4.5 Sélecteur en ligne

- enveloppe ;
- prédiction de durée ;
- coût de migration ;
- hystérésis ;
- surveillance du gain réel.

### Critère de passage

Le portefeuille produit plus de tokens conformes qu’un unique plan moyen sur plusieurs traces, à qualité de service égale.

## Phase 5 — Artefacts dérivés exacts

### Objectif

Exploiter la connaissance du modèle et de la machine sans modifier l’original ni le contrat E1.

### Sous-étapes

#### 5.1 Cache adressé par contenu

- empreinte modèle ;
- matériel ;
- pilote ;
- compilateur ;
- transformations ;
- fidélité.

#### 5.2 Transformations exactes

- transposition ;
- réordonnancement ;
- alignement ;
- empaquetage ;
- indices ;
- constantes ;
- compression sans perte.

#### 5.3 Autotuning hors ligne

- tailles de tuiles ;
- layouts ;
- préchargement ;
- fusion ;
- nombre de threads ;
- spécialisations de forme.

#### 5.4 Vérification

- opérateurs ;
- logits lorsque possible ;
- séquences E1 ;
- contexte ;
- pause/reprise ;
- transitions.

#### 5.5 Gestion d’espace

- quota ;
- artefacts obsolètes ;
- suppression limitée au cache du projet ;
- original protégé.

### Critère de passage

Gain de bout en bout au-delà de la variance et du coût amorti, sans divergence E1.

## Phase 6 — Hétérogénéité

### Objectif

Utiliser plusieurs unités seulement lorsqu’elles améliorent réellement le résultat.

### Sous-étapes

- ajouter un appareil à la fois ;
- mesurer calcul, transfert et contention ;
- tester appareil unique contre combinaison ;
- distinguer préfill et décodage ;
- tester rôles entiers avant découpage fin ;
- intégrer VRAM, RAM, bus et thermique ;
- construire un repli si le périphérique est repris par l’utilisateur.

### Critère de passage

La combinaison bat le meilleur appareil unique, transferts et gêne inclus.

## Phase 7 — Généralisation

### Objectif

Transformer la démonstration locale en architecture multi-machine et multi-modèle.

### Sous-étapes

- graphe de capacités ;
- API d’adaptateur OS ;
- API de backend ;
- IR extensible ;
- repli correct pour opérateurs inconnus ;
- base de résultats ;
- transfert d’apprentissage entre machines ;
- validation sur plusieurs classes matérielles.

### Critère de passage

Le système retrouve automatiquement une configuration proche du meilleur plan validé sur des machines nouvelles, sans règle dédiée à leur nom commercial.

## Phase 8 — Recherche à haut risque

Axes autorisés après baselines :

- calcul progressif certifié ;
- spéculation hétérogène ;
- compression sans perte fusionnée ;
- structure exacte ;
- kernels générés ;
- superoptimisation formelle locale ;
- contrôle thermique prédictif ;
- exécution hors mémoire ;
- service privilégié minimal ;
- environnement amorçable si l’OS est mesuré comme goulot.

Chaque axe doit définir : mécanisme, gain attendu, coût, contrat de fidélité, risque et expérience de falsification.

## Première tâche concrète après la documentation

Compléter `lab/config/experiment.example.json` pour le premier modèle et produire une version locale validée de cette configuration. Aucun code de contrôle ne doit précéder cette décision.

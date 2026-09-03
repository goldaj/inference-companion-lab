# Rapport fondateur — Superoptimiseur d’inférence intégrale

Version : 0.1
Date : 2026-09-03
Langue de référence : français
Statut : document de fondation, destiné à être transmis et exporté
Mode prioritaire : compagnon non destructif

---

## Résumé exécutif

Le projet vise à créer un système logiciel capable de recevoir un modèle d’intelligence artificielle choisi par l’utilisateur, d’analyser ce modèle et la machine locale, puis de produire l’exécution correcte la plus rapide qu’il sait découvrir sur le matériel existant.

Le système ne doit pas résoudre le problème en proposant un modèle plus petit. Le modèle cible est imposé. Si ce modèle est très lent sur la machine, le rôle du système consiste à extraire le meilleur débit réellement accessible, même si celui-ci reste faible.

La vision initiale évoquait une machine virtuelle exploitant tout le poste, jusqu’au moindre composant, à l’énergie et à la physique du silicium. Cette intuition contient un noyau valide, mais plusieurs formulations littérales ont été corrigées :

- une VM conventionnelle masque souvent le matériel ; le bon objet est un hyper-runtime portable en surface mais spécialisé en profondeur ;
- utiliser tout le matériel ne signifie pas faire travailler chaque composant, car certaines ressources créent davantage de contention qu’elles n’apportent de calcul ;
- un logiciel ne peut piloter que les degrés de liberté exposés par une instruction, un pilote, un firmware, un registre, un capteur ou un actionneur ;
- les privilèges administrateur ne rendent pas accessibles les transistors, les fusibles ou les unités à fonction fixe ;
- un optimum absolu parmi tous les programmes imaginables ne peut généralement pas être prouvé ; le résultat honnête est le meilleur plan validé trouvé, accompagné d’une borne conditionnelle et de l’espace exploré ;
- toute transformation doit préciser le niveau de fidélité conservé ;
- la sûreté, la réversibilité et la non-corruption font partie des contraintes de l’optimisation et ne sont pas des options.

Le projet commencera par le **mode compagnon**. Dans ce mode, l’utilisateur continue à employer son poste. Le système emprunte seulement la marge de ressources disponible sans dépasser un budget de gêne explicite. Il ralentit, migre ou se suspend lorsque l’utilisateur réclame ces ressources.

Le premier résultat scientifique attendu n’est pas un nouveau kernel. Il consiste à démontrer qu’un contrôleur adaptatif produit plus de tokens validés qu’une configuration statique conservatrice, sur une même trace d’activité, sans augmenter la gêne pour l’utilisateur.

Le premier programme sera donc un observateur passif. Il mesurera le modèle, le poste et des canaris de réactivité. Aucun droit administrateur, aucune suppression, aucune modification persistante et aucune transformation du modèle ne sont nécessaires pour ce premier jalon.

---

## 1. Contexte et origine du besoin

Le point de départ est un besoin pratique : faire fonctionner des modèles locaux sur des postes personnels, parfois anciens ou limités, en exploitant beaucoup mieux le matériel disponible.

La question initiale ne portait toutefois pas seulement sur un lanceur de modèles ou un moteur optimisé. Elle visait un système beaucoup plus général :

1. l’utilisateur choisit librement le modèle ;
2. le système reçoit la machine telle qu’elle existe ;
3. il analyse le graphe du modèle, les poids, la mémoire, les unités de calcul et l’état du poste ;
4. il synthétise ou sélectionne l’exécution la plus performante ;
5. il peut agir à travers les couches logicielles accessibles, jusqu’aux interfaces matérielles exposées ;
6. il mesure, apprend et adapte son plan ;
7. il ne dépend pas d’une configuration matérielle unique ;
8. il produit des résultats localement et respecte le modèle imposé.

Le projet se situe donc à l’intersection de plusieurs domaines :

- compilateurs et représentations intermédiaires ;
- kernels CPU, GPU et accélérateurs ;
- systèmes d’exploitation et planification ;
- inférence de réseaux neuronaux ;
- hiérarchies mémoire et interconnexions ;
- contrôle thermique et énergétique ;
- optimisation en ligne et autotuning ;
- vérification numérique ;
- sécurité système ;
- mesure expérimentale et reproductibilité.

Le nom descriptif retenu pour le moment est **superoptimiseur d’inférence intégrale**. L’expression **hyper-runtime d’inférence réflexif** décrit également bien l’objet : le runtime observe la machine sur laquelle il s’exécute, produit plusieurs variantes de lui-même et choisit selon les résultats mesurés.

---

## 2. Vision ultime

### 2.1 Formulation générale

Pour un modèle imposé, une machine imposée, une charge de travail, un contrat de fidélité et des contraintes de sûreté, le système doit découvrir automatiquement le programme d’inférence correct, stable et réversible qui maximise le débit soutenu de tokens acceptés parmi les ressources programmables accessibles.

Le résultat doit contenir :

- le meilleur plan trouvé ;
- le débit observé ;
- les conditions exactes de la mesure ;
- la variance et l’intervalle de confiance ;
- le goulot identifié ;
- la consommation de mémoire ;
- l’état thermique et électrique ;
- la fidélité vérifiée ;
- une borne supérieure conditionnelle ;
- l’écart à cette borne ;
- la description de l’espace de transformations exploré ;
- les expériences négatives pertinentes.

### 2.2 Ce que signifie « indépendant de la machine »

Le modèle et son contrat doivent être portables. Le programme d’exécution optimal ne le sera pas.

```text
Modèle et sémantique portables
             │
             ▼
      IR d’inférence commune
             │
             ▼
Analyse du poste et microbenchmarks
             │
             ▼
  Compilation et placement locaux
             │
             ▼
Artefacts propres au modèle, au CPU,
au GPU, au pilote et à l’état du poste
```

Une unique implémentation binaire optimale partout serait contradictoire avec l’objectif. Le même modèle doit produire des programmes différents selon :

- les instructions CPU ;
- la taille des caches ;
- la topologie mémoire ;
- la présence d’un GPU, iGPU ou NPU ;
- les formats numériques efficaces ;
- la bande passante des interconnexions ;
- le pilote ;
- la température et la puissance soutenable.

### 2.3 Ce que « tout le matériel » doit signifier

Le système doit **considérer** toutes les ressources observables et programmables. Il ne doit pas obligatoirement les activer.

Un composant est candidat seulement si le système peut :

1. configurer son état ;
2. lui transmettre des données ;
3. déclencher une opération pertinente ;
4. récupérer un résultat ;
5. le faire avec un coût inférieur au bénéfice.

Le CPU, l’iGPU et le GPU peuvent se disputer la RAM, le bus ou le budget thermique. Un NPU peut exiger des conversions trop coûteuses. Un moteur vidéo peut être non programmable. L’optimum peut laisser plusieurs unités inactives.

La règle correcte est donc :

> Utiliser toute ressource dont la contribution marginale nette réduit le chemin critique, et laisser les autres au repos.

### 2.4 Limite de la physique accessible

Les performances dépendent effectivement de phénomènes physiques :

- tension ;
- fréquence ;
- température ;
- bruit ;
- erreurs ;
- qualité de l’exemplaire de silicium ;
- refroidissement ;
- limites de courant et de puissance ;
- propagation des signaux ;
- vieillissement.

Mais un logiciel ne peut agir que sur ce que le matériel expose. La présence d’un degré de liberté physique ne crée pas automatiquement une interface informatique. Les atomes, transistors, registres cachés, fusibles, firmwares signés et blocs fixes ne sont pas des ressources programmables du seul fait qu’ils existent.

L’ambition réaliste est d’intégrer la physique dans une boucle de mesure et de contrôle :

```text
plan proposé
     ↓
exécution mesurée
     ↓
débit + compteurs + température + puissance + erreurs
     ↓
mise à jour du modèle de coût
     ↓
nouveau plan
```

Une nouvelle théorie physique ne créera pas une porte logique absente sur un processeur existant. En revanche, un nouveau langage intermédiaire, un kernel, un ordonnancement ou une représentation des données peut exploiter beaucoup mieux les mécanismes déjà présents.

---

## 3. Objectifs finaux

### 3.1 Mission principale

Construire un système général capable de maximiser l’inférence d’un modèle imposé sur une machine imposée, sous un contrat de fidélité et de sûreté explicite.

### 3.2 Objectif de portabilité

Fournir une couche d’entrée commune pour plusieurs modèles et plusieurs plateformes, tout en produisant une exécution locale spécialisée.

### 3.3 Objectif de connaissance de la machine

Construire un graphe mesuré du substrat :

- cœurs et topologie ;
- caches et TLB ;
- NUMA ;
- RAM et bande passante ;
- GPU, iGPU, NPU et VRAM ;
- moteurs de copie ;
- bus et synchronisations ;
- stockage ;
- capteurs ;
- domaines de puissance ;
- limites thermiques ;
- interférences entre ressources.

### 3.4 Objectif de compréhension du modèle

Extraire :

- graphe d’opérations ;
- formes et types ;
- durées de vie ;
- constantes ;
- attention et cache KV ;
- structures sparse ou MoE ;
- répétitions exactes ;
- possibilités de fusion ;
- intensité arithmétique ;
- trafic mémoire ;
- chemins critiques ;
- dimensions dynamiques.

### 3.5 Objectif de compilation

Créer une IR multi-niveaux et une fabrique de kernels permettant :

- réécriture algébrique ;
- spécialisation par forme ;
- spécialisation par poids ;
- tuilage ;
- vectorisation ;
- préchargement ;
- fusion ;
- layouts dédiés ;
- génération CPU/GPU ;
- partition et placement hétérogènes ;
- multiversion selon le contexte et l’enveloppe de ressources.

### 3.6 Objectif d’autotuning

Combiner modèles analytiques et expériences réelles afin de rechercher :

- backends ;
- kernels ;
- nombre de threads ;
- affinités ;
- dispositions ;
- placements ;
- tailles de blocs ;
- stratégies de transfert ;
- plans thermiques ;
- politiques de pause et de migration.

### 3.7 Objectif de vérification

Empêcher les faux gains en vérifiant :

- exactitude des opérateurs ;
- logits ou tokens selon le contrat ;
- distribution de sortie si nécessaire ;
- pause et reprise ;
- migration de cache ;
- stabilité prolongée ;
- absence de corruption silencieuse.

### 3.8 Objectif de preuve et de bornage

Publier non seulement le débit mesuré, mais une estimation rationnelle du plafond restant.

Une borne conditionnelle peut prendre la forme :

\[
\mathrm{TPS}
\leq
\min\left(
\frac{\Pi_{\mathrm{utile}}}{F_{\mathrm{tok}}},
\min_\ell\frac{\beta_\ell}{D_{\ell,\mathrm{tok}}},
\frac{1}{L_{\mathrm{crit}}},
\frac{P_{\mathrm{soutenable}}}{E_{\mathrm{tok}}}
\right)
\]

avec :

- \(\Pi_{\mathrm{utile}}\) : calcul réellement exploitable ;
- \(F_{\mathrm{tok}}\) : opérations minimales par token sous les hypothèses ;
- \(\beta_\ell\) : bande passante mesurée d’un niveau ou lien ;
- \(D_{\ell,\mathrm{tok}}\) : octets minimaux traversant ce lien ;
- \(L_{\mathrm{crit}}\) : latence minimale du chemin séquentiel ;
- \(P_{\mathrm{soutenable}}\) : puissance soutenable ;
- \(E_{\mathrm{tok}}\) : énergie minimale par token dans la classe considérée.

Cette borne doit toujours indiquer ses hypothèses. Elle ne prétend pas exclure une innovation algorithmique future.

### 3.9 Objectifs de déploiement à long terme

Trois modes sont envisagés :

1. **compagnon** — non destructif, utilisateur prioritaire ;
2. **exclusif temporaire** — ressources temporairement réservées, puis état restauré ;
3. **appliance dédié** — environnement minimal amorçable pour un poste consacré à l’inférence.

Le présent programme commence exclusivement par le premier.

---

## 4. Non-objectifs et exclusions actuelles

Le premier jalon ne cherche pas à :

- choisir un autre modèle ;
- quantifier ou élaguer le modèle ;
- écrire un nouveau noyau OS ;
- écrire des pilotes matériels ;
- désactiver des services ;
- demander les droits administrateur ;
- contrôler tensions ou fréquences ;
- modifier le BIOS ou le firmware ;
- exploiter des vulnérabilités ;
- supprimer des fichiers ;
- formater le poste ;
- prendre en charge toutes les plateformes ;
- garantir un optimum physique absolu ;
- entraîner un contrôleur neuronal ;
- battre immédiatement tous les engines existants.

Ces exclusions permettent d’isoler la première hypothèse de recherche : la valeur d’une adaptation opportuniste et non intrusive.

---

## 5. Contrat du modèle

### 5.1 Invariant

Le modèle original est immuable et identifié par empreinte cryptographique. Le tokenizer, la configuration et les éventuels composants multimodaux doivent être identifiés avec lui.

### 5.2 Catégories de transformation

#### Niveau 0 — Runtime seulement

- threads ;
- affinités ;
- backend ;
- placement ;
- allocations ;
- buffers ;
- préchargement ;
- ordonnancement ;
- cache ;
- pause et reprise.

#### Niveau 1 — Artefacts dérivés exacts

- transposition ;
- réordonnancement ;
- alignement ;
- empaquetage ;
- indices précalculés ;
- constantes précalculées ;
- layouts par appareil ;
- compression sans perte ;
- kernels spécialisés.

Le modèle original reste la référence. Les dérivés sont du cache compilé et peuvent être reconstruits.

#### Niveau 2 — Transformations sous contrat numérique

- réassociation flottante ;
- précision réduite ;
- cache KV compressé ;
- calcul progressif ;
- approximation certifiée ;
- spéculation vérifiée.

#### Niveau 3 — Modification réelle

- quantification permanente ;
- pruning ;
- factorisation approximative ;
- distillation ;
- modification des couches ;
- entraînement.

Interdit par défaut dans le projet tel qu’il est actuellement défini.

### 5.3 Niveaux de fidélité

- **E0** — valeurs de référence bit à bit ;
- **E1** — mêmes tokens avec décodage déterministe ;
- **E2** — même distribution dans une tolérance définie ;
- **E3** — qualité comportementale équivalente dans une tolérance définie.

Le premier prototype devrait employer E1. E0 limiterait trop vite la comparaison entre matériels ; E3 serait trop permissif pour une première démonstration.

---

## 6. Définition du mode compagnon

### 6.1 Principe

Le compagnon utilise seulement la marge que le poste peut prêter sans dépasser une qualité de service définie pour l’utilisateur.

Cette marge est appelée **slack**. Elle ne correspond pas à « 100 % moins le pourcentage affiché dans le gestionnaire de tâches ».

Elle comprend :

- calcul CPU ;
- capacité RAM ;
- bande passante RAM ;
- capacité et temps GPU ;
- VRAM ;
- E/S ;
- énergie ;
- marge thermique ;
- tolérance à la latence ;
- probabilité que l’utilisateur reprenne bientôt la ressource.

### 6.2 Objectif formel

Sur une période \([0,T]\), maximiser :

\[
N_{\mathrm{tokens\ conformes}}(0,T)
\]

sous les contraintes :

- dégradation de la qualité de service inférieure au budget ;
- fidélité au modèle ;
- sûreté ;
- capacité mémoire ;
- réversibilité ;
- absence de modification permanente.

### 6.3 Pourquoi un débit instantané ne suffit pas

Le poste change d’état. Un plan très rapide pendant une minute peut créer une migration coûteuse, chauffer la machine ou provoquer une pagination qui réduit ensuite le résultat cumulé.

Le compagnon doit optimiser le nombre total de tokens validés sur une trace d’utilisation représentative.

### 6.4 L’utilisateur reste prioritaire

Lorsque la marge disparaît, le système doit pouvoir :

- réduire le nombre de workers ;
- diminuer son quota ;
- arrêter de lancer de nouveaux kernels ;
- migrer si le coût est justifié ;
- libérer des buffers ;
- suspendre l’inférence ;
- reprendre plus tard avec le même état logique.

Le maintien artificiel d’un débit non nul n’est pas prioritaire face à la stabilité du poste.

### 6.5 État avant et après

Le système doit restaurer le même état logique et de configuration :

- aucun fichier utilisateur supprimé ;
- aucun programme désinstallé ;
- réglages temporaires restaurés ;
- services inchangés dans le premier mode ;
- caches du projet identifiés ;
- modèle original intact ;
- journal des actions ;
- reprise sûre après crash.

Un état physique parfaitement identique est impossible : l’exécution consomme de l’énergie, produit de la chaleur et occasionne une usure infinitésimale. Le contrat porte sur l’état fonctionnel et logiciel.

---

## 7. Limites fondamentales

### 7.1 Ensemble de travail minimal

Le modèle impose des poids, buffers et états. Si la marge disponible tombe sous le minimum, l’inférence doit employer une mémoire plus lente ou se suspendre.

### 7.2 Bande passante et dépendances

Le décodage token par token comporte un chemin séquentiel. Les poids, activations et caches doivent traverser des hiérarchies de mémoire finies. Aucune priorité de processus ne crée de bande passante supplémentaire.

### 7.3 Préemption imparfaite

Le CPU est relativement flexible. Le GPU et certains accélérateurs peuvent avoir des kernels longs, une préemption contrôlée par le pilote et de gros états résidents.

### 7.4 Migration coûteuse

Changer de plan peut exiger transfert des poids, conversion des layouts, déplacement du cache KV et reconstruction des buffers. Un gain potentiel doit amortir ce coût.

### 7.5 Ressources partagées

Une unité inactive peut néanmoins partager la RAM, le cache, le bus, la puissance ou le refroidissement avec une activité utilisateur.

### 7.6 Observation incomplète

Les compteurs disponibles varient et certaines ressources ne sont pas directement mesurables. Le système doit intégrer l’incertitude.

### 7.7 Futur imprévisible

L’utilisateur peut réclamer une ressource sans préavis. Le système ne peut fournir qu’une estimation et un mécanisme de retrait.

### 7.8 Optimum absolu non démontrable

L’espace des programmes, placements et transformations est gigantesque. Pour du code arbitraire, l’équivalence de programmes est indécidable dans le cas général. La promesse doit rester conditionnelle à un espace défini.

### 7.9 Hétérogénéité des plateformes

Les APIs de télémétrie, de priorité, de GPU et de puissance diffèrent fortement. Une abstraction commune devra prévoir des capacités absentes et des replis conservateurs.

---

## 8. Problèmes scientifiques et techniques à résoudre

### 8.1 Mesure non perturbatrice

La télémétrie doit être suffisamment légère pour ne pas fausser le système qu’elle observe.

### 8.2 Définition de la gêne

« L’utilisateur ne remarque rien » doit être transformé en indicateurs :

- latence de planification ;
- réactivité d’un canari CPU ;
- file GPU ou rendu canari ;
- pression mémoire ;
- fautes de page ;
- latence E/S ;
- température ;
- bruit ou puissance si mesurables.

### 8.3 Estimation du slack

Le système doit estimer une enveloppe multidimensionnelle et non un simple pourcentage d’utilisation.

### 8.4 Contrôle sûr

Une politique déterministe conservatrice doit toujours dominer l’apprentissage en matière de sécurité : retrait rapide, seuils, réserves, hystérésis et mode de secours.

### 8.5 Préemption et reprise

La première version suspendra entre tokens. Les points plus fins ne viendront qu’après preuve de nécessité.

### 8.6 Gestion d’état

Le runtime doit distinguer poids, buffers, cache KV, tokenizer, sampler, générateur aléatoire et historique de conversation.

### 8.7 Portefeuille de plans

Au lieu d’un plan unique, le système doit conserver des variantes pour plusieurs enveloppes : CPU discret, CPU agressif, GPU partiel, GPU complet, thermique limité, etc.

### 8.8 Coût de changement

Un plan ne doit être activé que si le gain futur probable dépasse son coût d’activation et de sortie.

### 8.9 Vérification des transitions

Deux plans corrects isolément peuvent diverger lorsqu’un cache est transféré entre eux. Les transitions sont des objets de test à part entière.

### 8.10 Autotuning sans gêne

Les campagnes lourdes doivent être réservées aux périodes libres. Le runtime actif choisit parmi des plans déjà validés.

### 8.11 Gestion du stockage

Les modèles et dérivés sont volumineux. Le cache doit être limité, indexé et nettoyable sans jamais toucher aux fichiers utilisateur.

### 8.12 Sécurité des entrées

Un modèle, un tokenizer ou un opérateur personnalisé peut être malformé ou hostile. Le parseur ne doit pas disposer des privilèges de contrôle du poste.

---

## 9. Architecture conceptuelle

```text
Modèle imposé + tokenizer + contrat de fidélité + charge
                           │
                           ▼
              Inspecteur et IR sémantique
                           │
                           ▼
          Graphe matériel et thermique mesuré
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      Générateur de plans       Référence de correction
              │                         │
              └────────────┬────────────┘
                           ▼
                Validateur de candidats
                           │
                           ▼
               Portefeuille de plans sûrs
                           │
                           ▼
Télémétrie ─► estimateur de slack ─► sélecteur de plan
    ▲                                      │
    │                                      ▼
    └──── runtime préemptible + gestionnaire d’état
                           │
                           ▼
           tokens conformes + preuves + mesures
```

### 9.1 Descripteur du modèle

Objet canonique décrivant le calcul et les invariants, sans confondre format de stockage et sémantique.

### 9.2 Descripteur de machine

Graphe de ressources construit par inventaire et microbenchmarks, avec coûts de calcul, de transfert, de contention et de changement d’état.

### 9.3 IR multi-niveaux

1. IR sémantique ;
2. IR algébrique tensorielle ;
3. IR de placement et de mémoire ;
4. IR de kernel et de machine ;
5. plan d’exécution figé et vérifié.

### 9.4 Fabrique de kernels

Réutiliser d’abord les meilleurs kernels accessibles, puis générer des variantes lorsque le profilage identifie un goulot réel.

### 9.5 Planificateur hétérogène

Placer une opération, une tête, une tuile, un expert, un cache ou une phase entière sur la ressource appropriée, avec transferts et synchronisations inclus dans le coût.

### 9.6 Gestionnaire de mémoire

Planifier allocations, durées de vie, pages, buffers épinglés, layouts, caches, transferts et éventuellement stockage comme dernier niveau.

### 9.7 Autotuner hiérarchique

Élimination analytique, microbenchmarks, sélection par sous-graphe, composition, mesure de bout en bout, validation thermique et adaptation en ligne.

### 9.8 Superviseur de sûreté

Composant indépendant qui impose les limites de température, de puissance, de mémoire, de privilèges et de restauration. L’optimiseur ne peut pas le désactiver pour augmenter son score.

---

## 10. Architecture temporelle du mode compagnon

### Boucle rapide

Ordre de grandeur : millisecondes à fractions de seconde.

- détecter une activité ;
- ne plus lancer de travail long ;
- réduire un quota ;
- céder les cœurs ;
- protéger une réserve ;
- déclencher une pause.

### Boucle intermédiaire

Ordre de grandeur : secondes à minutes.

- choisir un plan ;
- estimer une durée de disponibilité ;
- décider d’une migration ;
- appliquer l’hystérésis ;
- surveiller l’amortissement.

### Boucle lente

Ordre de grandeur : minutes à heures libres.

- benchmarker ;
- compiler ;
- produire un dérivé ;
- valider ;
- apprendre un modèle de coût ;
- enrichir le portefeuille.

---

## 11. Programme de démarrage retenu

### 11.1 Hypothèse initiale

Un contrôleur adaptatif élémentaire produit plus de tokens conformes qu’une configuration statique conservatrice sur une même trace, à gêne équivalente.

### 11.2 Périmètre initial

- une machine ;
- un OS ;
- un modèle choisi par l’utilisateur ;
- un moteur de référence ;
- batch 1 ;
- génération déterministe ;
- E1 ;
- modèle intact ;
- aucun droit administrateur ;
- aucune suppression ;
- aucune modification persistante ;
- suspension entre tokens ;
- contrôle d’un nombre réduit de paramètres.

### 11.3 Scénarios comparés

- **A** — poste sans inférence ;
- **B** — inférence statique conservatrice ;
- **C** — inférence statique agressive ;
- **D** — compagnon adaptatif élémentaire.

### 11.4 Trace initiale

```text
inactivité
→ activité interactive
→ charge CPU
→ retour au calme
→ pression mémoire
→ reprise
```

Une trace GPU sera ajoutée après la validation du contrôle de base.

### 11.5 Mesures

- tokens validés cumulés ;
- tokens/s de préfill ;
- tokens/s de décodage ;
- latence p50/p95 des canaris ;
- CPU et mémoire ;
- fautes de page ;
- GPU/VRAM lorsqu’utilisés ;
- température ;
- fréquence ;
- pauses ;
- changements de plan ;
- erreurs et divergences.

### 11.6 Critère de succès

D produit significativement plus de tokens que B sous le même budget de gêne et évite les dégradations de C.

### 11.7 Critère d’échec utile

Si D ne surpasse pas B, documenter :

- surcharge de la télémétrie ;
- mauvaise estimation du slack ;
- coût des changements ;
- insuffisance de préemption ;
- trace non représentative ;
- absence réelle de marge exploitable.

Un résultat négatif décidera si le contrôle adaptatif doit être simplifié, changé ou abandonné.

---

## 12. Feuille de route synthétique

1. **Phase 0 — Spécification** : invariants, fidélité, charge, gêne, sûreté.
2. **Phase 1 — Observation passive** : inventaire, télémétrie, canaris, baseline.
3. **Phase 2 — Compagnon statique sûr** : quotas, mémoire, pause/reprise.
4. **Phase 3 — Slack dynamique** : enveloppe, règles, hystérésis, repli.
5. **Phase 4 — Portefeuille de plans** : profils, domination, migration.
6. **Phase 5 — Dérivés exacts et autotuning** : empaquetage, layouts, validation.
7. **Phase 6 — Hétérogénéité** : GPU/iGPU/NPU, contention, rôles.
8. **Phase 7 — Généralisation** : plateformes, IR et adaptateurs.
9. **Phase 8 — Recherche avancée** : certification, spéculation, compression, thermique.

La description détaillée et les critères de passage se trouvent dans `docs/ROADMAP.md`.

---

## 13. Pistes d’innovation à conserver

### 13.1 Compilation spécialisée sur les poids

Réordonner et empaqueter les constantes selon la machine. Falsification : comparer au meilleur kernel générique de bout en bout.

### 13.2 Compression sans perte fusionnée au calcul

Réduire le trafic mémoire en décodant directement dans les registres. Falsification : les cycles ajoutés dépassent les octets économisés.

### 13.3 Calcul approximatif puis certifié

Calculer rapidement avec des bornes d’erreur, raffiner seulement si le prochain token pourrait changer. Obstacle majeur : état caché et cache KV.

### 13.4 Spéculation hétérogène

Employer une ressource secondaire pour proposer et la ressource principale pour vérifier. Seuls les tokens acceptés comptent. La ressource secondaire ne doit pas remplacer le modèle cible.

### 13.5 Détection de structure exacte

Chercher zéros, blocs répétés, symétries et rangs exacts. Abandonner si les métadonnées et indices coûtent plus que le calcul dense.

### 13.6 Plans sensibles au régime

Employer des plans différents selon préfill, contexte, température et disponibilité, en incluant le coût de migration.

### 13.7 Compilation vers accélérateurs oubliés

N’utiliser un DSP, NPU ou bloc spécialisé que si un sous-graphe peut être exécuté et transféré avec un gain net mesuré.

### 13.8 Contrôle thermique prédictif

Maximiser le débit cumulé à chaud, pas le pic initial. Les réglages de tension restent hors du périmètre initial et ne pourront être envisagés qu’avec protections et vérification.

### 13.9 Exécution hors mémoire

Double buffering, prélecture et compression peuvent rendre un modèle exécutable au-delà de la RAM. Ils ne suppriment pas le plafond de bande passante du stockage.

### 13.10 OS minimal

À envisager seulement si des mesures démontrent que l’OS généraliste est un goulot. La loi d’Amdahl doit précéder toute décision d’écrire un nouveau noyau.

---

## 14. Alertes et fausses pistes

### Alertes scientifiques

- Ne pas confondre meilleur résultat observé et optimum absolu.
- Ne pas changer la charge de travail entre candidats.
- Ne pas compter les tokens spéculatifs rejetés.
- Ne pas présenter du débit agrégé comme débit interactif.
- Ne pas mesurer uniquement à froid.
- Ne pas additionner les gains de microbenchmarks sans mesure complète.
- Ne pas surapprendre un unique prompt.
- Ne pas considérer l’absence d’erreur sur un test comme preuve générale.

### Alertes systèmes

- Ne pas utiliser tous les composants par principe.
- Ne pas faire migrer continuellement les poids et le cache.
- Ne pas saturer la RAM jusqu’à la pagination.
- Ne pas considérer la VRAM déclarée par une seule API comme vérité absolue.
- Ne pas attribuer directement des privilèges à un parseur de modèle.
- Ne pas désactiver les protections thermiques.
- Ne pas modifier un firmware sans besoin explicite, environnement de récupération et autorisation ciblée.

### Alertes produit

- « Inutilisé » ne signifie pas « gratuitement disponible ».
- L’utilisateur peut ressentir une gêne que les pourcentages d’utilisation ne montrent pas.
- Le comportement correct peut être une pause.
- Un cache dérivé doit avoir une limite d’espace.
- Le système ne décide jamais qu’un fichier personnel est inutile.

### Non-sens explicitement rejetés

- piloter des atomes individuels sans interface ;
- transformer la RAM en multiplicateur matriciel par logiciel seul ;
- exploiter Rowhammer comme calcul utile ;
- transformer arbitrairement un contrôleur SSD en GPU ;
- employer une faille comme API stable ;
- récupérer de la chaleur comme calcul sans transducteur matériel ;
- rendre chaque composant actif afin de « ne rien gaspiller » ;
- garantir qu’une persévérance infinie vaincra une limite physique.

---

## 15. Sûreté, privilèges et récupération

Le premier prototype fonctionne en espace utilisateur.

Plus tard, trois niveaux pourront exister :

1. utilisateur — compilation, threads, allocations, backends ;
2. administrateur contrôlé — courtier minimal pour quelques actions réversibles ;
3. appliance exclusif — environnement amorçable dédié, seulement après validation.

Tout futur réglage privilégié doit être :

- explicitement autorisé ;
- représenté par une action déclarative ;
- borné ;
- journalisé ;
- accompagné de l’ancienne valeur ;
- accompagné d’une opération inverse ;
- surveillé par un watchdog indépendant ;
- annulé à l’arrêt ou après incident.

Les détails sont dans `docs/SURETE.md`.

---

## 16. Panel de personas requis

Le projet doit maintenir des rôles contradictoires :

- directeur de recherche et intégrateur ;
- architecte systèmes/runtime ;
- spécialiste compilateurs et IR ;
- spécialiste kernels CPU/GPU ;
- architecte matériel et mémoire ;
- spécialiste numérique et fidélité des modèles ;
- spécialiste contrôle, QoS et thermique ;
- expérimentaliste et reproductibilité ;
- sécurité, privilèges et récupération ;
- théoricien des limites ;
- falsificateur/red team scientifique ;
- représentant de l’utilisateur du poste.

Un gain de performance ne doit pas être validé uniquement par la personne qui l’a proposé. Toute action privilégiée nécessite l’avis sécurité. Toute transformation du modèle nécessite l’avis fidélité. Toute invention d’un nouveau kernel, langage ou OS nécessite une preuve par profilage et une analyse d’Amdahl.

Les mandats complets et prompts réutilisables sont dans `docs/PANEL_PERSONAS.md`.

---

## 17. Premier poste concret

L’expérimentation commence sur le poste utilisé pour cette conversation.

Inventaire préliminaire du 2026-09-03 :

- Windows 10 Famille 64 bits, build 19045 ;
- Intel Core i5-6600K, 4 cœurs/4 threads ;
- 16 Gio de RAM, 2 × 8 Gio à 2 133 MT/s ;
- NVIDIA GeForce GTX 1070, 8 Gio de VRAM ;
- pilote NVIDIA 560.94 ;
- Samsung SSD 750 EVO 250 Go ;
- disque WDC 1 To ;
- environ 14 Gio libres sur `C:` ;
- environ 372 Gio libres sur `D:` ;
- fichier d’échange sur `D:` ;
- profil d’alimentation « Performances élevées » ;
- hyperviseur rapporté comme présent par Windows, point à clarifier.

Le dépôt reste sur le volume système. Les modèles, traces et artefacts lourds sont placés dans `D:\InferenceCompanionLab`.

Ce poste est un bon premier cas : matériel suffisamment ancien pour rendre les contraintes visibles, CPU à quatre cœurs sans SMT, GPU dédié de génération antérieure, quantité de RAM modeste et coexistence réelle avec un poste utilisateur.

---

## 18. État des opérations effectuées

À la création de ce rapport :

- le dépôt Git existant et vide a été conservé ;
- la branche de travail `codex/foundation` a été créée ;
- le laboratoire `D:\InferenceCompanionLab` et ses sous-répertoires ont été créés ;
- un inventaire matériel en lecture seule a été effectué ;
- aucun logiciel supplémentaire n’a été installé ;
- aucun service n’a été arrêté ;
- aucun fichier personnel n’a été supprimé ;
- aucun réglage système n’a été modifié ;
- aucun modèle n’a encore été sélectionné ou téléchargé.

---

## 19. Prochaine décision et ordre de travail

Avant le premier code, fixer :

1. modèle initial ;
2. moteur de référence ;
3. référence déterministe et seed ;
4. contextes et longueurs ;
5. canaris de réactivité ;
6. budget d’interférence ;
7. durée des traces ;
8. politique d’amortissement ;
9. politique de conservation des données.

Ensuite :

1. écrire l’observateur passif ;
2. vérifier sa propre surcharge ;
3. établir A, B et C ;
4. construire D avec une politique à règles ;
5. comparer sur les mêmes traces ;
6. décider selon les résultats, pas selon l’intuition.

---

## 20. Conclusion

Le projet ne consiste pas à promettre qu’un logiciel commandera chaque atome ou fera disparaître les contraintes du matériel. Il consiste à créer une couche informatique nouvelle qui observe, compile, mesure, vérifie et s’adapte beaucoup plus largement que les runtimes actuels.

La version scientifiquement défendable est :

> Pour un modèle imposé, une machine imposée et un contrat de fidélité explicite, découvrir automatiquement le programme d’inférence correct, stable et réversible qui maximise le débit soutenu de tokens acceptés parmi les ressources programmables accessibles, tout en quantifiant honnêtement l’écart restant aux limites architecturales connues.

La première étape pertinente n’est pas de réécrire le monde logiciel. C’est de démontrer, sur le poste initial, que l’on sait mesurer la marge réellement disponible et l’exploiter sans gêner l’utilisateur. Ce résultat fournira les données nécessaires pour décider quelles couches méritent ensuite d’être réinventées.

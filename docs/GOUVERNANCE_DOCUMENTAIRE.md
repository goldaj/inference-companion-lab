# Gouvernance documentaire et source de vérité

Version : 1.0
Date d’adoption : 2026-09-03
Statut : normative

## 1. Source principale

La documentation versionnée dans Git constitue la source principale et durable du projet.

Références actuelles :

- dépôt local : `C:\Users\golda\Documents\ChatGPT\software d'optimisation générale d'inférence` ;
- dépôt GitHub privé : `https://github.com/goldaj/inference-companion-lab` ;
- remote : `origin` ;
- branche de travail et branche par défaut actuelle : `codex/foundation`.

Une affirmation ou décision présente uniquement dans une conversation n’est pas encore intégrée au projet. Elle devient durable lorsqu’elle est consignée dans le document approprié, validée, commitée et poussée.

La copie locale peut contenir un travail en cours. Après une tâche significative terminée, la référence durable est le commit Git poussé dont le hash local correspond au hash distant.

## 2. Distinction entre documentation et données

Git est la source principale pour :

- contexte, objectifs et architecture ;
- décisions et hypothèses ;
- protocoles et manifestes ;
- code et tests ;
- descriptions de machines ;
- résultats synthétiques et interprétations ;
- journal des installations et changements ;
- instructions de continuité ;
- biographies et règles du panel.

Git n’est pas destiné aux éléments suivants :

- poids de modèles ;
- secrets, jetons ou identifiants ;
- traces contenant des données personnelles ;
- profils, dumps ou journaux volumineux ;
- résultats bruts massifs ;
- artefacts compilés reproductibles.

Ces objets résident dans `D:\InferenceCompanionLab`. Leur existence et leur provenance doivent toutefois être représentées dans Git par des manifestes, hachages, versions, identifiants de runs et règles de conservation.

GitHub ne constitue donc pas, à lui seul, une sauvegarde du laboratoire volumineux. Une politique de sauvegarde séparée sera nécessaire avant que des données non reproductibles importantes soient confiées uniquement au volume `D:`.

## 3. Définition d’une tâche significative

Une tâche est significative dès qu’elle produit au moins un des effets suivants :

1. change un objectif, une contrainte ou une priorité ;
2. adopte, rejette ou reformule une décision durable ;
3. modifie une architecture, une interface, un format ou un invariant ;
4. ajoute ou modifie du code exécutable, un test ou un manifeste ;
5. installe, met à niveau ou retire un logiciel ;
6. modifie le système, un service, un pilote, un réglage ou un privilège ;
7. choisit ou change un modèle, un moteur, une baseline ou un oracle ;
8. exécute une expérience dont le résultat influence la suite ;
9. découvre une limite, un risque, une contradiction ou une fausse piste ;
10. change la structure du laboratoire ou la politique de données ;
11. modifie le panel, son protocole ou une responsabilité ;
12. crée une information dont une autre conversation aurait besoin pour reprendre sans deviner.

Une simple lecture, un contrôle sans nouveauté, une correction typographique isolée ou une discussion explicitement provisoire n’exige pas nécessairement un commit séparé. Dès qu’une discussion provisoire devient une décision, elle doit être documentée.

## 4. Matrice de mise à jour

| Nature du changement | Documents minimaux à examiner |
| --- | --- |
| Tout jalon significatif | `PROJECT_STATE.md`, `docs/JOURNAL_TRAVAUX.md` |
| Décision durable | `docs/DECISIONS.md` |
| Contexte utile à une reprise | `CONTEXT_TRANSFER.md` |
| Changement de vision ou d’objectif | `docs/RAPPORT_FONDATEUR.md` |
| Changement d’ordre ou de phase | `docs/ROADMAP.md` |
| Changement du mode compagnon | `docs/MODE_COMPAGNON.md` |
| Règle expérimentale ou de preuve | `docs/CHARTE_RECHERCHE.md` |
| Risque, privilège ou récupération | `docs/SURETE.md` |
| Installation ou modification de l’hôte | `lab/INSTALLATIONS.md` |
| Machine ou capacité observée | `lab/machine/` |
| Expérience | `lab/experiments/`, manifeste du run et résultat synthétique |
| Panel ou méthode de délibération | `docs/PANEL_PERSONAS.md` |
| Nouvelle entrée documentaire | `README.md` et, si nécessaire, `AGENTS.md` |

« Examiner » ne veut pas dire modifier artificiellement. Le responsable de la tâche vérifie le document et le modifie seulement si son contenu deviendrait incomplet, faux ou trompeur.

## 5. Cycle obligatoire après une tâche significative

### 5.1 Réconcilier le résultat et les documents

Décrire ce qui a réellement été accompli, les écarts au plan, les résultats négatifs, les incertitudes et la prochaine action. Ne pas documenter une action projetée comme si elle avait réussi.

### 5.2 Vérifier la cohérence

Au minimum :

- vérifier les liens Markdown ;
- valider les JSON, TOML ou YAML modifiés ;
- exécuter les tests pertinents ;
- rechercher les chemins, versions et statuts devenus obsolètes ;
- vérifier l’absence de secrets et d’artefacts volumineux ;
- exécuter `git diff --check` sur les changements préparés ;
- inspecter le diff avant le commit.

### 5.3 Créer un commit atomique

Le commit doit réunir le travail et la documentation qui explique ce même travail. Éviter un commit de code important suivi, beaucoup plus tard, d’un commit documentaire réparant son contexte.

Le message doit décrire le résultat, pas seulement l’action mécanique. Les décisions controversées doivent rester lisibles dans le diff et dans `docs/DECISIONS.md`.

### 5.4 Pousser vers GitHub

Après validation, pousser la branche suivie vers `origin`, sauf si :

- l’utilisateur demande explicitement de rester local ;
- le réseau ou GitHub est indisponible ;
- le diff contient une donnée qui ne peut pas être publiée, même dans un dépôt privé ;
- une revue humaine préalable a été explicitement demandée.

Dans ces cas, ne pas prétendre que la source distante est à jour. Inscrire l’état local non poussé dans `PROJECT_STATE.md` lorsque l’écart doit survivre à la conversation.

### 5.5 Vérifier la sauvegarde

Comparer le hash de `HEAD` avec la branche distante. La tâche documentaire n’est close que lorsque :

- le worktree est dans l’état attendu ;
- la branche locale suit la bonne branche distante ;
- le hash distant correspond, ou l’écart est explicitement documenté ;
- aucune donnée exclue ne s’est glissée dans l’index.

## 6. Documents vivants et documents historiques

### Documents vivants

- `PROJECT_STATE.md` doit refléter la situation courante et la prochaine action.
- `CONTEXT_TRANSFER.md` doit permettre une reprise autonome.
- `README.md` doit servir d’index exact.
- `docs/ROADMAP.md` doit montrer l’ordre actuel du programme.

Ils peuvent être reformulés lorsque le projet évolue.

### Documents historiques

- `docs/DECISIONS.md` conserve les décisions acceptées, remplacées ou rejetées ; une décision remplacée ne doit pas disparaître.
- `docs/JOURNAL_TRAVAUX.md` conserve les jalons et résultats, y compris négatifs.
- `lab/INSTALLATIONS.md` conserve les changements de l’hôte et leurs retours arrière.
- les dossiers d’expériences conservent les protocoles et conclusions.

Une erreur factuelle peut être corrigée, mais la correction doit rester visible dans Git.

## 7. Politique de branches

La branche principale actuelle est `codex/foundation`. Tant que le projet est conduit de manière linéaire dans cette conversation, les tâches cohérentes peuvent y être commités directement.

Une branche séparée devient préférable lorsque :

- plusieurs expériences avancent en parallèle ;
- un changement risqué doit être isolé ;
- une revue avant intégration est nécessaire ;
- le travail incomplet durerait au-delà d’une tâche ;
- plusieurs conversations ou agents peuvent modifier les mêmes fichiers.

Toute branche significative doit indiquer son objectif dans `PROJECT_STATE.md` si elle devient le lieu actif de travail.

## 8. Concurrence et reprise par une autre conversation

Avant de travailler, toute nouvelle conversation doit :

1. lire `AGENTS.md` ;
2. lire `PROJECT_STATE.md` et `CONTEXT_TRANSFER.md` ;
3. inspecter `git status`, la branche, le suivi distant et les derniers commits ;
4. tirer les changements distants seulement après avoir vérifié les modifications locales ;
5. préserver tout changement utilisateur non lié ;
6. mettre à jour les documents de continuité avec son propre résultat.

La conversation n’est jamais une source plus autoritaire qu’un commit récent sans expliquer explicitement pourquoi elle le remplace.

## 9. Protection des informations

Un dépôt privé réduit l’exposition, mais ne transforme pas un secret en contenu acceptable. Sont interdits dans Git :

- jetons d’API et cookies ;
- clés privées ;
- mots de passe ;
- données personnelles brutes ;
- prompts confidentiels non nécessaires ;
- chemins ou identifiants personnels sans utilité scientifique ;
- binaires et modèles sans examen de licence.

Tout secret découvert dans l’historique exige une rotation du secret et une procédure d’assainissement dédiée ; supprimer simplement le fichier dans un commit suivant ne suffit pas.

## 10. Définition documentaire de « terminé »

Une tâche significative n’est terminée que si :

1. son résultat est vérifié proportionnellement au risque ;
2. les documents touchés sont exacts ;
3. les décisions et résultats négatifs sont conservés ;
4. la prochaine action est explicite ;
5. le diff ne contient ni secret ni artefact interdit ;
6. un commit cohérent existe ;
7. ce commit est poussé et vérifié sur GitHub, ou l’empêchement est documenté.

## 11. Responsabilité de maintenance

L’agent ou la personne qui termine la tâche en assume la mise à jour documentaire. Il ne doit pas reporter cette responsabilité à une conversation future.

La règle pratique est :

> Modifier le système, c’est aussi modifier la représentation versionnée que le projet possède de ce système.

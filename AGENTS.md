# Instructions permanentes du projet

Ce dépôt porte le programme de recherche « superoptimiseur d’inférence intégrale », en commençant par le **mode compagnon** sur le poste Windows initial.

Toute personne ou tout agent travaillant dans ce dépôt doit lire, dans cet ordre :

1. `PROJECT_STATE.md` ;
2. `CONTEXT_TRANSFER.md` ;
3. `docs/RAPPORT_FONDATEUR.md` ;
4. `docs/CHARTE_RECHERCHE.md` ;
5. le document spécialisé pertinent pour la tâche.

## Invariants non négociables

- Le modèle choisi par l’utilisateur est imposé. Ne pas proposer de le remplacer par un modèle plus petit ou différent comme solution au problème de recherche.
- Le modèle original est immuable. Toute représentation spécialisée est un artefact dérivé, identifié, vérifiable, supprimable et reproductible.
- Le mode compagnon est prioritaire : l’utilisateur reste prioritaire et l’inférence ralentit ou se suspend si les ressources minimales ne sont plus disponibles.
- Aucun fichier utilisateur, logiciel, service ou réglage persistant ne doit être supprimé ou modifié sans demande explicite et ciblée de l’utilisateur.
- Ne jamais utiliser de vulnérabilité, contourner une protection thermique, désactiver une protection électrique, modifier aveuglément un firmware ou tolérer une corruption silencieuse pour obtenir un gain.
- Les droits administrateur ne sont pas accordés implicitement à l’optimiseur. Toute future action privilégiée doit passer par un courtier minimal, une liste d’actions autorisées, un journal et une procédure de restauration.
- Mesurer uniquement des tokens acceptés et conformes au contrat de fidélité. Ne jamais gonfler le débit avec des propositions spéculatives rejetées, un contexte réduit, un batch différent ou une charge de travail modifiée.
- Séparer systématiquement préremplissage, décodage, débit instantané, débit soutenu, mémoire, température, puissance et impact utilisateur.
- Toute affirmation de performance doit comparer la même charge, le même modèle, le même contrat de fidélité et des conditions thermiques comparables.
- Les résultats négatifs et les fausses pistes doivent être conservés : ils font partie du produit scientifique.

## Discipline de laboratoire

- Le dépôt Git contient le code, les protocoles, les configurations, les résultats synthétiques et les documents.
- Les données volumineuses résident dans `D:\InferenceCompanionLab` et ne doivent pas être ajoutées à Git.
- Le modèle original va dans `D:\InferenceCompanionLab\models`.
- Les représentations compilées vont dans `D:\InferenceCompanionLab\derived`.
- Les traces brutes vont dans `D:\InferenceCompanionLab\traces`.
- Chaque exécution isolée va dans `D:\InferenceCompanionLab\runs`.
- Les exports vont dans `D:\InferenceCompanionLab\exports`.
- Les artefacts invalides ou suspects vont dans `D:\InferenceCompanionLab\quarantine`.
- Toute installation ou modification de configuration du poste doit être ajoutée au journal prévu dans `lab/INSTALLATIONS.md`, avec motif, version, portée, procédure de vérification et procédure de retrait.
- Préférer les dépendances portables ou isolées. Ne rien installer globalement simplement par commodité.
- Ne pas exécuter de code personnalisé fourni par un modèle avec des privilèges élevés.

## Méthode d’édition et de validation

- Préserver les changements existants de l’utilisateur.
- Documenter les décisions durables dans `docs/DECISIONS.md`.
- Mettre à jour `PROJECT_STATE.md` après chaque jalon ou changement de direction.
- Un nouveau kernel, langage, noyau OS ou mécanisme privilégié doit répondre à un goulot mesuré, pas seulement à une intuition.
- Toute nouvelle transformation du modèle doit indiquer son niveau de fidélité E0, E1, E2 ou E3 et fournir sa méthode de vérification.

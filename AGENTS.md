## Addendum contribution ChatGPT du 27/10/2026, branche isolée

**PR #2 :** https://github.com/goldaj/inference-companion-lab/pull/2
Branche `chatgpt/trial-audit-gate-20261027` dérivée de `chatgpt/research-review-20261025`, sans modifier `codex/foundation`.
Lire `docs/AUDIT_EXPERIENCES_HORS_LIGNE_20261027.md` avant de reprendre `lab/scripts/audit_experiment.py`. Il s'agit d'une **porte documentaire/de données agrégées** : aucune inference, aucune collecte ni expérimentation réelle. L'outil n'émet JAMAIS « succès scientifique » : `REVIEW_REQUIRED` impose une validation extérieure. La fixture de laboratoire est fictive et volontairement `NOT_ADMISSIBLE`. Ne jamais remplacer le modèle choisi par le propriétaire, inventer de mesures ou activer une allocation du PC. La présente PR nécessite une revue et ne doit pas être fusionnée automatiquement.

---

# Instructions permanentes du projet

Ce dépôt porte le programme de recherche « superoptimiseur d’inférence intégrale », en commençant par le **mode compagnon** sur le poste Windows initial.

Toute personne ou tout agent travaillant dans ce dépôt doit lire, dans cet ordre :

1. `PROJECT_STATE.md` ;
2. `CONTEXT_TRANSFER.md` ;
3. `docs/GOUVERNANCE_DOCUMENTAIRE.md` ;
4. `docs/RAPPORT_FONDATEUR.md` ;
5. `docs/CHARTE_RECHERCHE.md` ;
6. le document spécialisé pertinent pour la tâche.

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

## Gouvernance documentaire obligatoire

- Git est la source principale de la documentation, du code, des protocoles et des résultats synthétiques.
- Après chaque tâche significative, appliquer intégralement `docs/GOUVERNANCE_DOCUMENTAIRE.md` dans le même tour de travail.
- Examiner au minimum `PROJECT_STATE.md` et `docs/JOURNAL_TRAVAUX.md` ; les mettre à jour si la tâche crée une information durable.
- Mettre à jour `CONTEXT_TRANSFER.md` dès qu’une autre conversation aurait besoin de la nouvelle information pour reprendre correctement.
- Une information présente seulement dans la conversation n’est pas considérée comme intégrée au projet.
- Valider les formats, tests, liens, secrets, tailles et le diff avant le commit.
- Après une tâche significative terminée, créer un commit cohérent, le pousser vers `origin` et vérifier l’égalité des hashes local et distant, sauf demande explicite de rester local ou empêchement documenté.
- Ne jamais pousser de secret, modèle, trace personnelle, dump ou artefact volumineux, même vers un dépôt privé.

## Utilisation du panel

- `docs/PANEL_PERSONAS.md` définit douze individus synthétiques stables, pas seulement douze métiers.
- Lorsqu’une persona est convoquée, conserver sa biographie, son tempérament, ses valeurs, ses biais, ses relations et ses limites de compétence.
- Ne jamais déduire une position technique de son sexe, genre, âge, nationalité, langue, origine sociale, handicap ou autre identité.
- Les personas organisent la contradiction ; elles ne remplacent ni les sources, ni les mesures, ni les expériences.


## Contexte conversationnel ChatGPT / passation Codex

Lire aussi **`docs/CHATGPT_PROJECT_HISTORY.md`** pour les échanges et décisions retrouvés. Ce journal est explicitement partiel ; ne jamais présenter un résumé comme un verbatim. À chaque changement de projet, ajouter les nouveaux échanges pertinents avec rôles Utilisateur/Assistant, texte exact et horodatages uniquement lorsqu'ils sont disponibles ; sinon noter la lacune. Préserver l'ensemble des règles et documents existants de ce dépôt et ne publier aucun secret.

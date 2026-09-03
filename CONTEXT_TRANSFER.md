# Dossier de transfert vers une autre conversation

Version : 0.1
Date : 2026-09-03
Statut : contexte fondateur consolidé

## Résumé autonome

L’utilisateur veut créer un système logiciel général d’optimisation de l’inférence locale. Le modèle est choisi par l’utilisateur et imposé au système. Il ne s’agit pas de recommander un modèle plus petit, mais d’obtenir le meilleur débit physiquement accessible pour le modèle retenu sur la machine disponible.

La vision ultime est un hyper-runtime d’inférence réflexif : une couche portable reçoit le modèle, l’analyse et produit une exécution agressivement spécialisée pour chaque machine. Elle inventorie et mesure les ressources programmables, génère ou sélectionne des kernels, place les données et les opérations, contrôle la mémoire, tient compte de la puissance et de la température, vérifie la fidélité et apprend par autotuning.

Les formulations littérales « chaque atome » et « optimum absolu garanti » ont été corrigées. Un logiciel ne peut exploiter que les degrés de liberté observables et contrôlables par l’ISA, les pilotes, le firmware ou les capteurs/actionneurs exposés. Il ne peut pas rendre programmable un bloc fixe, créer de la bande passante ou commander des particules sans interface. Il ne peut généralement pas prouver qu’aucun programme imaginable ne serait plus rapide. Il doit produire le meilleur plan validé trouvé, une borne supérieure conditionnelle, les hypothèses et l’écart restant.

La recherche commencera par le **mode compagnon**. Celui-ci utilise la marge de ressources que le poste peut prêter sans dépasser un budget de gêne pour l’utilisateur. Il considère toutes les ressources, mais n’utilise que celles dont la contribution marginale est positive. Il ralentit ou se suspend lorsque l’utilisateur reprend les ressources minimales requises.

Le modèle original est immuable. Les transformations sont séparées en quatre catégories :

- niveau 0 : aucun changement du modèle, seulement orchestration du runtime ;
- niveau 1 : artefacts dérivés exacts — poids réordonnés, empaquetage, layouts, kernels, constantes ;
- niveau 2 : arithmétique ou représentation non bit-exacte, sous contrat de fidélité ;
- niveau 3 : modification réelle du modèle, interdite par défaut et uniquement possible avec consentement explicite.

Le premier jalon ne transforme pas le modèle. Il mesure et contrôle de façon non privilégiée.

## Objectif du mode compagnon

Maximiser le nombre de tokens acceptés du modèle cible sur une durée donnée, sous les contraintes suivantes :

- budget d’interférence utilisateur respecté ;
- mémoire et VRAM sous les budgets disponibles ;
- température, puissance et stabilité dans les limites autorisées ;
- fidélité au modèle imposé ;
- aucune modification irréversible du poste.

La notion centrale est le **slack** : non pas le pourcentage momentanément inutilisé, mais la marge que l’inférence peut emprunter sans violer la qualité de service de l’utilisateur. Cette marge comprend CPU, RAM, bande passante mémoire, GPU, VRAM, E/S, puissance et thermique.

Le contrôle doit fonctionner à trois échelles :

- boucle rapide : protection immédiate et retrait ;
- boucle intermédiaire : choix d’un plan et migration ;
- boucle lente : benchmark, compilation et apprentissage pendant les périodes libres.

Le runtime doit disposer d’un portefeuille de plans validés correspondant à différentes enveloppes de ressources. Il ne doit pas recompiler continuellement. Il change de plan seulement si le gain futur estimé amortit la migration des poids, buffers et cache KV.

## Premier résultat scientifique attendu

Comparer quatre scénarios sur la même trace :

- A : poste sans inférence ;
- B : inférence statique conservatrice ;
- C : inférence statique agressive ;
- D : compagnon adaptatif élémentaire.

Le scénario D réussit s’il produit davantage de tokens validés que B sous le même budget d’interférence, tout en évitant les dégradations de C.

Le premier programme sera un observateur passif, puis un contrôleur simple à règles. Il ne doit pas commencer par un nouveau kernel, un nouvel OS, une transformation du modèle ou un contrôleur neuronal.

## Règles de sûreté

- Ne rien supprimer du poste en mode compagnon.
- Ne pas arrêter de services ni modifier le firmware dans le premier jalon.
- Aucun droit administrateur pour le premier observateur et le premier contrôleur.
- Ne jamais désactiver les protections thermiques ou électriques.
- Ne pas employer de vulnérabilités comme mécanisme d’optimisation.
- Les fichiers de modèle et le code personnalisé sont des entrées non fiables.
- Les futures actions privilégiées devront passer par un courtier minimal et transactionnel.
- Toute modification devra être journalisée et réversible.
- Seuls les tokens acceptés et conformes sont comptés.

## Niveaux de fidélité

- E0 : exactitude bit à bit.
- E1 : mêmes tokens qu’une référence déterministe.
- E2 : même distribution à une tolérance définie.
- E3 : équivalence comportementale mesurée.

Le contrat recommandé pour le premier prototype est E1.

## Poste concret initial

- Windows 10 Famille 64 bits, build 19045.
- Intel Core i5-6600K, 4 cœurs/4 threads.
- 16 Gio de RAM, 2 × 8 Gio à 2 133 MT/s.
- NVIDIA GeForce GTX 1070, 8 Gio de VRAM, pilote 560.94.
- SSD Samsung 750 EVO 250 Go : environ 14 Gio libres sur `C:` à l’inventaire.
- HDD WDC 1 To : environ 372 Gio libres sur `D:`.
- Fichier d’échange sur `D:`.
- Profil d’alimentation « Performances élevées ».
- Aucun logiciel n’a été installé pour le projet à ce stade.

## Répertoires

- Dépôt Git : `C:\Users\golda\Documents\ChatGPT\software d'optimisation générale d'inférence`
- Branche : `codex/foundation`
- Laboratoire de données : `D:\InferenceCompanionLab`
- Modèles originaux : `D:\InferenceCompanionLab\models`
- Artefacts dérivés : `D:\InferenceCompanionLab\derived`
- Traces : `D:\InferenceCompanionLab\traces`
- Exécutions : `D:\InferenceCompanionLab\runs`
- Résultats : `D:\InferenceCompanionLab\results`
- Exports : `D:\InferenceCompanionLab\exports`
- Temporaire : `D:\InferenceCompanionLab\tmp`
- Quarantaine : `D:\InferenceCompanionLab\quarantine`

## État exact et prochaine étape

La structure de laboratoire et la documentation fondatrice sont créées. Il n’existe pas encore de moteur propre au projet. Aucune dépendance n’a été installée et aucune modification système n’a été faite.

La prochaine étape est de finaliser la spécification expérimentale v0.1 : choisir le modèle initial, le moteur de référence, la génération déterministe, les contextes, les canaris, le budget de gêne et la durée des traces. Ensuite, construire l’observateur passif.

## Prompt de reprise conseillé

> Reprends le projet de superoptimiseur d’inférence intégrale dans le dépôt indiqué. Lis d’abord `AGENTS.md`, `PROJECT_STATE.md`, `CONTEXT_TRANSFER.md` et `docs/RAPPORT_FONDATEUR.md`. Le mode compagnon non destructif est la priorité. Le modèle est imposé et ne doit pas être remplacé. Vérifie l’état Git et les changements existants avant toute édition. Ne commence pas par installer un moteur, transformer le modèle ou demander des privilèges : commence par la prochaine décision encore ouverte dans `PROJECT_STATE.md`, sauf instruction plus récente de l’utilisateur.

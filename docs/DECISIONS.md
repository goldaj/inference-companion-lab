# Journal des décisions

Ce fichier contient les décisions durables. Les questions encore ouvertes restent dans `PROJECT_STATE.md`.

## ADR-001 — Le modèle est imposé

Date : 2026-09-03
Statut : accepté

Le système optimise le modèle choisi par l’utilisateur. Remplacer ce modèle par un autre, même plus efficace, ne satisfait pas le projet.

Conséquence : un débit très faible peut être le meilleur résultat accessible et doit être rapporté honnêtement.

## ADR-002 — Original immuable et dérivés séparés

Date : 2026-09-03
Statut : accepté

Le modèle original est conservé intact. Les layouts, poids empaquetés, kernels et autres variantes sont des artefacts dérivés supprimables, identifiés par empreintes et niveau de fidélité.

## ADR-003 — Mode compagnon prioritaire

Date : 2026-09-03
Statut : accepté

Le premier produit emprunte seulement la marge de ressources qui ne viole pas la qualité de service de l’utilisateur. L’inférence peut se suspendre.

Les modes exclusif temporaire et appliance dédié sont reportés.

## ADR-004 — Aucune suppression en mode compagnon

Date : 2026-09-03
Statut : accepté

Aucun fichier, programme ou service n’est supprimé. Le projet peut retirer ses propres artefacts de cache selon une politique explicite.

## ADR-005 — Mesurer avant d’optimiser

Date : 2026-09-03
Statut : accepté

Le premier programme est un observateur passif. Les nouveaux kernels, transformations et contrôleurs appris sont interdits avant l’établissement des baselines.

## ADR-006 — Premier contrat recommandé E1

Date : 2026-09-03
Statut : accepté comme recommandation initiale

Le premier benchmark devrait exiger les mêmes tokens qu’une référence déterministe. La décision finale sera figée avec le premier modèle et moteur.

## ADR-007 — Trois boucles temporelles

Date : 2026-09-03
Statut : accepté

La protection rapide, la sélection de plan intermédiaire et l’autotuning lent sont séparés. La sûreté ne dépend pas du composant d’apprentissage.

## ADR-008 — Portefeuille de plans

Date : 2026-09-03
Statut : accepté

Le système prépare plusieurs plans validés pour différentes enveloppes au lieu de retuner continuellement un plan unique.

## ADR-009 — Données lourdes sur le volume D

Date : 2026-09-03
Statut : accepté

Le dépôt reste dans le répertoire de projet actuel. `D:\InferenceCompanionLab` contient modèles, dérivés, traces, runs, résultats et exports volumineux.

Motif : environ 14 Gio libres sur `C:` contre environ 372 Gio sur `D:` lors de l’inventaire.

## ADR-010 — Aucun privilège initial

Date : 2026-09-03
Statut : accepté

L’observateur et le premier contrôleur fonctionnent sans privilèges élevés. Toute future capacité administrateur nécessite un courtier limité, des actions déclaratives, un journal et une restauration.

## ADR-011 — Meilleur plan connu, pas optimum absolu proclamé

Date : 2026-09-03
Statut : accepté

Le système publie le meilleur plan validé trouvé, l’espace exploré, une borne conditionnelle et l’incertitude. Il ne prétend pas prouver l’optimum parmi tous les programmes possibles.

## ADR-012 — Première comparaison A/B/C/D

Date : 2026-09-03
Statut : accepté

La première démonstration compare sans inférence, statique conservateur, statique agressif et adaptatif élémentaire sur une trace identique.

## ADR-013 — Dépôt GitHub privé et données lourdes séparées

Date : 2026-09-03
Statut : accepté ; visibilité remplacée par ADR-016 le 2026-10-18, séparation des données maintenue

Le code et les documents sont sauvegardés dans le dépôt GitHub privé `goldaj/inference-companion-lab`. Les modèles, traces, runs et résultats volumineux restent hors Git dans `D:\InferenceCompanionLab`. Cette séparation évite de publier des modèles, des données personnelles ou des artefacts volumineux et signifie qu’une sauvegarde indépendante du laboratoire de données devra être organisée séparément si nécessaire.

## ADR-014 — Git comme source documentaire principale

Date : 2026-09-03
Statut : accepté

Une décision uniquement présente dans une conversation reste provisoire. Après chaque tâche significative, les documents concernés sont réconciliés avec le résultat réel, validés, commités, poussés vers `origin` et comparés à la branche distante. `docs/GOUVERNANCE_DOCUMENTAIRE.md` définit les critères, exceptions et documents à examiner.

## ADR-015 — Le panel est composé d’individus synthétiques stables

Date : 2026-09-03
Statut : accepté

Les douze fonctions du panel sont incarnées par douze individus fictifs possédant identité, biographie, tempérament, valeurs, biais et relations durables. Leurs caractéristiques démographiques enrichissent les vécus sans déterminer aucune position technique. Les personas structurent la contradiction mais ne remplacent ni expertise vérifiée, ni source, ni mesure.

## ADR-016 — Publication de la fondation de recherche dans le portfolio

Date : 2026-10-18
Statut : accepté

Le propriétaire souhaite montrer aussi ses recherches, réflexions et projets inaboutis dans son portfolio GitHub. Le dépôt documentaire `goldaj/inference-companion-lab` devient public après revue des fichiers, de l’historique accessible et des métadonnées de machine, commit, push et contrôle des hashes.

La revue Gitleaks n’a détecté aucun secret dans les fichiers ni dans les références Git examinées. Le profil d’hôte contient des caractéristiques matérielles génériques et pas de numéro de série ni d’identifiant unique ; les personnages du panel sont fictifs. Cette vérification ne constitue pas une preuve mathématique d’absence de toute information sensible.

Cette décision remplace uniquement la visibilité privée adoptée dans ADR-013. Les modèles, données personnelles, traces brutes et artefacts lourds restent locaux et interdits dans Git. L’historique de la sauvegarde privée initiale est conservé. Aucune promesse de performance, expérience supplémentaire ou implémentation n’est ajoutée par cette publication.

## ADR-017 — Premier observateur L0 limité à un canari de réveil

Date : 2026-10-29
Statut : expérimental, branche de revue non fusionnée

La première tranche exécutable mesure uniquement les retards de réveil et le CPU de son propre processus. Pas de modèle, système, GPU, mémoire privée ou changement de priorité. Motivation : instrumenter le protocole non privilégié de façon vérifiable avant d'optimiser. Ne pas prétendre que cette instrumentation constitue le benchmark A/B/C/D ou prouve une absence de gêne. Voir `docs/OBSERVATEUR_L0.md`.

# Laboratoire du superoptimiseur d’inférence intégrale

Ce dépôt contient la documentation, les protocoles et, à terme, le code d’un système logiciel destiné à maximiser l’inférence d’un **modèle imposé** sur une **machine imposée**, en commençant par un mode compagnon non destructif.

Le mode compagnon utilise seulement la marge de ressources que le poste peut prêter sans dépasser un budget explicite de gêne pour l’utilisateur. Il doit ralentir, migrer ou se suspendre lorsque l’utilisateur reprend ces ressources.

## État actuel

- Phase : fondation scientifique et préparation du laboratoire.
- Mode retenu : compagnon non privilégié et non destructif.
- Premier poste : Windows 10, Intel Core i5-6600K, 16 Gio de RAM, NVIDIA GeForce GTX 1070 8 Gio.
- Sauvegarde distante : dépôt GitHub privé `goldaj/inference-companion-lab`.
- Modèle de départ : pas encore choisi.
- Moteur de référence : pas encore choisi.
- Logiciels ajoutés au poste : GitHub CLI 2.99.0, uniquement pour l’authentification et la publication du dépôt.
- Données volumineuses : `D:\InferenceCompanionLab`.

Consulter [PROJECT_STATE.md](PROJECT_STATE.md) pour l’état opérationnel exact.

## Documents essentiels

- [Rapport fondateur](docs/RAPPORT_FONDATEUR.md) — contexte complet, objectifs, limites, architecture, alertes et plan.
- [Charte de recherche](docs/CHARTE_RECHERCHE.md) — invariants, fidélité, preuve et règles de mesure.
- [Mode compagnon](docs/MODE_COMPAGNON.md) — définition du slack, qualité de service, contrôle et migration.
- [Feuille de route](docs/ROADMAP.md) — phases, sous-étapes, livrables et critères de passage.
- [Panel de personas](docs/PANEL_PERSONAS.md) — rôles contradictoires à mobiliser pendant la recherche.
- [Sûreté et réversibilité](docs/SURETE.md) — limites d’autorité, protections et récupération.
- [Décisions](docs/DECISIONS.md) — décisions architecturales déjà prises.
- [Transfert de contexte](CONTEXT_TRANSFER.md) — résumé autonome destiné à une autre conversation.

## Structure du laboratoire

Le dépôt Git et les données expérimentales sont volontairement séparés :

```text
<dépôt Git>
├── docs/                    protocoles et décisions
├── lab/                     configurations et outils de laboratoire
├── PROJECT_STATE.md         état vivant du projet
└── CONTEXT_TRANSFER.md      dossier de continuité conversationnelle

D:\InferenceCompanionLab
├── models/                  modèles originaux immuables
├── derived/                 artefacts compilés et représentations spécialisées
├── traces/                  télémétrie brute
├── runs/                    répertoires isolés par expérience
├── results/                 résultats volumineux
├── exports/                 rapports exportés
├── tmp/                     données jetables
└── quarantine/              artefacts invalides ou suspects
```

## Premier résultat scientifique recherché

Comparer, sur une même trace d’activité :

1. poste sans inférence ;
2. inférence statique conservatrice ;
3. inférence statique agressive ;
4. compagnon adaptatif élémentaire.

Le compagnon doit produire davantage de tokens validés que le profil statique conservateur tout en respectant le même budget d’interférence utilisateur et en évitant les dégradations du profil agressif.

Le premier code sera donc un **observateur passif**, pas un nouvel engine ni un optimiseur de modèle.

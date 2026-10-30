# Audit de passation recherche — 2026-10-30

## Mission, limites et preuve
Laboratoire « superoptimiseur d'inférence intégrale », mode compagnon Windows prioritaire. **Ce dépôt n'a pas démontré d'accélération d'inférence ni de fidélité modèle** : le canari L0 est un observateur CPU passif, les audits expérimentaux sont des portes documentaires. Aucun programme, benchmark, instrument ou test Windows exécuté pendant cet audit GitHub.

## Branches vs `codex/foundation`
- `codex/foundation` : `8b4f437dc5a9af4790e8ab8739f04ed953bed40f` (conserver).
- `chatgpt/research-review-20261025` (`7513d6a77c722e1ebfe0cab9ce086717dda9eb40`) : behind, ahead 0, behind 21. Historique inclus, candidat à nettoyage après vérification des liens externes.
- `chatgpt/trial-audit-gate-20261027` (`2d9f55bcf92f2ac1ad2623443d298645bf8e1d49`) : behind, ahead 0, behind 8. Historique inclus, candidat à nettoyage après vérification des liens externes.
- `feat/l0-passive-canary-observer-20261029` (`fff41216436867a3aab5d16c123a35f6b882dea3`) : behind, ahead 0, behind 5. Historique inclus, candidat à nettoyage après vérification des liens externes.

## PR
- [#3](https://github.com/goldaj/inference-companion-lab/pull/3) : fusionnée ; `feat/l0-passive-canary-observer-20261029` → `codex/foundation`.
- [#2](https://github.com/goldaj/inference-companion-lab/pull/2) : fusionnée ; `chatgpt/trial-audit-gate-20261027` → `feat/l0-passive-canary-observer-20261029`.
- [#1](https://github.com/goldaj/inference-companion-lab/pull/1) : fermée sans fusion ; `chatgpt/research-review-20261025` → `codex/foundation`.

## Challenge scientifique et invariants non négociables
- Mesurer un canari sur poste utilisateur compatible, avec horloge et distribution p50/p95/p99, sans effets persistants ni surcharge CPU. Les runners CI GitHub ne sont PAS des observations Windows.
- Ne jamais substituer un autre modèle à celui choisi par le propriétaire ; modèle original immuable et artefacts dérivés identifiables.
- Ajouter un contrôle externe de fidélité, qualité, ressources et jouabilité avant tout projet d'inférence accélérée ; ne pas déduire une amélioration des chiffres de démonstration.
- Aucun changement de réglages système, pilotes, firmware ou fichiers personnels sans autorisation explicite.

## Reprise
Lire `PROJECT_STATE.md`, `CONTEXT_TRANSFER.md`, `docs/GOUVERNANCE_DOCUMENTAIRE.md`, `docs/CHARTE_RECHERCHE.md`, `docs/OBSERVATEUR_L0.md`. Exécuter tests unitaires Python en environnement isolé, puis faire un protocole instrumenté sur poste réel avant décision d'expérience E1. Respecter les gates `REVIEW_REQUIRED` ; n'inventer ni gain ni tests.

Source : GitHub branches, PR et README (« # Laboratoire du superoptimiseur d’inférence intégrale »), vérifiés le 30/10/2026. Aucun merge, suppression ou code modifié dans cette passe.

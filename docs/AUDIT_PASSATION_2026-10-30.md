# Audit contradictoire et passation — Inference Companion Lab (2026-10-30)

Interrogation GitHub directe de 4 branches, 3 PR et racine. Aucune mesure sur le poste de l'utilisateur ni inférence réelle exécutée.

## Graphe Git
- `codex/foundation` : `a629e21021126cb97147654dfb0d9c08c743acc1` ; référence à garder.
- `chatgpt/research-review-20261025` (`7513d6a77c722e1ebfe0cab9ce086717dda9eb40`), statut **behind**, avance 0, retard 18 : contenu déjà ancêtre de foundation, candidate nettoyage après vérification des refs.
- `chatgpt/trial-audit-gate-20261027` (`2d9f55bcf92f2ac1ad2623443d298645bf8e1d49`), statut **behind**, avance 0, retard 5 : contenu déjà ancêtre de foundation, candidate nettoyage après vérification des refs.
- `feat/l0-passive-canary-observer-20261029` (`fff41216436867a3aab5d16c123a35f6b882dea3`), statut **behind**, avance 0, retard 2 : contenu déjà ancêtre de foundation, candidate nettoyage après vérification des refs.

## PR
- [#3](https://github.com/goldaj/inference-companion-lab/pull/3) : fusionnée (closed), [CONSOLIDÉ][Codex] Canari L0 + protocole scientifique + audit des preuves.
- [#2](https://github.com/goldaj/inference-companion-lab/pull/2) : fusionnée (closed), [DRAFT][GPT6] Gate scientifique hors ligne pour A0/A1 + ABCD, 15 tests verts.
- [#1](https://github.com/goldaj/inference-companion-lab/pull/1) : fermée sans merge (closed), [DRAFT] Inference Companion : protocole de falsification avant tout observateur.

## Périmètre observé
`.gitattributes`, `.github`, `.gitignore`, `AGENTS.md`, `CONTEXT_TRANSFER.md`, `PROJECT_STATE.md`, `README.md`, `docs`, `lab`, `tests`.

## Hypothèses à vérifier par l'agent
1. Le canari L0 mesure un retard de réveil CPU de son propre processus, **pas** un gain d'intelligence, de vitesse de tokens, ni une QoS sur le PC utilisateur.
2. Exécuter les contrôles offline avec horloge synthétique et confronter au poste Windows réel (p50/p95/p99, CPU, variabilité et bruit externe), sans changer les paramètres systèmes.
3. Vérifier confinement des écritures de preuves, absence d'écrasement et permissions minimales.
4. Établir des critères Go/No-Go E1 et un témoin de calcul avant de conclure à une performance de modèle ou recommander un changement d'inférence.
5. Les trois anciennes branches sont ancêtres de `codex/foundation`; la PR #3 a été fusionnée, ne créer aucune PR de rattrapage redondante.

Ne pas activer d'optimisation système intrusive ni d'inférence de secrets. Résultats hors ligne à documenter avant claims.


## Observation CI GitHub (30 octobre 2026)
- [Observer L0 tests](https://github.com/goldaj/inference-companion-lab/actions/runs/41046796350) : **success** ; [Offline research evidence audit](https://github.com/goldaj/inference-companion-lab/actions/runs/41046796256) : **success**, sur commit documentaire.

Les contrôles ci-dessus ne démontrent ni la validité fonctionnelle en environnement réel ni la publication d'une release. Ne pas substituer ce statut aux tests manuels et matériels prévus dans la passation.

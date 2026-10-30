# Audit de branches et passation — 30 octobre 2026

**Source :** branches et PR ouvertes GitHub vérifiées. **Limite :** audit complet des différences de code et tests non exécutés dans cette passe. Ne pas déduire qu'une branche est supprimable de son nom.

- Dépôt : `goldaj/inference-companion-lab` ; branche par défaut : `codex/foundation`.
- PR ouvertes : aucune.

## Branches (4)
- `chatgpt/research-review-20261025`
- `chatgpt/trial-audit-gate-20261027`
- `codex/foundation` (défaut)
- `feat/l0-passive-canary-observer-20261029`

## Défis et passation
- Préserver l'isolement du canari passif, le protocole expérimental et les critères de falsification ; ne pas transformer des preuves synthétiques en preuves de production.
- Pour chaque branche, comparer SHA et ascendance à la bonne cible ; inspecter les diffs divergents et les PR historiques.
- Ne jamais fusionner vers la production sans tests ni autorisation.

**Décision :** inventaire documenté ; suppression et fusion laissées en attente de validation individualisée.

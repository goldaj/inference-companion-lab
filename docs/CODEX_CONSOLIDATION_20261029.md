# Reprise unique pour Codex — consolidation du 29 octobre 2026

## Périmètre

**PR unique :** https://github.com/goldaj/inference-companion-lab/pull/3 — branche `feat/l0-passive-canary-observer-20261029` → `codex/foundation`.

Cette branche réunit par fusion Git à deux parents :
- **#1** : protocole de falsification et cadre scientifique du laboratoire.
- **#2** : auditeur de déclarations d'expériences A0/A1/ABCD, fixtures synthétiques et tests de preuves.
- **#3** : canari L0 non privilégié (ordonnancement CPU), métriques et rapport local.

Les travaux de Codex présents sur `codex/foundation` n'ont pas été écrasés. Les anciens textes de passation divergents sont archivés sous `docs/merge-archive/`, et leurs commits sont parents de l'unique évolution. Les nouveaux scripts et tests sont à leurs chemins d'origine.

## Validation obligatoire avant intégration

1. Revoir les résultats des workflows **sur le dernier commit de la PR #3**, pas seulement sur les anciennes branches.
2. Lancer séparément les tests de l'auditeur de preuves et du canari ; vérifier les chemins de fixtures et leur indépendance de toute API privée.
3. Vérifier que les mesures ne dépassent pas leur périmètre : aucune instrumentation privilégiée, aucun pilote, aucune altération des réglages du poste, aucune expérimentation invasive et aucune revendication d'un gain d'inférence.
4. Revoir les archives historiques si une décision ou règle paraît contradictoire ; conserver les consignes de sécurité du dépôt Codex.
5. Faire intégrer la PR #3 par Codex seulement après revue des risques, consentements et résultats. Ne pas interpréter « test vert » comme preuve d'une accélération IA réelle.

## État

Code et documentation consolidés ; tests CI post-fusion à consulter. Les résultats antérieurs ne valent pas validation du nouveau HEAD. Aucune action sur le matériel de l'utilisateur n'a été effectuée.

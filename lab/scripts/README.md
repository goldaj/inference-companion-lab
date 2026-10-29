# Scripts du laboratoire

Ordre de construction recommandé :

1. `inventory` — descripteur statique de l’hôte avec source et confiance ;
2. `observe` — télémétrie passive horodatée et coût propre ;
3. `canary` — petites sondes de réactivité sans inspection du contenu utilisateur ;
4. `run-baseline` — moteur de référence et manifeste résolu ;
5. `validate` — fidélité E0/E1 et validation des résultats ;
6. `compare` — analyse A/B/C/D et intervalles d’incertitude ;
7. `package` — export reproductible sans modèles, secrets ni données personnelles.

Les scripts doivent être non privilégiés par défaut, refuser les chemins non résolus, écrire seulement dans les racines autorisées et produire un statut explicite en cas d’arrêt partiel.

## Instrument L0 disponible (2026-10-29)

`observe_passive.py` : première sonde réellement exécutable de réveil CPU et overhead, sans privilèges ni dépendances. `python lab/scripts/observe_passive.py --samples 20 --interval-ms 50`. Aucune écriture sans `--report` et `--lab-root` explicites. Tests `python -m unittest discover -s tests -v`. Ne pas confondre ces mesures avec les tokens acceptés ou les performances du moteur. Voir `docs/OBSERVATEUR_L0.md`.

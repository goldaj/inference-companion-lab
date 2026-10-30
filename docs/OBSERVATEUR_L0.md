# Premier outil réel : observateur L0 passif (2026-10-29)

## Fonction effectivement ajoutée

`lab/scripts/observe_passive.py` est un canari d'ordonnancement non privilégié, sans dépendances externes. Il mesure le retard réel entre le réveil planifié d'un processus léger et son réveil observé par `perf_counter_ns`, produit p50/p95/p99 et renseigne l'empreinte temporelle CPU du **processus de mesure**. Il ne récupère aucun contenu d'activité utilisateur.

Ce jalon respecte « mesurer avant d'optimiser ». Il ne charge **aucun modèle** et ne propose aucune optimisation système.

## Exécuter sous Windows / PyCharm

```powershell
python lab/scripts/observe_passive.py --samples 40 --interval-ms 100
```

La sortie JSON apparaît seulement sur la console. Durée de la sonde : environ 4 secondes, sous conditions normales. Aucun fichier ni paramètre système modifié.

Pour exporter volontairement dans le laboratoire existant (créer au préalable le répertoire `results`) :

```powershell
python lab/scripts/observe_passive.py --samples 40 --interval-ms 100 --lab-root D:\InferenceCompanionLab --report results\L0_canary_01.json
```

Le programme exige la racine absolue, refuse toute traversée hors laboratoire, refuse d'écraser un fichier existant et ne crée pas silencieusement des dossiers. Le rapport contient seulement les mesures, la configuration, le type d'OS et le nombre de CPU logiques. Pas de modèle, trace personnelle ni secret.

## Mesures et interprétations

- `wake_delay_ms` est le retard du *canari de réveil* par rapport à son échéance.
- `observer_process_cpu_s` est le temps CPU du **processus de la sonde**, pas l'utilisation totale du CPU.
- `elapsed_s` est la durée murale ; `observer_process_cpu_over_wall_percent` n'est pas un équivalent de Task Manager.
- Les moyennes et quantiles sont calculés sur les événements observés, pas sur une métrique graphique fictive.

Ce protocole ne mesure pas : latence de l'interface utilisateur, température, puissance, disponibilité VRAM/GPU, inférence, débit en tokens ou fidélité E1. **Aucun gain de performance d'inférence ne peut être revendiqué à cette étape**.

## Sujets à mesurer ensuite

1. Exécuter au moins trois répétitions sans modèle sur le poste Windows, dans des conditions comparables : définir les processus de premier plan, relever les conditions et interpréter la variance.
2. Ajouter progressivement télémétrie mémoire et CPU système via API natives documentées, en non privilégié, avec gestion explicite des mesures indisponibles.
3. Établir un canari de réactivité orienté expérience utilisateur ; mesurer la surcharge propre de l'observateur.
4. Choisir ensuite le modèle et moteur de référence, l'empreinte du modèle, le contrat E1 et le budget de gêne, puis seulement construire la baseline B.
5. Conserver A/B/C/D sous traces identiques et distinguer absence d'inférence, politique statique et contrôleur adaptatif.

## Validation reproductible

`python -m unittest discover -s tests -v` vérifie les dates/sommeil simulés, les limites, les quantiles et l'écriture confinée. La CI exécute aussi une très courte sonde **sur un runner GitHub, pas sur le PC de référence**. Ses chiffres ne doivent pas être interprétés comme un benchmark du matériel utilisateur.

Le manifeste d'expérience global demeure `template_not_runnable` tant que modèle, moteur et oracle ne sont pas choisis. Ce canari L0 isolé ne transforme donc pas la phase A/B/C/D en résultat scientifique complet.

**Branche de livraison :** `feat/l0-passive-canary-observer-20261029`, ciblant `codex/foundation`. Lire `AGENTS.md` et le paquet documentaire fondateur avant reprise.

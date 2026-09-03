# Laboratoire opérationnel

Ce répertoire versionné contient les conventions, manifestes et scripts légers du laboratoire. Les données volumineuses et les résultats bruts vivent hors Git dans :

```text
D:\InferenceCompanionLab
```

## Séparation des responsabilités

| Emplacement | Contenu | Versionné |
| --- | --- | --- |
| dépôt Git | spécifications, code, exemples de configuration, petits rapports synthétiques | oui |
| `D:\InferenceCompanionLab\models` | modèles originaux, immuables logiquement | non |
| `D:\InferenceCompanionLab\derived` | représentations et plans dérivés | non |
| `D:\InferenceCompanionLab\traces` | traces d’activité synthétiques ou consenties | non |
| `D:\InferenceCompanionLab\runs` | manifestes et journaux de chaque exécution | non |
| `D:\InferenceCompanionLab\results` | mesures brutes et agrégats volumineux | non |
| `D:\InferenceCompanionLab\exports` | paquets de résultats à partager | non |
| `D:\InferenceCompanionLab\tmp` | temporaires recréables | non |
| `D:\InferenceCompanionLab\quarantine` | artefacts du laboratoire suspects ou invalides | non |

Le dépôt ne doit contenir ni poids de modèles, ni secrets, ni gros dumps matériels, ni contenu personnel capturé.

## Convention de run

Un run reçoit un identifiant du type :

```text
20260903T143000Z__exp-0001__scenario-a__rep-01
```

Son dossier doit contenir au minimum :

```text
manifest.json
environment.json
events.jsonl
metrics.jsonl
summary.json
```

Un run est incomplet tant que le manifeste, le statut final et la raison d’arrêt ne sont pas enregistrés.

## Provenance minimale

Chaque artefact dérivé doit être relié à :

- un hachage du modèle source ;
- la version du tokenizer et du format ;
- la version du moteur et du compilateur ;
- le descripteur de la machine ;
- la transformation et ses paramètres ;
- le niveau de fidélité vérifié ;
- les tests passés ou échoués.

Chaque résultat doit pouvoir être invalidé indépendamment sans effacer l’historique scientifique.

## Première expérience

La première étude compare :

- **A** : utilisateur seul, aucune inférence ;
- **B** : inférence à quota statique conservateur ;
- **C** : inférence à quota statique agressif ;
- **D** : politique adaptative simple avec pause et hystérésis.

Avant cela, l’observateur doit produire une baseline passive et son propre coût de mesure.

## État initial

Le laboratoire a été créé sans installation logicielle et sans modification persistante du poste. Le journal correspondant se trouve dans `INSTALLATIONS.md`.

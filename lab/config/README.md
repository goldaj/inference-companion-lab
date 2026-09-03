# Configurations expérimentales

Les fichiers de ce dossier sont des exemples versionnés. Un run réel doit en produire une copie résolue, sans variables implicites, dans son dossier sous `D:\InferenceCompanionLab\runs`.

Règles :

- ne jamais placer de secret dans un manifeste ;
- utiliser des chemins absolus dans le manifeste résolu ;
- enregistrer hachages et versions, pas seulement des noms ;
- séparer paramètres du modèle, moteur, politique compagnon et instrumentation ;
- refuser le démarrage si un champ obligatoire reste sous forme `REPLACE_ME` ;
- enregistrer les valeurs réellement appliquées, même lorsqu’elles diffèrent de la demande ;
- conserver le niveau de fidélité et l’oracle avec le résultat.

`experiment.example.json` décrit une expérience complète. `companion-policy.example.json` décrit la politique de partage de ressources indépendamment du moteur d’inférence.

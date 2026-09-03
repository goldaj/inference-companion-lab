# État vivant du projet

Dernière mise à jour : 2026-09-03

## Statut

- Dépôt Git : initialisé dans `C:\Users\golda\Documents\ChatGPT\software d'optimisation générale d'inférence`.
- Branche de fondation : `codex/foundation`.
- Racine des données de laboratoire : `D:\InferenceCompanionLab`.
- Stade : documentation fondatrice terminée ; spécification expérimentale v0.1 à finaliser avant le premier programme.
- Aucune dépendance de recherche n’a encore été installée.
- Aucune donnée utilisateur n’a été supprimée ou modifiée.
- Aucune modification de système, de firmware, de pilote, de fréquence ou de service n’a été effectuée.

## Décisions actives

1. L’utilisateur impose le modèle ; le système ne le remplace pas.
2. Le modèle original reste immuable.
3. Le mode compagnon est le premier produit et le premier sujet expérimental.
4. Le compagnon maximise les tokens validés sous une contrainte de non-gêne, et non l’utilisation brute de tous les composants.
5. L’inférence peut ralentir ou se suspendre lorsque les ressources minimales disparaissent.
6. Aucun effacement ou formatage ne fait partie du mode compagnon.
7. Les premiers essais seront non privilégiés et entièrement réversibles.
8. Le premier contrat de fidélité recommandé est E1 : mêmes tokens qu’une référence déterministe.
9. Le premier système mesure avant d’optimiser.
10. Les données lourdes sont séparées du dépôt Git.

## Premier poste de laboratoire

Profil préliminaire non intrusif :

- OS : Microsoft Windows 10 Famille 64 bits, version 10.0.19045.
- Carte mère : MSI Z170A SLI PLUS (MS-7998).
- CPU : Intel Core i5-6600K, 4 cœurs physiques, 4 processeurs logiques, fréquence nominale observée 3,50 GHz.
- RAM : 16 Gio, deux modules de 8 Gio, 2 133 MT/s configurés.
- GPU : NVIDIA GeForce GTX 1070, 8 192 Mio de VRAM confirmés par le pilote.
- Pilote NVIDIA : 560.94 au moment de l’inventaire.
- Stockage : Samsung SSD 750 EVO 250 Go et disque WDC 1 To.
- Espace libre lors de l’inventaire : environ 14 Gio sur `C:` et 372 Gio sur `D:`.
- Fichier d’échange : environ 19 Gio sur `D:` ; utilisation observée environ 3,2 Gio au moment de l’inventaire.
- Profil d’alimentation actif : Performances élevées.
- Présence d’un hyperviseur rapportée par Windows : oui ; interprétation à vérifier avant toute conclusion.

Le profil complet est dans `lab/machine/initial-host.md` et `lab/machine/initial-host.json`.

## Prochaine action recommandée

Finaliser la spécification expérimentale v0.1 en choisissant explicitement :

1. le premier modèle et son empreinte ;
2. le moteur de référence ;
3. le protocole de décodage déterministe ;
4. les longueurs de contexte et de génération ;
5. les canaris de qualité de service ;
6. la valeur ou la politique du budget d’interférence ;
7. la durée d’une trace expérimentale ;
8. l’inclusion ou l’amortissement du temps de chargement et d’autotuning.

Ensuite seulement : écrire l’observateur passif et établir les scénarios A/B/C/D décrits dans `docs/ROADMAP.md`.

## Questions ouvertes

- Quel modèle exact sera le premier cas ?
- Quel moteur servira de référence sémantique et de baseline de performance ?
- E1 suffit-il comme contrat initial, ou une référence numérique plus stricte est-elle souhaitée ?
- Quelle dégradation mesurable de la réactivité est acceptable dans le premier profil compagnon ?
- Faut-il commencer CPU seul pour isoler le contrôle, ou utiliser directement la GTX 1070 si le modèle rend le CPU expérimentalement impraticable ?
- Quelle durée d’utilisation attendue doit servir à amortir les artefacts compilés ?
- Quelles données de télémétrie peuvent être conservées et pendant combien de temps ?

## Conditions de reprise par une autre conversation

La conversation suivante ne doit pas repartir d’une recommandation de petit modèle ou d’un simple outil local existant. Elle doit reprendre au niveau d’un programme de R&D général, tout en conservant le périmètre expérimental étroit du premier jalon.

Lire `CONTEXT_TRANSFER.md` avant toute action.

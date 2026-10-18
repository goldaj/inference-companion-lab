# État vivant du projet

Dernière mise à jour : 2026-10-18

## Statut

- Dépôt Git : initialisé dans `C:\Users\golda\Documents\ChatGPT\software d'optimisation générale d'inférence`.
- Branche de fondation : `codex/foundation`.
- Dépôt distant : `https://github.com/goldaj/inference-companion-lab`, visibilité publique (décision du 2026-10-18), remote `origin`.
- Racine des données de laboratoire : `D:\InferenceCompanionLab`.
- Stade : documentation fondatrice, gouvernance documentaire et panel individuel terminés ; spécification expérimentale v0.1 à finaliser avant le premier programme.
- Source documentaire principale : Git ; toute tâche significative se termine par mise à jour documentaire, validation, commit, push et vérification du hash distant.
- Panel : douze individus synthétiques complets décrits dans `docs/PANEL_PERSONAS.md` version 2.0.
- Aucune dépendance d’inférence ou de mesure n’a encore été installée. GitHub CLI 2.99.0 a été installé pour sauvegarder le dépôt.
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
11. Git et le dépôt GitHub public constituent la source principale des documents et du code.
12. Les douze membres du panel possèdent une identité et une personnalité stables ; leurs caractéristiques démographiques n’ont aucune valeur de preuve technique.

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

## Publication pour le portfolio — 2026-10-18

Le propriétaire autorise la publication de cette recherche documentaire. La revue des fichiers et de toutes les références Git n’a détecté aucun secret avec Gitleaks ; la revue complémentaire n’a relevé ni adresse réseau privée, ni numéro de série, ni identifiant unique de machine. Le profil matériel décrit des caractéristiques génériques utiles à la reproductibilité. Les biographies du panel sont explicitement fictives.

Le dépôt est présenté comme une fondation de recherche : aucune mesure de gain, expérience d’inférence ou implémentation de moteur n’a été ajoutée. Les modèles, traces et données personnelles restent hors Git dans le laboratoire local. La bascule de visibilité GitHub suit le push et la vérification des hashes de ce jalon. La prochaine étape scientifique reste la spécification expérimentale v0.1.

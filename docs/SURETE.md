# Politique de sûreté, de privilèges et de récupération

Version : 0.1
Périmètre : poste de développement initial et futurs hôtes en mode compagnon

## 1. Principe directeur

Le logiciel cherche le meilleur débit d’inférence connu **à l’intérieur d’une enveloppe de sûreté explicite**. Il ne traite jamais la sécurité, l’intégrité des données ou le contrôle de l’utilisateur comme des ressources à sacrifier.

Une optimisation n’est acceptable que si son action est bornée, observable, attribuable, réversible lorsque nécessaire, et validée sous le contrat expérimental courant.

## 2. État de sûreté initial

Le projet démarre au niveau **L0 — observation passive** :

- aucune élévation administrateur ;
- aucun arrêt de service ;
- aucune désinstallation ;
- aucun effacement de données ;
- aucune modification persistante du système ;
- aucun changement de pilote, BIOS ou firmware ;
- aucune modification de tension, fréquence ou limite thermique ;
- aucune exécution d’un artefact provenant d’un modèle comme instruction système.

Les seules écritures initiales sont les fichiers du dépôt et du laboratoire explicitement créés pour le projet.

## 3. Échelle de privilèges

### L0 — Observation passive

Lecture de caractéristiques statiques, compteurs documentés et état instantané. Aucun changement de politique du système.

### L1 — Contrôle du processus du projet

Allocation et libération de mémoire par le processus, nombre de threads, affinité non privilégiée, priorité autorisée, cadence d’inférence, pause, reprise, caches du projet et fichiers du laboratoire.

### L2 — Réglage temporaire borné

Changement temporaire d’un paramètre documenté, limité au projet ou restauré automatiquement à l’arrêt. Il exige une valeur initiale enregistrée, une valeur cible bornée, une durée maximale, une vérification et une restauration testée.

### L3 — Action administrateur ciblée

Une petite interface privilégiée peut réaliser une opération précisément listée. Elle ne reçoit ni script arbitraire ni instruction issue du modèle. Chaque opération exige une autorisation explicite, un journal avant/après et un chemin de retour arrière.

### L4 — Mode poste dédié

Reconfiguration profonde, désinstallation ou image système spécialisée. Ce niveau appartient à une phase distincte, sur un poste déclaré dédié, avec sauvegarde vérifiée et procédure de restauration. Il n’est pas autorisé par le mode compagnon.

Le projet ne monte de niveau que lorsqu’un test de niveau inférieur a montré la nécessité et quantifié le gain potentiel.

## 4. Interdictions du mode compagnon

- Exploiter une vulnérabilité ou contourner les limites de sécurité de l’OS.
- Court-circuiter silencieusement l’antivirus, le chiffrement, les contrôles d’accès ou les protections thermiques.
- Modifier un firmware ou un pilote sans protocole séparé, sauvegarde et autorisation ciblée.
- Tuer un processus utilisateur pour récupérer une ressource.
- Supprimer un fichier, une application ou une donnée qui ne provient pas du laboratoire.
- Écrire hors du dépôt et du laboratoire sans opération annoncée et justifiée.
- Dépasser les limites documentées de température, tension, courant ou puissance.
- Exécuter du code ou des commandes extraits des poids, métadonnées, prompts ou sorties du modèle.
- Masquer une divergence numérique, un crash, une gêne utilisateur ou un résultat négatif.
- Présenter un pic bref comme débit durable.

## 5. Modèle de menace minimal

### Entrées non fiables

Sont considérés comme des données non fiables : modèles, métadonnées, tokenizers, fichiers de configuration importés, prompts, sorties, plugins, kernels téléchargés et résultats provenant d’une autre machine.

Le parseur de modèle et les convertisseurs doivent être traités comme une surface d’attaque. À terme, ils devront fonctionner avec validation stricte des tailles, limites de ressources et isolation appropriée.

### Confusion données/instructions

Aucun contenu du modèle ou d’un benchmark ne peut autoriser une commande, une installation ou un changement de privilège. L’autorité provient uniquement d’une politique du projet validée par l’utilisateur.

### Déni de service local

Le superviseur doit borner RAM, VRAM, stockage, threads, files d’attente et durée d’une opération. Une demande d’allocation irréalisable doit échouer proprement, sans pousser l’hôte à la pagination incontrôlée.

### Corruption et dérive

Les poids originaux sont en lecture seule du point de vue logique. Les artefacts dérivés sont adressés par le hachage du modèle, du moteur, du compilateur, de la machine et de la transformation. Un artefact dont la provenance ne correspond pas ne doit pas être réutilisé.

## 6. Réversibilité

Toute action L2 ou L3 doit posséder un enregistrement transactionnel :

```text
identifiant de l’action
raison et expérience associée
état observé avant
commande ou API exacte
valeur cible et bornes
horodatage et durée maximale
condition d’arrêt
méthode de vérification
opération de restauration
état vérifié après restauration
```

Une action sans méthode de restauration crédible est persistante et doit être traitée comme telle, même si sa documentation la présente comme temporaire.

L’affirmation « même état avant et après » signifie ici : mêmes données utilisateur, mêmes applications et services, mêmes réglages persistants intentionnels. Elle ne signifie pas identité physique des cellules mémoire, températures, compteurs d’usure, caches ou énergie consommée.

## 7. Arrêt d’urgence et repli

Le futur runtime devra disposer d’au moins quatre voies d’arrêt indépendantes :

1. bouton ou commande utilisateur ;
2. canari de latence déclenchant la pause ;
3. garde mémoire/thermique déclenchant la libération ;
4. surveillance du processus capable de terminer le worker et nettoyer ses ressources.

La politique sûre par défaut est : **en cas d’incertitude, ralentir puis mettre en pause**. Une reprise exige une période de stabilité et de l’hystérésis.

Après crash, les verrous, fichiers temporaires et artefacts incomplets doivent être reconnaissables et nettoyables dans le seul laboratoire. Aucun nettoyage générique du système n’est autorisé.

## 8. Budget de gêne et ressources

Les limites ne se réduisent pas à un pourcentage CPU. La politique doit considérer simultanément :

- latence interactive et files d’attente ;
- RAM disponible et pression de pagination ;
- VRAM disponible et coût de restitution ;
- bande passante mémoire et stockage ;
- température, puissance et fréquence soutenue ;
- activité audio/vidéo, réseau et périphériques lorsque mesurable sans inspecter le contenu ;
- délai de pause et de reprise.

Une ressource inutilisée en capacité peut être indisponible en bande passante, en latence ou en enveloppe thermique.

## 9. Vie privée

Le mode compagnon doit préférer des signaux structurels : files d’attente, temps de réponse, utilisation, pression mémoire, températures et changements de premier plan lorsque cela peut être obtenu sans contenu.

Il ne doit pas enregistrer frappes, captures d’écran, noms de documents, textes, historique de navigation ou contenu audio afin d’inférer l’activité. Toute instrumentation plus intrusive demanderait un besoin scientifique précis, un consentement séparé, une rétention minimale et une alternative moins intrusive examinée.

## 10. Intégrité des performances annoncées

Un résultat publiable doit inclure : modèle et hachage, moteur, niveau de fidélité, charge, contexte, paramètres d’échantillonnage, machine, température, puissance, mémoire, répétitions, dispersion, métriques de QoS et coûts de préparation/migration.

Il est interdit de compter :

- des tokens rejetés par l’oracle de fidélité ;
- un débit obtenu sur une charge différente ;
- un gain dû à un contexte, batch ou niveau de qualité non comparable ;
- la compilation hors du temps total sans publier son coût et son amortissement ;
- une mesure pendant un état thermique transitoire comme performance soutenue.

## 11. Procédure avant toute installation

Avant d’installer un outil, documenter dans `lab/INSTALLATIONS.md` :

1. le besoin exact ;
2. l’éditeur et la source ;
3. la version et, si possible, le hachage ;
4. les fichiers, services, pilotes et variables susceptibles d’être modifiés ;
5. la méthode de désinstallation ou de restauration ;
6. l’alternative portable ou déjà présente ;
7. le bénéfice attendu pour l’expérience courante.

L’autorisation générale d’installer des dépendances ne transforme pas un pilote, un hyperviseur, un réglage firmware ou une désactivation de protection en opération ordinaire. Ces actions exigent une décision ciblée.

## 12. Critères de passage vers une action privilégiée

Une action L3 n’est recevable que si :

- une baseline L0/L1 existe ;
- le goulet d’étranglement est démontré ;
- l’API privilégiée visée a un lien causal avec ce goulet ;
- le gain maximal plausible justifie le risque ;
- P09 a validé le périmètre et la récupération ;
- l’utilisateur a autorisé cette action précise ;
- un arrêt indépendant et un contrôle après restauration sont disponibles.

## 13. Incident et quarantaine

Tout crash, divergence, surchauffe, ralentissement sévère ou écriture inattendue entraîne :

1. arrêt de l’expérience ;
2. conservation des journaux pertinents ;
3. déplacement logique des artefacts concernés vers `D:\InferenceCompanionLab\quarantine` sans exécution ultérieure ;
4. description de l’incident et de l’état de l’hôte ;
5. analyse avant reprise ;
6. ajout d’un test empêchant la récurrence lorsque possible.

La quarantaine n’autorise jamais à déplacer ou modifier une donnée utilisateur : seulement les artefacts créés ou importés explicitement dans le laboratoire.

# Journal des installations et modifications de l’hôte

Ce journal doit être mis à jour **avant et après** chaque installation, mise à niveau, ajout de pilote, création de service ou modification persistante utile au projet.

## État initial — 2026-09-03

- Aucun logiciel installé pour le projet.
- Aucun paquet mis à niveau.
- Aucun service créé, arrêté, désactivé ou reconfiguré.
- Aucun pilote, BIOS ou firmware modifié.
- Aucun réglage de sécurité, de puissance ou de fréquence modifié.
- Aucun fichier utilisateur supprimé ou déplacé.
- Écritures effectuées : dépôt Git du projet et création de `D:\InferenceCompanionLab` avec ses sous-répertoires dédiés.

## GitHub CLI — 2026-09-03

- Statut : installation réussie et vérifiée.
- Statut avant opération : GitHub CLI absent ; aucun remote Git configuré.
- Besoin : créer le dépôt privé de sauvegarde demandé par l’utilisateur, authentifier son compte et pousser le dépôt local.
- Composant : GitHub CLI (`GitHub.cli`).
- Éditeur et source : GitHub, Inc., catalogue officiel WinGet.
- Version proposée par WinGet : 2.99.0.
- Installateur annoncé : `gh_2.99.0_windows_amd64.msi`.
- SHA-256 annoncé par WinGet : `43c2035cb8ee77cfb44462c42ecb9e409a112ff6e53af96c19cf12be62a4d7b1`.
- Privilège de projet : L2, installation persistante d’un outil utilisateur/système ; aucune action matérielle.
- Alternative examinée : création manuelle dans le navigateur puis ajout d’un remote Git. Elle imposerait davantage d’étapes manuelles et ne simplifierait pas l’authentification reproductible.
- Changements attendus : installation de la commande `gh` et ajout de son emplacement au `PATH` pour les nouvelles sessions.
- Retour arrière prévu : `winget uninstall --id GitHub.cli --exact`, puis suppression explicite des identifiants GitHub CLI si l’utilisateur le demande.
- Vérification de l’installation : WinGet a confirmé le hachage de l’installateur et la réussite de l’installation ; `gh --version` rapporte 2.99.0.
- Authentification : compte GitHub `goldaj`, protocole Git HTTPS, identifiant conservé par le trousseau système de GitHub CLI. Aucun jeton n’est stocké dans le dépôt.
- Portée GitHub : dépôt privé `goldaj/inference-companion-lab`, remote `origin`.
- Résultat : dépôt distant créé ; publication et vérification effectuées dans la même séquence opérationnelle que cette entrée.

## Gabarit d’entrée

```text
Date et heure :
Expérience / décision associée :
Besoin :
Outil ou composant :
Éditeur / source officielle :
Version :
Hachage de l’installateur ou du paquet :
Privilège requis : L0 / L1 / L2 / L3 / L4
Alternative sans installation examinée :
Changements attendus :
Procédure de retour arrière :
Autorisation ciblée si nécessaire :

Résultat de l’installation :
Changements réellement observés :
Vérification :
Résultat du retour arrière, le cas échéant :
```

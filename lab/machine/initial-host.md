# Profil initial du poste de laboratoire

Date de l’inventaire : 2026-09-03
Nature : photographie initiale, lecture seule
Niveau de confiance : caractéristiques statiques élevées ; métriques d’utilisation instantanées transitoires

## Système

- Système : Microsoft Windows 10 Famille, 64 bits
- Version : 10.0.19045
- Fabricant / modèle : MSI / MS-7998
- Carte mère : MSI Z170A SLI PLUS (MS-7998)
- BIOS : American Megatrends Inc. 1.60, daté du 23 mai 2016
- Mode d’alimentation observé : Performances élevées

## Processeur

- Intel Core i5-6600K à 3,50 GHz
- 4 cœurs physiques, 4 processeurs logiques
- Architecture 64 bits
- Fréquence maximale rapportée par WMI : 3 504 MHz

Les jeux d’instructions réellement disponibles et utilisables par le processus restent à vérifier avec une sonde dédiée ; ils ne doivent pas être inférés uniquement du nom commercial.

## Mémoire

- Mémoire installée rapportée : 17 137 790 976 octets, soit environ 16 Gio
- Deux modules de 8 Gio
- Vitesse configurée rapportée : 2 133 MT/s

## Accélérateur graphique

- NVIDIA GeForce GTX 1070
- VRAM confirmée par `nvidia-smi` : 8 192 Mio
- Pilote NVIDIA observé : 560.94

Photographie transitoire lors de l’inventaire : environ 4 290 Mio libres, P0, 56 °C, 31,77 W sur une limite rapportée de 151 W, 29 % d’utilisation GPU et 7 % d’utilisation mémoire. Ces nombres ne décrivent pas une capacité stable et ne doivent pas être utilisés comme baseline.

WMI a rapporté une taille mémoire graphique incohérente d’environ 4 Gio, limite classique de ce champ. La valeur `nvidia-smi` est retenue pour l’inventaire, mais toute sonde future devra conserver la source de chaque mesure.

## Stockage

- Samsung SSD 750 EVO, environ 250 Go
- Western Digital WDC WD10EZEX, environ 1 To
- Volume `C:` NTFS : environ 249 Go, 15 025 225 728 octets libres lors de l’inventaire, soit environ 14 Gio
- Volume `D:` : environ 1 To, 399 888 130 048 octets libres lors de l’inventaire, soit environ 372 Gio
- Fichier d’échange : `D:\pagefile.sys`, allocation rapportée 19 642 Mio

Le laboratoire volumineux est placé sur `D:` afin de ne pas aggraver la faible marge disponible sur `C:`. Cela ne prouve pas encore que `D:` est le meilleur emplacement pour tous les accès à faible latence ; cette question devra être mesurée.

## Virtualisation

- `HypervisorPresent` a été rapporté vrai.
- `VirtualizationFirmwareEnabled` a été rapporté faux par une autre source WMI.

Ces observations sont apparemment contradictoires. Elles ne doivent pas être transformées en conclusion tant qu’une sonde plus précise n’a pas distingué hyperviseur actif, VBS, capacités du firmware et visibilité depuis l’OS.

## Conséquences initiales

- La VRAM de 8 Gio et la RAM de 16 Gio imposeront probablement des choix serrés pour les modèles dont l’ensemble de travail approche ou dépasse ces capacités.
- La coexistence GPU/CPU/RAM/disque mérite d’être testée, mais chaque transfert peut coûter plus qu’il ne rapporte.
- La faible marge sur `C:` interdit d’y laisser grossir caches, modèles ou traces.
- Le premier travail doit mesurer les ressources, leur contention et la gêne avant toute optimisation invasive.

## Ce que cet inventaire ne prétend pas connaître

- bande passante mémoire réellement soutenue ;
- capacités exactes des instructions CPU et bibliothèques ;
- latence et débit réels des deux disques ;
- puissance et températures stabilisées en charge ;
- capacité de préemption du GPU dans le moteur choisi ;
- performances d’un modèle donné ;
- tolérance concrète de l’utilisateur à la gêne.

Ces points appartiennent à l’observateur et aux premières expériences, pas à une supposition documentaire.

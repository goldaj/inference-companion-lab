# Panel de recherche et protocole de délibération

Version : 0.1
Statut : panel de référence pour le programme de recherche

## 1. Pourquoi un panel

Le projet traverse plusieurs disciplines dont aucune ne peut, isolément, garantir un bon résultat : inférence de réseaux de neurones, systèmes d’exploitation, compilateurs, microarchitecture, contrôle en ligne, métrologie, sûreté et expérience utilisateur.

Le mot « persona » désigne ici une fonction critique à incarner, par un humain ou un agent, et non une autorité fictive. Une persona doit produire un raisonnement falsifiable, indiquer ses incertitudes et pouvoir être contredite par les mesures.

Le panel a quatre fonctions :

1. produire des hypothèses indépendantes ;
2. exposer les conflits entre performance, exactitude, sûreté et confort ;
3. construire des expériences capables de réfuter les hypothèses ;
4. empêcher qu’un gain local soit pris pour un progrès du système entier.

## 2. Les douze personas de référence

### P01 — Directeur ou directrice de recherche et intégration

**Mandat :** maintenir la cohérence du problème, arbitrer les dépendances et convertir les idées en décisions explicites.

**Questions obligatoires :**

- Quel objectif mesurable cette proposition sert-elle ?
- Quelle hypothèse est testée ?
- Quel résultat ferait abandonner ou reformuler la piste ?
- Quel est le plus petit test informatif ?

**Livrables :** synthèse, ordre des expériences, registre des décisions, définition de « terminé ».

**Biais à surveiller :** consensus prématuré, plan trop vaste, préférence implicite pour une technologie.

### P02 — Architecte runtime et systèmes d’exploitation

**Mandat :** concevoir l’observateur, le superviseur, la préemption, la reprise et l’isolation du mode compagnon.

**Questions obligatoires :**

- Quelles ressources sont réellement contrôlables depuis l’espace utilisateur ?
- Quel est le coût et le délai de préemption de chaque sous-système ?
- Quel état doit survivre à une pause ou à un changement de plan ?
- Comment arrêter proprement le système en cas d’incertitude ?

**Livrables :** frontières de processus, API de contrôle, machine à états, chemins de repli.

**Droit d’arrêt :** comportement non borné, absence de pause fiable, corruption possible de l’hôte.

### P03 — Spécialiste compilateurs, graphes et représentation intermédiaire

**Mandat :** transformer le modèle en représentations et plans exécutables spécialisés sans modifier le contrat choisi.

**Questions obligatoires :**

- Quelle information du graphe, des poids et de la machine doit être conservée dans l’IR ?
- Quelle transformation est exacte, tolérée, ou sémantiquement modificatrice ?
- Quelle preuve ou quel test accompagne la transformation ?
- Le temps de compilation peut-il être amorti ?

**Livrables :** IR multi-niveaux, passes, manifeste de plan, cache adressé par contenu.

**Biais à surveiller :** compiler pour un benchmark au lieu du régime réel ; confondre élégance de l’IR et débit.

### P04 — Ingénieur ou ingénieure de kernels CPU/GPU

**Mandat :** produire et mesurer les primitives de calcul adaptées au CPU, au GPU et à leur coopération.

**Questions obligatoires :**

- La primitive est-elle limitée par le calcul, la bande passante, la latence ou les synchronisations ?
- Quelle disposition mémoire et quelle granularité conviennent au matériel concret ?
- Le transfert ou la conversion annule-t-il le gain du kernel ?
- Le résultat respecte-t-il le contrat numérique ?

**Livrables :** microbenchmarks, kernels candidats, profils de performance, résultats de validation.

### P05 — Spécialiste microarchitecture, mémoire et énergie

**Mandat :** relier compteurs matériels, topologie, caches, RAM, VRAM, stockage, alimentation et thermique au débit soutenable.

**Questions obligatoires :**

- Où se situe le goulet d’étranglement dominant dans chaque régime ?
- Quelle ressource paraît libre mais partage un chemin critique avec l’utilisateur ?
- Le débit est-il soutenable après stabilisation thermique ?
- Quels compteurs sont fiables sur ce poste précis ?

**Livrables :** carte de la machine, modèle de bande passante, enveloppes thermiques, bornes conditionnelles.

**Biais à surveiller :** extrapoler une capacité théorique à partir d’une fiche technique.

### P06 — Spécialiste inférence numérique et fidélité du modèle

**Mandat :** définir et vérifier ce que signifie « le même modèle » pour chaque expérience.

**Questions obligatoires :**

- Le contrat est-il E0, E1, E2 ou E3 ?
- Quelles sources de non-déterminisme existent ?
- Les logits, tokens, distributions et comportements divergent-ils ?
- Une optimisation change-t-elle réellement le modèle ?

**Livrables :** oracle de référence, jeux de validation, seuils, rapport de divergence.

**Droit d’arrêt :** gain annoncé sans contrôle de fidélité ou comparaison sous contrats différents.

### P07 — Spécialiste contrôle en ligne, qualité de service et thermique

**Mandat :** convertir le slack observé en décisions stables et prudentes sous incertitude.

**Questions obligatoires :**

- Quels canaris reflètent réellement la gêne ressentie ?
- Quelle enveloppe et quelle marge de sécurité utiliser ?
- Quel horizon amortit un changement de plan ?
- Comment éviter oscillations, emballement thermique et faux positifs ?

**Livrables :** contrôleur, seuils adaptatifs, hystérésis, politique de repli, courbes de compromis.

### P08 — Expérimentateur ou expérimentatrice et métrologue

**Mandat :** rendre toute affirmation reproductible et statistiquement interprétable.

**Questions obligatoires :**

- La charge, les graines, la température, le contexte et la configuration sont-ils fixés ?
- La mesure perturbe-t-elle le phénomène ?
- Quelle variance existe entre répétitions et entre sessions ?
- Un témoin négatif et une baseline indépendante sont-ils présents ?

**Livrables :** protocole, manifeste de run, données brutes, analyse d’incertitude, rapport reproductible.

**Droit d’arrêt :** benchmark non reproductible, comparaison déséquilibrée, sélection opportuniste des résultats.

### P09 — Responsable sûreté, sécurité et récupération

**Mandat :** réduire la surface privilégiée, borner les actions et garantir une récupération compréhensible.

**Questions obligatoires :**

- Pourquoi ce privilège est-il nécessaire ?
- La même expérience peut-elle être menée avec moins d’autorité ?
- Quelle action exacte sera effectuée, comment sera-t-elle annulée et vérifiée ?
- Un modèle, un plugin ou un fichier non fiable peut-il devenir une instruction système ?

**Livrables :** analyse de menace, niveaux de privilège, journal d’actions, plan de retour arrière.

**Droit d’arrêt :** suppression non ciblée, exploitation d’une faille, modification firmware opaque, absence de récupération.

### P10 — Théoricien ou théoricienne des limites physiques et algorithmiques

**Mandat :** séparer les limites de représentation, de communication, de calcul, d’énergie et d’observabilité.

**Questions obligatoires :**

- Quelle borne est universelle, conditionnelle, empirique ou seulement heuristique ?
- Quelle quantité d’information minimale doit être lue ou conservée ?
- Quelle dépendance séquentielle empêche le parallélisme ?
- L’idée déplace-t-elle le coût au lieu de le réduire ?

**Livrables :** bornes conditionnelles, hypothèses explicites, ratios d’efficacité, impossibilités partielles.

**Biais à surveiller :** invoquer la physique comme décoration ; prétendre prouver un optimum global sur un système non fermé.

### P11 — Falsificateur ou falsificatrice contradictoire

**Mandat :** chercher activement comment la proposition peut être fausse, fragile ou trompeuse.

**Questions obligatoires :**

- Quel effet confondu explique le gain observé ?
- Quel cas limite provoque une régression ?
- Quelle métrique a été omise ?
- Quelle hypothèse tacite empêche la généralisation ?

**Livrables :** contre-exemples, expériences adversariales, liste des affirmations invalidées ou affaiblies.

**Droit d’arrêt :** conclusion irréfutable par construction ou vocabulaire absolu sans preuve.

### P12 — Représentant ou représentante de l’utilisateur, de la vie privée et du produit

**Mandat :** défendre l’utilité réelle : l’utilisateur doit pouvoir travailler, comprendre le mode actif et reprendre immédiatement ses ressources.

**Questions obligatoires :**

- Quel ralentissement ou changement perceptible est acceptable ?
- Les signaux nécessaires révèlent-ils le contenu de l’activité ?
- L’interface explique-t-elle pourquoi le système accélère, ralentit ou s’arrête ?
- Le gain justifie-t-il la complexité, le stockage et la consommation ?

**Livrables :** scénarios d’usage, budget de gêne, exigences de confidentialité, critères d’acceptation.

**Droit d’arrêt :** captation inutile du contenu utilisateur, absence de contrôle clair, restauration lente ou opaque.

## 3. Composition selon la décision

Tout le panel n’a pas besoin d’intervenir à chaque microdécision. Le quorum dépend du risque.

| Décision | Personas minimales |
| --- | --- |
| Nouvelle métrique ou benchmark | P01, P08, P11, P12 |
| Changement de runtime non privilégié | P02, P07, P08, P09 |
| Nouveau kernel ou plan matériel | P03, P04, P05, P06, P08 |
| Transformation du modèle | P03, P06, P08, P11 |
| Action administrateur ou réglage persistant | P02, P05, P09, P12 |
| Affirmation de limite ou d’optimalité | P05, P08, P10, P11 |
| Nouveau kernel, langage ou OS complet | P01, P02, P03, P05, P08, P10, P11 |

Le rôle P09 peut bloquer une action dangereuse. Le rôle P06 peut bloquer une affirmation de performance si le contrat du modèle n’est plus respecté. Le rôle P08 peut bloquer une conclusion non mesurable. Le rôle P12 peut bloquer une politique compagnon qui viole le budget de gêne.

## 4. Protocole de brainstorming

### Étape 1 — Brief commun

Donner à chaque persona le même contrat expérimental, les mêmes données et la même question. Distinguer explicitement les faits, hypothèses et souhaits.

### Étape 2 — Avis indépendants

Les personas répondent avant de lire les conclusions des autres. Cela réduit l’ancrage et le consensus artificiel.

Chaque avis doit contenir :

- une conclusion provisoire ;
- les trois hypothèses les plus fragiles ;
- un mécanisme causal ;
- un test minimal ;
- un critère d’abandon ;
- les risques et inconnues.

### Étape 3 — Matrice de contradictions

Le directeur de recherche ne cherche pas immédiatement un compromis. Il recense d’abord les désaccords : métriques incompatibles, hypothèses opposées, estimations de coût et niveaux de risque.

### Étape 4 — Expériences discriminantes

Le panel choisit les expériences qui départagent plusieurs explications, plutôt que celles qui illustrent seulement l’idée préférée.

### Étape 5 — Revue contradictoire

P11 tente de casser la conclusion. P08 vérifie le protocole. Les détenteurs d’un droit d’arrêt statuent sur leur domaine.

### Étape 6 — Décision et traçabilité

La décision, ses raisons, les alternatives rejetées et la preuve attendue sont inscrites dans `docs/DECISIONS.md` ou dans un futur ADR dédié.

## 5. Gabarit réutilisable pour convoquer une persona

```text
Rôle : [Pxx et intitulé]
Question : [question unique et falsifiable]
Contexte expérimental : [modèle, hôte, moteur, charge, niveau E0-E3]
Contraintes : [QoS, température, mémoire, énergie, temps, privilèges]
Faits disponibles : [mesures et sources]
Hypothèses à distinguer : [H1, H2, ...]

Produire :
1. conclusion provisoire et niveau de confiance ;
2. mécanisme causal proposé ;
3. inconnues critiques ;
4. test minimal et instrumentation ;
5. critère de succès et critère d’abandon ;
6. risques, retour arrière et effets confondus ;
7. données qu’il serait trompeur de ne pas publier.
```

## 6. Règles contre le théâtre de personas

- Un nom de rôle n’ajoute aucune crédibilité à une affirmation sans mécanisme ni mesure.
- Une majorité de personas ne remplace pas une expérience.
- Les personas ne doivent pas inventer des capacités du matériel ou des garanties du système d’exploitation.
- L’intégrateur doit conserver les avis minoritaires testables.
- Une même personne ou un même agent peut incarner plusieurs rôles, mais les avis doivent rester séparés avant la synthèse.
- Les résultats négatifs ont la même valeur documentaire que les gains.

## 7. Panel initial recommandé

Pour la première expérience A/B/C/D sur ce poste, activer P01, P02, P05, P07, P08, P09, P11 et P12. P03, P04 et P06 rejoignent la revue dès qu’un moteur et un modèle précis sont choisis. P10 intervient pour construire les premières bornes conditionnelles et empêcher les affirmations abusives d’optimalité.

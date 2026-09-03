# Charte de recherche et protocole de preuve

Version : 0.1
Statut : normative pour le démarrage du projet

## 1. Objet

Cette charte définit les règles qui empêchent le projet de confondre une optimisation réelle avec une modification du modèle, une altération de la charge de travail, une mesure biaisée ou une prise de risque injustifiée.

Elle s’applique aux benchmarks, autotuners, kernels, plans de placement, changements de représentation, contrôleurs de ressources et recherches avancées.

## 2. Invariants

### 2.1 Modèle imposé

Le modèle, ses poids, son tokenizer et sa configuration sont choisis par l’utilisateur. La substitution par un autre modèle ne constitue pas une optimisation valide.

### 2.2 Original immuable

Le modèle original est conservé en lecture seule et identifié par SHA-256. Les artefacts dérivés sont séparés et doivent inclure :

- empreinte de l’original ;
- version du compilateur ;
- cible matérielle ;
- pilote ;
- niveau de fidélité ;
- transformations ;
- tests réussis ;
- date de création.

### 2.3 Utilisateur prioritaire

En mode compagnon, le débit d’inférence est subordonné à la qualité de service définie pour l’utilisateur. Une pause est un comportement valide.

### 2.4 Réversibilité

Aucune action permanente ne fait partie du premier jalon. Toute évolution future doit fournir une opération inverse et un mécanisme de récupération indépendant.

### 2.5 Tokens validés

Un token n’est compté que s’il appartient à la sortie acceptée du modèle cible selon le contrat d’exécution. Les brouillons rejetés, calculs internes et sorties hors contrat ne sont pas des tokens produits.

## 3. Contrat expérimental

Chaque expérience doit figer avant son lancement :

- identifiant unique ;
- question de recherche ;
- hypothèse falsifiable ;
- machine et état de départ ;
- modèle et empreinte ;
- moteur et version ;
- niveau de fidélité ;
- tokenizer ;
- sampling, seed et critères d’arrêt ;
- prompts ou générateur de charge ;
- longueurs de contexte ;
- batch et concurrence ;
- conditions de cache froid ou chaud ;
- durée d’échauffement ;
- durée mesurée ;
- température initiale ou protocole de stabilisation ;
- métriques ;
- seuils de sûreté ;
- budget d’interférence ;
- transformations autorisées ;
- règle de succès et d’échec.

Toute modification après le début crée une nouvelle expérience ou une nouvelle révision explicitement liée.

## 4. Niveaux de fidélité

### E0 — Bit-exact

Même représentation numérique ou résultat bit à bit selon une référence définie. Employer uniquement lorsque la comparaison interplateforme n’est pas nécessaire ou lorsque le sous-problème permet une preuve exacte.

### E1 — Token-exact déterministe

Même séquence de tokens pour un protocole déterministe, sur le corpus de validation publié. C’est le niveau initial recommandé.

E1 ne prouve pas l’égalité sur toutes les entrées. Il garantit une couverture expérimentale et doit être accompagné, lorsque possible, de comparaisons de logits ou d’opérateurs.

### E2 — Distribution préservée

La loi de sortie respecte une distance statistique et un protocole définis. Adapté aux méthodes spéculatives correctement vérifiées et à l’échantillonnage.

### E3 — Équivalence comportementale

La qualité sur un ensemble de tâches reste dans une tolérance. Ce niveau autorise des transformations beaucoup plus fortes et ne doit jamais être présenté comme E0, E1 ou E2.

## 5. Métriques obligatoires

### 5.1 Performance du modèle

- temps de chargement ;
- temps au premier token ;
- débit de préremplissage ;
- débit de décodage ;
- tokens acceptés cumulés ;
- latence inter-token p50, p95 et p99 ;
- coût de compilation ou d’autotuning ;
- nombre et durée des pauses ;
- coût des migrations.

### 5.2 Ressources

- CPU global et par cœur ;
- mémoire engagée et résidente ;
- pression mémoire et fautes de page ;
- GPU et VRAM lorsque disponibles ;
- E/S ;
- fréquence ;
- température ;
- puissance et énergie lorsque accessibles ;
- throttling ou erreurs rapportées.

### 5.3 Qualité de service utilisateur

- latence des canaris ;
- dégradation relative à la baseline A ;
- interruptions ou violations ;
- durée passée au-dessus des seuils ;
- réserve mémoire et VRAM restante.

## 6. Séparation des phases

Les mesures de préremplissage et de décodage ne doivent pas être fusionnées en un chiffre unique sans détail. Le chargement, la compilation et l’échauffement doivent être publiés séparément, même lorsqu’ils sont amortis dans l’objectif principal.

## 7. Baselines

Toute innovation doit être comparée à :

1. une implémentation de référence correcte ;
2. le meilleur réglage raisonnablement disponible du moteur utilisé ;
3. le dernier meilleur plan validé du projet ;
4. en mode compagnon, une stratégie statique conservatrice soumise au même budget de gêne.

Réimplémenter un mécanisme existant plus lentement n’est pas un progrès, même si la nouvelle architecture est plus élégante.

## 8. Interdiction des faux gains

Un résultat est invalide si, sans le déclarer, il :

- change le modèle ;
- modifie les poids ;
- réduit le contexte ;
- change les prompts ;
- change le batch ;
- change le sampling ;
- compte des tokens rejetés ;
- exclut une phase coûteuse incluse chez le concurrent ;
- compare un système froid à un système chaud ;
- mesure un pic avant throttling comme débit soutenu ;
- ignore une divergence ;
- ignore la gêne imposée au poste ;
- échoue à reproduire ses conditions.

## 9. Mesure en régime dynamique

Le mode compagnon doit être évalué sur des traces identiques. Les scénarios A/B/C/D reçoivent la même séquence de charges et les mêmes paramètres de modèle.

L’ordre des essais doit être alterné ou randomisé lorsque les effets thermiques ou de cache risquent de biaiser les résultats. Des répétitions sont nécessaires pour estimer la variance.

## 10. Borne et efficacité

Chaque fois que possible, calculer une borne conditionnelle à partir de :

- opérations minimales ;
- octets par niveau mémoire ;
- bande passante soutenue ;
- capacité ;
- latence du chemin critique ;
- puissance soutenable.

Publier :

- résultat mesuré \(R\) ;
- borne \(U\) ;
- efficacité \(R/U\) ;
- hypothèses ;
- incertitude ;
- ressource limitante.

Ne jamais présenter \(U\) comme une limite physique universelle si elle dépend d’une représentation ou d’une famille de programmes.

## 11. Falsifiabilité

Chaque piste de recherche doit avoir une expérience capable de conclure qu’elle ne vaut pas la poursuite.

Exemples :

- une compression sans perte est abandonnée si le coût de décodage dépasse le trafic économisé ;
- un accélérateur est écarté si les conversions et transferts annulent son gain ;
- un changement de plan est refusé si son coût n’est pas amorti ;
- un OS minimal n’est pas développé si l’OS actuel ne représente pas un goulot significatif ;
- un contrôleur appris est rejeté s’il viole plus souvent le budget qu’une politique déterministe.

## 12. Résultats négatifs

Un résultat négatif doit documenter :

- hypothèse ;
- configuration ;
- mesure ;
- raison probable ;
- conditions où la conclusion pourrait changer ;
- décision : abandon, pause ou reformulation.

Les résultats négatifs empêchent de répéter les mêmes fausses pistes.

## 13. Reproductibilité

Chaque résultat retenu doit fournir :

- commit Git ;
- configuration ;
- versions ;
- profil de machine ;
- commande ou plan ;
- données synthétiques suffisantes ;
- empreintes ;
- protocole de reproduction ;
- résumé des données brutes conservées hors Git.

## 14. Décision scientifique

Une affirmation de gain doit être examinée par au moins :

- la personne ou persona qui propose ;
- l’expérimentaliste ;
- le falsificateur ;
- le spécialiste fidélité si le calcul change ;
- le spécialiste sûreté si les privilèges ou limites matérielles changent.

La décision finale doit être ajoutée à `docs/DECISIONS.md` lorsqu’elle affecte durablement l’architecture.

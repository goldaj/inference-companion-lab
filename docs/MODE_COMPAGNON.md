# Mode compagnon — Architecture et contraintes

Version : 0.1

## 1. Définition

Le mode compagnon exécute le modèle imposé en arrière-plan tout en laissant l’utilisateur prioritaire. Il ne cherche pas à occuper toutes les ressources momentanément libres ; il cherche à exploiter la marge qui peut être consommée sans dépasser une qualité de service définie.

Cette nuance est centrale : une ressource inactive peut partager une bande passante, un cache, une alimentation ou un système de refroidissement avec une application de premier plan.

## 2. Invariants opérationnels

- Aucune suppression ou désinstallation.
- Aucun formatage.
- Modèle original immuable.
- Aucune transformation approximative dans le premier jalon.
- Aucun privilège administrateur dans le premier jalon.
- L’utilisateur est prioritaire.
- Le compagnon peut se suspendre.
- Toute configuration temporaire est restaurée.
- Les données personnelles ne sont pas inspectées pour prédire l’activité.
- Les événements d’activité sont collectés au niveau minimal nécessaire et selon une politique documentée.

## 3. Slack

Le slack est une enveloppe de ressources empruntables :

\[
E(t)=
(C_{cpu}, M_{ram}, B_{ram}, C_{gpu}, M_{vram}, B_{io}, P, T)
\]

Les dimensions correspondent respectivement au calcul CPU, à la capacité RAM, à la bande passante RAM, au temps ou calcul GPU, à la VRAM, aux E/S, à la puissance et à la marge thermique.

Le système doit également conserver une confiance pour chaque estimation. Une capacité mal observée doit conduire à une marge plus conservatrice.

## 4. Qualité de service

La première qualité de service sera construite avec des canaris reproductibles plutôt qu’avec une promesse subjective d’invisibilité.

Canaris envisagés :

- tâche CPU périodique et mesure de retard ;
- petite opération mémoire ;
- rendu GPU minimal lorsque le GPU entre dans le périmètre ;
- E/S légère facultative ;
- pression mémoire et taux de fautes de page.

Les métriques réelles d’applications pourront être ajoutées plus tard avec autorisation.

## 5. Trois boucles de contrôle

### 5.1 Boucle rapide de protection

Responsabilités :

- détecter activité et pression ;
- cesser de soumettre de longues tâches ;
- diminuer les quotas ;
- protéger la réserve mémoire ;
- mettre en pause ;
- déclencher le plan sûr.

Elle doit être déterministe et rester opérationnelle même si l’optimiseur ou le modèle de coût échoue.

### 5.2 Boucle intermédiaire de planification

Responsabilités :

- sélectionner un plan déjà validé ;
- estimer le temps de disponibilité ;
- comparer gain et migration ;
- gérer l’hystérésis ;
- surveiller l’amortissement ;
- revenir à un plan plus discret.

### 5.3 Boucle lente d’apprentissage

Responsabilités :

- profiler ;
- construire de nouveaux plans ;
- compiler des artefacts exacts ;
- valider ;
- apprendre les coûts ;
- éliminer les plans dominés.

Elle s’exécute seulement lorsque le budget de gêne le permet.

## 6. Portefeuille de plans

Un plan doit décrire :

- exigences minimales CPU/RAM/GPU/VRAM ;
- bande passante estimée ;
- plage de contexte ;
- fidélité ;
- artefacts nécessaires ;
- débit mesuré ;
- coût d’activation ;
- coût de sortie ;
- coût de migration ;
- impact utilisateur ;
- plage thermique validée ;
- conditions d’invalidation.

Plans initiaux envisagés :

- pause ;
- CPU minimal ;
- CPU discret ;
- CPU disponible ;
- un seul accélérateur discret ;
- accélérateur agressif ;
- hybride ;
- thermique limité.

Le premier prototype n’a besoin que de pause, CPU discret et CPU disponible.

## 7. Changement de plan

Un changement est envisagé seulement si :

1. le plan cible est validé ;
2. les ressources minimales sont disponibles avec marge ;
3. le budget de gêne reste respecté ;
4. le gain futur attendu dépasse le coût de migration ;
5. le système peut revenir au plan sûr ;
6. la fréquence de changement reste sous une limite.

Des seuils distincts d’entrée et de sortie évitent les oscillations.

## 8. État du modèle

L’état doit être séparé en :

- modèle original ;
- représentations de poids ;
- buffers temporaires ;
- cache KV ;
- état du tokenizer ;
- état du sampler ;
- état aléatoire ;
- historique logique.

La première pause se fait entre tokens. Le modèle reste chargé si le budget mémoire le permet. Si la mémoire doit être rendue, le plan choisit entre éviction, transfert ou suspension prolongée.

## 9. Ressources difficiles à partager

### RAM

Une allocation résidente peut empêcher l’utilisateur de lancer une application. Le compagnon doit maintenir une réserve et surveiller la pression, pas seulement la mémoire dite libre.

### VRAM

Le pilote et les applications graphiques peuvent réclamer rapidement la VRAM. Un plan compagnon GPU doit réserver une marge et pouvoir cesser de soumettre du calcul avant d’envisager une éviction lourde.

### Bande passante mémoire

Elle peut être saturée alors que le CPU affiche une utilisation partielle. Des compteurs ou des canaris sont nécessaires.

### Thermique

La marge doit être estimée sur un horizon soutenu. CPU et GPU peuvent partager le refroidissement ou le budget de puissance.

### Stockage

Les lectures de modèle ou de dérivés ne doivent pas provoquer une latence visible. Les campagnes de compilation sont réservées aux périodes appropriées.

## 10. Activité utilisateur et vie privée

La première version doit privilégier les signaux minimaux :

- événement d’entrée récent sans enregistrer le contenu ;
- application au premier plan seulement si nécessaire ;
- compteurs de ressources ;
- canaris ;
- secteur ou batterie ;
- verrouillage de session.

Le système ne doit pas enregistrer les frappes, documents, fenêtres ou contenus de l’utilisateur pour améliorer sa prédiction.

## 11. Réaction à l’incertitude

Lorsque les signaux sont absents, contradictoires ou instables :

- réduire la charge ;
- conserver davantage de marge ;
- revenir au plan minimal ;
- suspendre si la mémoire est menacée.

La politique de sécurité ne doit pas dépendre d’un modèle appris.

## 12. Critère de valeur

Le mode compagnon apporte de la valeur s’il augmente le nombre de tokens conformes produits sur une trace réelle ou synthétique, à qualité de service identique, par rapport au meilleur profil statique conservateur.

Une stratégie adaptative plus complexe qui ne dépasse pas cette baseline doit être simplifiée ou abandonnée.

## 13. Hors périmètre

- suppression de fichiers ou logiciels ;
- arrêt autonome de services ;
- formatage ;
- réglages de tension ;
- firmware ;
- prise de contrôle exclusive ;
- apprentissage invasif des habitudes ;
- modèle substitutif ;
- altération silencieuse du contexte ou du sampling.

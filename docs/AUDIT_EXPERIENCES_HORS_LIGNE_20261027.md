# Porte d'audit hors ligne avant les expériences A0/A1 et A/B/C/D

**27 octobre 2026. Statut : instrument de recherche soumis à revue, aucun résultat scientifique sur la machine.**

## Pourquoi cette contribution

L'objectif du mode compagnon est de produire davantage de tokens du **modèle choisi par le propriétaire**, sans ralentir sa machine au-delà d'un budget de gêne **calibré et fixé à l'avance**. Le protocole candidat du 25/10/2026 insiste sur des comparaisons appariées, l'effet observateur A0/A1, la fidélité E1, les coûts d'allocation et le traitement des pertes.

Le risque déjà concret : un rapport pourrait sembler favorable à D alors que les campagnes B/D n'ont ni le même modèle, ni le même tokenizer, ni la même trace, ou lorsque l'observateur A1 perturbe le système. Le validateur détecte ces **contradictions déclaratives** à coût logiciel presque nul. Il ne collecte rien.

### Fichiers ajoutés

- `lab/scripts/audit_experiment.py` : fonctions `audit_study`, `load_study`, et CLI pure Python standard. Aucun `psutil`, `nvidia-smi`, GPU, runner d'inférence, mutation OS, élévation de droits ou accès réseau.
- `tests/test_audit_experiment.py` : tests adversariaux sur doubles, champs interdits, fidélité, QoS, arrêt, fenêtre, seeds, identités, gain, données manquantes et parseur JSON strict.
- `lab/config/study-audit.synthetic.json` : jeu de **fausses observations**, généré à la main, marqué `origin=synthetic` et `protocol_status=candidate_not_frozen`, volontairement inadmissible scientifiquement.
- `.github/workflows/offline-evidence-audit.yml` : Python 3.11, vérification de syntaxe, `unittest`, preuve que la fixture synthétique est explicitement rejetée. La CI teste du code de recherche uniquement.

### Exécution

Depuis la racine du repo, sans dépendances tierces :

```bash
python -m unittest discover -s tests -v
python lab/scripts/audit_experiment.py lab/config/study-audit.synthetic.json
```

L'exemple doit retourner un **code de sortie 1** et un objet JSON avec `decision=NOT_ADMISSIBLE`. C'est le comportement voulu, pas une expérience qui a échoué.

Autres codes : `0` indique **REVIEW_REQUIRED**, même si tous les contrôles déclaratifs passent ; `2` indique une entrée malformée ou inaccessible. Aucune sortie ne constitue un `PASS` scientifique ou une autorisation d'exécuter le contrôleur sur le poste.

## Contrat proposé pour un compte rendu agrégé

Racine JSON exactement `protocol`, `observer_preflight`, `runs`. Les champs non prévus sont refusés pour ne pas absorber silencieusement de prompts, titres de fenêtres, informations personnelles ou chemins privés.

**Protocol** : ID/version/statut (`candidate_not_frozen` ou `pre_registered`), `origin` (`synthetic` ou `externally_measured`), `fidelity_contract=E1`, empreintes SHA256 *déclarées* du modèle, moteur, tokenizer, corpus prompts, trace, graine, durée fixe, blocs minimaux, amélioration souhaitée et seuils QoS.

**Observer preflight A0/A1** : deux lignes par bloc, avec IDs, condition, p99 du canari et surcharge CPU déclarée. Une détérioration du p99 A1/A0 supérieure au maximum fixé rend le lot non admissible. Les valeurs CPU sont enregistrées mais **ne sont pas une vérification de QoS** ; budget/calibration CPU explicite à ajouter avant protocole exécutable.

**ABCD** : un enregistrement unique par bloc/scénario. L'auditeur refuse une campagne non appariée, une identité (modèle, moteur, tokenizer, corpus et trace) incohérente, des durées/graines inégales, E1 annoncé faux, un arrêt d'urgence sur B/D, une gêne excessive sur B/D, un nombre de blocs insuffisant ou un gain B→D inférieur aux critères du protocole. **C** est une baseline agressive qui peut dépasser la QoS et l'excès est **publié sans disqualifier artificiellement D**.

Le gain `pooled_gain_pct` est calculé sur **la somme des tokens B/D des blocs appariés**, pas en sélectionnant le meilleur bloc. Un minimum de blocs individuellement améliorés doit aussi être respecté. Le seuil de gain est une décision de l'expérience, **aucune constante « 5 % » imposée au propriétaire** ; 5 % et 2 blocs sont seulement les valeurs factices du fichier synthétique.

## Frontières et risques, à relire avant Codex

1. **Déclarations ≠ vérifications indépendantes :** des SHA256 fournis ne prouvent pas que des artefacts ont été réellement hachés ; `e1_tokens_match_oracle=true` est une auto-déclaration. Prévoir extraction horodatée depuis sorties réelles et oracle E1 lors du futur harnais.
2. **p99 déclaré ≠ p99 mesuré :** l'outil ne voit aucune observation latence individuelle, ne reconstitue pas les percentiles, ne calcule pas d'intervalles de confiance ni de puissance statistique. Un `REVIEW_REQUIRED` ne signifie ni « gain significatif » ni « absence de gêne ».
3. **Suffisance des canaris inconnue :** un poste réel peut être désagréable à utiliser même si le canari reste vert. Inclure les autres indicateurs de QoS, ressources, thermiques, pause latencies et retours humains avant une conclusion.
4. **Pas de protocole adopté :** le modèle, moteur, budget QoS, hôte et canaris ne sont pas encore choisis par le propriétaire. Les chiffres de la fixture sont du **mock**, ne doivent pas être promus.
5. **Risque de pseudoréplication :** des blocs reportés comme indépendants peuvent en réalité partager le même état thermique et la même séquence. Le contrôle automatique exige un ID unique mais ne prouve pas l'indépendance.
6. **Sécurité :** ne jamais envoyer de traces privées, prompts, frappes, fenêtres ni secrets dans ce schéma ; ne jamais rendre le gate capable de démarrer un modèle, de stopper des services ou de piloter l'hôte. Aucun `D:\\` n'est utilisé par ce code.
7. **Mode compagnon et fidélité :** le modèle reste imposé et immuable ; cet outil ne propose aucun moteur et ne transforme aucun poids. Il est utile **avant** l'observateur, mais ne remplace pas le calibrage A0/A1 ni le contrôleur.

## Prochain travail de Codex (non réalisé)

- Vérifier CI et schéma/diagnostics ; décider s'il est pertinent d'adopter la contribution après revue, en respectant `docs/GOUVERNANCE_DOCUMENTAIRE.md`.
- Définir le vrai oracle E1 et un format brut de résultats **sans contenu utilisateur**, avec hachages calculés et provenances fiables. Ne pas publier les données brutes si elles sont sensibles.
- Ajouter un outil indépendant qui reconstitue canari p95/p99 à partir de mesures réelles et relie tous les seuils QoS de `lab/config/companion-policy.example.json` (mémoire, températures, pause). Préciser réchauffement/répétitions.
- Préenregistrer seuils et nombre de blocs puis comparer le contrôle A0/A1 avant même l'inférence B/C/D.
- Après accord du propriétaire et réalisation du protocole : produire des mesures E1 sur le poste et distinguer *résultat physique réel* du contrôle interne de manifestes.
- Si les résultats invalidants apparaissent, conserver une preuve négative et **ne jamais démarrer un mode compagnon actif simplement parce que la CI est verte**.

### Coordination Git / contribution

Branche `chatgpt/trial-audit-gate-20261027` fondée sur `chatgpt/research-review-20261025`, PR de contribution en **brouillon** ciblant cette branche, et non la branche fondatrice `codex/foundation`. Le protocole du 25/10 est réutilisé plutôt que réécrit. Aucun fichier du modèle, du PC, du dossier D:, d'un bot trading ou de Jade n'est manipulé ici. État précis de la PR et checks GitHub à actualiser dans le message de revue. Les limitations ci-dessus restent valables même si tous les tests unitaires passent.

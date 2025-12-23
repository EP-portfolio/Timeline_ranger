# Questions Ouvertes - Timeline Ranger

Ce document liste les questions qui nécessitent des clarifications avant de continuer le développement.

## 🎮 Questions sur les Mécaniques de Jeu

### 1. Système de Tours ✅
- **Question** : Comment est déterminé l'ordre de jeu initial ?
- **Réponse** : 
  - Le premier joueur est choisi aléatoirement et dispose de 0 points
  - Le deuxième joueur dispose de 1 point
  - Le troisième joueur dispose de 2 points
  - Le quatrième joueur dispose de 3 points
  - (Points initiaux selon la position dans l'ordre de jeu)

### 2. Actions par Tour ✅
- **Question** : Un joueur peut-il effectuer plusieurs actions par tour ?
- **Réponse** : 
  - Le joueur ne peut effectuer qu'**une carte action par tour**
  - Cependant, **certaines cartes permettent d'effectuer des actions supplémentaires**
  - Les actions supplémentaires sont déclenchées par les effets des cartes
  - **Action Construction améliorée** : Peut construire **plusieurs bâtiments** en un seul tour
  - **Action Animaux** : Peut jouer **plusieurs animaux** en un tour selon la puissance (1-5 animaux)

### 3. Pioche de Cartes ✅
- **Question** : Comment fonctionne la pioche ?
- **Réponse** : 
  - **Début de partie** : Chaque joueur reçoit 8 cartes aléatoirement et en conserve 4
  - **RIVER (Display Row)** : Une zone commune avec 6 cartes visibles
  - Les cartes de la RIVER peuvent être jouées par les joueurs sous certaines conditions
  - **Remplacement** : Quand une carte de la RIVER est jouée, elle est remplacée par une nouvelle carte de la pioche
  - **Action Cartes** :
    - **Puissance 1-3** : Pioche uniquement depuis la pioche (1-3 cartes)
    - **Puissance 4-5** : Peut piocher depuis la pioche ET choisir parmi la rivière (4-5 cartes)
  - **Action Cartes améliorée** : Permet de piocher des cartes à hauteur de la **réputation** du joueur (au lieu de la puissance)

### 4. Main de Cartes ✅
- **Question** : Y a-t-il une limite de cartes en main ?
- **Réponse** : 
  - **Pas de limite** pendant le jeu normal
  - **À la pause** : Limite à conserver 3 cartes (ou plus selon bonus)
  - Les cartes excédentaires doivent être défaussées à la pause

### 5. Placement sur l'Armure Méca ✅
- **Question** : Quelles sont les règles exactes de placement ?
- **Réponse** : 
  - **Première pièce** : Doit être posée sur une case du **bord de l'armure**
  - **Pièces suivantes** : Doivent être **adjacentes** à une pièce existante
  - **Exception** : Certaines cartes peuvent avoir des règles de placement spécifiques explicites

### 6. Actions de Couleur ✅
- **Question** : Comment fonctionnent exactement les actions de couleur ?
- **Réponse** : 
  - **Système de piste 1-5** : Chaque joueur dispose de 5 cartes Action placées sur une piste numérotée de 1 à 5
  - **Puissance** : La position de la carte détermine sa puissance (1 = faible, 5 = forte)
  - **Rotation** : Quand une carte Action est jouée :
    - Elle revient en position 1
    - Les autres cartes avancent d'une position
  - **Jetons X (Croix)** : 
    - Obtenus lorsqu'un joueur ne peut/souhaite pas effectuer une action OU atteint la fin de la piste de pause (symbole tasse)
    - Maximum 5 jetons X
    - **Utilisation** : 1 jeton X = +1 niveau de puissance pour une action
    - Permet de jouer une action à un niveau supérieur à sa position actuelle
  - **Amélioration** : Les cartes Action peuvent être améliorées pour augmenter leur efficacité
  - **Détails par Action** :
    - **🟡 ACTION CARTES** : Pioche 1-5 cartes selon puissance. Puissance 4-5 : accès à la rivière. Améliorée : pioche selon réputation
    - **🟠 ACTION CONSTRUCTION** : Construit enclos taille 1-5 selon puissance. Coût : 2 crédits/case. Améliorée : plusieurs bâtiments en un tour
    - **⚫ ACTION ANIMAUX** : Joue 1-5 animaux selon puissance. Conditions : enclos + prérequis. Améliorée : peut jouer depuis la rivière
    - **🟢 ACTION ASSOCIATION** : Missions selon puissance (réputation, partenariats, projets). Plus la puissance est élevée, plus les options sont nombreuses
    - **🔵 ACTION MECENE** : Joue carte Mécène niveau 1-5 selon puissance OU avance pion Pause + crédits. Les mécènes offrent revenus, bonus, points

### 7. Effets de Cartes ✅
- **Question** : Quand les effets sont-ils appliqués ?
- **Réponse** : 
  - **Effets d'invocation** : Appliqués **immédiatement** lors du placement de la troupe
  - **Effets après pause** : Certains effets sont activés **après que la pause ait lieu** (récolte)
  - **Effets permanents/récurrents (fond bleu)** : Probablement activés à chaque pause ou à chaque tour (à confirmer)
  - **Effets de dernier souffle** : Seulement en fin de partie
  - **Activation manuelle** : À déterminer selon les cartes spécifiques

### 8. Ressources ✅
- **Question** : Comment sont gagnées les ressources ?
- **Réponse** : 
  - **Récolte** : Les ressources (or) sont généralement gagnées **après la pause** (récolte)
  - **Montant de la récolte** : Dépend de l'**attrait du zoo** (piste d'attrait) - plus l'attrait est élevé, plus les revenus sont élevés
  - **Action Mécène (Alternative)** : 
    - Au lieu de jouer une carte Mécène, peut **avancer le pion Pause** et recevoir des crédits
    - Montant des crédits : Probablement égal à la puissance de l'action (1-5 crédits)
  - **Action Construction** : Coût fixe de **2 crédits par case** construite
  - **One-shot** : Il est possible de gagner des ressources **une seule fois** via certaines cartes ou actions
  - **Deux types** : Récolte (récurrent) ou one-shot (unique)
  - **À préciser** : Limite de ressources ?

### 9. Quêtes ✅
- **Question** : Comment fonctionnent les quêtes ?
- **Réponse** : 
  - **Types de quêtes** : 
    - Quêtes de base (toujours disponibles sur le plateau principal)
    - Quêtes dans la pioche (à piocher)
  - **Fonctionnement** : 
    - Les joueurs peuvent **contribuer** aux projets de conservation en remplissant les conditions requises
    - Cela leur permet de gagner des **points de conservation** (lasers)
  - **Ajout de nouveaux projets** : 
    - Il est possible d'ajouter de nouveaux projets
    - L'ajout d'un nouveau projet entraîne le **retrait du plus ancien**
    - En fonction de l'espace disponible selon le nombre de joueurs
  - **Plusieurs projets actifs** : Oui, plusieurs projets peuvent être actifs simultanément
  - **Récompenses** : 
    - Points de conservation (lasers) - toujours
    - Points de réputation (développement technique) - parfois

### 10. Conditions de Fin de Partie ✅
- **Question** : Quelles sont les conditions exactes de fin ?
- **Réponse** : 
  - **Condition principale (Ark Nova)** : Un joueur fait **se croiser ses marqueurs** sur les pistes d'Attrait et de Conservation
  - **Condition principale (Timeline Ranger)** : Un joueur atteint **120 points de dégâts** (variantes : 80 ou 100 points)
  - **Dernier tour** : Chaque autre joueur a droit à **un dernier tour**
  - **Décompte final** : 
    - Application des effets "Dernier Souffle" de toutes les cartes (troupes, technologies, etc.)
    - Calcul : Addition de la valeur de l'Attrait (points de dégâts) + numéro de l'espace de Conservation (lasers)
  - **Départage en cas d'égalité** :
    1. Nombre de quêtes réalisées
    2. Score de réputation (points de développement technique)

## 💻 Questions Techniques

### 11. Gestion de l'État ✅
- **Question** : Comment gérer l'état du jeu ?
- **Réponse** : 
  - **Replay complet souhaité** : Gestion d'état de chaque action lors de chacun des tours
  - **Objectif** : Possibilité d'accéder à un replay total de la partie
  - **Implémentation recommandée** :
    - Sauvegarde complète de l'état après chaque action
    - Historique complet des actions avec timestamps
    - Versioning pour permettre le replay pas à pas
  - **À définir** : Taille maximale de l'état JSON (optimisation si nécessaire)

### 12. WebSockets
- **Question** : Stratégie de synchronisation ?
  - Push complet de l'état à chaque action ?
  - Push incrémental (deltas) ?
  - Polling en fallback ?
  - Gestion des reconnexions ?
- **Réponse attendue** : [À définir]

### 13. Gestion des Conflits ✅
- **Question** : Comment gérer les actions simultanées ?
- **Réponse** : 
  - **Tour par tour** : Pas d'actions simultanées
  - **Implémentation** : 
    - Verrouillage du tour (un seul joueur actif à la fois)
    - Rejet des actions des autres joueurs pendant le tour d'un joueur
    - File d'attente non nécessaire (système séquentiel)

### 14. Performance
- **Question** : Contraintes de performance ?
  - Temps de réponse maximum pour une action ?
  - Nombre de parties simultanées supportées ?
  - Taille maximale d'une partie ?
- **Réponse attendue** : [À définir]

### 15. Historique et Replay ✅
- **Question** : Faut-il implémenter un système de replay ?
- **Réponse** : 
  - **Oui** : Replay complet souhaité (voir question 11)
  - **Historique complet des actions** : Oui, avec timestamps
  - **Possibilité de revoir une partie** : Oui, replay pas à pas
  - **Export des parties** : À considérer (optionnel)

## 🎨 Questions UX/UI

### 16. Interface Utilisateur
- **Question** : Quelles sont les priorités d'affichage ?
  - Vue principale : Plateau ou main ?
  - Informations des autres joueurs : Toujours visibles ?
  - Notifications : Comment afficher ?
- **Réponse attendue** : [À définir]

### 17. Feedback Utilisateur
- **Question** : Comment informer l'utilisateur ?
  - Messages d'erreur : Niveau de détail ?
  - Confirmations : Pour quelles actions ?
  - Animations : Souhaitées ?
- **Réponse attendue** : [À définir]

## 📊 Questions de Données

### 18. Configuration des Armures Méca
- **Question** : Les configurations détaillées sont-elles disponibles ?
  - Dimensions exactes ?
  - Cases bloquées ?
  - Zones spéciales ?
  - Capacités spéciales ?
- **Réponse attendue** : [À définir - Voir CONFIGURATIONS_PLATEAUX_ARMURES.md]

### 19. Données des Cartes
- **Question** : Toutes les données sont-elles complètes ?
  - Effets de toutes les cartes ?
  - Coûts exacts ?
  - Prérequis ?
- **Réponse attendue** : [À vérifier dans la base de données]

### 20. Statistiques
- **Question** : Quelles statistiques doivent être trackées ?
  - Parties jouées/gagnées ?
  - Scores moyens ?
  - Cartes les plus jouées ?
  - Temps de partie moyen ?
- **Réponse attendue** : [À définir]

---

## 📝 Notes

- Les questions marquées "[À définir]" nécessitent une décision avant l'implémentation
- Les questions marquées "[À vérifier]" nécessitent une vérification dans les données existantes
- Certaines questions peuvent être résolues en testant avec le jeu physique Ark Nova

---

*Document créé le : 2025-01-XX*
*À mettre à jour au fur et à mesure des réponses*


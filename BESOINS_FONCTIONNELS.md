# Besoins Fonctionnels - Timeline Ranger

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Flux Utilisateur](#flux-utilisateur)
3. [Mécaniques de Jeu](#mécaniques-de-jeu)
4. [Actions de Jeu](#actions-de-jeu)
5. [Gestion de l'État](#gestion-de-létat)
6. [Synchronisation Temps Réel](#synchronisation-temps-réel)
7. [Besoins Techniques](#besoins-techniques)

---

## 🎯 Vue d'ensemble

Timeline Ranger est une adaptation en ligne du jeu de société Ark Nova, transformé en thème sci-fi/militaire. Le jeu se joue en 2-4 joueurs (extensible à 20 pour les parties multijoueurs).

### Objectif du Jeu
Les joueurs construisent et développent leur base militaire (Armure Méca) en déployant des troupes, technologies et quêtes pour accumuler des points de dégâts, lasers, développement technique et paires d'ailes.

### Durée d'une Partie
- Temps moyen : 60-120 minutes
- Nombre de tours : Variable (selon les conditions de fin de partie)

---

## 👥 Flux Utilisateur

### 1. Authentification et Inscription
- **Inscription** : Email, mot de passe, username (optionnel)
- **Connexion** : Email + mot de passe → Token JWT
- **Session** : Token valide 24h, renouvelable

### 2. Création/Rejoindre une Partie
- **Créer une partie** :
  - Choisir le nombre max de joueurs (2-4, extensible)
  - Générer un code unique (6 caractères)
  - L'hôte devient automatiquement joueur #1
  - Statut : "waiting"
  
- **Rejoindre une partie** :
  - Entrer le code de la partie
  - Choisir une Armure Méca (optionnel au début)
  - Rejoindre en tant que joueur suivant (#2, #3, #4)
  - Statut de la partie : "waiting" tant que < max_players

- **Démarrer une partie** :
  - Seul l'hôte peut démarrer
  - Minimum 2 joueurs requis
  - Initialisation :
    - Distribution des cartes de départ
    - Attribution des ressources initiales
    - Détermination de l'ordre de jeu
    - Statut : "started"

### 3. Déroulement d'une Partie

#### Phase d'Initialisation
1. Chaque joueur reçoit :
   - 1 Armure Méca (plateau de jeu)
   - 8 cartes aléatoirement (en conserve 4, défausse 4)
   - **2 cartes "Dernier Souffle"** aléatoirement (le premier joueur à 10 lasers oblige tous les joueurs à défausser 1)
   - Ressources initiales (or, matières premières)
   - 5 cartes Action (Rangers de couleurs) avec niveaux 1-5
   - 1 émissaire (pour Action Association)

2. Ordre de jeu :
   - Premier joueur choisi aléatoirement
   - Points initiaux selon position :
     - Joueur 1 : 0 point
     - Joueur 2 : 1 point
     - Joueur 3 : 2 points
     - Joueur 4 : 3 points
   - Tour par tour, sens horaire

3. RIVER :
   - 6 cartes visibles dans une zone commune
   - Cartes jouables sous certaines conditions

#### Phase de Jeu (Tour par Tour)
Chaque tour se compose de :

1. **Phase d'Action** :
   - Le joueur actif choisit une carte Action (parmi 5 disponibles)
   - Le joueur choisit le niveau auquel jouer l'action (1-5)
   - Option : Jouer au niveau 1 et terminer → obtient une croix (max 5 croix)
   - Option : Utiliser des croix pour augmenter le niveau de l'action
   - Exécution de l'action choisie
   - Actions supplémentaires possibles via effets de cartes
   - Mise à jour de l'état du jeu

2. **Phase de Fin de Tour** :
   - Vérification des conditions de fin
   - Passage au joueur suivant
   - Notifications aux autres joueurs

3. **Phase de Pause** (périodique) :
   - Limite de main : 3 cartes (ou plus selon bonus)
   - Défausse des cartes excédentaires
   - Récolte des ressources (or, matières premières)
   - Activation des effets "après pause"

#### Conditions de Fin de Partie
- **Condition principale** : Un joueur atteint 120 points de dégâts (variantes : 80 ou 100 points)
- **Événement à 10 lasers** : Le premier joueur à atteindre 10 lasers oblige tous les joueurs à défausser une carte Dernier Souffle
- **Variantes** : 80 ou 100 points (configurables)
- **Dernier tour** : Chaque autre joueur a droit à un dernier tour

#### Phase de Décompte Final
1. Application des effets "Dernier Souffle" :
   - Toutes les cartes avec effet de dernier souffle (troupes, technologies, etc.)
   - **Carte "Dernier Souffle" conservée** (celle non défaussée quand le premier joueur a atteint 10 lasers)
   - Calcul des scores finaux
2. Calcul des points de dégâts des lasers :
   - **0-6 lasers** : Lasers × 2 points de dégâts
   - **7+ lasers** : Lasers × 3 points de dégâts
3. Classement des joueurs :
   - Par score total (points de dégâts de troupes + points de dégâts des lasers + autres)
   - En cas d'égalité : Nombre de quêtes réalisées
   - En cas d'égalité encore : Score de réputation (points de développement technique)
4. Statut : "finished"

---

## 🎮 Mécaniques de Jeu

### 1. Les 5 Actions de Couleur (Cartes Action)

Chaque joueur dispose de 5 cartes Action représentées par des Rangers de couleurs :

#### Système de Niveaux
- Chaque carte Action a un niveau (1-5)
- Le joueur choisit le niveau auquel jouer l'action
- **Croix** : 
  - Obtenues en jouant une action au niveau 1 et terminant son tour
  - Maximum 5 croix
  - Utilisables pour augmenter le niveau d'une action

#### 🔵 Action Bleue (MECENES)
- **Effet** : Jouer des cartes Technologies/Mécènes OU gagner des crédits
- **Carte non améliorée** :
  - **Option 1** : Jouer 1 carte Mécène niveau max = puissance (1-5)
  - **Option 2** : Gagner 1-5 crédits selon puissance
- **Carte améliorée** :
  - **Option 1** : Jouer plusieurs cartes Mécène (total niveau max = puissance + 1)
    - Exemple puissance 3 : Peut jouer cartes niveau 1+2, ou 3, ou 2+2, etc. (total ≤ 4)
  - **Option 2** : Gagner 2 × le niveau de l'action (2, 4, 6, 8, 10 crédits)
- **Autres effets** : Peut avoir d'autres effets selon les cartes
- **Coût** : Variable selon les cartes jouées
- **Résultat** : Cartes placées sur l'Armure Méca OU crédits gagnés

#### ⚫ Action Noire (ANIMAUX)
- **Effet** : Jouer des cartes Troupes/Animaux
- **Carte non améliorée** : 
  - Puissance 1 : 0 animal (peut passer)
  - Puissance 2-4 : 1 animal maximum
  - Puissance 5 : 2 animaux maximum + gagne 1 point de réputation
- **Carte améliorée** : 
  - Puissance 1-2 : 1 animal maximum
  - Puissance 3-5 : 2 animaux maximum
  - Puissance 5 : Gagne 1 point de réputation
- **Conditions** : Enclos approprié + prérequis spécifiques (eau, rochers, etc.)
- **Coût** : Coût de la carte + conditions requises
- **Améliorée** : Peut jouer des troupes directement depuis la rivière
- **Résultat** : Cartes placées sur l'Armure Méca (armes installées dans slots)

#### 🟠 Action Orange (CONSTRUCTION)
- **Effet** : Construire des parties d'armure méca et créer des slots pour armes
- **Puissance 1-5** : Construit parties d'armure taille 1-5 selon la puissance
- **Coût** : 2 crédits (or) par case construite
- **Types** : Parties d'armure, slots pour armes
- **Améliorée** : Peut construire plusieurs bâtiments en un seul tour
- **Résultat** : Construction sur l'Armure Méca + slots créés pour le Ranger Noir

#### 🟢 Action Verte (ASSOCIATION)
- **Effet** : Envoyer des émissaires pour missions associatives
- **Système d'émissaires** : 
  - Début : 1 émissaire disponible
  - Pendant partie : Peut débloquer jusqu'à 3 émissaires supplémentaires (max 4)
  - **Bonus à 2 lasers** : Peut obtenir un nouvel émissaire (alternative à améliorer une carte Action)
- **Carte non améliorée** :
  - Peut réaliser 1 quête niveau max = puissance
  - Puissance 2 : Gagne 2 points de réputation
  - Puissance 3 : Peut récupérer une mine (réduit de 3 po les pièces d'armure de ce matériau)
  - Puissance 4 : Peut récupérer une relique (bonus à définir)
  - Puissance 5 : Peut réaliser une quête si conditions remplies
  - **Limite de mines** : Maximum **2 mines** (sans amélioration)
- **Carte améliorée** :
  - Peut réaliser une ou plusieurs quêtes niveau max = puissance
  - Niveau 0 : Peut payer or pour obtenir **1 laser supplémentaire** (coût à définir)
  - Niveaux 2-5 : Mêmes effets que non améliorée (réputation, mine, relique, quête)
  - **Limite de mines** : Maximum **3 ou 4 mines** (à confirmer : 3 ou 4 ?)
- **Résultat** : Quêtes réalisées, réputation gagnée, mines/reliques récupérées, lasers obtenus

#### 🟡 Action Jaune (CARTES)
- **Effet** : Piocher des cartes
- **Puissance 1-3** : Pioche 1-3 cartes depuis la pioche uniquement
- **Puissance 4-5** : Pioche 4-5 cartes ET accès à la rivière (6 cartes visibles)
- **Améliorée** : 
  - Pioche selon la **réputation** du joueur (au lieu de la puissance)
  - **Déblocage** : Permet de dépasser la limite de 9 points de réputation
- **Résultat** : Cartes ajoutées à la main du joueur

### 2. Système de Cartes

#### Types de Cartes

**Troupes** (ex-Animaux) :
- Types : Explosifs, Munitions, Torpilles, Missiles, Armes Intelligentes, Armes Toxiques, etc.
- Attributs :
  - Points de dégâts (ex-Points Attrait)
  - Nombre de lasers (ex-Points Conservation)
  - Points de développement technique (ex-Points Réputation)
  - Paires d'ailes (ex-Points Science)
  - Coût (Or + Matières premières)
  - Taille (pour placement sur l'Armure Méca)
  - Effets : Invocation, Quotidien, Dernier Souffle

**Technologies** (ex-Mécènes) :
- Types : Systèmes, Spécialistes, Experts, Pièces d'armure
- Attributs :
  - Niveau
  - Coût
  - Revenus par jour (si applicable)
  - Effets : Invocation, Quotidien, Dernier Souffle
  - Actions bleues disponibles

**Quêtes** (ex-Projets de Conservation) :
- Types : Maîtrise, Forteresse, etc.
- Conditions : Objectifs à atteindre
- Récompenses : Points, ressources, bonus

### 3. Armure Méca (Plateau de Jeu)

- **Grille** : Configuration unique par Armure Méca
- **Dimensions** : Variable selon l'armure
- **Cases bloquées** : Certaines cases ne peuvent pas recevoir de cartes
- **Zones spéciales** : Zones avec effets particuliers
- **Placement** : Les cartes doivent respecter les contraintes de placement
- **Capacité** : Nombre maximum de cartes par zone

### 4. Ressources

#### Or (Crédits)
- Utilisé pour : Jouer des cartes, construire, actions
- Gagné par : 
  - Récolte (après la pause) - récurrent
  - One-shot (via certaines cartes/actions) - unique
  - Action Noire (montant à préciser : fixe/variable)
- Stocké : Par joueur, limite à définir

#### Matières Premières
- Types : Titanium, Platine, Vibranium, Carbone, Kevlar
- Utilisé pour : Coût des cartes
- Gagné par : 
  - Récolte (après la pause) - récurrent
  - One-shot (via certaines cartes/actions) - unique
- Stocké : Par joueur, par type, limite à définir

### 5. Système de Points

#### Points de Dégâts (ex-Points Attrait)
- **Gagnés** : 
  - Par les troupes déployées (colonne `points_degats`)
  - Par les lasers (valeur variable selon nombre)
  - Par les technologies (si applicable)
  - Par les bonus aux seuils de lasers
- **Calcul des lasers** :
  - 0-6 lasers : Lasers × 2 points de dégâts
  - 7+ lasers : Lasers × 3 points de dégâts
- **Utilisation** : Score final, conditions de fin de partie (120 points), conditions de quêtes

#### Lasers (ex-Points Conservation)
- **Gagnés** : Par les troupes, technologies, quêtes et Action Association
- **Valeur en points de dégâts** :
  - **0-6 lasers** : Chaque laser vaut **2 points de dégâts**
  - **7+ lasers** : Chaque laser vaut **3 points de dégâts**
- **Bonus aux seuils** :
  - **2 lasers** : Choisir entre améliorer une carte Action OU obtenir un nouvel émissaire
  - **5 lasers** : Bonus disponible (à définir)
  - **8 lasers** : Bonus disponible (à définir)
  - **10 lasers** : **Le premier joueur à 10 lasers** oblige **TOUS les joueurs** à défausser une des deux cartes "Dernier Souffle" (choix de chaque joueur)
- **Utilisation** : Score final (points de dégâts), conditions de quêtes
- **Note** : Les lasers représentent une source importante de points de dégâts, surtout à partir de 7 lasers

#### Points de Développement Technique (ex-Points Réputation)
- **Gagnés** : Par les troupes, technologies, quêtes et certaines actions
  - Action Animaux puissance 5 : +1 point de réputation
  - Action Association puissance 2 : +2 points de réputation
- **Limite standard** : **9 points de réputation maximum** (sans amélioration)
- **Dépassement** : Améliorer la carte Action **"Cartes"** (Ranger Jaune) pour dépasser 9 points
- **Maximum avec amélioration** : **15 points de réputation** (la piste s'étend jusqu'à la case 15)
- **Bonus aux seuils** : Bonus obtenus immédiatement en atteignant certaines cases (crédits, jetons X, points d'attrait, émissaires, etc.) - détails sur le plateau de jeu
- **Case 15** : Si réputation déjà à 15, choix entre gagner 1 point d'attrait ou prendre la tuile bonus
- **Utilisation** : Score final, déblocage d'actions
- **Action Cartes améliorée** : Permet de piocher selon la réputation au lieu de la puissance

#### Paires d'Ailes (ex-Points Science)
- Gagnés : Par les troupes et technologies
- Utilisation : Score final, conditions de quêtes

### 6. Système de Tours

- **Ordre** : Déterminé à l'initialisation (premier joueur aléatoire)
- **Tour actif** : Un seul joueur à la fois (verrouillage)
- **Actions par tour** : 
  - 1 carte Action principale (obligatoire)
  - Actions supplémentaires possibles via effets de cartes
- **Système de croix (Jetons X)** :
  - Obtenues en jouant niveau 1 + fin de tour OU si on ne peut/souhaite pas jouer
  - Maximum 5 croix
  - Utilisation : 1 jeton X = +1 niveau de puissance pour une action
- **Amélioration des cartes Action** :
  - Via bonus à 2 lasers (choix : améliorer carte OU obtenir émissaire)
  - Amélioration permanente pour la partie
- **Fin de tour** : Automatique après action ou passe

---

## 🎯 Actions de Jeu

### Actions Disponibles par Tour

#### 1. Jouer une Action de Couleur
- **Input** : Type d'action (Bleu, Noir, Orange, Vert, Jaune)
- **Validation** :
  - Le joueur est le joueur actif
  - L'action est disponible (pas déjà utilisée ce tour)
  - Les prérequis sont remplis
- **Effet** : Exécution de l'action choisie
- **Résultat** : Mise à jour de l'état du joueur et du jeu

#### 2. Jouer une Carte
- **Input** : ID de la carte, position sur l'Armure Méca
- **Validation** :
  - La carte est dans la main du joueur
  - Le joueur a assez de ressources
  - La position est valide sur l'Armure Méca
  - Les contraintes de placement sont respectées
- **Effet** :
  - Retrait de la carte de la main
  - Placement sur l'Armure Méca
  - Déduction des ressources
  - Application des effets d'invocation
  - Mise à jour des scores
- **Résultat** : Carte en jeu, état mis à jour

#### 3. Activer une Action Bleue
- **Input** : ID de la carte avec action bleue
- **Validation** :
  - La carte est en jeu
  - La carte a une action bleue disponible
  - Le joueur a assez de ressources (si coût requis)
- **Effet** : Exécution de l'action bleue
- **Résultat** : Effet appliqué, ressources déduites

#### 4. Piocher des Cartes
- **Input** : Nombre de cartes (selon niveau de l'action)
- **Validation** :
  - Action Jaune (CARTES) activée
  - Pioche disponible (deck non vide)
- **Effet** : Cartes ajoutées à la main
- **Résultat** : Main mise à jour
- **Note** : Pas de limite de main pendant le jeu (sauf à la pause)

#### 5. Passer son Tour
- **Input** : Confirmation
- **Effet** : Fin du tour du joueur
- **Résultat** : Passage au joueur suivant

#### 6. Utiliser un Effet de Carte
- **Input** : ID de la carte, type d'effet (Invocation, Quotidien, Après Pause, Dernier Souffle)
- **Validation** :
  - La carte est en jeu
  - L'effet est disponible
  - Les conditions sont remplies
- **Effet** : Application de l'effet
- **Résultat** : État mis à jour
- **Timing** :
  - Invocation : Immédiat lors du placement
  - Après Pause : Activé après la pause (récolte)
  - Quotidien : À préciser (début/fin de tour)
  - Dernier Souffle : Seulement en fin de partie

---

## 💾 Gestion de l'État

### État d'une Partie

L'état d'une partie doit contenir :

#### Informations Générales
- ID de la partie
- Code de la partie
- Statut (waiting, started, finished)
- Tour actuel
- Joueur actif
- Ordre des joueurs

#### État de Chaque Joueur
- ID utilisateur
- Numéro de joueur
- Points initiaux (selon position : 0, 1, 2, 3)
- Armure Méca choisie
- Main (cartes en main)
- Plateau (cartes en jeu sur l'Armure Méca)
- RIVER (6 cartes visibles - zone commune)
- Ressources :
  - Or
  - Matières premières (par type)
- Scores :
  - Points de dégâts
  - Lasers (points de conservation)
  - Points de développement technique (réputation)
  - Paires d'ailes
- Croix (0-5)
- Cartes Action disponibles (5 cartes avec niveaux)
- Quêtes actives/complétées
- Statut (actif, en attente, éliminé)

#### État du Jeu
- Deck de pioche (cartes restantes)
- Défausse (cartes jouées)
- RIVER (6 cartes visibles communes)
- Quêtes de base (toujours disponibles)
- Quêtes dans la pioche
- Quêtes complétées par joueur
- Historique complet des actions (pour replay)
- Conditions de fin de partie (seuil configurable : 80/100/120 points)
- Phase actuelle (action, pause, récolte, fin)

### Persistance de l'État

- **Base de données** : État complet sauvegardé dans `game_states`
- **Format** : JSONB pour flexibilité
- **Fréquence** : Après chaque action (pour replay complet)
- **Versioning** : Historique complet des états pour replay pas à pas
- **Replay** : Possibilité de revoir la partie complète action par action

### Synchronisation

- **Temps réel** : WebSockets pour mise à jour immédiate
- **Polling** : Alternative si WebSockets indisponibles
- **Conflits** : 
  - Tour par tour (pas d'actions simultanées)
  - Verrouillage du tour (un seul joueur actif)
  - Rejet des actions des autres joueurs pendant le tour actif
- **Validation** : Vérification côté serveur avant application

---

## 🔄 Synchronisation Temps Réel

### Événements à Synchroniser

#### Événements de Partie
- Nouveau joueur rejoint
- Partie démarrée
- Partie terminée
- Changement de statut

#### Événements de Tour
- Nouveau tour commencé
- Joueur actif changé
- Action effectuée
- Tour terminé

#### Événements de Joueur
- Carte jouée
- Ressources modifiées
- Scores mis à jour
- Main modifiée
- Plateau modifié

#### Événements Système
- Erreur survenue
- Notification
- Message système

### WebSockets

#### Connexion
- Authentification via token JWT
- Souscription à une partie
- Gestion de la reconnexion

#### Messages
- **Format** : JSON
- **Types** :
  - `game_state_update` : Mise à jour complète de l'état
  - `player_action` : Action d'un joueur
  - `notification` : Notification système
  - `error` : Erreur
  - `ping/pong` : Keep-alive

#### Gestion des Connexions
- Multiples connexions par joueur (onglets)
- Détection de déconnexion
- Reconnexion automatique
- Synchronisation à la reconnexion

---

## 🛠️ Besoins Techniques

### API REST

#### Endpoints Existants (✅ Implémentés)
- `POST /api/v1/auth/register` - Inscription
- `POST /api/v1/auth/login` - Connexion
- `GET /api/v1/auth/me` - Profil utilisateur
- `POST /api/v1/games` - Créer une partie
- `GET /api/v1/games` - Lister les parties
- `GET /api/v1/games/{code}` - Récupérer une partie
- `POST /api/v1/games/join` - Rejoindre une partie
- `GET /api/v1/games/{id}/players` - Liste des joueurs
- `POST /api/v1/games/{id}/start` - Démarrer une partie

#### Endpoints à Implémenter

**Actions de Jeu** :
- `POST /api/v1/games/{id}/actions/play-color` - Jouer une action de couleur
- `POST /api/v1/games/{id}/actions/play-card` - Jouer une carte
- `POST /api/v1/games/{id}/actions/activate-blue` - Activer une action bleue
- `POST /api/v1/games/{id}/actions/draw-cards` - Piocher des cartes
- `POST /api/v1/games/{id}/actions/pass` - Passer son tour
- `POST /api/v1/games/{id}/actions/use-effect` - Utiliser un effet de carte

**État du Jeu** :
- `GET /api/v1/games/{id}/state` - Récupérer l'état complet
- `GET /api/v1/games/{id}/history` - Historique des actions
- `GET /api/v1/games/{id}/my-hand` - Ma main (cartes)
- `GET /api/v1/games/{id}/my-board` - Mon plateau (cartes en jeu)

**Cartes** :
- `GET /api/v1/cards/troupes` - Liste des troupes disponibles
- `GET /api/v1/cards/technologies` - Liste des technologies
- `GET /api/v1/cards/quetes` - Liste des quêtes
- `GET /api/v1/cards/{id}` - Détails d'une carte

**Armures Méca** :
- `GET /api/v1/armures` - Liste des armures disponibles
- `GET /api/v1/armures/{id}` - Détails d'une armure (grille, zones)

### WebSockets

#### Endpoint
- `WS /api/v1/games/{id}/ws` - Connexion WebSocket à une partie

#### Messages Entrants (Client → Serveur)
```json
{
  "type": "subscribe",
  "game_id": 123,
  "token": "jwt_token"
}
```

```json
{
  "type": "action",
  "action_type": "play_color",
  "color": "blue",
  "game_id": 123
}
```

#### Messages Sortants (Serveur → Client)
```json
{
  "type": "game_state_update",
  "game_id": 123,
  "state": { ... },
  "timestamp": "2025-01-XX..."
}
```

```json
{
  "type": "player_action",
  "game_id": 123,
  "player_id": 456,
  "action": { ... },
  "timestamp": "2025-01-XX..."
}
```

### Base de Données

#### Tables Existantes (✅ Créées)
- `users` - Utilisateurs
- `games` - Parties
- `game_players` - Joueurs dans les parties
- `game_states` - États des parties
- `troupes` - Cartes troupes
- `technologies` - Cartes technologies
- `quetes` - Cartes quêtes
- `armures_meca` - Configurations des armures
- `rangers` - Types de rangers
- `weapon_types` - Types d'armes
- `raw_materials` - Matières premières

#### Tables à Créer/Compléter

**État du Jeu** :
- `game_hands` - Mains des joueurs (cartes en main)
- `game_boards` - Plateaux des joueurs (cartes en jeu)
- `game_resources` - Ressources des joueurs
- `game_scores` - Scores des joueurs
- `game_actions` - Historique des actions

**Cartes en Jeu** :
- `game_cards` - Cartes dans une partie (pioche, défausse, mains, plateaux)
- `card_positions` - Positions des cartes sur les armures méca

### Validation et Règles Métier

#### Validation des Actions
- Vérifier que c'est le tour du joueur
- Vérifier les ressources disponibles
- Vérifier les contraintes de placement
- Vérifier les prérequis des cartes
- Vérifier les conditions de fin de partie

#### Calculs Automatiques
- Calcul des scores après chaque action
- Application des effets automatiques
- Vérification des conditions de quêtes
- Détection de fin de partie

### Sécurité

- Authentification JWT pour toutes les actions
- Vérification de l'appartenance à la partie
- Validation côté serveur de toutes les actions
- Protection contre la triche
- Rate limiting sur les actions

---

## 📊 Priorisation

### Phase 1 : MVP (Minimum Viable Product)
1. ✅ Authentification
2. ✅ Création/Rejoindre des parties
3. ⏳ Actions de base (jouer une carte, action de couleur)
4. ⏳ Gestion de l'état basique
5. ⏳ WebSockets pour synchronisation

### Phase 2 : Fonctionnalités Essentielles
1. Toutes les actions de jeu
2. Calcul des scores
3. Gestion complète des ressources
4. Système de tours
5. Conditions de fin de partie

### Phase 3 : Améliorations
1. Effets de cartes complexes
2. Quêtes
3. Historique et replay
4. Statistiques
5. Optimisations

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*



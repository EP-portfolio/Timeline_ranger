# Endpoints d'Actions Créés - Backend

## ✅ Fichiers Créés

### 1. `backend/app/schemas/action.py`
Schémas Pydantic pour les actions de jeu :
- `PlayColorActionRequest` - Jouer une action de couleur (Ranger)
- `PlayCardActionRequest` - Jouer une carte
- `PassActionRequest` - Passer son tour
- `GameActionResponse` - Réponse après une action
- `GameStateResponse` - État complet du jeu
- Enums : `ActionType`, `ColorAction`

### 2. `backend/app/services/game_logic.py`
Logique métier du jeu :
- `initialize_game()` - Initialise une nouvelle partie
- `rotate_ranger()` - Fait tourner les Rangers après une action
- `get_next_player()` - Détermine le prochain joueur
- `validate_color_action()` - Valide une action de couleur
- `calculate_laser_damage_points()` - Calcule les points de dégâts des lasers
- `calculate_total_damage_points()` - Calcule le total des points de dégâts

### 3. `backend/app/api/v1/actions.py`
Endpoints REST pour les actions :
- `POST /api/v1/games/{game_id}/actions/play-color` - Jouer une action de couleur
- `POST /api/v1/games/{game_id}/actions/play-card` - Jouer une carte
- `POST /api/v1/games/{game_id}/actions/pass` - Passer son tour
- `GET /api/v1/games/{game_id}/state` - Récupérer l'état complet du jeu

### 4. `backend/app/models/game_state.py`
Modèle pour sauvegarder l'état du jeu :
- `create()` - Crée un nouvel état
- `get_latest()` - Récupère le dernier état
- `update()` - Met à jour l'état

### 5. `backend/app/services/__init__.py`
Fichier d'initialisation du package services

---

## 🔧 Modifications Apportées

### `backend/app/main.py`
- Ajout de l'import `actions`
- Ajout du router `actions.router`

### `backend/app/api/v1/games.py`
- Modification de `start_game()` pour initialiser l'état du jeu

---

## 📋 Endpoints Disponibles

### Actions de Jeu

#### `POST /api/v1/games/{game_id}/actions/play-color`
Joue une action de couleur (Ranger).

**Body** :
```json
{
  "color": "blue",  // blue, black, orange, green, yellow
  "power": 3,  // 1-5
  "use_x_token": false,
  "action_data": {
    // Données selon l'action
    // Exemple pour Action Bleue : {"gain_credits": 3}
  }
}
```

**Réponse** :
```json
{
  "success": true,
  "message": "Action blue jouée avec succès",
  "game_state": {...},
  "next_player": 2
}
```

#### `POST /api/v1/games/{game_id}/actions/play-card`
Joue une carte (troupe ou technologie).

**Body** :
```json
{
  "card_id": 123,
  "card_type": "troupe",  // ou "technology"
  "position_x": 5,
  "position_y": 3,
  "action_data": {}
}
```

#### `POST /api/v1/games/{game_id}/actions/pass`
Passe son tour.

**Body** :
```json
{
  "reason": "Pas d'action possible"  // optionnel
}
```

#### `GET /api/v1/games/{game_id}/state`
Récupère l'état complet du jeu.

**Réponse** :
```json
{
  "game_id": 1,
  "status": "started",
  "turn_number": 5,
  "current_player": 2,
  "players": [...],
  "game_data": {
    "game_id": 1,
    "status": "started",
    "turn_number": 5,
    "current_player": 2,
    "player_order": [1, 2, 3, 4],
    "players": {
      "1": {
        "player_id": 1,
        "rangers": [...],
        "hand": [...],
        "resources": {...},
        "scores": {...},
        "board": {...}
      },
      ...
    }
  }
}
```

---

## 🎮 État du Jeu Initialisé

Quand une partie démarre, l'état suivant est créé :

- **Rangers** : 5 Rangers (Bleu, Noir, Orange, Vert, Jaune) en positions 1-5
- **Main** : Vide (à remplir avec les vraies cartes)
- **Ressources** : Toutes à 0 (à initialiser selon les règles)
- **Scores** : Tous à 0
- **Plateau** : Vide
- **Émissaires** : 1
- **Jetons X** : 0
- **Cartes Dernier Souffle** : Vide (à initialiser avec 2 cartes)

---

## ⚠️ À Compléter

### Logique Métier
- [ ] Distribution réelle des cartes initiales (8 cartes, garder 4)
- [ ] Initialisation des ressources selon les règles
- [ ] Distribution des cartes Dernier Souffle (2 par joueur)
- [ ] Validation complète des actions selon les règles
- [ ] Application des effets des cartes
- [ ] Calcul des scores en temps réel

### Actions Spécifiques
- [ ] Action Bleue : Jouer cartes Mécène (plusieurs si améliorée)
- [ ] Action Noire : Jouer animaux (0-1-1-1-2 ou 1-1-2-2-2)
- [ ] Action Orange : Construire parties d'armure (coût 2 crédits/case)
- [ ] Action Verte : Quêtes, mines, reliques, lasers
- [ ] Action Jaune : Piocher cartes (selon puissance ou réputation si améliorée)

### Sauvegarde d'État
- [ ] Optimiser la sauvegarde (ne pas créer un nouvel état à chaque action)
- [ ] Versioning des états pour replay
- [ ] Compression des données si nécessaire

---

## 🧪 Tests à Effectuer

1. **Créer une partie** : `POST /api/v1/games`
2. **Rejoindre la partie** : `POST /api/v1/games/join`
3. **Démarrer la partie** : `POST /api/v1/games/{id}/start`
4. **Récupérer l'état** : `GET /api/v1/games/{id}/state`
5. **Jouer une action** : `POST /api/v1/games/{id}/actions/play-color`
6. **Vérifier la rotation des Rangers**
7. **Vérifier le passage au joueur suivant**

---

## 📝 Notes

- Pour le POC, certaines validations sont simplifiées
- L'état est sauvegardé dans `game_states` à chaque action
- Les cartes ne sont pas encore intégrées (à faire)
- Les ressources initiales ne sont pas encore définies (à faire)

---

*Document créé le : 2025-01-XX*
*Endpoints d'actions créés pour le POC*


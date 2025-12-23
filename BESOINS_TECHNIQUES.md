# Besoins Techniques - Timeline Ranger

## 📋 Table des Matières

1. [Architecture Technique](#architecture-technique)
2. [API REST - Détails](#api-rest---détails)
3. [WebSockets - Spécifications](#websockets---spécifications)
4. [Base de Données - Schéma Étendu](#base-de-données---schéma-étendu)
5. [Logique Métier - Détails](#logique-métier---détails)
6. [Sécurité](#sécurité)
7. [Performance et Scalabilité](#performance-et-scalabilité)

---

## 🏗️ Architecture Technique

### Stack Technologique

**Backend** :
- FastAPI (Python) - Framework web async
- PostgreSQL (Supabase) - Base de données principale
- WebSockets (FastAPI) - Communication temps réel
- JWT - Authentification
- Pydantic - Validation de données

**Frontend** (à développer) :
- React/Vue.js - Framework UI
- WebSocket Client - Synchronisation temps réel
- Axios/Fetch - Requêtes HTTP

**Infrastructure** :
- Supabase - PostgreSQL + Realtime (optionnel)
- Render/Vercel - Hébergement

### Structure des Modules

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── auth.py          ✅
│   │   ├── games.py         ✅
│   │   ├── actions.py       ⏳ À créer
│   │   ├── cards.py         ⏳ À créer
│   │   └── websocket.py     ⏳ À créer
│   ├── core/
│   │   ├── config.py        ✅
│   │   ├── database.py      ✅
│   │   └── security.py      ✅
│   ├── models/
│   │   ├── user.py          ✅
│   │   ├── game.py          ✅
│   │   ├── action.py        ⏳ À créer
│   │   └── card.py          ⏳ À créer
│   ├── schemas/
│   │   ├── user.py          ✅
│   │   ├── game.py          ✅
│   │   ├── action.py        ⏳ À créer
│   │   └── card.py          ⏳ À créer
│   ├── services/
│   │   ├── game_logic.py    ⏳ À créer
│   │   ├── card_logic.py   ⏳ À créer
│   │   └── scoring.py       ⏳ À créer
│   └── main.py              ✅
```

---

## 🔌 API REST - Détails

### Endpoints d'Actions de Jeu

#### 1. Jouer une Action de Couleur

```http
POST /api/v1/games/{game_id}/actions/play-color
Authorization: Bearer {token}
Content-Type: application/json

{
  "color": "blue",  // "blue", "black", "orange", "green", "yellow"
  "action_details": {}  // Détails spécifiques selon l'action
}
```

**Validation** :
- Le joueur est le joueur actif
- L'action de couleur est disponible
- Les prérequis sont remplis

**Réponse** :
```json
{
  "success": true,
  "action": {
    "id": 123,
    "type": "play_color",
    "color": "blue",
    "player_id": 456,
    "timestamp": "2025-01-XX..."
  },
  "game_state": { ... }
}
```

#### 2. Jouer une Carte

```http
POST /api/v1/games/{game_id}/actions/play-card
Authorization: Bearer {token}
Content-Type: application/json

{
  "card_id": 789,  // ID de la carte (troupe ou technologie)
  "position": {
    "x": 2,
    "y": 3,
    "armure_meca_id": 1
  },
  "cost_paid": {
    "or": 5,
    "materials": {
      "titanium": 1,
      "platine": 2
    }
  }
}
```

**Validation** :
- La carte est dans la main du joueur
- Le joueur a assez de ressources
- La position est valide
- Les contraintes de placement sont respectées

**Réponse** :
```json
{
  "success": true,
  "card_played": {
    "id": 789,
    "name": "Explosif Rapide",
    "position": { "x": 2, "y": 3 }
  },
  "resources_remaining": {
    "or": 10,
    "materials": { ... }
  },
  "scores_updated": {
    "points_degats": 5,
    "lasers": 2
  },
  "effects_applied": [ ... ]
}
```

#### 3. Activer une Action Bleue

```http
POST /api/v1/games/{game_id}/actions/activate-blue
Authorization: Bearer {token}
Content-Type: application/json

{
  "card_id": 456,  // ID de la carte avec action bleue
  "action_type": "build",  // Type d'action bleue
  "target": { ... }  // Cible de l'action
}
```

#### 4. Piocher des Cartes

```http
POST /api/v1/games/{game_id}/actions/draw-cards
Authorization: Bearer {token}
Content-Type: application/json

{
  "count": 3  // Nombre de cartes (optionnel, défaut: 3)
}
```

#### 5. Passer son Tour

```http
POST /api/v1/games/{game_id}/actions/pass
Authorization: Bearer {token}
```

#### 6. Utiliser un Effet de Carte

```http
POST /api/v1/games/{game_id}/actions/use-effect
Authorization: Bearer {token}
Content-Type: application/json

{
  "card_id": 123,
  "effect_type": "daily",  // "invocation", "daily", "last_breath"
  "target": { ... }  // Cible de l'effet
}
```

### Endpoints d'État

#### Récupérer l'État Complet

```http
GET /api/v1/games/{game_id}/state
Authorization: Bearer {token}
```

**Réponse** :
```json
{
  "game": {
    "id": 1,
    "code": "ABC123",
    "status": "started",
    "turn": 5,
    "current_player": 2
  },
  "players": [
    {
      "id": 1,
      "user_id": 10,
      "player_number": 1,
      "armure_meca_id": 1,
      "resources": {
        "or": 15,
        "materials": { ... }
      },
      "scores": {
        "points_degats": 20,
        "lasers": 10,
        "points_developpement_technique": 15,
        "paires_ailes": 5
      },
      "hand_size": 5,
      "board_cards": 8
    }
  ],
  "deck": {
    "remaining": 45
  },
  "quests": {
    "available": [ ... ],
    "completed": [ ... ]
  }
}
```

#### Récupérer Ma Main

```http
GET /api/v1/games/{game_id}/my-hand
Authorization: Bearer {token}
```

**Réponse** :
```json
{
  "cards": [
    {
      "id": 123,
      "type": "troupe",
      "name": "Explosif Rapide",
      "cost": {
        "or": 5,
        "materials": { "titanium": 1 }
      },
      "points": {
        "points_degats": 3,
        "lasers": 1
      }
    }
  ]
}
```

#### Récupérer Mon Plateau

```http
GET /api/v1/games/{game_id}/my-board
Authorization: Bearer {token}
```

**Réponse** :
```json
{
  "armure_meca": {
    "id": 1,
    "name": "Armure Méca Standard",
    "grid": { ... }
  },
  "cards": [
    {
      "id": 456,
      "card_id": 123,
      "position": { "x": 2, "y": 3 },
      "rotation": 0
    }
  ]
}
```

### Endpoints de Cartes

#### Liste des Cartes Disponibles

```http
GET /api/v1/cards/troupes?limit=20&offset=0
GET /api/v1/cards/technologies?limit=20&offset=0
GET /api/v1/cards/quetes?limit=20&offset=0
```

#### Détails d'une Carte

```http
GET /api/v1/cards/{card_id}
```

### Endpoints d'Armures Méca

#### Liste des Armures

```http
GET /api/v1/armures
```

#### Détails d'une Armure

```http
GET /api/v1/armures/{id}
```

**Réponse** :
```json
{
  "id": 1,
  "name": "Armure Méca Standard",
  "type": "Débutant",
  "difficulty": "Facile",
  "grid": {
    "width": 10,
    "height": 8,
    "blocked_cells": [
      { "x": 0, "y": 0 },
      { "x": 9, "y": 7 }
    ],
    "special_zones": [
      {
        "id": 1,
        "name": "Zone de Construction",
        "cells": [ ... ],
        "effect": "Bonus +2 or par tour"
      }
    ]
  },
  "special_ability": {
    "name": "Construction Rapide",
    "description": "..."
  }
}
```

---

## 🔄 WebSockets - Spécifications

### Connexion

```javascript
// Client
const ws = new WebSocket('ws://localhost:8000/api/v1/games/123/ws?token=jwt_token');
```

### Messages Entrants (Client → Serveur)

#### Souscrire à une Partie

```json
{
  "type": "subscribe",
  "game_id": 123
}
```

#### Envoyer une Action

```json
{
  "type": "action",
  "action_type": "play_card",
  "data": {
    "card_id": 789,
    "position": { "x": 2, "y": 3 }
  }
}
```

#### Ping (Keep-alive)

```json
{
  "type": "ping"
}
```

### Messages Sortants (Serveur → Client)

#### Mise à Jour de l'État

```json
{
  "type": "game_state_update",
  "game_id": 123,
  "state": { ... },
  "timestamp": "2025-01-XX..."
}
```

#### Action d'un Joueur

```json
{
  "type": "player_action",
  "game_id": 123,
  "player_id": 456,
  "action": {
    "id": 789,
    "type": "play_card",
    "card_id": 123,
    "timestamp": "2025-01-XX..."
  }
}
```

#### Notification

```json
{
  "type": "notification",
  "level": "info",  // "info", "warning", "error", "success"
  "message": "C'est votre tour !",
  "timestamp": "2025-01-XX..."
}
```

#### Erreur

```json
{
  "type": "error",
  "code": "INVALID_ACTION",
  "message": "Cette action n'est pas valide",
  "timestamp": "2025-01-XX..."
}
```

#### Pong (Réponse au Ping)

```json
{
  "type": "pong",
  "timestamp": "2025-01-XX..."
}
```

### Gestion des Connexions

- **Authentification** : Token JWT dans l'URL ou header
- **Multiples connexions** : Un joueur peut avoir plusieurs onglets ouverts
- **Déconnexion** : Détection automatique, notification aux autres joueurs
- **Reconnexion** : Synchronisation automatique de l'état à la reconnexion

---

## 💾 Base de Données - Schéma Étendu

### Tables à Créer

#### État du Jeu

```sql
CREATE TABLE game_hands (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    card_id INTEGER,  -- Référence à troupes, technologies, ou quetes
    card_type VARCHAR(20),  -- 'troupe', 'technology', 'quete'
    position_in_hand INTEGER,  -- Ordre dans la main
    drawn_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE game_boards (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    card_id INTEGER,
    card_type VARCHAR(20),
    position_x INTEGER,
    position_y INTEGER,
    rotation INTEGER DEFAULT 0,
    placed_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE game_resources (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    or_amount INTEGER DEFAULT 0,
    titanium INTEGER DEFAULT 0,
    platine INTEGER DEFAULT 0,
    vibranium INTEGER DEFAULT 0,
    carbone INTEGER DEFAULT 0,
    kevlar INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(game_id, player_id)
);

CREATE TABLE game_actions (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    action_type VARCHAR(50),  -- 'play_color', 'play_card', 'pass', etc.
    action_data JSONB,  -- Détails de l'action
    turn_number INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE game_deck (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    card_id INTEGER,
    card_type VARCHAR(20),
    position_in_deck INTEGER,
    drawn BOOLEAN DEFAULT FALSE,
    drawn_by_player_id INTEGER REFERENCES game_players(id),
    drawn_at TIMESTAMP
);
```

---

## 🧠 Logique Métier - Détails

### Validation des Actions

#### Vérifications Générales
1. La partie est en statut "started"
2. C'est le tour du joueur
3. Le joueur n'a pas déjà joué ce tour
4. Les ressources sont suffisantes

#### Validation du Placement de Carte
1. La carte est dans la main du joueur
2. La position est dans les limites de l'Armure Méca
3. La case n'est pas bloquée
4. La case n'est pas déjà occupée
5. Les contraintes de taille sont respectées
6. Les prérequis de la carte sont remplis

#### Validation des Ressources
1. Or suffisant
2. Matières premières suffisantes (par type)
3. Coût total calculé correctement

### Calcul des Scores

#### Après Chaque Action
1. Recalculer les points de dégâts (troupes en jeu)
2. Recalculer les lasers (troupes + technologies)
3. Recalculer les points de développement technique
4. Recalculer les paires d'ailes
5. Vérifier les conditions de quêtes

#### Application des Effets
1. Effets d'invocation (immédiat)
2. Effets quotidiens (chaque tour)
3. Effets de dernier souffle (fin de partie)

### Gestion des Tours

#### Début de Tour
1. Vérifier les conditions de fin
2. Activer les effets quotidiens
3. Notifier le joueur actif
4. Mettre à jour l'état

#### Fin de Tour
1. Vérifier si le joueur a joué ou passé
2. Appliquer les effets de fin de tour
3. Passer au joueur suivant
4. Vérifier les conditions de fin de partie

### Conditions de Fin de Partie

1. **Points atteints** : Un joueur atteint X points totaux
2. **Quêtes complétées** : Toutes les quêtes sont complétées
3. **Tours maximum** : Nombre maximum de tours atteint
4. **Tous passent** : Tous les joueurs passent consécutivement

### Décompte Final

1. Calculer les scores finaux
2. Appliquer les effets "Dernier Souffle"
3. Classer les joueurs
4. Déterminer le gagnant
5. Sauvegarder les statistiques

---

## 🔒 Sécurité

### Authentification
- JWT avec expiration (24h)
- Refresh token (optionnel)
- Validation à chaque requête

### Autorisation
- Vérification de l'appartenance à la partie
- Vérification du tour actif
- Validation des actions côté serveur

### Protection contre la Triche
- Validation serveur de toutes les actions
- Vérification des ressources avant déduction
- Vérification de la main avant de jouer une carte
- Logs de toutes les actions

### Rate Limiting
- Limite de requêtes par minute
- Limite d'actions par tour
- Protection contre le spam

---

## ⚡ Performance et Scalabilité

### Optimisations Base de Données
- Index sur les colonnes fréquemment utilisées
- Pool de connexions
- Requêtes optimisées
- Cache des états fréquents

### Optimisations API
- Pagination des listes
- Compression des réponses
- Cache des données statiques (cartes, armures)
- Lazy loading des données lourdes

### Scalabilité
- Support de 4-20 joueurs simultanés
- Gestion de multiples parties en parallèle
- WebSockets avec gestion de connexions multiples
- Queue pour les actions si nécessaire

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*



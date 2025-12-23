# Architecture du Jeu en Ligne Multijoueur - Timeline Ranger

Ce document définit l'architecture complète pour transformer Timeline Ranger en un jeu en ligne multijoueur accessible via internet.

## 🎯 Objectifs

- **Jeu multijoueur en ligne** : Plusieurs joueurs peuvent jouer ensemble
- **Authentification par email** : Les joueurs s'identifient avec leur adresse email
- **Parties synchronisées** : Les actions des joueurs sont synchronisées en temps réel
- **Persistance des données** : Sauvegarde des parties, statistiques, progression

## 📊 État Actuel du Projet

### Ce qui existe déjà :
- ✅ **Base de données Neo4j** : Stockage des cartes (Animal, Mécène, Projet de Conservation, etc.)
- ✅ **Mapping complet** : Transformation Ark Nova → Timeline Ranger
- ✅ **Scripts Python** : Import de données, analyse, documentation
- ✅ **Structure de données** : Configurations des plateaux, mappings des noms

### Ce qui manque :
- ❌ **Backend API** : Pas d'API REST/GraphQL
- ❌ **Système d'authentification** : Pas de gestion des utilisateurs
- ❌ **Base de données utilisateurs** : Pas de stockage des comptes
- ❌ **Gestion de parties** : Pas de système de création/rejoindre des parties
- ❌ **Communication temps réel** : Pas de WebSockets
- ❌ **Frontend** : Pas d'interface utilisateur web
- ❌ **Infrastructure** : Pas de déploiement

## 🏗️ Architecture Proposée

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  (React/Vue.js - Interface Web)                              │
│  - Authentification                                           │
│  - Lobby / Création de parties                               │
│  - Interface de jeu                                           │
│  - Visualisation des armures méca                            │
└──────────────────────┬────────────────────────────────────────┘
                       │ HTTP/WebSocket
                       │
┌──────────────────────▼────────────────────────────────────────┐
│                      BACKEND API                              │
│  (FastAPI - Python)                                           │
│  ├── API REST                                                 │
│  │   - /auth (login, register, logout)                        │
│  │   - /users (profile, stats)                               │
│  │   - /games (create, join, list)                            │
│  │   - /cards (query Neo4j)                                  │
│  │   - /armures (configurations)                             │
│  │                                                             │
│  └── WebSocket Server                                         │
│      - Gestion des parties en cours                           │
│      - Synchronisation des actions                            │
│      - Notifications temps réel                               │
└──────────────────────┬────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
│   PostgreSQL │ │   Neo4j    │ │   Redis    │
│   (Users,   │ │   (Cards)   │ │  (Cache,   │
│   Games,    │ │             │ │  Sessions) │
│   Stats)    │ │             │ │            │
└─────────────┘ └─────────────┘ └────────────┘
```

## 🔧 Composants à Développer

### 1. Backend API (FastAPI)

#### Structure du Projet Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── config.py               # Configuration
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py             # Routes d'authentification
│   │   ├── users.py            # Routes utilisateurs
│   │   ├── games.py            # Routes de parties
│   │   ├── cards.py            # Routes de cartes (Neo4j)
│   │   └── armures.py          # Routes des armures méca
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # Modèle utilisateur
│   │   ├── game.py             # Modèle partie
│   │   ├── card.py             # Modèle carte
│   │   └── armure.py           # Modèle armure méca
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Service d'authentification
│   │   ├── game_service.py    # Logique métier des parties
│   │   ├── neo4j_service.py   # Accès à Neo4j
│   │   └── websocket_service.py # Gestion WebSocket
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── postgres.py         # Connexion PostgreSQL
│   │   ├── neo4j.py            # Connexion Neo4j
│   │   └── redis.py            # Connexion Redis
│   │
│   ├── websocket/
│   │   ├── __init__.py
│   │   ├── game_manager.py     # Gestionnaire de parties
│   │   └── handlers.py        # Handlers WebSocket
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py         # Hash passwords, JWT tokens
│       └── validators.py        # Validation des données
│
├── requirements.txt
├── .env.example
└── Dockerfile
```

#### Technologies Backend

- **FastAPI** : Framework Python moderne et performant
- **PostgreSQL** : Base de données relationnelle pour utilisateurs et parties
- **Neo4j** : Base de données graphe (déjà utilisée pour les cartes)
- **Redis** : Cache et gestion des sessions WebSocket
- **WebSockets** : Communication temps réel
- **JWT** : Authentification par tokens
- **SQLAlchemy** : ORM pour PostgreSQL
- **Pydantic** : Validation des données

### 2. Base de Données

#### PostgreSQL - Schéma Utilisateurs et Parties

```sql
-- Table des utilisateurs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Table des parties
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,  -- Code pour rejoindre
    host_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'waiting',  -- waiting, playing, finished
    max_players INTEGER DEFAULT 4,
    current_players INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    finished_at TIMESTAMP
);

-- Table des joueurs dans une partie
CREATE TABLE game_players (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    user_id INTEGER REFERENCES users(id),
    player_number INTEGER,  -- 1, 2, 3, 4
    armure_meca_id VARCHAR(50),  -- Type d'armure choisie
    score INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',  -- active, disconnected, eliminated
    joined_at TIMESTAMP DEFAULT NOW()
);

-- Table de l'état de la partie
CREATE TABLE game_states (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    turn_number INTEGER DEFAULT 0,
    current_player INTEGER,  -- player_number
    state_data JSONB,  -- État complet de la partie (JSON)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table des statistiques
CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    favorite_armure VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Neo4j - Extension pour les Parties

Ajouter des nœuds et relations pour les parties :

```cypher
// Nœud Partie
(:Game {game_id: "123", status: "playing"})

// Relation Joueur → Partie
(:User {email: "player@example.com"})-[:PLAYS_IN]->(:Game)

// Relation Carte → Partie (cartes en jeu)
(:Card)-[:IN_GAME]->(:Game)
```

### 3. Système d'Authentification

#### Fonctionnalités

- **Inscription** : Email + mot de passe
- **Connexion** : Email + mot de passe → JWT token
- **Vérification email** : Optionnel (pour production)
- **Récupération de mot de passe** : Reset par email
- **Sessions** : Gestion avec JWT

#### Flow d'Authentification

```
1. Client → POST /api/auth/register
   { email, password }
   → Backend vérifie email unique
   → Hash password (bcrypt)
   → Créer utilisateur
   → Retourner JWT token

2. Client → POST /api/auth/login
   { email, password }
   → Backend vérifie credentials
   → Retourner JWT token

3. Client → Utilise JWT dans header
   Authorization: Bearer <token>
   → Backend valide token
   → Accès aux routes protégées
```

### 4. Gestion des Parties

#### Création d'une Partie

```
POST /api/games/create
Headers: Authorization: Bearer <token>
Body: { max_players: 4, armure_meca_id: "plateau_A" }
→ Créer partie avec code unique (ex: "ABC123")
→ Ajouter créateur comme joueur
→ Retourner { game_id, code, status }
```

#### Rejoindre une Partie

```
POST /api/games/join
Headers: Authorization: Bearer <token>
Body: { code: "ABC123", armure_meca_id: "plateau_1" }
→ Vérifier que la partie existe et n'est pas pleine
→ Ajouter joueur à la partie
→ Retourner { game_id, player_number }
```

#### Liste des Parties Disponibles

```
GET /api/games/list?status=waiting
→ Retourner liste des parties en attente
```

### 5. Communication Temps Réel (WebSocket)

#### Événements WebSocket

```python
# Connexion
ws://api.timelineranger.com/game/{game_id}
Headers: Authorization: Bearer <token>

# Événements émis par le serveur
{
    "type": "game_state_update",
    "data": { ... état de la partie ... }
}

{
    "type": "player_action",
    "data": {
        "player": 1,
        "action": "use_ranger",
        "ranger": "blue",
        "action_id": 123
    }
}

{
    "type": "player_joined",
    "data": {
        "player": 2,
        "username": "Player2"
    }
}

# Événements envoyés par le client
{
    "type": "action",
    "data": {
        "ranger": "blue",
        "action_id": 123,
        "target": { ... }
    }
}
```

### 6. Frontend

#### Structure du Projet Frontend

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── ForgotPassword.jsx
│   │   ├── Lobby/
│   │   │   ├── GameList.jsx
│   │   │   ├── CreateGame.jsx
│   │   │   └── JoinGame.jsx
│   │   ├── Game/
│   │   │   ├── GameBoard.jsx
│   │   │   ├── Rangers.jsx
│   │   │   ├── ArmureMeca.jsx
│   │   │   ├── Cards.jsx
│   │   │   └── Actions.jsx
│   │   └── Common/
│   │       ├── Header.jsx
│   │       └── Footer.jsx
│   │
│   ├── services/
│   │   ├── api.js          # Client API REST
│   │   ├── websocket.js    # Client WebSocket
│   │   └── auth.js         # Gestion authentification
│   │
│   ├── store/
│   │   ├── authStore.js    # État authentification
│   │   ├── gameStore.js    # État partie
│   │   └── userStore.js    # État utilisateur
│   │
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useWebSocket.js
│   │   └── useGame.js
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── vite.config.js (ou webpack.config.js)
```

#### Technologies Frontend

- **React** ou **Vue.js** : Framework UI
- **Vite** ou **Webpack** : Build tool
- **Axios** : Client HTTP
- **Socket.io-client** : Client WebSocket
- **Zustand** ou **Redux** : State management
- **React Router** : Navigation
- **Tailwind CSS** : Styling

### 7. Infrastructure et Déploiement

#### Options de Déploiement

**Option 1 : Cloud Simple (Démarrage rapide)**
- **Backend** : Railway, Render, Fly.io
- **Frontend** : Vercel, Netlify
- **PostgreSQL** : Supabase, Neon, Railway
- **Neo4j** : Neo4j Aura (déjà utilisé)
- **Redis** : Upstash, Redis Cloud

**Option 2 : Docker + Cloud**
- **Backend** : Container Docker sur Railway/Render
- **Frontend** : Container Docker ou Vercel/Netlify
- **PostgreSQL** : Managed service
- **Neo4j** : Neo4j Aura
- **Redis** : Managed service

**Option 3 : Kubernetes (Production)**
- **Backend** : Kubernetes cluster
- **Frontend** : Kubernetes ou CDN
- **PostgreSQL** : Managed service
- **Neo4j** : Neo4j Aura
- **Redis** : Managed service

## 📋 Plan de Développement

### Phase 1 : Backend de Base (2-3 semaines)
- [ ] Configuration FastAPI
- [ ] Connexion PostgreSQL
- [ ] Modèles de données (User, Game)
- [ ] API d'authentification (register, login)
- [ ] API de gestion des parties (create, join, list)
- [ ] Tests unitaires

### Phase 2 : Intégration Neo4j (1 semaine)
- [ ] Service Neo4j pour les cartes
- [ ] API de requêtes de cartes
- [ ] Intégration avec les parties

### Phase 3 : WebSocket (2 semaines)
- [ ] Serveur WebSocket
- [ ] Gestionnaire de parties
- [ ] Synchronisation des actions
- [ ] Gestion des déconnexions

### Phase 4 : Frontend (3-4 semaines)
- [ ] Setup React/Vue
- [ ] Pages d'authentification
- [ ] Lobby (créer/rejoindre parties)
- [ ] Interface de jeu de base
- [ ] Intégration WebSocket

### Phase 5 : Logique de Jeu (4-6 semaines)
- [ ] Système de Rangers
- [ ] Gestion des actions
- [ ] Système d'armures méca
- [ ] Calcul des scores
- [ ] Fin de partie

### Phase 6 : Polish et Production (2-3 semaines)
- [ ] Tests end-to-end
- [ ] Optimisations
- [ ] Déploiement
- [ ] Documentation

## 🔐 Sécurité

- **HTTPS** : Obligatoire en production
- **JWT** : Tokens avec expiration
- **CORS** : Configuration stricte
- **Rate Limiting** : Protection contre les abus
- **Validation** : Validation stricte des entrées
- **Hash passwords** : bcrypt avec salt
- **SQL Injection** : Utiliser ORM (SQLAlchemy)
- **XSS** : Sanitization côté frontend

## 📊 Monitoring et Logs

- **Logs** : Structured logging (JSON)
- **Monitoring** : Sentry pour les erreurs
- **Analytics** : Suivi des parties, temps de jeu
- **Performance** : Métriques API (temps de réponse)

## 🚀 Prochaines Étapes Immédiates

1. **Créer la structure du backend** : Dossiers et fichiers de base
2. **Configurer PostgreSQL** : Schéma de base de données
3. **Implémenter l'authentification** : Register/Login
4. **Créer l'API de parties** : Create/Join/List
5. **Setup WebSocket** : Connexion de base
6. **Créer le frontend de base** : Pages d'auth et lobby

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


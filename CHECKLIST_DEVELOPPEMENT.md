# Checklist de Développement - Timeline Ranger Online

Liste concrète de tout ce qui doit être développé pour créer le jeu en ligne multijoueur.

## ✅ Ce qui Existe Déjà

- [x] Base de données Neo4j avec les cartes
- [x] Mapping complet Ark Nova → Timeline Ranger
- [x] Scripts Python d'import et d'analyse
- [x] Configurations des plateaux (structure)
- [x] Documentation des mappings

## ❌ Ce qui Doit Être Développé

### 1. Backend API

#### Infrastructure
- [ ] Créer structure du projet `backend/`
- [ ] Configurer FastAPI
- [ ] Setup PostgreSQL (local + cloud)
- [ ] Configurer Redis (cache + sessions)
- [ ] Variables d'environnement (.env)
- [ ] Dockerfile pour le backend

#### Authentification
- [ ] Modèle User (SQLAlchemy)
- [ ] Table users dans PostgreSQL
- [ ] Route `POST /api/auth/register`
- [ ] Route `POST /api/auth/login`
- [ ] Route `POST /api/auth/logout`
- [ ] Route `GET /api/auth/me` (profil utilisateur)
- [ ] Service de hash de mots de passe (bcrypt)
- [ ] Génération JWT tokens
- [ ] Validation JWT (middleware)
- [ ] Gestion des sessions

#### Gestion des Parties
- [ ] Modèle Game (SQLAlchemy)
- [ ] Modèle GamePlayer (SQLAlchemy)
- [ ] Modèle GameState (SQLAlchemy)
- [ ] Tables PostgreSQL (games, game_players, game_states)
- [ ] Route `POST /api/games/create`
- [ ] Route `POST /api/games/join`
- [ ] Route `GET /api/games/list`
- [ ] Route `GET /api/games/{game_id}`
- [ ] Route `POST /api/games/{game_id}/start`
- [ ] Route `POST /api/games/{game_id}/leave`
- [ ] Service de génération de codes uniques
- [ ] Validation (max joueurs, etc.)

#### API des Cartes (Neo4j)
- [ ] Service Neo4j (réutiliser code existant)
- [ ] Route `GET /api/cards`
- [ ] Route `GET /api/cards/{card_id}`
- [ ] Route `GET /api/cards/by-type/{type}`
- [ ] Route `GET /api/cards/search?q={query}`
- [ ] Intégration des cartes dans les parties

#### API des Armures Méca
- [ ] Route `GET /api/armures`
- [ ] Route `GET /api/armures/{armure_id}`
- [ ] Route `GET /api/armures/{armure_id}/configuration`
- [ ] Chargement depuis `configurations_plateaux.json`

#### WebSocket
- [ ] Serveur WebSocket (FastAPI)
- [ ] Route WebSocket `/ws/game/{game_id}`
- [ ] Gestionnaire de connexions
- [ ] Système de rooms (une room par partie)
- [ ] Événements WebSocket :
  - [ ] `game_state_update`
  - [ ] `player_action`
  - [ ] `player_joined`
  - [ ] `player_left`
  - [ ] `turn_change`
  - [ ] `game_started`
  - [ ] `game_ended`
- [ ] Gestion des déconnexions
- [ ] Reconnexion automatique

#### Logique de Jeu
- [ ] Service de gestion de partie
- [ ] Système de Rangers (rotation, puissance)
- [ ] Validation des actions
- [ ] Application des effets
- [ ] Gestion des tours
- [ ] Calcul des scores
- [ ] Conditions de fin de partie

#### Statistiques
- [ ] Modèle UserStats (SQLAlchemy)
- [ ] Table user_stats dans PostgreSQL
- [ ] Route `GET /api/users/{user_id}/stats`
- [ ] Mise à jour automatique des stats

### 2. Base de Données

#### PostgreSQL
- [ ] Créer schéma de base de données
- [ ] Table `users`
- [ ] Table `games`
- [ ] Table `game_players`
- [ ] Table `game_states`
- [ ] Table `user_stats`
- [ ] Index pour performance
- [ ] Migrations (Alembic)

#### Neo4j
- [ ] Extension du schéma pour les parties
- [ ] Nœuds Game
- [ ] Relations User → Game
- [ ] Relations Card → Game

#### Redis
- [ ] Configuration Redis
- [ ] Cache des requêtes fréquentes
- [ ] Stockage des sessions WebSocket

### 3. Frontend

#### Setup
- [ ] Créer projet React/Vue
- [ ] Configuration build (Vite/Webpack)
- [ ] Routing (React Router)
- [ ] State management (Zustand/Redux)
- [ ] Client API (Axios)
- [ ] Client WebSocket

#### Authentification
- [ ] Page Login
- [ ] Page Register
- [ ] Page Forgot Password (optionnel)
- [ ] Service d'authentification
- [ ] Gestion des tokens JWT
- [ ] Redirection après auth
- [ ] Protection des routes

#### Lobby
- [ ] Page Lobby principale
- [ ] Composant liste des parties
- [ ] Composant créer partie
- [ ] Composant rejoindre partie (code)
- [ ] Intégration WebSocket pour updates
- [ ] Navigation vers la partie

#### Interface de Jeu
- [ ] Layout principal de jeu
- [ ] Composant Rangers (5 rangers avec positions)
- [ ] Composant ArmureMeca (grille interactive)
- [ ] Composant main de cartes
- [ ] Composant actions disponibles
- [ ] Composant scores
- [ ] Composant tour actif
- [ ] Écran de fin de partie
- [ ] Retour au lobby

#### Interactions
- [ ] Sélection de Ranger (clic)
- [ ] Filtrage des actions par couleur
- [ ] Exécution d'action
- [ ] Feedback visuel (loading, success, error)
- [ ] Mise à jour temps réel via WebSocket

#### Styling
- [ ] Configuration Tailwind CSS
- [ ] Design system (couleurs, typographie)
- [ ] Responsive design
- [ ] Animations (rotation Rangers, etc.)

### 4. Infrastructure

#### Déploiement Backend
- [ ] Dockerfile
- [ ] docker-compose.yml (dev)
- [ ] Configuration production
- [ ] Déploiement (Railway/Render/Fly.io)
- [ ] Variables d'environnement production

#### Déploiement Frontend
- [ ] Configuration build production
- [ ] Déploiement (Vercel/Netlify)
- [ ] Variables d'environnement
- [ ] Configuration CORS

#### Base de Données
- [ ] PostgreSQL cloud (Supabase/Neon/Railway)
- [ ] Neo4j Aura (déjà configuré)
- [ ] Redis cloud (Upstash/Redis Cloud)
- [ ] Backups

#### Domaine et HTTPS
- [ ] Nom de domaine
- [ ] Configuration HTTPS
- [ ] DNS

### 5. Sécurité

- [ ] HTTPS obligatoire
- [ ] Validation stricte des entrées
- [ ] Protection CSRF
- [ ] Rate limiting
- [ ] CORS configuré
- [ ] Sanitization des données
- [ ] Hash passwords (bcrypt)
- [ ] JWT avec expiration
- [ ] Gestion des erreurs (pas d'exposition de détails)

### 6. Tests

#### Backend
- [ ] Tests unitaires (pytest)
- [ ] Tests d'intégration API
- [ ] Tests WebSocket
- [ ] Tests de la logique de jeu

#### Frontend
- [ ] Tests unitaires (Jest/Vitest)
- [ ] Tests de composants
- [ ] Tests E2E (Playwright/Cypress)

### 7. Documentation

- [ ] Documentation API (Swagger/OpenAPI)
- [ ] Documentation technique
- [ ] Guide de déploiement
- [ ] Guide utilisateur
- [ ] README mis à jour

### 8. Monitoring et Logs

- [ ] Logging structuré
- [ ] Monitoring des erreurs (Sentry)
- [ ] Métriques de performance
- [ ] Analytics (parties, joueurs)

## 🚀 Ordre de Priorité

### Priorité 1 (Essentiel)
1. Backend API de base (auth + parties)
2. PostgreSQL setup
3. WebSocket de base
4. Frontend auth + lobby
5. Interface de jeu minimale

### Priorité 2 (Important)
1. Logique de jeu complète
2. Intégration Neo4j
3. Fin de partie
4. Statistiques

### Priorité 3 (Améliorations)
1. Tests complets
2. Optimisations
3. Monitoring
4. Documentation complète

## 📊 Estimation

- **Backend** : ~8-10 semaines
- **Frontend** : ~6-8 semaines
- **Infrastructure** : ~2 semaines
- **Tests et Polish** : ~2 semaines

**Total** : ~16-20 semaines (4-5 mois)

## 🎯 MVP (Minimum Viable Product)

Pour une première version fonctionnelle :

- ✅ Authentification (register/login)
- ✅ Créer/rejoindre une partie (2-4 joueurs)
- ✅ Interface de jeu de base
- ✅ Actions de base (utiliser un Ranger)
- ✅ Synchronisation temps réel
- ✅ Fin de partie simple

**Durée MVP** : ~10-12 semaines

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


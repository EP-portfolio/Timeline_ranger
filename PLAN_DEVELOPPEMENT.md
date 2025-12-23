# Plan de Développement - Timeline Ranger Online

Ce document détaille le plan de développement étape par étape pour créer le jeu en ligne multijoueur.

## 🎯 Vue d'Ensemble

**Objectif** : Transformer Timeline Ranger en jeu multijoueur en ligne avec authentification par email.

**Durée estimée** : 12-16 semaines (3-4 mois)

## 📅 Phases de Développement

### Phase 1 : Setup Backend (Semaine 1-2)

#### Semaine 1 : Infrastructure de Base

**Objectifs** :
- [ ] Créer la structure du projet backend
- [ ] Configurer FastAPI
- [ ] Setup PostgreSQL (local puis cloud)
- [ ] Créer les modèles de base (User, Game)

**Tâches détaillées** :
1. Créer `backend/` avec structure FastAPI
2. Installer dépendances (FastAPI, SQLAlchemy, etc.)
3. Configurer `.env` pour les variables d'environnement
4. Créer schéma PostgreSQL (tables users, games, etc.)
5. Créer modèles SQLAlchemy
6. Tests de connexion à la base

**Livrables** :
- ✅ Backend FastAPI fonctionnel
- ✅ Base de données PostgreSQL configurée
- ✅ Modèles User et Game créés

#### Semaine 2 : Authentification

**Objectifs** :
- [ ] Implémenter l'inscription (register)
- [ ] Implémenter la connexion (login)
- [ ] Système JWT
- [ ] Hash des mots de passe

**Tâches détaillées** :
1. Route `POST /api/auth/register`
2. Route `POST /api/auth/login`
3. Service d'authentification (hash, vérification)
4. Génération et validation JWT
5. Middleware d'authentification
6. Tests d'authentification

**Livrables** :
- ✅ API d'authentification complète
- ✅ JWT fonctionnel
- ✅ Tests d'authentification

### Phase 2 : Gestion des Parties (Semaine 3-4)

#### Semaine 3 : API de Parties

**Objectifs** :
- [ ] Créer une partie
- [ ] Rejoindre une partie
- [ ] Lister les parties
- [ ] Gérer les joueurs dans une partie

**Tâches détaillées** :
1. Route `POST /api/games/create`
2. Route `POST /api/games/join`
3. Route `GET /api/games/list`
4. Route `GET /api/games/{game_id}`
5. Service de gestion des parties
6. Génération de codes uniques pour rejoindre
7. Validation (max joueurs, etc.)

**Livrables** :
- ✅ API de parties complète
- ✅ Création et rejoindre fonctionnels

#### Semaine 4 : État des Parties

**Objectifs** :
- [ ] Modèle d'état de partie
- [ ] Sauvegarde de l'état
- [ ] Chargement de l'état
- [ ] Gestion des tours

**Tâches détaillées** :
1. Modèle `GameState` dans PostgreSQL
2. Structure JSON pour l'état de partie
3. Service de sauvegarde/chargement
4. Gestion des tours de jeu
5. Validation des transitions d'état

**Livrables** :
- ✅ Système d'état de partie fonctionnel
- ✅ Persistance des parties

### Phase 3 : Intégration Neo4j (Semaine 5)

#### Semaine 5 : API des Cartes

**Objectifs** :
- [ ] Service Neo4j pour les cartes
- [ ] API de requêtes de cartes
- [ ] Intégration avec les parties

**Tâches détaillées** :
1. Service Neo4j (réutiliser code existant)
2. Route `GET /api/cards` (liste, recherche)
3. Route `GET /api/cards/{card_id}`
4. Route `GET /api/cards/by-type/{type}`
5. Intégration des cartes dans les parties
6. Tests d'intégration

**Livrables** :
- ✅ API de cartes fonctionnelle
- ✅ Intégration Neo4j complète

### Phase 4 : WebSocket (Semaine 6-7)

#### Semaine 6 : Setup WebSocket

**Objectifs** :
- [ ] Serveur WebSocket
- [ ] Connexion à une partie
- [ ] Gestion des connexions/déconnexions
- [ ] Broadcast de base

**Tâches détaillées** :
1. Setup WebSocket avec FastAPI
2. Route WebSocket `/ws/game/{game_id}`
3. Gestionnaire de connexions
4. Système de rooms (une room par partie)
5. Broadcast simple
6. Gestion des déconnexions

**Livrables** :
- ✅ WebSocket fonctionnel
- ✅ Connexion à une partie possible

#### Semaine 7 : Synchronisation

**Objectifs** :
- [ ] Synchronisation des actions
- [ ] Événements de partie
- [ ] Gestion des tours
- [ ] Notifications temps réel

**Tâches détaillées** :
1. Événements WebSocket (action, turn_change, etc.)
2. Synchronisation de l'état de partie
3. Gestion des tours (qui joue)
4. Notifications (joueur rejoint, action effectuée)
5. Gestion des erreurs et reconnexions

**Livrables** :
- ✅ Synchronisation temps réel fonctionnelle
- ✅ Parties multijoueurs opérationnelles

### Phase 5 : Frontend - Authentification et Lobby (Semaine 8-9)

#### Semaine 8 : Setup Frontend

**Objectifs** :
- [ ] Setup React/Vue
- [ ] Configuration build
- [ ] Routing
- [ ] Pages d'authentification

**Tâches détaillées** :
1. Créer projet React/Vue
2. Installer dépendances (router, axios, etc.)
3. Configuration Vite/Webpack
4. Page Login
5. Page Register
6. Service API (client HTTP)
7. Gestion des tokens JWT
8. Redirection après auth

**Livrables** :
- ✅ Frontend fonctionnel
- ✅ Authentification complète

#### Semaine 9 : Lobby

**Objectifs** :
- [ ] Page Lobby
- [ ] Liste des parties
- [ ] Créer une partie
- [ ] Rejoindre une partie

**Tâches détaillées** :
1. Page Lobby principale
2. Composant liste des parties
3. Composant créer partie
4. Composant rejoindre partie (code)
5. Intégration WebSocket pour updates
6. Navigation vers la partie

**Livrables** :
- ✅ Lobby fonctionnel
- ✅ Création/rejoindre parties possible

### Phase 6 : Frontend - Interface de Jeu (Semaine 10-12)

#### Semaine 10 : Interface de Base

**Objectifs** :
- [ ] Layout de jeu
- [ ] Affichage des Rangers
- [ ] Affichage de l'armure méca
- [ ] Connexion WebSocket

**Tâches détaillées** :
1. Layout principal de jeu
2. Composant Rangers (5 rangers avec positions)
3. Composant ArmureMeca (grille)
4. Client WebSocket
5. Intégration avec le store (state management)
6. Affichage de l'état de partie

**Livrables** :
- ✅ Interface de jeu de base
- ✅ Connexion WebSocket fonctionnelle

#### Semaine 11 : Actions et Interactions

**Objectifs** :
- [ ] Sélection de Ranger
- [ ] Affichage des actions disponibles
- [ ] Exécution d'actions
- [ ] Feedback visuel

**Tâches détaillées** :
1. Sélection de Ranger (clic)
2. Filtrage des actions par couleur
3. Affichage des actions disponibles
4. Exécution d'action (envoi WebSocket)
5. Feedback (loading, success, error)
6. Mise à jour de l'état après action

**Livrables** :
- ✅ Actions fonctionnelles
- ✅ Interactions complètes

#### Semaine 12 : Finitions Interface

**Objectifs** :
- [ ] Affichage des cartes
- [ ] Gestion des tours
- [ ] Scores et statistiques
- [ ] Fin de partie

**Tâches détaillées** :
1. Composant main de cartes
2. Affichage de la main du joueur
3. Indicateur de tour actif
4. Affichage des scores
5. Écran de fin de partie
6. Retour au lobby

**Livrables** :
- ✅ Interface de jeu complète
- ✅ Toutes les interactions fonctionnelles

### Phase 7 : Logique de Jeu (Semaine 13-14)

#### Semaine 13 : Système de Rangers

**Objectifs** :
- [ ] Rotation des Rangers
- [ ] Calcul de puissance
- [ ] Validation des actions
- [ ] Effets des actions

**Tâches détaillées** :
1. Logique de rotation (après action)
2. Calcul puissance selon position
3. Validation (Ranger peut faire cette action ?)
4. Application des effets (crédits, cartes, etc.)
5. Tests de la logique

**Livrables** :
- ✅ Système de Rangers fonctionnel
- ✅ Actions validées et appliquées

#### Semaine 14 : Armures Méca et Fin de Partie

**Objectifs** :
- [ ] Construction d'armure méca
- [ ] Placement de garnisons
- [ ] Installation d'armes
- [ ] Calcul de score final

**Tâches détaillées** :
1. Logique de construction (Ranger Orange)
2. Placement de garnisons
3. Installation d'armes (Ranger Noir)
4. Calcul des scores (dégâts, lasers, etc.)
5. Conditions de fin de partie
6. Détermination du gagnant

**Livrables** :
- ✅ Logique de jeu complète
- ✅ Fin de partie fonctionnelle

### Phase 8 : Polish et Production (Semaine 15-16)

#### Semaine 15 : Tests et Optimisations

**Objectifs** :
- [ ] Tests end-to-end
- [ ] Optimisations performance
- [ ] Gestion d'erreurs
- [ ] Logs et monitoring

**Tâches détaillées** :
1. Tests E2E (Playwright/Cypress)
2. Optimisations (cache, requêtes)
3. Gestion d'erreurs complète
4. Logging structuré
5. Monitoring de base (Sentry)

**Livrables** :
- ✅ Application testée
- ✅ Optimisée pour production

#### Semaine 16 : Déploiement

**Objectifs** :
- [ ] Déploiement backend
- [ ] Déploiement frontend
- [ ] Configuration production
- [ ] Documentation

**Tâches détaillées** :
1. Déploiement backend (Railway/Render)
2. Déploiement frontend (Vercel/Netlify)
3. Configuration variables d'environnement
4. HTTPS, domaines
5. Documentation utilisateur
6. Documentation technique

**Livrables** :
- ✅ Application déployée
- ✅ Accessible en ligne
- ✅ Documentation complète

## 📦 Dépendances à Ajouter

### Backend (`backend/requirements.txt`)

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
python-dotenv>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
redis>=5.0.0
websockets>=12.0
neo4j>=5.0.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

### Frontend (`frontend/package.json`)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "socket.io-client": "^4.6.0",
    "zustand": "^4.4.0",
    "tailwindcss": "^3.3.0"
  }
}
```

## 🎯 Critères de Succès

- ✅ Les joueurs peuvent s'inscrire et se connecter avec leur email
- ✅ Les joueurs peuvent créer et rejoindre des parties
- ✅ Les parties sont synchronisées en temps réel
- ✅ Le jeu fonctionne avec plusieurs joueurs simultanés
- ✅ Les données sont persistées (parties, scores)
- ✅ L'application est déployée et accessible en ligne

## 📝 Notes Importantes

1. **Priorités** : Commencer par le backend, puis frontend
2. **Tests** : Tester chaque phase avant de passer à la suivante
3. **Itérations** : Version minimale d'abord, puis améliorations
4. **Documentation** : Documenter au fur et à mesure
5. **Sécurité** : Ne pas négliger la sécurité dès le début

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


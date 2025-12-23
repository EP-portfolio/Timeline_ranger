# Checklist POC avec Frontend - Timeline Ranger

Ce document liste tout ce qui est nécessaire pour réaliser un premier POC fonctionnel avec un frontend.

## ✅ Ce qui Existe Déjà

### Backend
- ✅ Structure FastAPI complète
- ✅ Authentification (register, login, me)
- ✅ Gestion des parties (create, join, list, start)
- ✅ Base de données PostgreSQL (Supabase)
- ✅ Modèles et schémas de base
- ✅ Configuration et sécurité

### Documentation
- ✅ Mappings complets
- ✅ Schéma PostgreSQL
- ✅ Besoins fonctionnels et techniques
- ✅ Architecture définie

---

## ❌ Ce qui Manque pour le POC

### 1. Backend - Endpoints Manquants (Priorité HAUTE)

#### Actions de Jeu
- [ ] `POST /api/v1/games/{id}/actions/play-color` - Jouer une action de couleur (Ranger)
- [ ] `POST /api/v1/games/{id}/actions/play-card` - Jouer une carte (troupe/technologie)
- [ ] `POST /api/v1/games/{id}/actions/pass` - Passer son tour
- [ ] `GET /api/v1/games/{id}/state` - Récupérer l'état complet du jeu
- [ ] `GET /api/v1/games/{id}/hand` - Récupérer la main du joueur
- [ ] `GET /api/v1/games/{id}/board` - Récupérer l'état du plateau (armure méca)

#### Cartes
- [ ] `GET /api/v1/cards` - Lister les cartes disponibles
- [ ] `GET /api/v1/cards/{id}` - Détails d'une carte
- [ ] `GET /api/v1/cards/types/{type}` - Cartes par type (troupes/technologies/quetes)

#### Ressources
- [ ] `GET /api/v1/games/{id}/resources` - Ressources du joueur (or, matières premières)
- [ ] `POST /api/v1/games/{id}/resources/update` - Mettre à jour les ressources

#### WebSockets
- [ ] WebSocket endpoint pour synchronisation temps réel
- [ ] Gestion des connexions multiples
- [ ] Broadcast des événements de jeu

---

### 2. Backend - Logique Métier (Priorité HAUTE)

#### Gestion d'État du Jeu
- [ ] Initialisation d'une partie (distribution des cartes, ressources initiales)
- [ ] Système de tours (ordre, joueur actif)
- [ ] Rotation des cartes Action (Rangers)
- [ ] Validation des actions (règles de jeu)
- [ ] Calcul des scores (points de dégâts, lasers, réputation)

#### Actions de Couleur
- [ ] Action Bleue (Mécène) - Jouer cartes technologies OU gagner crédits
- [ ] Action Noire (Animaux) - Jouer cartes troupes
- [ ] Action Orange (Construction) - Construire parties d'armure
- [ ] Action Verte (Association) - Quêtes, mines, reliques
- [ ] Action Jaune (Cartes) - Piocher des cartes

#### Placement et Validation
- [ ] Validation du placement sur l'armure méca
- [ ] Vérification des prérequis (matières premières, or)
- [ ] Gestion des slots pour armes
- [ ] Calcul des coûts réduits (mines)

---

### 3. Frontend - Structure de Base (Priorité HAUTE)

#### Configuration
- [ ] Créer le projet frontend (React ou Vue.js)
- [ ] Configuration de build (Vite/Webpack)
- [ ] Configuration pour déploiement (Vercel/Netlify)
- [ ] Variables d'environnement (URL API)

#### Authentification
- [ ] Page de connexion (`/login`)
- [ ] Page d'inscription (`/register`)
- [ ] Gestion du token JWT (localStorage)
- [ ] Redirection si non authentifié
- [ ] Déconnexion

#### Navigation
- [ ] Layout principal avec navigation
- [ ] Router (React Router ou Vue Router)
- [ ] Pages principales :
  - `/` - Accueil
  - `/games` - Liste des parties
  - `/games/:id` - Partie en cours
  - `/profile` - Profil utilisateur

---

### 4. Frontend - Interface de Jeu (Priorité MOYENNE)

#### Lobby
- [ ] Page de création de partie
- [ ] Liste des parties en attente
- [ ] Rejoindre une partie par code
- [ ] Liste des joueurs dans le lobby
- [ ] Démarrer la partie (hôte uniquement)

#### Interface de Jeu
- [ ] Affichage du plateau (armure méca)
- [ ] Affichage de la main du joueur
- [ ] Affichage des cartes Action (Rangers) avec positions
- [ ] Affichage des ressources (or, matières premières)
- [ ] Affichage des scores (points de dégâts, lasers, réputation)
- [ ] Indicateur du joueur actif
- [ ] Historique des actions

#### Actions
- [ ] Bouton pour jouer une action de couleur
- [ ] Sélection de carte à jouer
- [ ] Placement sur le plateau (drag & drop ou clic)
- [ ] Confirmation d'action
- [ ] Bouton "Passer son tour"

#### Temps Réel
- [ ] Connexion WebSocket
- [ ] Mise à jour automatique de l'état
- [ ] Notifications d'événements
- [ ] Indicateur de connexion

---

### 5. Frontend - Composants UI (Priorité BASSE pour POC)

#### Composants de Base
- [ ] Boutons
- [ ] Cartes (affichage)
- [ ] Modales
- [ ] Notifications/Toast
- [ ] Loading states

#### Composants Spécialisés
- [ ] Composant Carte (troupe/technologie/quête)
- [ ] Composant Plateau (armure méca)
- [ ] Composant Main (cartes du joueur)
- [ ] Composant Rangers (cartes Action)
- [ ] Composant Ressources
- [ ] Composant Scores

---

### 6. Intégration et Tests (Priorité MOYENNE)

#### Tests Backend
- [ ] Tests des endpoints d'authentification
- [ ] Tests des endpoints de parties
- [ ] Tests des actions de jeu
- [ ] Tests de validation

#### Tests Frontend
- [ ] Tests de connexion
- [ ] Tests de création/rejoindre partie
- [ ] Tests d'affichage de l'état

#### Intégration
- [ ] Connexion frontend-backend
- [ ] Gestion des erreurs
- [ ] Gestion des timeouts
- [ ] Reconnexion automatique

---

## 🎯 Plan Minimum pour POC Fonctionnel

### Phase 1 : Backend Minimal (1-2 semaines)

**Objectif** : Pouvoir jouer une action basique

1. **Endpoints Actions** :
   - `POST /api/v1/games/{id}/actions/play-color` - Jouer une action de couleur
   - `GET /api/v1/games/{id}/state` - État du jeu
   - `POST /api/v1/games/{id}/actions/pass` - Passer son tour

2. **Logique Métier Basique** :
   - Initialisation d'une partie (cartes, ressources)
   - Système de tours simple
   - Rotation des cartes Action
   - Validation basique

3. **WebSockets Basiques** :
   - Connexion WebSocket
   - Broadcast des changements d'état

### Phase 2 : Frontend Minimal (1-2 semaines)

**Objectif** : Interface basique pour jouer

1. **Authentification** :
   - Login/Register
   - Gestion du token

2. **Lobby** :
   - Créer/Rejoindre partie
   - Liste des joueurs

3. **Interface de Jeu Basique** :
   - Affichage de l'état du jeu
   - Boutons pour jouer une action
   - Affichage de la main
   - Mise à jour temps réel (WebSocket)

### Phase 3 : Améliorations (1 semaine)

**Objectif** : Rendre le POC plus jouable

1. **Actions Complètes** :
   - Toutes les actions de couleur
   - Placement de cartes
   - Validation complète

2. **UI Améliorée** :
   - Meilleur affichage du plateau
   - Drag & drop pour les cartes
   - Feedback visuel

---

## 📦 Stack Technique Recommandée pour POC

### Frontend
- **Framework** : React (avec Vite) ou Vue.js
- **Routing** : React Router ou Vue Router
- **HTTP Client** : Axios ou Fetch
- **WebSocket** : Native WebSocket API ou Socket.io-client
- **State Management** : Context API (React) ou Pinia (Vue) - optionnel pour POC
- **UI** : Tailwind CSS ou CSS simple pour POC

### Backend (déjà en place)
- **Framework** : FastAPI
- **WebSocket** : FastAPI WebSockets
- **Database** : PostgreSQL (Supabase)

### Déploiement
- **Frontend** : Vercel (gratuit)
- **Backend** : Render (gratuit)
- **Database** : Supabase (gratuit)

---

## 🚀 Ordre de Priorité pour Démarrer

1. **Backend - Actions de Jeu** (CRITIQUE)
   - Créer les endpoints pour jouer une action
   - Implémenter la logique de base

2. **Backend - État du Jeu** (CRITIQUE)
   - Endpoint pour récupérer l'état complet
   - Initialisation d'une partie

3. **Frontend - Structure** (CRITIQUE)
   - Créer le projet
   - Authentification basique
   - Connexion au backend

4. **Frontend - Interface de Jeu** (IMPORTANT)
   - Affichage de l'état
   - Actions basiques

5. **WebSockets** (IMPORTANT)
   - Synchronisation temps réel

6. **Améliorations** (NICE TO HAVE)
   - UI améliorée
   - Validation complète
   - Toutes les actions

---

## 📝 Notes

- Pour un POC, on peut simplifier certaines règles
- L'important est d'avoir un flux de jeu fonctionnel
- On peut commencer avec 2 joueurs seulement
- L'UI peut être basique (l'important est la fonctionnalité)

---

*Document créé le : 2025-01-XX*
*Pour réaliser un POC fonctionnel avec frontend*


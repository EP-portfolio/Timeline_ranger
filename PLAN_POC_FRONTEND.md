# Plan Détaillé - POC avec Frontend

Plan d'action concret pour réaliser un POC fonctionnel avec frontend.

## 🎯 Objectif du POC

Créer une version minimale mais jouable du jeu Timeline Ranger avec :
- Authentification fonctionnelle
- Création/Rejoindre une partie
- Interface de jeu basique
- Possibilité de jouer quelques actions
- Synchronisation temps réel entre joueurs

---

## 📋 Étapes Détaillées

### Étape 1 : Backend - Endpoints Actions (3-5 jours)

#### 1.1 Créer le fichier `backend/app/api/v1/actions.py`

```python
# Endpoints pour les actions de jeu
- POST /api/v1/games/{id}/actions/play-color
- POST /api/v1/games/{id}/actions/play-card
- POST /api/v1/games/{id}/actions/pass
- GET /api/v1/games/{id}/state
```

#### 1.2 Créer le fichier `backend/app/services/game_logic.py`

```python
# Logique métier du jeu
- Initialisation d'une partie
- Gestion des tours
- Rotation des cartes Action
- Validation des actions
- Calcul des scores
```

#### 1.3 Créer les schémas `backend/app/schemas/action.py`

```python
# Schémas Pydantic pour les actions
- PlayColorAction
- PlayCardAction
- GameStateResponse
```

#### 1.4 Créer les modèles `backend/app/models/game_state.py`

```python
# Modèles pour l'état du jeu
- Sauvegarde de l'état
- Récupération de l'état
```

---

### Étape 2 : Backend - WebSockets (2-3 jours)

#### 2.1 Créer le fichier `backend/app/api/v1/websocket.py`

```python
# WebSocket endpoint
- Connexion WebSocket
- Authentification via token
- Broadcast des événements
- Gestion des déconnexions
```

#### 2.2 Intégrer dans `backend/app/main.py`

```python
# Ajouter le router WebSocket
app.include_router(websocket.router)
```

---

### Étape 3 : Frontend - Structure de Base (2-3 jours)

#### 3.1 Créer le projet

```bash
# Option 1 : React avec Vite
npm create vite@latest frontend -- --template react
cd frontend
npm install

# Option 2 : Vue.js avec Vite
npm create vite@latest frontend -- --template vue
cd frontend
npm install
```

#### 3.2 Installer les dépendances

```bash
npm install axios react-router-dom
# ou pour Vue
npm install axios vue-router
```

#### 3.3 Structure des dossiers

```
frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   └── Game/
│   │       ├── GameBoard.jsx
│   │       ├── PlayerHand.jsx
│   │       └── ActionCards.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Games.jsx
│   │   └── GameRoom.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── websocket.js
│   ├── utils/
│   │   └── auth.js
│   └── App.jsx
```

---

### Étape 4 : Frontend - Authentification (1-2 jours)

#### 4.1 Créer le service API (`src/services/api.js`)

```javascript
// Configuration Axios
// Fonctions : login, register, getCurrentUser
```

#### 4.2 Créer les pages Login/Register

```javascript
// Pages avec formulaires
// Gestion du token JWT
// Redirection après connexion
```

#### 4.3 Créer le système de routes

```javascript
// Routes protégées
// Redirection si non authentifié
```

---

### Étape 5 : Frontend - Lobby (2-3 jours)

#### 5.1 Page Liste des Parties

```javascript
// Afficher les parties en attente
// Bouton pour créer une partie
// Bouton pour rejoindre par code
```

#### 5.2 Page Lobby de Partie

```javascript
// Liste des joueurs
// Choix de l'armure méca
// Bouton "Démarrer" (hôte uniquement)
```

---

### Étape 6 : Frontend - Interface de Jeu (3-5 jours)

#### 6.1 Affichage de l'État

```javascript
// Composant pour afficher :
// - Plateau (armure méca)
// - Main du joueur
// - Cartes Action (Rangers)
// - Ressources
// - Scores
```

#### 6.2 Actions de Jeu

```javascript
// Boutons pour :
// - Jouer une action de couleur
// - Jouer une carte
// - Passer son tour
```

#### 6.3 WebSocket Client

```javascript
// Connexion WebSocket
// Écoute des événements
// Mise à jour automatique de l'état
```

---

### Étape 7 : Intégration et Tests (2-3 jours)

#### 7.1 Tests de Connexion

```bash
# Tester :
# - Authentification
# - Création de partie
# - Rejoindre partie
# - Actions de jeu
```

#### 7.2 Tests Multi-Joueurs

```bash
# Tester avec 2-4 joueurs :
# - Synchronisation temps réel
# - Actions simultanées
# - Gestion des tours
```

---

## 🛠️ Fichiers à Créer

### Backend

1. `backend/app/api/v1/actions.py` - Endpoints actions
2. `backend/app/api/v1/websocket.py` - WebSocket
3. `backend/app/services/game_logic.py` - Logique métier
4. `backend/app/schemas/action.py` - Schémas actions
5. `backend/app/models/game_state.py` - Modèles état

### Frontend

1. `frontend/` - Projet complet
2. `frontend/src/services/api.js` - Service API
3. `frontend/src/services/websocket.js` - Service WebSocket
4. `frontend/src/pages/Login.jsx` - Page login
5. `frontend/src/pages/Register.jsx` - Page register
6. `frontend/src/pages/Games.jsx` - Liste parties
7. `frontend/src/pages/GameRoom.jsx` - Interface de jeu
8. `frontend/src/components/GameBoard.jsx` - Plateau
9. `frontend/src/components/PlayerHand.jsx` - Main
10. `frontend/src/components/ActionCards.jsx` - Rangers

---

## ⏱️ Estimation Totale

- **Backend Actions** : 3-5 jours
- **Backend WebSockets** : 2-3 jours
- **Frontend Structure** : 2-3 jours
- **Frontend Auth** : 1-2 jours
- **Frontend Lobby** : 2-3 jours
- **Frontend Jeu** : 3-5 jours
- **Intégration** : 2-3 jours

**Total** : 15-24 jours (3-5 semaines)

---

## 🚀 Démarrage Rapide

### Commencer par le Backend

1. Créer `backend/app/api/v1/actions.py`
2. Implémenter `POST /api/v1/games/{id}/actions/play-color`
3. Implémenter `GET /api/v1/games/{id}/state`
4. Tester avec Postman/Thunder Client

### Puis le Frontend

1. Créer le projet React/Vue
2. Créer les pages Login/Register
3. Connecter au backend
4. Créer l'interface de jeu basique

---

*Document créé le : 2025-01-XX*
*Plan d'action pour POC avec frontend*


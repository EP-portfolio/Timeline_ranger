# Timeline Ranger - Frontend

Frontend React pour Timeline Ranger.

## 🚀 Installation

```bash
cd frontend
npm install
```

## 🏃 Démarrage

```bash
npm run dev
```

L'application sera accessible sur http://localhost:3000

## 📦 Structure

```
frontend/
├── src/
│   ├── components/      # Composants réutilisables
│   ├── contexts/        # Contextes React (Auth)
│   ├── pages/           # Pages de l'application
│   ├── services/        # Services API et WebSocket
│   ├── App.jsx          # Composant principal
│   └── main.jsx         # Point d'entrée
├── package.json
└── vite.config.js
```

## 🔧 Configuration

Créez un fichier `.env` à la racine du projet frontend :

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## 📝 Pages

- `/login` - Connexion
- `/register` - Inscription
- `/` - Accueil
- `/games` - Liste des parties
- `/games/:id` - Partie en cours

## 🔌 WebSocket

Le service WebSocket se connecte automatiquement quand vous entrez dans une partie.
Il écoute les événements suivants :
- `game_state_update` - Mise à jour de l'état du jeu
- `player_connected` - Un joueur se connecte
- `player_disconnected` - Un joueur se déconnecte


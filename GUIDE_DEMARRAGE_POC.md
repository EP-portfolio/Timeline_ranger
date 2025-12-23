# Guide de Démarrage - POC Timeline Ranger

Guide complet pour démarrer et tester le POC.

## 📋 Prérequis

- Python 3.8+
- Node.js 18+
- PostgreSQL (Supabase)
- Variables d'environnement configurées (`.env`)

---

## 🚀 Démarrage Rapide

### 1. Backend

```bash
# Aller dans le dossier backend
cd backend

# Installer les dépendances (si pas déjà fait)
pip install -r requirements.txt

# Démarrer le serveur
uvicorn app.main:app --reload
```

Le backend sera accessible sur : `http://localhost:8000`
Documentation API : `http://localhost:8000/docs`

### 2. Frontend

```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances (première fois)
npm install

# Démarrer le serveur de développement
npm run dev
```

Le frontend sera accessible sur : `http://localhost:3000`

---

## 🧪 Tests

### Tests des Endpoints

```bash
cd backend
python test_endpoints.py
```

Le script va :
1. Tester le health check
2. Créer 2 utilisateurs de test
3. Créer une partie
4. Rejoindre la partie
5. Démarrer la partie
6. Tester les actions de jeu

---

## 🎮 Utilisation

### 1. Créer un Compte

1. Aller sur `http://localhost:3000`
2. Cliquer sur "S'inscrire"
3. Remplir le formulaire (email, username, password)
4. Vous serez automatiquement connecté

### 2. Créer une Partie

1. Sur la page d'accueil, cliquer sur "Créer une Partie"
2. Ou aller sur `/games` et cliquer sur "Créer une Partie"

### 3. Rejoindre une Partie

**Option 1** : Via la liste
- Aller sur `/games`
- Cliquer sur "Rejoindre" sur une partie disponible

**Option 2** : Par code
- Aller sur `/games`
- Entrer le code de la partie
- Cliquer sur "Rejoindre"

### 4. Démarrer la Partie

- L'hôte de la partie peut cliquer sur "Démarrer"
- Il faut au moins 2 joueurs

### 5. Jouer

- Quand c'est votre tour, vous verrez "C'est votre tour !"
- Cliquer sur un Ranger pour jouer son action
- Ou cliquer sur "Passer mon Tour"

---

## 🔌 WebSocket

Le WebSocket se connecte automatiquement quand vous entrez dans une partie.

**Événements reçus** :
- `game_state_update` - Mise à jour de l'état du jeu
- `player_connected` - Un joueur se connecte
- `player_disconnected` - Un joueur se déconnecte

**Indicateur de connexion** :
- 🟢 Connecté (en haut à droite de la partie)
- 🔴 Déconnecté

---

## 🐛 Dépannage

### Backend ne démarre pas

1. Vérifier que PostgreSQL est accessible
2. Vérifier les variables d'environnement dans `.env`
3. Vérifier que le port 8000 est libre

### Frontend ne se connecte pas au backend

1. Vérifier que le backend tourne sur `http://localhost:8000`
2. Vérifier la configuration dans `frontend/vite.config.js`
3. Vérifier les CORS dans `backend/app/main.py`

### WebSocket ne fonctionne pas

1. Vérifier que le backend supporte WebSocket
2. Vérifier que le token JWT est valide
3. Vérifier les logs du backend pour les erreurs

---

## 📝 Notes

- Pour le POC, certaines fonctionnalités sont simplifiées
- Les cartes ne sont pas encore intégrées
- L'UI est basique mais fonctionnelle
- Les règles complètes ne sont pas encore implémentées

---

*Guide créé le : 2025-01-XX*


# Timeline Ranger - Backend API

API FastAPI pour le jeu Timeline Ranger (version en ligne d'Ark Nova).

## 🚀 Installation

### 1. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Créer un fichier `.env` à la racine du projet (ou utiliser celui du projet parent) :

```env
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=votre_mot_de_passe
SUPABASE_PORT=5432
SECRET_KEY=votre_cle_secrete_jwt
```

### 4. Lancer l'API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : http://localhost:8000

## 📚 Documentation

Une fois l'API lancée, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### Inscription
```bash
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "motdepasse",
  "username": "username"
}
```

### Connexion
```bash
POST /api/v1/auth/login
{
  "username": "user@example.com",  # OAuth2 utilise 'username' pour l'email
  "password": "motdepasse"
}
```

Réponse :
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Utiliser le token

Ajoutez le header dans vos requêtes :
```
Authorization: Bearer eyJ...
```

## 🎮 Endpoints Principaux

### Parties

- `POST /api/v1/games` - Créer une partie
- `GET /api/v1/games` - Lister les parties en attente
- `GET /api/v1/games/{game_code}` - Récupérer une partie
- `POST /api/v1/games/join` - Rejoindre une partie
- `GET /api/v1/games/{game_id}/players` - Liste des joueurs
- `POST /api/v1/games/{game_id}/start` - Démarrer une partie

## 🏗️ Structure du Projet

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py      # Routes d'authentification
│   │       └── games.py     # Routes des parties
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Gestion DB
│   │   └── security.py      # Sécurité (JWT, hash)
│   ├── models/
│   │   ├── user.py          # Modèles utilisateurs
│   │   └── game.py          # Modèles parties
│   ├── schemas/
│   │   ├── user.py          # Schémas Pydantic utilisateurs
│   │   └── game.py          # Schémas Pydantic parties
│   └── main.py              # Application principale
├── requirements.txt
└── README.md
```

## 🔄 Prochaines Étapes

- [ ] WebSockets pour la synchronisation temps réel
- [ ] Endpoints pour les actions de jeu
- [ ] Gestion de l'état des parties
- [ ] Système de tour par tour
- [ ] Calcul des scores


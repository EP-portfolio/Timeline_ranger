# Guide de Démarrage Rapide - Backend Timeline Ranger

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Depuis le dossier backend/
pip install -r requirements.txt
```

### 2. Configuration

Le backend utilise le fichier `.env` à la racine du projet (TIMELINE_RANGER/.env).

Assurez-vous qu'il contient :
```env
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=votre_mot_de_passe
SUPABASE_PORT=5432
SECRET_KEY=votre_cle_secrete_jwt
```

### 3. Lancer l'API

```bash
# Depuis le dossier backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : **http://localhost:8000**

### 4. Tester l'API

- **Documentation Swagger** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health

## 📝 Exemples de Requêtes

### Inscription

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "motdepasse123",
    "username": "testuser"
  }'
```

### Connexion

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=motdepasse123"
```

Réponse :
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Créer une partie

```bash
curl -X POST "http://localhost:8000/api/v1/games" \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "max_players": 4
  }'
```

### Lister les parties

```bash
curl -X GET "http://localhost:8000/api/v1/games"
```

### Rejoindre une partie

```bash
curl -X POST "http://localhost:8000/api/v1/games/join" \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "game_code": "ABC123"
  }'
```

## 🔧 Structure du Code

```
backend/
├── app/
│   ├── api/v1/          # Routes API
│   │   ├── auth.py      # Authentification
│   │   └── games.py     # Parties
│   ├── core/            # Configuration
│   │   ├── config.py    # Settings
│   │   ├── database.py  # Pool DB
│   │   └── security.py  # JWT, hash
│   ├── models/          # Accès DB
│   │   ├── user.py
│   │   └── game.py
│   ├── schemas/         # Pydantic
│   │   ├── user.py
│   │   └── game.py
│   └── main.py          # App principale
├── requirements.txt
└── README.md
```

## ⚠️ Notes Importantes

1. **Pool de Connexions** : Le backend utilise un pool de connexions PostgreSQL pour optimiser les performances.

2. **JWT** : Les tokens JWT expirent après 24 heures par défaut (configurable dans `config.py`).

3. **CORS** : Les origines autorisées sont configurées dans `config.py` (par défaut : localhost:3000 et localhost:5173).

4. **Base de Données** : Assurez-vous que le schéma SQL a été exécuté dans Supabase avant de lancer l'API.

## 🐛 Dépannage

### Erreur de connexion à la base de données
- Vérifiez que le fichier `.env` est correctement configuré
- Vérifiez que Supabase est accessible
- Vérifiez que le schéma SQL a été exécuté

### Erreur d'import
- Assurez-vous d'être dans le dossier `backend/` ou d'avoir ajouté le chemin au PYTHONPATH
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`

### Erreur JWT
- Vérifiez que `SECRET_KEY` est défini dans `.env`
- Utilisez une clé secrète forte en production


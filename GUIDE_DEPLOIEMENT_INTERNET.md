# Guide de Déploiement sur Internet - Timeline Ranger

Guide complet pour déployer le jeu sur internet et le tester en ligne.

## 🎯 Objectif

Déployer le jeu sur internet pour pouvoir y jouer depuis n'importe où avec d'autres joueurs.

## 📋 Architecture Recommandée (Low-Cost)

### Stack Gratuit
- **Frontend** : Vercel (gratuit)
- **Backend** : Render (gratuit - 750h/mois)
- **Base de données** : Supabase (gratuit - 500MB)

---

## 🚀 Étape 1 : Préparer le Backend

### 1.1 Créer un compte Render

1. Aller sur https://render.com
2. Créer un compte (gratuit)
3. Connecter votre compte GitHub (recommandé)

### 1.2 Créer un Web Service sur Render

1. Dans Render, cliquer sur "New +" → "Web Service"
2. Connecter votre repository GitHub
3. Configuration :
   - **Name** : `timeline-ranger-backend`
   - **Environment** : `Python 3`
   - **Build Command** : `cd backend && pip install -r requirements.txt`
   - **Start Command** : `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan** : Free

### 1.3 Variables d'Environnement sur Render

Dans les settings du service, ajouter les variables d'environnement :

```
SUPABASE_HOST=votre-host.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=votre-mot-de-passe
SUPABASE_PORT=5432
SECRET_KEY=votre-secret-key-tres-long-et-aleatoire
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=https://votre-frontend.vercel.app,https://votre-frontend.netlify.app
APP_NAME=Timeline Ranger API
APP_VERSION=0.1.0
DEBUG=False
```

**Important** : 
- Générer un `SECRET_KEY` sécurisé (ex: `openssl rand -hex 32`)
- Ajouter l'URL du frontend dans `CORS_ORIGINS`

### 1.4 Créer le fichier `render.yaml` (Optionnel)

Créer `render.yaml` à la racine du projet :

```yaml
services:
  - type: web
    name: timeline-ranger-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SUPABASE_HOST
        sync: false
      - key: SUPABASE_DB
        sync: false
      - key: SUPABASE_USER
        sync: false
      - key: SUPABASE_PASSWORD
        sync: false
      - key: SUPABASE_PORT
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 1440
      - key: CORS_ORIGINS
        sync: false
      - key: APP_NAME
        value: Timeline Ranger API
      - key: APP_VERSION
        value: 0.1.0
      - key: DEBUG
        value: False
```

---

## 🌐 Étape 2 : Déployer le Frontend

### 2.1 Créer un compte Vercel

1. Aller sur https://vercel.com
2. Créer un compte (gratuit)
3. Connecter votre compte GitHub

### 2.2 Déployer le Frontend

1. Dans Vercel, cliquer sur "Add New..." → "Project"
2. Importer votre repository GitHub
3. Configuration :
   - **Framework Preset** : Vite
   - **Root Directory** : `frontend`
   - **Build Command** : `npm run build`
   - **Output Directory** : `dist`

### 2.3 Variables d'Environnement sur Vercel

Dans les settings du projet, ajouter :

```
VITE_API_URL=https://votre-backend.onrender.com/api/v1
```

**Important** : Remplacer `votre-backend.onrender.com` par l'URL réelle de votre backend Render.

### 2.4 Créer le fichier `vercel.json` (Optionnel)

Créer `vercel.json` dans le dossier `frontend/` :

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## 🔧 Étape 3 : Configurations

### 3.1 Mettre à jour le Backend pour Internet

#### Modifier `backend/app/core/config.py`

S'assurer que les CORS acceptent les URLs de production :

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "https://votre-frontend.vercel.app",  # À remplacer
    "https://votre-frontend.netlify.app",  # Si vous utilisez Netlify
]
```

#### Modifier `backend/app/api/v1/websocket.py`

Mettre à jour l'URL WebSocket pour la production :

```python
# Dans le frontend, utiliser wss:// au lieu de ws:// pour HTTPS
```

### 3.2 Mettre à jour le Frontend

#### Modifier `frontend/src/services/api.js`

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
```

#### Modifier `frontend/src/services/websocket.js`

```javascript
// Détecter automatiquement l'URL WebSocket
const getWebSocketUrl = () => {
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
  const wsUrl = apiUrl.replace('http://', 'ws://').replace('https://', 'wss://')
  return wsUrl.replace('/api/v1', '')
}

// Dans la fonction connect :
const wsUrl = `${getWebSocketUrl()}/ws/games/${gameId}?token=${token}`
```

---

## 📝 Étape 4 : Fichiers à Créer/Modifier

### 4.1 Backend - `backend/Procfile` (pour Render)

```
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4.2 Backend - `backend/runtime.txt` (Optionnel)

```
python-3.11.0
```

### 4.3 Frontend - `.env.production` (Optionnel)

```
VITE_API_URL=https://votre-backend.onrender.com/api/v1
```

---

## 🧪 Étape 5 : Tester le Déploiement

### 5.1 Tester le Backend

1. Une fois déployé sur Render, vous obtiendrez une URL : `https://votre-backend.onrender.com`
2. Tester : `https://votre-backend.onrender.com/health`
3. Tester : `https://votre-backend.onrender.com/docs` (documentation Swagger)

### 5.2 Tester le Frontend

1. Une fois déployé sur Vercel, vous obtiendrez une URL : `https://votre-frontend.vercel.app`
2. Ouvrir l'URL dans un navigateur
3. Tester la connexion
4. Tester la création de partie

### 5.3 Tester le WebSocket

1. Ouvrir la console du navigateur (F12)
2. Aller dans une partie
3. Vérifier les logs WebSocket
4. Tester une action et vérifier la mise à jour temps réel

---

## 🔒 Étape 6 : Sécurité

### 6.1 HTTPS

- Vercel et Render fournissent HTTPS automatiquement
- Assurez-vous d'utiliser `wss://` pour WebSocket sur HTTPS

### 6.2 Variables d'Environnement

- **Ne jamais** commiter les variables d'environnement dans Git
- Utiliser les variables d'environnement des plateformes
- Générer des `SECRET_KEY` sécurisés

### 6.3 CORS

- Limiter les origines CORS aux URLs de production uniquement
- Ne pas utiliser `*` en production

---

## 🐛 Dépannage

### Backend ne démarre pas sur Render

1. Vérifier les logs dans Render Dashboard
2. Vérifier que toutes les variables d'environnement sont définies
3. Vérifier que le port est bien `$PORT` (variable d'environnement Render)

### Frontend ne se connecte pas au backend

1. Vérifier l'URL dans `VITE_API_URL`
2. Vérifier les CORS dans le backend
3. Vérifier la console du navigateur pour les erreurs

### WebSocket ne fonctionne pas

1. Vérifier que vous utilisez `wss://` pour HTTPS
2. Vérifier que le backend supporte WebSocket
3. Vérifier les logs du backend

---

## 📊 URLs Finales

Après déploiement, vous aurez :

- **Backend API** : `https://votre-backend.onrender.com`
- **Backend Docs** : `https://votre-backend.onrender.com/docs`
- **Frontend** : `https://votre-frontend.vercel.app`
- **WebSocket** : `wss://votre-backend.onrender.com/ws/games/{id}`

---

## 🎮 Tester avec Plusieurs Joueurs

1. Ouvrir le jeu dans plusieurs navigateurs/onglets
2. Créer des comptes différents
3. Créer une partie
4. Rejoindre avec les autres comptes
5. Tester les actions et la synchronisation temps réel

---

## 💡 Alternatives

### Netlify au lieu de Vercel

1. Aller sur https://netlify.com
2. Connecter votre repository
3. Configuration similaire à Vercel

### Railway au lieu de Render

1. Aller sur https://railway.app
2. Configuration similaire à Render

---

*Guide créé le : 2025-01-XX*
*Pour déployer Timeline Ranger sur internet*


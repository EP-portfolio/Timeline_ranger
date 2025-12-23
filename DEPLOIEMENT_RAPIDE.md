# Déploiement Rapide sur Internet - Timeline Ranger

Guide simplifié pour déployer le jeu sur internet en 30 minutes.

## 🎯 Objectif

Avoir le jeu accessible sur internet pour le tester avec d'autres joueurs.

---

## 📋 Prérequis

1. Compte GitHub (gratuit)
2. Compte Render (gratuit) - https://render.com
3. Compte Vercel (gratuit) - https://vercel.com
4. Compte Supabase (gratuit) - https://supabase.com (déjà configuré)

---

## 🚀 Étape 1 : Préparer le Code (5 min)

### 1.1 Pousser le code sur GitHub

```bash
# Si pas déjà fait
git init
git add .
git commit -m "Initial commit - Timeline Ranger POC"
git remote add origin https://github.com/votre-username/timeline-ranger.git
git push -u origin main
```

---

## 🌐 Étape 2 : Déployer le Backend sur Render (10 min)

### 2.1 Créer le service

1. Aller sur https://render.com
2. Se connecter avec GitHub
3. Cliquer sur "New +" → "Web Service"
4. Sélectionner votre repository GitHub

### 2.2 Configuration

- **Name** : `timeline-ranger-backend`
- **Environment** : `Python 3`
- **Build Command** : `cd backend && pip install -r requirements.txt`
- **Start Command** : `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.3 Variables d'Environnement

Dans "Environment Variables", ajouter :

```
SUPABASE_HOST=votre-host.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=votre-mot-de-passe
SUPABASE_PORT=5432
SECRET_KEY=<générer-une-clé-sécurisée>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
APP_NAME=Timeline Ranger API
APP_VERSION=0.1.0
DEBUG=False
```

**Pour générer SECRET_KEY** :
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.4 Déployer

Cliquer sur "Create Web Service"

**Note** : Le premier déploiement prend 5-10 minutes.

### 2.5 Récupérer l'URL

Une fois déployé, vous obtiendrez une URL comme :
`https://timeline-ranger-backend.onrender.com`

**⚠️ Important** : Notez cette URL, vous en aurez besoin pour le frontend !

---

## 🎨 Étape 3 : Déployer le Frontend sur Vercel (10 min)

### 3.1 Créer le projet

1. Aller sur https://vercel.com
2. Se connecter avec GitHub
3. Cliquer sur "Add New..." → "Project"
4. Importer votre repository

### 3.2 Configuration

- **Framework Preset** : Vite
- **Root Directory** : `frontend`
- **Build Command** : `npm run build` (automatique)
- **Output Directory** : `dist` (automatique)

### 3.3 Variables d'Environnement

Dans "Environment Variables", ajouter :

```
VITE_API_URL=https://timeline-ranger-backend.onrender.com/api/v1
```

**⚠️ Important** : Remplacer par votre URL Render réelle !

### 3.4 Déployer

Cliquer sur "Deploy"

**Note** : Le déploiement prend 2-3 minutes.

### 3.5 Récupérer l'URL

Une fois déployé, vous obtiendrez une URL comme :
`https://timeline-ranger.vercel.app`

---

## 🔧 Étape 4 : Mettre à Jour les CORS (5 min)

### 4.1 Retour sur Render

1. Aller dans les settings de votre service backend
2. Modifier la variable `CORS_ORIGINS` :

```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://timeline-ranger.vercel.app
```

**⚠️ Important** : Remplacer par votre URL Vercel réelle !

### 4.2 Redéployer

Le service va redémarrer automatiquement.

---

## ✅ Étape 5 : Tester (5 min)

### 5.1 Tester le Backend

1. Ouvrir : `https://votre-backend.onrender.com/health`
2. Devrait retourner : `{"status": "healthy"}`

### 5.2 Tester le Frontend

1. Ouvrir : `https://votre-frontend.vercel.app`
2. Créer un compte
3. Créer une partie
4. Tester les actions

### 5.3 Tester avec Plusieurs Joueurs

1. Ouvrir le jeu dans plusieurs navigateurs/onglets
2. Créer des comptes différents
3. Rejoindre la même partie
4. Tester la synchronisation temps réel

---

## 🐛 Problèmes Courants

### Backend ne démarre pas

1. Vérifier les logs dans Render Dashboard
2. Vérifier que toutes les variables d'environnement sont définies
3. Vérifier que `SECRET_KEY` est bien défini

### Frontend ne se connecte pas

1. Vérifier `VITE_API_URL` dans Vercel
2. Vérifier les CORS dans Render
3. Ouvrir la console du navigateur (F12) pour voir les erreurs

### WebSocket ne fonctionne pas

1. Vérifier que vous utilisez `wss://` (pas `ws://`) pour HTTPS
2. Vérifier les logs du backend
3. Le WebSocket devrait fonctionner automatiquement avec la configuration actuelle

---

## 📝 Checklist de Déploiement

- [ ] Code poussé sur GitHub
- [ ] Backend déployé sur Render
- [ ] Variables d'environnement backend configurées
- [ ] URL backend notée
- [ ] Frontend déployé sur Vercel
- [ ] Variable `VITE_API_URL` configurée dans Vercel
- [ ] URL frontend notée
- [ ] CORS mis à jour avec l'URL frontend
- [ ] Backend redéployé
- [ ] Test du backend (health check)
- [ ] Test du frontend (connexion)
- [ ] Test avec plusieurs joueurs

---

## 🎮 URLs Finales

Après déploiement :

- **Backend** : `https://votre-backend.onrender.com`
- **Backend Docs** : `https://votre-backend.onrender.com/docs`
- **Frontend** : `https://votre-frontend.vercel.app`
- **WebSocket** : `wss://votre-backend.onrender.com/ws/games/{id}`

---

## 💡 Astuces

1. **Render Free Tier** : Se met en veille après 15 min d'inactivité. Le premier appel après veille prend 30-60 secondes.

2. **Vercel** : Déploiement automatique à chaque push sur GitHub (optionnel).

3. **Supabase** : Déjà configuré, pas besoin de changer quoi que ce soit.

4. **HTTPS** : Automatique sur Render et Vercel, pas besoin de certificat SSL.

---

## 🔄 Mises à Jour

Pour mettre à jour le code :

1. Faire les modifications localement
2. Pousser sur GitHub : `git push`
3. Render et Vercel redéploient automatiquement (si configuré)

---

*Guide créé le : 2025-01-XX*
*Déploiement rapide sur internet*


# Checklist de Déploiement sur Internet

Checklist étape par étape pour déployer Timeline Ranger sur internet.

## ✅ Préparation

- [ ] Code poussé sur GitHub
- [ ] Repository GitHub créé et accessible
- [ ] Compte Render créé
- [ ] Compte Vercel créé
- [ ] Compte Supabase configuré (déjà fait)

---

## 🌐 Backend (Render)

### Configuration
- [ ] Service Web créé sur Render
- [ ] Repository GitHub connecté
- [ ] Build Command : `cd backend && pip install -r requirements.txt`
- [ ] Start Command : `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Variables d'Environnement
- [ ] `SUPABASE_HOST` défini
- [ ] `SUPABASE_DB` défini (postgres)
- [ ] `SUPABASE_USER` défini (postgres)
- [ ] `SUPABASE_PASSWORD` défini
- [ ] `SUPABASE_PORT` défini (5432)
- [ ] `SECRET_KEY` généré et défini
- [ ] `ALGORITHM` défini (HS256)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` défini (1440)
- [ ] `CORS_ORIGINS` défini (avec localhost + URL frontend)
- [ ] `APP_NAME` défini
- [ ] `APP_VERSION` défini
- [ ] `DEBUG` défini (False)

### Déploiement
- [ ] Service déployé
- [ ] URL backend notée : `https://________________.onrender.com`
- [ ] Health check fonctionne : `/health`
- [ ] Documentation accessible : `/docs`

---

## 🎨 Frontend (Vercel)

### Configuration
- [ ] Projet créé sur Vercel
- [ ] Repository GitHub connecté
- [ ] Root Directory : `frontend`
- [ ] Framework Preset : Vite
- [ ] Build Command : `npm run build` (automatique)
- [ ] Output Directory : `dist` (automatique)

### Variables d'Environnement
- [ ] `VITE_API_URL` défini avec l'URL backend Render

### Déploiement
- [ ] Frontend déployé
- [ ] URL frontend notée : `https://________________.vercel.app`
- [ ] Page d'accueil accessible

---

## 🔧 Configuration Finale

### CORS
- [ ] Retour sur Render
- [ ] Variable `CORS_ORIGINS` mise à jour avec l'URL Vercel
- [ ] Backend redéployé

### WebSocket
- [ ] Vérifier que le WebSocket utilise `wss://` (automatique)
- [ ] Tester la connexion WebSocket dans une partie

---

## 🧪 Tests

### Backend
- [ ] Health check : `/health` → `{"status": "healthy"}`
- [ ] Documentation : `/docs` accessible
- [ ] Endpoint auth : `/api/v1/auth/register` fonctionne

### Frontend
- [ ] Page d'accueil charge
- [ ] Connexion fonctionne
- [ ] Inscription fonctionne
- [ ] Création de partie fonctionne
- [ ] Rejoindre une partie fonctionne

### Intégration
- [ ] Frontend se connecte au backend
- [ ] WebSocket se connecte
- [ ] Actions de jeu fonctionnent
- [ ] Synchronisation temps réel fonctionne

### Multi-Joueurs
- [ ] 2 joueurs peuvent se connecter
- [ ] Les actions sont synchronisées
- [ ] Les tours alternent correctement

---

## 📝 URLs Finales

- **Backend** : `https://________________.onrender.com`
- **Backend Docs** : `https://________________.onrender.com/docs`
- **Frontend** : `https://________________.vercel.app`
- **WebSocket** : `wss://________________.onrender.com/ws/games/{id}`

---

## 🎉 C'est Prêt !

Une fois toutes les cases cochées, le jeu est accessible sur internet !

---

*Checklist créée le : 2025-01-XX*


# Variables d'Environnement pour la Production

## 🌐 Backend (Render)

Copier-coller ces variables dans Render → Environment Variables :

```
SUPABASE_HOST=votre-host.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=votre-mot-de-passe-supabase
SUPABASE_PORT=5432
SECRET_KEY=<générer-une-clé-sécurisée>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://votre-frontend.vercel.app
APP_NAME=Timeline Ranger API
APP_VERSION=0.1.0
DEBUG=False
```

### Générer SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Mettre à jour CORS_ORIGINS

Après avoir déployé le frontend, mettre à jour `CORS_ORIGINS` avec l'URL Vercel réelle :

```
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://timeline-ranger.vercel.app
```

---

## 🎨 Frontend (Vercel)

Copier-coller cette variable dans Vercel → Environment Variables :

```
VITE_API_URL=https://votre-backend.onrender.com/api/v1
```

**⚠️ Important** : Remplacer `votre-backend.onrender.com` par l'URL réelle de votre backend Render !

---

## 📝 Notes

- Les variables sont sensibles, ne jamais les commiter dans Git
- Utiliser les variables d'environnement des plateformes (Render/Vercel)
- Le `SECRET_KEY` doit être unique et sécurisé

---

*Document créé le : 2025-01-XX*


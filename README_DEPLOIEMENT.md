# 🚀 Déploiement sur Internet - Timeline Ranger

Guide complet pour déployer Timeline Ranger sur internet et le tester en ligne.

## 📚 Documentation

- **Guide Rapide** : `DEPLOIEMENT_RAPIDE.md` - Déploiement en 30 minutes
- **Guide Complet** : `GUIDE_DEPLOIEMENT_INTERNET.md` - Guide détaillé
- **Checklist** : `CHECKLIST_DEPLOIEMENT.md` - Checklist étape par étape
- **Variables** : `VARIABLES_ENVIRONNEMENT_PRODUCTION.md` - Variables d'environnement

## 🎯 Architecture

```
Frontend (Vercel) → Backend (Render) → Supabase (PostgreSQL)
```

**Tout gratuit** pour un prototype !

## ⚡ Démarrage Rapide

1. **Backend sur Render** (10 min)
   - Créer un Web Service
   - Configurer les variables d'environnement
   - Déployer

2. **Frontend sur Vercel** (10 min)
   - Importer le repository
   - Configurer `VITE_API_URL`
   - Déployer

3. **Mettre à jour CORS** (5 min)
   - Ajouter l'URL Vercel dans `CORS_ORIGINS` sur Render
   - Redéployer

4. **Tester** (5 min)
   - Ouvrir le frontend
   - Créer un compte
   - Tester avec plusieurs joueurs

**Total : ~30 minutes**

## 🔗 URLs

Après déploiement :
- **Backend** : `https://votre-backend.onrender.com`
- **Frontend** : `https://votre-frontend.vercel.app`

## 📖 Pour Plus de Détails

Voir `DEPLOIEMENT_RAPIDE.md` pour les instructions complètes.

---

*Document créé le : 2025-01-XX*


# Note sur les Conflits de Dépendances

## ⚠️ Conflits Potentiels

Si vous avez d'autres packages installés globalement (comme `selenium`, `streamlit`, `torch`, etc.), vous pourriez voir des avertissements de conflits de dépendances.

## ✅ Solution Recommandée : Environnement Virtuel

Pour éviter ces conflits, il est **fortement recommandé** d'utiliser un environnement virtuel dédié au backend :

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate

# Sur Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 📦 Dépendances du Backend

Les dépendances principales du backend sont :
- `fastapi>=0.115.0` - Framework web
- `uvicorn[standard]>=0.32.0` - Serveur ASGI
- `psycopg2-binary` - Driver PostgreSQL
- `pydantic>=2.7.0` - Validation de données
- `python-jose` - JWT
- `passlib[bcrypt]` - Hashage de mots de passe
- `anyio>=4.8.0,<5.0.0` - Compatibilité async

Ces versions sont compatibles entre elles et ne devraient pas causer de conflits dans un environnement virtuel propre.

## 🔍 Vérification

Pour vérifier que tout fonctionne :

```bash
cd backend
python -c "import fastapi; import uvicorn; print('OK')"
```

Si aucune erreur n'apparaît, vous pouvez lancer l'API :

```bash
uvicorn app.main:app --reload --port 8000
```


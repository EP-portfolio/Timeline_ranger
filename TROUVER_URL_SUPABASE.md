# Comment Trouver l'URL de la Base de Données Supabase

## 🔍 Où Trouver l'URL de la Base de Données

Dans Supabase, il y a **deux types d'URLs** :

1. **URL API** : `https://xxxxx.supabase.co` (pour l'API REST)
2. **URL Database** : `db.xxxxx.supabase.co` (pour PostgreSQL)

## 📋 Méthode 1 : Via Settings → Database

1. Dans votre projet Supabase, allez dans **Settings** (icône ⚙️ en bas à gauche)
2. Cliquez sur **Database** dans le menu de gauche
3. Cherchez la section **Connection string** ou **Connection pooling**

Vous verrez quelque chose comme :

### Connection String (URI)
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

### Connection String (Session mode)
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres?sslmode=require
```

### Connection Info
- **Host** : `db.xxxxx.supabase.co`
- **Database name** : `postgres`
- **Port** : `5432`
- **User** : `postgres`
- **Password** : (celui que vous avez créé)

## 📋 Méthode 2 : Via Connection Pooling

1. Dans **Settings** → **Database**
2. Allez dans l'onglet **Connection pooling**
3. Vous verrez l'URL de connexion avec le format :
   ```
   db.xxxxx.supabase.co
   ```

## 📋 Méthode 3 : Extraire depuis l'URL API

Si vous avez l'URL API : `https://abcdefghijklmnop.supabase.co`

L'URL de la base de données sera : `db.abcdefghijklmnop.supabase.co`

**Exemple** :
- URL API : `https://xyzabc123.supabase.co`
- URL Database : `db.xyzabc123.supabase.co`

## 🔧 Configuration du Fichier .env

Une fois que vous avez trouvé l'URL, configurez votre `.env` :

```env
# Si vous avez l'URL complète de connexion
# Exemple : postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
# Extrayez les parties :

SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=votre_mot_de_passe
SUPABASE_PORT=5432
```

## 🎯 Exemple Complet

Si votre URL API est : `https://abcdefghijklmnopqrst.supabase.co`

Votre `.env` devrait être :

```env
SUPABASE_HOST=db.abcdefghijklmnopqrst.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=le_mot_de_passe_que_vous_avez_cree
SUPABASE_PORT=5432
```

## ⚠️ Important

- **Ne pas utiliser** l'URL API (`https://...`) pour PostgreSQL
- **Utiliser** l'URL Database (`db....supabase.co`)
- Le **mot de passe** est celui que vous avez créé lors de la création du projet
- Le **nom de la base** est toujours `postgres` (ne pas créer une nouvelle base)

## 🧪 Test de Connexion

Pour tester si l'URL est correcte, vous pouvez utiliser le script :

```bash
python setup_supabase.py
```

Ou tester directement dans Python :

```python
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv('SUPABASE_HOST'),
        database=os.getenv('SUPABASE_DB'),
        user=os.getenv('SUPABASE_USER'),
        password=os.getenv('SUPABASE_PASSWORD'),
        port=os.getenv('SUPABASE_PORT'),
        sslmode='require'
    )
    print("✅ Connexion réussie !")
    conn.close()
except Exception as e:
    print(f"❌ Erreur : {e}")
```

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*



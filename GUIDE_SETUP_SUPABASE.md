# Guide de Configuration Supabase - Timeline Ranger

Guide complet pour configurer Supabase et importer les données Timeline Ranger.

## 🎯 Pourquoi Supabase ?

- ✅ **100% Gratuit** pour commencer (500MB base, 2GB/mois bande passante)
- ✅ **PostgreSQL** complet (pas de limitations majeures)
- ✅ **Realtime** gratuit (WebSocket pour synchronisation)
- ✅ **Auth** intégré (optionnel, peut utiliser JWT custom)
- ✅ **Interface web** pour gérer la base
- ✅ **Parfait pour prototype** (4-20 joueurs)

## 📋 Étapes de Configuration

### Étape 1 : Créer un Compte Supabase

1. Aller sur https://supabase.com
2. Cliquer sur "Start your project"
3. S'inscrire avec GitHub, Google, ou email
4. Confirmer l'email si nécessaire

### Étape 2 : Créer un Nouveau Projet

1. Cliquer sur "New Project"
2. Remplir les informations :
   - **Organization** : Créer une nouvelle ou utiliser existante
   - **Name** : `timeline-ranger` (ou autre nom)
   - **Database Password** : Choisir un mot de passe fort (⚠️ **À NOTER**)
   - **Region** : Choisir la région la plus proche (ex: Europe West)
   - **Pricing Plan** : Free (gratuit)

3. Cliquer sur "Create new project"
4. ⏳ Attendre 2-3 minutes que le projet soit créé

### Étape 3 : Récupérer les Informations de Connexion

1. Dans le projet Supabase, aller dans **Settings** → **Database**
2. Noter les informations suivantes :
   - **Host** : `db.xxxxx.supabase.co`
   - **Database name** : `postgres`
   - **Port** : `5432`
   - **User** : `postgres`
   - **Password** : Le mot de passe que vous avez créé

3. **Connection string** (pour référence) :
   ```
   postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

### Étape 4 : Exécuter le Schéma SQL

1. Dans Supabase, aller dans **SQL Editor** (icône SQL dans la barre latérale)
2. Cliquer sur "New query"
3. Ouvrir le fichier `SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql`
4. **Copier TOUT le contenu** du fichier
5. **Coller** dans l'éditeur SQL de Supabase
6. Cliquer sur "Run" (ou Ctrl+Enter)
7. ✅ Vérifier qu'il n'y a pas d'erreurs

**Note** : Si vous avez des erreurs, vérifier :
- Que toutes les tables sont créées
- Que les index sont créés
- Que les vues sont créées

### Étape 5 : Vérifier les Tables

Dans le **SQL Editor**, exécuter :

```sql
-- Vérifier les Rangers
SELECT * FROM rangers;

-- Vérifier les Types d'Armes
SELECT * FROM weapon_types;

-- Vérifier les Matières Premières
SELECT * FROM raw_materials;

-- Vérifier que les tables existent
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

Vous devriez voir :
- ✅ 5 Rangers
- ✅ 8 Types d'armes
- ✅ 5 Matières premières
- ✅ Toutes les autres tables

### Étape 6 : Configurer le Script d'Import

1. Créer un fichier `.env` à la racine du projet :
   ```env
   # Supabase Configuration
   SUPABASE_HOST=db.xxxxx.supabase.co
   SUPABASE_DB=postgres
   SUPABASE_USER=postgres
   SUPABASE_PASSWORD=votre_mot_de_passe
   SUPABASE_PORT=5432
   ```

2. ⚠️ **Important** : Ajouter `.env` au `.gitignore` pour ne pas commiter le mot de passe

### Étape 7 : Adapter le Script d'Import

Le script `SCRIPT_IMPORT_MAPPED_DATA.py` doit être adapté pour Supabase.

**Modifications nécessaires** :
- Utiliser les credentials Supabase
- Utiliser SSL pour la connexion (Supabase le requiert)

### Étape 8 : Exécuter l'Import

```bash
# Installer les dépendances si nécessaire
pip install psycopg2-binary pandas odfpy python-dotenv

# Exécuter l'import
python SCRIPT_IMPORT_MAPPED_DATA.py
```

### Étape 9 : Vérifier les Données Importées

Dans le **SQL Editor** de Supabase :

```sql
-- Compter les troupes
SELECT COUNT(*) as total_troupes FROM troupes;

-- Compter les technologies
SELECT COUNT(*) as total_technologies FROM technologies;

-- Compter les quêtes
SELECT COUNT(*) as total_quetes FROM quetes;

-- Voir quelques exemples
SELECT card_number, original_name, mapped_name, weapon_type_id 
FROM troupes 
LIMIT 10;

SELECT card_number, original_name, mapped_name 
FROM technologies 
LIMIT 10;
```

## 🔐 Sécurité Supabase

### API Keys

Supabase génère automatiquement :
- **anon key** : Pour les requêtes publiques (frontend)
- **service_role key** : Pour les requêtes admin (backend uniquement)

**Où les trouver** :
- Settings → API → Project API keys

**⚠️ Important** :
- Ne jamais exposer la `service_role key` dans le frontend
- Utiliser `anon key` pour le frontend
- Utiliser `service_role key` uniquement dans le backend

### Row Level Security (RLS)

Par défaut, Supabase active RLS. Pour un prototype, vous pouvez :
- Désactiver RLS temporairement (Settings → Database)
- Ou configurer des politiques selon vos besoins

## 📊 Utilisation dans le Backend

### Connexion avec psycopg2

```python
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

# Pool de connexions
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    host=os.getenv('SUPABASE_HOST'),
    database=os.getenv('SUPABASE_DB'),
    user=os.getenv('SUPABASE_USER'),
    password=os.getenv('SUPABASE_PASSWORD'),
    port=os.getenv('SUPABASE_PORT'),
    sslmode='require'  # Supabase requiert SSL
)
```

### Connexion avec SQLAlchemy

```python
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('SUPABASE_USER')}:{os.getenv('SUPABASE_PASSWORD')}@{os.getenv('SUPABASE_HOST')}:{os.getenv('SUPABASE_PORT')}/{os.getenv('SUPABASE_DB')}?sslmode=require"

engine = create_engine(DATABASE_URL)
```

## 🚀 Fonctionnalités Supabase Utiles

### 1. Realtime (WebSocket)

Supabase offre Realtime gratuit pour :
- Synchronisation des parties en temps réel
- Notifications de changements
- Pas besoin de WebSocket custom au début

### 2. Auth (Optionnel)

Si vous voulez utiliser l'auth Supabase :
- Email/password
- OAuth (Google, GitHub, etc.)
- Magic links

Sinon, vous pouvez utiliser JWT custom avec FastAPI.

### 3. Storage (Optionnel)

Pour stocker :
- Images des cartes
- Avatars utilisateurs
- Configurations

## 📝 Checklist de Configuration

- [ ] Compte Supabase créé
- [ ] Projet créé
- [ ] Mot de passe noté
- [ ] Schéma SQL exécuté
- [ ] Tables vérifiées
- [ ] Fichier `.env` créé
- [ ] Script d'import adapté
- [ ] Données importées
- [ ] Données vérifiées
- [ ] API keys notées

## 🐛 Dépannage

### Erreur de connexion SSL

Si vous avez une erreur SSL :
```python
# Ajouter sslmode='require' dans la connexion
conn = psycopg2.connect(
    ...,
    sslmode='require'
)
```

### Erreur "password authentication failed"

- Vérifier le mot de passe dans `.env`
- Vérifier que vous utilisez le bon utilisateur (`postgres`)

### Erreur "database does not exist"

- Supabase utilise toujours `postgres` comme nom de base
- Ne pas créer une nouvelle base, utiliser `postgres`

### Erreur lors de l'import

- Vérifier que le fichier ODS est accessible
- Vérifier les noms de feuilles dans l'ODS
- Vérifier les colonnes dans l'ODS

## 🎯 Prochaines Étapes

Une fois Supabase configuré :

1. ✅ Base de données prête
2. ⏳ Créer le backend FastAPI
3. ⏳ Configurer la connexion Supabase dans le backend
4. ⏳ Créer les routes API
5. ⏳ Tester avec les données réelles

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


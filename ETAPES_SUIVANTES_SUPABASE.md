# Étapes Suivantes - Après le Schéma SQL

## ✅ Étape Complétée

Vous avez exécuté le schéma SQL avec succès ! "No rows returned" est normal pour les commandes CREATE TABLE.

## 🔍 Vérification du Schéma

### 1. Vérifier que les Tables Existent

Dans Supabase SQL Editor, exécutez :

```sql
-- Voir toutes les tables créées
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

Vous devriez voir environ **18 tables** :
- `rangers`
- `weapon_types`
- `raw_materials`
- `armures_meca`
- `troupes`
- `technologies`
- `quetes`
- `color_actions`
- `users`
- `games`
- `game_players`
- `game_states`
- `user_stats`
- `garnisons`
- `weapon_slots`
- `armor_pieces`
- `lasers`
- `game_actions`

### 2. Vérifier les Données Initiales

```sql
-- Vérifier les Rangers (5 rangers)
SELECT * FROM rangers;

-- Vérifier les Types d'Armes (8 types)
SELECT * FROM weapon_types;

-- Vérifier les Matières Premières (5 matières)
SELECT * FROM raw_materials;
```

Si ces requêtes retournent des données, le schéma est correctement créé ! ✅

## 📋 Prochaine Étape : Importer les Données

### Étape 1 : Configurer le Fichier .env

1. Créer un fichier `.env` à la racine du projet :
   ```bash
   # Copier le template
   cp .env.example .env
   ```

2. Modifier `.env` avec vos informations Supabase :
   ```env
   SUPABASE_HOST=db.xxxxx.supabase.co
   SUPABASE_DB=postgres
   SUPABASE_USER=postgres
   SUPABASE_PASSWORD=votre_mot_de_passe
   SUPABASE_PORT=5432
   ```

   **Où trouver ces infos** :
   - Supabase → Settings → Database
   - Connection string ou Connection pooling

### Étape 2 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

### Étape 3 : Vérifier la Configuration

```bash
python setup_supabase.py
```

Ce script vérifie :
- ✅ Fichier .env existe
- ✅ Variables d'environnement configurées
- ✅ Connexion à Supabase fonctionne
- ✅ Schéma créé

### Étape 4 : Importer les Données

```bash
python SCRIPT_IMPORT_MAPPED_DATA.py
```

Le script va :
1. Se connecter à Supabase
2. Lire le fichier ODS `Ark_Nova_Mondes_marins_cartes_stats_FR.ods`
3. Appliquer tous les mappings Timeline Ranger
4. Importer dans les tables :
   - `troupes` (ex-Animaux)
   - `technologies` (ex-Mécènes)
   - `quetes` (ex-Projets de Conservation)
   - `color_actions` (actions de couleur)

### Étape 5 : Vérifier les Données Importées

Dans Supabase SQL Editor :

```sql
-- Compter les troupes importées
SELECT COUNT(*) as total_troupes FROM troupes;

-- Compter les technologies importées
SELECT COUNT(*) as total_technologies FROM technologies;

-- Compter les quêtes importées
SELECT COUNT(*) as total_quetes FROM quetes;

-- Voir quelques exemples de troupes
SELECT 
    card_number,
    original_name,
    mapped_name,
    points_degats,
    nombre_lasers
FROM troupes
LIMIT 10;

-- Voir quelques exemples de technologies
SELECT 
    card_number,
    original_name,
    mapped_name,
    is_armor_piece
FROM technologies
LIMIT 10;

-- Vérifier les actions de couleur créées
SELECT 
    ca.id,
    r.name as ranger_name,
    ca.action_type,
    ca.name as action_name
FROM color_actions ca
JOIN rangers r ON ca.ranger_id = r.id
LIMIT 20;
```

## 🎯 Résultats Attendus

Après l'import, vous devriez avoir :
- ✅ ~200-300 troupes (selon le nombre de cartes Animal)
- ✅ ~80-90 technologies (selon le nombre de cartes Mécène)
- ✅ ~40-50 quêtes (selon le nombre de Projets de Conservation)
- ✅ Actions de couleur créées automatiquement

## 🐛 Dépannage

### Erreur : "Fichier ODS non trouvé"
- Vérifier que `Ark_Nova_Mondes_marins_cartes_stats_FR.ods` est dans le même dossier
- Vérifier le nom exact du fichier

### Erreur : "Connection refused" ou "SSL required"
- Vérifier que `sslmode='require'` est dans la connexion
- Vérifier vos credentials Supabase

### Erreur : "Table does not exist"
- Vérifier que le schéma SQL a bien été exécuté
- Vérifier que vous êtes connecté à la bonne base de données

### Erreur : "Column does not exist"
- Vérifier que le schéma SQL est à jour
- Vérifier les noms de colonnes dans l'ODS

## 🚀 Après l'Import

Une fois les données importées :

1. ✅ Base de données complète avec données mappées
2. ⏳ Créer le backend FastAPI
3. ⏳ Connecter le backend à Supabase
4. ⏳ Créer les routes API
5. ⏳ Tester avec les données réelles

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*



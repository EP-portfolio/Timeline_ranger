# Schéma PostgreSQL Timeline Ranger - Explication Complète

Ce document explique comment le schéma PostgreSQL reflète TOUS les mappings Timeline Ranger.

## 🎯 Principe Fondamental

Le schéma PostgreSQL ne stocke **PAS** les données brutes d'Ark Nova, mais **directement les données mappées** de Timeline Ranger. Tous les concepts transformés sont intégrés dans la structure de la base de données.

## 📊 Structure Complète

### 1. Rangers de Couleurs

**Table** : `rangers`

Stocke les 5 Rangers avec leurs mappings :
- `Ranger Bleu` (ex-ACTION MECENE)
- `Ranger Noir` (ex-ACTION ANIMAUX)
- `Ranger Orange` (ex-ACTION CONSTRUCTION)
- `Ranger Vert` (ex-ACTION ASSOCIATION)
- `Ranger Jaune` (ex-ACTION CARTES)

**Champs clés** :
- `color` : Code couleur ('blue', 'black', etc.)
- `original_action` : Action originale d'Ark Nova
- `role` : Rôle du Ranger dans Timeline Ranger

### 2. Types d'Armes/Munitions

**Table** : `weapon_types`

Mapping des catégories d'animaux → Types d'armes :
- `Prédateur` → `Explosifs`
- `Animal domestique` → `Munitions Standard`
- `Animal marin` → `Torpilles`
- `Herbivore` → `Munitions Nucléaires`
- `Oiseau` → `Missiles Aériens`
- `Ours` → `Armes Lourdes`
- `Primate` → `Armes Intelligentes`
- `Reptile` → `Armes Toxiques`

### 3. Matières Premières

**Table** : `raw_materials`

Mapping des continents → Matières premières :
- `Afrique` → `Titanium`
- `Amériques` → `Platine`
- `Asie` → `Vibranium`
- `Australie` → `Carbone`
- `Europe` → `Kevlar`

### 4. Troupes (ex-Animaux)

**Table** : `troupes`

Les animaux deviennent des **Troupes** (armes) avec :

**Mappings appliqués** :
- `original_name` : Nom original (ex: "Lion")
- `mapped_name` : Nom mappé (ex: "Explosif - Lion")
- `weapon_type_id` : Type d'arme (Explosifs, etc.)
- `points_degats` : Points Attrait → Points de Dégâts
- `nombre_lasers` : Points Conservation → Nombre de Lasers
- `points_developpement_technique` : Points Réputation → Points de Développement Technique
- `paires_ailes` : Points Science → Nombre de Paires d'Ailes
- `raw_materials_required` : Continents → Matières Premières (JSONB)
- `cost` : Crédits → Or
- `bonus` : Capacité → Bonus
- `effet_invocation` : Effet unique immédiat → Effet d'invocation
- `effet_quotidien` : Effet permanent → Effet quotidien
- `dernier_souffle` : Effet fin de partie → Dernier souffle

### 5. Technologies (ex-Mécènes)

**Table** : `technologies`

Les Mécènes deviennent des **Technologies** (Actions Bleues) avec :

**Mappings appliqués** :
- `original_name` : Nom original
- `mapped_name` : Nom mappé (ex: "Système Fondation Wildlife")
- `is_armor_piece` : True si c'est une pièce d'armure
- `armor_piece_type` : Type de pièce ('Renfort', 'Blindage', etc.)
- `points_degats`, `nombre_lasers`, etc. : Points mappés
- `cost` : Crédits → Or
- `or_par_jour` : Revenus → Or par jour

### 6. Quêtes (ex-Projets de Conservation)

**Table** : `quetes`

Les Projets de Conservation deviennent des **Quêtes** avec :
- `mapped_name` : "Quête : [Nom]"
- `quest_type` : Type de quête (maîtrise, forteresse, etc.)

### 7. Armures Méca

**Table** : `armures_meca`

Mapping des plateaux de jeu → Armures méca :
- `original_plateau` : Plateau original (ex: "Plateau A")
- `name` : Nom mappé (ex: "Armure Méca Débutante")
- `configuration` : Configuration de la grille (JSONB)
- `special_ability` : Capacité spéciale (JSONB)

### 8. Actions de Couleur

**Table** : `color_actions`

Lien entre Rangers et leurs actions disponibles :
- `ranger_id` : Ranger qui peut faire cette action
- `action_type` : Type d'action ('blue', 'black', etc.)
- `source_type` : Source ('troupe', 'technology', etc.)
- `source_id` : ID de la carte source

### 9. Tables de Jeu

**Tables** : `games`, `game_players`, `game_states`, etc.

Gestion des parties multijoueurs avec :
- Utilisateurs authentifiés
- Parties en cours
- État de chaque partie
- Actions effectuées
- Scores avec points mappés

## 🔄 Flux de Données

### Import depuis l'ODS

```
ODS (Ark Nova)
    ↓
Script d'import (SCRIPT_IMPORT_MAPPED_DATA.py)
    ↓
Application des mappings
    ↓
PostgreSQL (Timeline Ranger)
```

### Exemple : Import d'un Animal

1. **Lecture depuis l'ODS** :
   - Nom : "Lion"
   - Catégorie : "Prédateur"
   - Points Attrait : 5
   - Points Conservation : 2
   - Continent : "Afrique"

2. **Application des mappings** :
   - Nom → "Explosif - Lion"
   - Catégorie → Type d'arme : "Explosifs"
   - Points Attrait → Points de Dégâts : 5
   - Points Conservation → Nombre de Lasers : 2
   - Continent → Matière première : "Titanium"

3. **Insertion dans PostgreSQL** :
   ```sql
   INSERT INTO troupes (
       card_number, original_name, mapped_name,
       weapon_type_id, points_degats, nombre_lasers,
       raw_materials_required
   ) VALUES (
       1, 'Lion', 'Explosif - Lion',
       (SELECT id FROM weapon_types WHERE code = 'explosifs'),
       5, 2,
       '[{"material_id": 1, "quantity": 1}]'::jsonb
   );
   ```

## 📋 Requêtes Utiles

### Obtenir toutes les troupes avec leurs types d'armes

```sql
SELECT 
    t.mapped_name,
    wt.name as weapon_type,
    t.points_degats,
    t.nombre_lasers
FROM troupes t
JOIN weapon_types wt ON t.weapon_type_id = wt.id;
```

### Obtenir les actions disponibles pour un Ranger

```sql
SELECT 
    ca.name,
    ca.action_type,
    r.name as ranger_name
FROM color_actions ca
JOIN rangers r ON ca.ranger_id = r.id
WHERE r.color = 'black';
```

### Obtenir les troupes nécessitant une matière première

```sql
SELECT 
    t.mapped_name,
    rm.name as material_name
FROM troupes t,
     jsonb_array_elements(t.raw_materials_required) as material,
     raw_materials rm
WHERE rm.id = (material->>'material_id')::int;
```

## 🎮 Utilisation dans le Jeu

### Lorsqu'un joueur utilise le Ranger Noir

1. **Requête** : Obtenir les actions noires disponibles
   ```sql
   SELECT * FROM color_actions 
   WHERE action_type = 'black' 
   AND ranger_id = (SELECT id FROM rangers WHERE color = 'black');
   ```

2. **Affichage** : Afficher les troupes (armes) disponibles
   ```sql
   SELECT * FROM troupes 
   WHERE weapon_type_id IN (...);
   ```

3. **Installation** : Créer un slot et installer l'arme
   ```sql
   INSERT INTO weapon_slots (game_id, player_id, size, troupe_id)
   VALUES (...);
   ```

### Calcul des scores

Les scores utilisent directement les points mappés :
- `total_points_degats` : Somme des points de dégâts
- `total_lasers` : Nombre de lasers installés
- `total_points_developpement_technique` : Points de développement
- `total_paires_ailes` : Nombre de paires d'ailes

## ✅ Avantages de cette Approche

1. **Données directement utilisables** : Pas besoin de mapper à chaque requête
2. **Performance** : Index sur les champs mappés
3. **Cohérence** : Tous les mappings appliqués une seule fois
4. **Simplicité** : Requêtes SQL directes avec les concepts Timeline Ranger
5. **Évolutivité** : Facile d'ajouter de nouveaux mappings

## 🚀 Prochaines Étapes

1. ✅ Créer le schéma PostgreSQL
2. ✅ Créer le script d'import avec mappings
3. ⏳ Exécuter le script d'import
4. ⏳ Vérifier les données importées
5. ⏳ Créer les vues et fonctions utiles
6. ⏳ Intégrer dans l'API backend

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


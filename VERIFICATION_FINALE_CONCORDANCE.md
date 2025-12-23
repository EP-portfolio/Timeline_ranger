# Vérification Finale de Concordance - Timeline Ranger

## ✅ Statut Global : 100% Cohérent et Clair

Tous les mappings sont maintenant cohérents, détaillés et prêts pour l'implémentation.

---

## 📋 Mappings Confirmés et Cohérents

### 1. Cartes Action → Rangers ✅

| Ark Nova | Timeline Ranger | Détails | Statut |
|----------|----------------|---------|--------|
| ACTION MECENE | RANGER BLEU | Pièces d'armure, crédits | ✅ Complet |
| ACTION ANIMAUX | RANGER NOIR | 0-1-1-1-2 / 1-1-2-2-2 animaux | ✅ Complet |
| ACTION CONSTRUCTION | RANGER ORANGE | Taille 1-5, 2 crédits/case | ✅ Complet |
| ACTION ASSOCIATION | RANGER VERT | Quêtes, émissaires, mines, reliques | ✅ Complet |
| ACTION CARTES | RANGER JAUNE | Pioche 1-5, accès rivière (4-5) | ✅ Complet |

### 2. Types de Cartes ✅

| Ark Nova | Timeline Ranger | Table SQL | Statut |
|----------|----------------|-----------|--------|
| Animal | Troupe | `troupes` | ✅ Cohérent |
| Mécène | Technologie | `technologies` | ✅ Cohérent (corrigé) |
| Projet_de_conservation | Quête | `quetes` | ✅ Cohérent |
| Décompte_final | Dernier Souffle | À créer | ⚠️ À ajouter |

### 3. Points et Scores ✅

| Ark Nova | Timeline Ranger | Calcul | Statut |
|----------|----------------|--------|--------|
| Points Attrait | Points de Dégâts | Troupes + Lasers (variable) + Technologies | ✅ Complet |
| Points Conservation | Nombre de Lasers | 0-6 : 2 pd/laser, 7+ : 3 pd/laser | ✅ Complet |
| Points Réputation | Points de Développement Technique | Cumul | ✅ Complet |
| Points Science | Paires d'Ailes | Cumul | ✅ Complet |

### 4. Système de Lasers ✅

**Valeur en Points de Dégâts** :
- 0-6 lasers : 2 points de dégâts par laser
- 7+ lasers : 3 points de dégâts par laser

**Bonus aux Seuils** :
- 2 lasers : Choisir entre améliorer une carte Action OU obtenir un nouvel émissaire
- 5 lasers : Bonus (à définir)
- 8 lasers : Bonus (à définir)
- 10 lasers : **Le premier joueur à 10 lasers** oblige **TOUS les joueurs** à défausser une carte Dernier Souffle

**Cartes Dernier Souffle** :
- Début : 2 cartes aléatoires par joueur
- À 10 lasers (premier joueur) : **TOUS les joueurs** défaussent 1, conservent 1

### 5. Actions Détaillées ✅

**Action Animaux** :
- Non améliorée : 0-1-1-1-2 animaux
- Améliorée : 1-1-2-2-2 animaux
- Puissance 5 : +1 réputation

**Action Mécène** :
- Non améliorée : 1 carte niveau max OU 1-5 crédits
- Améliorée : Plusieurs cartes (total ≤ puissance+1) OU 2×puissance crédits

**Action Association** :
- Système d'émissaires : 1 au début, max 4
- Quêtes, réputation, mines, reliques, lasers

**Action Construction** :
- Taille 1-5 selon puissance
- Coût : 2 crédits/case

**Action Cartes** :
- Puissance 1-3 : Pioche uniquement
- Puissance 4-5 : Accès rivière
- Améliorée : Selon réputation

---

## 🔧 Schéma SQL - État Actuel

### Tables Existantes ✅
- `rangers` : 5 Rangers de couleurs
- `weapon_types` : 8 types d'armes
- `raw_materials` : 5 matières premières
- `armures_meca` : Configurations des armures
- `troupes` : Cartes troupes (ex-Animaux)
- `technologies` : Cartes technologies (ex-Mécènes)
- `quetes` : Cartes quêtes (ex-Projets)
- `games` : Parties
- `game_players` : Joueurs dans les parties
- `game_states` : États des parties
- `garnisons` : Garnisons construites
- `weapon_slots` : Slots pour armes
- `armor_pieces` : Pièces d'armure posées
- `lasers` : Lasers installés
- `game_actions` : Actions effectuées

### Tables à Ajouter ⚠️

#### 1. Cartes Dernier Souffle
```sql
CREATE TABLE dernier_souffle_cards (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    condition_type VARCHAR(50),  -- Type de condition
    condition_value INTEGER,  -- Valeur de la condition
    reward_points INTEGER,  -- Points de récompense
    description TEXT,
    original_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE game_last_breath_cards (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    card_id INTEGER REFERENCES dernier_souffle_cards(id),
    received_at TIMESTAMP DEFAULT NOW(),
    kept BOOLEAN DEFAULT TRUE,  -- True si conservée, False si défaussée
    discarded_at TIMESTAMP,  -- Quand défaussée (à 10 lasers)
    UNIQUE(game_id, player_id, card_id)
);
```

#### 2. Émissaires
```sql
ALTER TABLE game_players ADD COLUMN emissaires_count INTEGER DEFAULT 1;
-- 1 au début, peut débloquer jusqu'à 3 supplémentaires (max 4)
```

#### 3. Mines et Reliques
```sql
CREATE TABLE game_mines (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    raw_material_id INTEGER REFERENCES raw_materials(id),
    obtained_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE game_relics (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    relic_type VARCHAR(50),
    bonus_data JSONB,  -- Bonus à définir
    obtained_at TIMESTAMP DEFAULT NOW()
);
```

#### 4. Jetons X (Croix)
```sql
ALTER TABLE game_players ADD COLUMN x_tokens INTEGER DEFAULT 0;
-- Maximum 5 jetons X
```

#### 5. Bonus aux Seuils de Lasers
```sql
CREATE TABLE game_laser_bonuses (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    threshold INTEGER NOT NULL,  -- 2, 5, 8
    bonus_type VARCHAR(50),  -- Type de bonus (à définir)
    bonus_data JSONB,  -- Détails du bonus
    obtained_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(game_id, player_id, threshold)
);
```

---

## 📊 Fonction de Calcul des Points de Dégâts des Lasers

### Fonction SQL Recommandée

```sql
CREATE OR REPLACE FUNCTION calculate_laser_damage_points(total_lasers INTEGER)
RETURNS INTEGER AS $$
BEGIN
    IF total_lasers <= 6 THEN
        RETURN total_lasers * 2;
    ELSE
        RETURN total_lasers * 3;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Utilisation
```sql
-- Calculer les points de dégâts des lasers pour un joueur
SELECT 
    total_lasers,
    calculate_laser_damage_points(total_lasers) as laser_damage_points
FROM game_players
WHERE id = 1;
```

---

## ✅ Checklist Finale

### Mappings ✅
- [x] Cartes Action → Rangers
- [x] Types de Cartes
- [x] Points et Scores
- [x] Continents → Matières Premières
- [x] Catégories → Types d'Armes
- [x] Plateaux → Armures Méca

### Actions Détaillées ✅
- [x] Action Animaux (0-1-1-1-2 / 1-1-2-2-2)
- [x] Action Mécène (cartes OU crédits)
- [x] Action Construction (taille 1-5, 2 crédits/case)
- [x] Action Association (émissaires, quêtes, mines, reliques)
- [x] Action Cartes (pioche, rivière)

### Système de Lasers ✅
- [x] Valeur variable (2 pd jusqu'à 6, 3 pd à partir de 7)
- [x] Bonus aux seuils (2, 5, 8, 10)
- [x] Cartes Dernier Souffle (2 au début, défausser 1 à 10 lasers)

### Schéma SQL ⚠️
- [x] Tables principales existantes
- [ ] Table `dernier_souffle_cards` (à ajouter)
- [ ] Table `game_last_breath_cards` (à ajouter)
- [ ] Colonne `emissaires_count` dans `game_players` (à ajouter)
- [ ] Colonne `x_tokens` dans `game_players` (à ajouter)
- [ ] Tables `game_mines` et `game_relics` (à ajouter)
- [ ] Table `game_laser_bonuses` (à ajouter)
- [ ] Fonction `calculate_laser_damage_points` (à ajouter)

---

## 📝 Points à Définir (Non Bloquants)

1. **Bonus à 5 lasers** : Quel est le bonus exact ?
2. **Bonus à 8 lasers** : Quel est le bonus exact ?
3. **Amélioration d'une carte Action** : Quelles sont les conditions exactes ?
4. **Reliques** : Quels sont les bonus exacts des reliques ?
5. **Action Association niveau 0** : Coût exact en or pour 1 laser ?

---

## 🎯 Conclusion

**Tous les mappings sont cohérents et clairs.**

Les documents sont complets et prêts pour l'implémentation. Les seules modifications nécessaires au schéma SQL sont l'ajout de tables pour gérer les cartes Dernier Souffle, les émissaires, les mines, les reliques et les bonus aux seuils de lasers.

---

*Vérification effectuée le : 2025-01-XX*
*Statut : ✅ Prêt pour l'implémentation*


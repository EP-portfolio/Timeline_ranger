# Mise à Jour - Système des Lasers

Ce document résume les mises à jour apportées suite aux informations précises sur le système des lasers.

## ✅ Informations Ajoutées

### 1. Valeur des Lasers en Points de Dégâts

**Système de valeur variable** :
- **0-6 lasers** : Chaque laser vaut **2 points de dégâts**
- **7+ lasers** : Chaque laser vaut **3 points de dégâts**

**Exemples** :
- 3 lasers = 3 × 2 = **6 points de dégâts**
- 6 lasers = 6 × 2 = **12 points de dégâts**
- 7 lasers = 7 × 3 = **21 points de dégâts**
- 10 lasers = 10 × 3 = **30 points de dégâts**

### 2. Bonus aux Seuils de Lasers

**Bonus disponibles** :
- **2 lasers** : Choisir entre améliorer une carte Action OU obtenir un nouvel émissaire
- **5 lasers** : Bonus (à définir)
- **8 lasers** : Bonus (à définir)
- **10 lasers** : **Le premier joueur à 10 lasers** oblige **TOUS les joueurs** à défausser une des deux cartes "Dernier Souffle"

### 3. Cartes Dernier Souffle

**Distribution initiale** :
- Chaque joueur reçoit **2 cartes "Dernier Souffle"** aléatoirement au début de la partie
- Ces cartes sont conservées jusqu'à ce que le joueur atteigne 10 lasers

**À 10 lasers (premier joueur)** :
- **TOUS les joueurs** doivent **défausser une des deux cartes**
- Chaque joueur **choisit** laquelle conserver
- Les cartes conservées seront utilisées lors du décompte final
- **Note** : C'est un événement global déclenché par le premier joueur à atteindre 10 lasers

## 📝 Documents Mis à Jour

### 1. SYSTEME_LASERS.md (Nouveau)
- Document complet sur le système des lasers
- Valeur variable selon nombre
- Bonus aux seuils
- Cartes Dernier Souffle

### 2. SYSTEME_POINTS_DEGATS.md (Nouveau)
- Document complet sur le calcul des points de dégâts
- Formule complète incluant les lasers
- Exemples de calcul

### 3. BESOINS_FONCTIONNELS.md
- Section "Points de Dégâts" mise à jour avec valeur variable des lasers
- Section "Lasers" mise à jour avec bonus aux seuils
- Phase d'initialisation : Ajout des 2 cartes Dernier Souffle
- Phase de décompte final : Calcul des lasers selon valeur variable

### 4. QUESTIONS_OUVERTES.md
- Question sur les lasers : Complétée

## 🔧 Modifications Nécessaires au Schéma SQL

### Table à Ajouter/Modifier

#### Option 1 : Ajouter dans `game_players`
```sql
ALTER TABLE game_players ADD COLUMN dernier_souffle_cards JSONB;
-- Stocke les 2 cartes Dernier Souffle reçues au début
-- Format : [{"card_id": 1, "kept": true}, {"card_id": 2, "kept": false}]
```

#### Option 2 : Table dédiée (Recommandé)
```sql
CREATE TABLE game_last_breath_cards (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    card_id INTEGER,  -- Référence à la table des cartes Dernier Souffle
    received_at TIMESTAMP DEFAULT NOW(),
    kept BOOLEAN DEFAULT TRUE,  -- True si conservée, False si défaussée
    discarded_at TIMESTAMP  -- Quand défaussée (à 10 lasers)
);
```

## 📊 Calcul des Points de Dégâts des Lasers

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

## ⚠️ Points à Définir

1. **Bonus à 5 lasers** : Quel est le bonus exact ?
2. **Bonus à 8 lasers** : Quel est le bonus exact ?
3. **Amélioration d'une carte Action** : Quelles sont les conditions exactes pour améliorer une carte Action ?
4. **Table des cartes Dernier Souffle** : Existe-t-elle dans le schéma ? Sinon, à créer.

## 🔗 Relations avec les Autres Systèmes

### Action Association
- Niveau 0 (améliorée) : Peut payer or pour obtenir 1 laser supplémentaire
- Les quêtes réalisées peuvent donner des lasers

### Décompte Final
- Calcul des points de dégâts des lasers selon la formule (2 ou 3 points selon nombre)
- Application de la carte Dernier Souffle conservée

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


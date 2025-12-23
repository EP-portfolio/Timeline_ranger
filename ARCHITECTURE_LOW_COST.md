# Architecture Low-Cost - Timeline Ranger Online

Architecture optimisée pour minimiser les coûts tout en permettant 4-20 joueurs simultanés.

## 💰 Analyse des Coûts

### Neo4j : Est-ce Nécessaire ?

**Réponse : NON, pas pour un prototype !**

#### Utilisation Actuelle de Neo4j
- Stockage des cartes (Animal, Mécène, Projet de Conservation)
- Relations entre cartes et leurs propriétés
- Environ 200-300 cartes au total

#### Alternatives Moins Coûteuses

**Option 1 : PostgreSQL (RECOMMANDÉ)**
- ✅ **Gratuit** sur Render (PostgreSQL gratuit jusqu'à 90 jours, puis $7/mois)
- ✅ Peut stocker les cartes en JSONB
- ✅ Requêtes efficaces avec index
- ✅ Déjà nécessaire pour utilisateurs/parties
- ✅ Une seule base de données à gérer

**Option 2 : JSON/CSV en Mémoire**
- ✅ **100% gratuit**
- ✅ Charger les cartes au démarrage
- ✅ Parfait pour un prototype
- ⚠️ Limité si beaucoup de cartes

**Option 3 : SQLite**
- ✅ **100% gratuit**
- ✅ Fichier local
- ✅ Pas de serveur nécessaire
- ⚠️ Limité pour production multi-instances

## 🏗️ Architecture Low-Cost Recommandée

### Stack Gratuit/Low-Cost

```
┌─────────────────────────────────────────┐
│         FRONTEND (GRATUIT)               │
│  Vercel / Netlify                        │
│  - React/Vue.js                          │
│  - Build automatique                     │
│  - HTTPS inclus                          │
└──────────────────┬──────────────────────┘
                   │ HTTPS
                   │
┌──────────────────▼──────────────────────┐
│      BACKEND (GRATUIT - Render)          │
│  Render Free Tier                        │
│  - FastAPI                               │
│  - WebSocket                              │
│  - 750h/mois gratuit                     │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │                     │
┌───────▼──────┐      ┌───────▼──────┐
│  PostgreSQL │      │   Fichiers   │
│  (GRATUIT)  │      │   JSON/CSV   │
│  Render     │      │  (CARTES)    │
│  Free Tier  │      │  (GRATUIT)    │
└─────────────┘      └──────────────┘
```

### Coûts Estimés

| Service | Coût | Limites |
|---------|------|---------|
| **Frontend (Vercel)** | **GRATUIT** | Illimité pour usage normal |
| **Backend (Render)** | **GRATUIT** | 750h/mois, se met en veille après inactivité |
| **PostgreSQL (Render)** | **GRATUIT** | 90 jours, puis $7/mois (ou migrer vers Supabase gratuit) |
| **Cartes (JSON/CSV)** | **GRATUIT** | Stockage dans le repo |
| **Total MVP** | **$0-7/mois** | Parfait pour prototype |

### Alternative : Supabase (100% Gratuit)

Si vous voulez rester 100% gratuit :

```
┌─────────────────────────────────────────┐
│         FRONTEND                        │
│  Vercel (GRATUIT)                       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      BACKEND                             │
│  Render Free Tier (GRATUIT)             │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      Supabase (100% GRATUIT)             │
│  - PostgreSQL gratuit                    │
│  - 500MB base de données                │
│  - 2GB bande passante/mois              │
│  - Realtime (WebSocket) gratuit          │
└─────────────────────────────────────────┘
```

## 📊 Migration Neo4j → PostgreSQL

### Structure des Cartes dans PostgreSQL

#### Option 1 : Table avec JSONB (Recommandé)

```sql
-- Table des cartes
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,
    card_type VARCHAR(50) NOT NULL,  -- 'Animal', 'Mecene', 'Projet', etc.
    name VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,  -- Toutes les propriétés en JSON
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index pour recherches rapides
CREATE INDEX idx_cards_type ON cards(card_type);
CREATE INDEX idx_cards_name ON cards USING gin(name gin_trgm_ops);
CREATE INDEX idx_cards_data ON cards USING gin(data);

-- Exemple de données
INSERT INTO cards (card_number, card_type, name, data) VALUES
(1, 'Animal', 'Lion', '{"credits": 15, "size": 4, "appeal": 9, "continent": "Afrique", "category": "Predateur"}');
```

**Avantages** :
- ✅ Flexible (ajout de propriétés facile)
- ✅ Requêtes JSONB efficaces
- ✅ Pas besoin de relations complexes
- ✅ Parfait pour un prototype

#### Option 2 : Tables Normalisées

```sql
-- Table principale des cartes
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- Table des propriétés (clé-valeur)
CREATE TABLE card_properties (
    id SERIAL PRIMARY KEY,
    card_id INTEGER REFERENCES cards(id),
    property_key VARCHAR(100) NOT NULL,
    property_value TEXT NOT NULL
);

-- Index
CREATE INDEX idx_properties_card ON card_properties(card_id);
CREATE INDEX idx_properties_key ON card_properties(property_key);
```

**Avantages** :
- ✅ Structure claire
- ✅ Requêtes SQL standard
- ⚠️ Plus de tables à gérer

### Script de Migration

Créer un script Python pour migrer les données depuis Neo4j (ou directement depuis l'ODS) vers PostgreSQL.

## 🚀 Architecture Simplifiée pour Prototype

### Backend Minimal

```
backend/
├── app/
│   ├── main.py                 # FastAPI
│   ├── config.py               # Configuration
│   │
│   ├── api/
│   │   ├── auth.py             # Authentification
│   │   ├── games.py            # Parties
│   │   └── cards.py            # Cartes (depuis PostgreSQL ou JSON)
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── game.py
│   │   └── card.py
│   │
│   ├── database/
│   │   ├── postgres.py         # Connexion PostgreSQL
│   │   └── cards_loader.py    # Chargement cartes (JSON/CSV)
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── game_service.py
│   │   └── card_service.py    # Service cartes (PostgreSQL ou mémoire)
│   │
│   └── websocket/
│       └── game_manager.py
│
├── data/
│   └── cards.json              # Cartes en JSON (backup)
│
└── requirements.txt
```

### Chargement des Cartes

**Option A : Depuis PostgreSQL** (Recommandé pour production)
```python
# Charger depuis PostgreSQL
cards = db.query(Card).all()
```

**Option B : Depuis JSON** (Pour prototype rapide)
```python
# Charger depuis fichier JSON au démarrage
with open('data/cards.json') as f:
    cards = json.load(f)
    CARDS_CACHE = {card['card_number']: card for card in cards}
```

## 📋 Plan de Migration

### Étape 1 : Exporter les Données

1. **Depuis Neo4j** (si vous avez déjà des données) :
```cypher
// Exporter toutes les cartes
MATCH (c:Card)
RETURN c.card_number, labels(c), properties(c)
```

2. **Depuis l'ODS** (recommandé) :
- Utiliser le script Python existant
- Exporter directement vers PostgreSQL ou JSON

### Étape 2 : Créer le Schéma PostgreSQL

```sql
-- Créer les tables
CREATE TABLE cards (...);
CREATE TABLE users (...);
CREATE TABLE games (...);
```

### Étape 3 : Importer les Données

```python
# Script d'import
python scripts/import_cards_to_postgres.py
```

### Étape 4 : Mettre à Jour le Code

- Remplacer les requêtes Neo4j par des requêtes PostgreSQL
- Adapter les services

## 💡 Recommandations pour Prototype

### Pour 4-20 Joueurs Simultanés

**Stack Recommandé** :
1. **Frontend** : Vercel (gratuit)
2. **Backend** : Render Free Tier (gratuit, 750h/mois)
3. **Base de données** : 
   - **Option A** : Supabase PostgreSQL (100% gratuit, 500MB)
   - **Option B** : Render PostgreSQL (gratuit 90 jours)
4. **Cartes** : JSON/CSV dans le repo (gratuit)

**Pas besoin de** :
- ❌ Neo4j (trop cher pour prototype)
- ❌ Redis (peut utiliser PostgreSQL ou mémoire)
- ❌ Services payants

### Optimisations pour Limites Gratuites

1. **Render Free Tier** :
   - Se met en veille après 15 min d'inactivité
   - Solution : Ping automatique ou utiliser Supabase Realtime

2. **Supabase** :
   - 500MB suffisant pour des milliers de cartes
   - 2GB/mois bande passante suffisant pour 20 joueurs
   - Realtime gratuit (remplace WebSocket custom)

3. **Vercel** :
   - Illimité pour usage normal
   - Build automatique à chaque push

## 🎯 Architecture Finale Recommandée

```
┌─────────────────────────────────────────┐
│    FRONTEND (Vercel - GRATUIT)          │
│    React/Vue.js                          │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    BACKEND (Render Free - GRATUIT)       │
│    FastAPI + WebSocket                   │
│    OU                                    │
│    Supabase Edge Functions (GRATUIT)     │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Supabase (100% GRATUIT)               │
│    - PostgreSQL (500MB)                  │
│    - Realtime (WebSocket)                 │
│    - Auth (optionnel)                     │
│    - Storage (cartes JSON)                │
└─────────────────────────────────────────┘
```

## 📊 Comparaison des Coûts

| Solution | Coût/Mois | Limites | Recommandation |
|----------|-----------|---------|----------------|
| **Neo4j Aura** | $65+ | 50K nodes | ❌ Trop cher |
| **Render + PostgreSQL** | $0-7 | 90 jours gratuit | ✅ Bon pour début |
| **Supabase** | $0 | 500MB, 2GB/mois | ✅ **MEILLEUR pour prototype** |
| **Vercel + Supabase** | $0 | Illimité usage normal | ✅ **IDÉAL** |

## 🚀 Prochaines Étapes

1. **Migrer les cartes** : Neo4j → PostgreSQL/JSON
2. **Choisir Supabase** : 100% gratuit, parfait pour prototype
3. **Simplifier l'architecture** : Pas besoin de Neo4j
4. **Développer le prototype** : Stack gratuit complet

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


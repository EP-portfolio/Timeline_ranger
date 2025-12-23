# Migration Neo4j → PostgreSQL - Guide Pratique

Guide pour migrer les cartes de Neo4j vers PostgreSQL pour réduire les coûts.

## 🎯 Objectif

Remplacer Neo4j par PostgreSQL pour stocker les cartes, réduisant les coûts de $65+/mois à $0-7/mois.

## 📊 Analyse des Données Actuelles

### Structure Neo4j Actuelle

```
(:Card:Animal {card_number: 1, sheet_name: "Animal"})
  -[:HAS_Nom_Animal]->(:Value_Nom_Animal {value: "Lion"})
  -[:HAS_Crédits]->(:Value_Crédits {value: 15})
  -[:HAS_Continent_s_d_origine]->(:Value_Continent_s_d_origine {value: "Afrique"})
```

### Structure PostgreSQL Proposée

```sql
-- Table principale
cards (
    id, card_number, card_type, name, data (JSONB)
)

-- Exemple de données
{
    "card_number": 1,
    "card_type": "Animal",
    "name": "Lion",
    "data": {
        "credits": 15,
        "size": 4,
        "appeal": 9,
        "continent": "Afrique",
        "category": "Predateur",
        ...
    }
}
```

## 🔧 Script de Migration

### Étape 1 : Exporter depuis Neo4j (si nécessaire)

```python
# scripts/export_from_neo4j.py
from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("neo4j://localhost", auth=("neo4j", "password"))

def export_cards():
    with driver.session() as session:
        # Récupérer toutes les cartes avec leurs propriétés
        query = """
        MATCH (c:Card)
        OPTIONAL MATCH (c)-[r]->(v)
        RETURN c.card_number as card_number,
               labels(c) as labels,
               collect({rel: type(r), value: v.value}) as properties
        """
        result = session.run(query)
        
        cards = []
        for record in result:
            card = {
                "card_number": record["card_number"],
                "card_type": [l for l in record["labels"] if l != "Card"][0],
                "properties": {}
            }
            
            for prop in record["properties"]:
                if prop["rel"]:
                    key = prop["rel"].replace("HAS_", "").lower()
                    card["properties"][key] = prop["value"]
            
            cards.append(card)
        
        # Sauvegarder en JSON
        with open("data/cards_export.json", "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)
        
        print(f"Exported {len(cards)} cards")

if __name__ == "__main__":
    export_cards()
```

### Étape 2 : Exporter depuis l'ODS (Recommandé)

```python
# scripts/export_from_ods.py
import pandas as pd
import json
from pathlib import Path

def export_cards_from_ods():
    """Exporte les cartes depuis l'ODS vers JSON."""
    ods_file = "Ark_Nova_Mondes_marins_cartes_stats_FR.ods"
    
    # Feuilles à traiter
    sheets = ["Animal", "Mécène", "Projet_de_conservation", "Décompte_final"]
    
    all_cards = []
    
    for sheet_name in sheets:
        try:
            df = pd.read_excel(ods_file, sheet_name=sheet_name, engine="odf")
            
            # Convertir chaque ligne en carte
            for _, row in df.iterrows():
                card = {
                    "card_number": row.get("N° Carte", None),
                    "card_type": sheet_name,
                    "name": row.get("Nom", ""),
                    "data": {}
                }
                
                # Ajouter toutes les colonnes comme propriétés
                for col in df.columns:
                    if col not in ["N° Carte", "Nom"]:
                        value = row.get(col)
                        if pd.notna(value):
                            # Nettoyer le nom de la colonne
                            key = col.replace(" ", "_").lower()
                            card["data"][key] = str(value)
                
                all_cards.append(card)
        
        except Exception as e:
            print(f"Erreur avec la feuille {sheet_name}: {e}")
    
    # Sauvegarder
    output_file = Path("data/cards.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_cards, f, ensure_ascii=False, indent=2)
    
    print(f"Exported {len(all_cards)} cards to {output_file}")

if __name__ == "__main__":
    export_cards_from_ods()
```

### Étape 3 : Créer le Schéma PostgreSQL

```sql
-- scripts/create_schema.sql

-- Table des cartes
CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index pour performances
CREATE INDEX IF NOT EXISTS idx_cards_type ON cards(card_type);
CREATE INDEX IF NOT EXISTS idx_cards_number ON cards(card_number);
CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_data ON cards USING gin(data);

-- Index GIN pour recherches dans JSONB
CREATE INDEX IF NOT EXISTS idx_cards_data_gin ON cards USING gin(data jsonb_path_ops);
```

### Étape 4 : Importer dans PostgreSQL

```python
# scripts/import_to_postgres.py
import json
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path

def import_cards_to_postgres():
    """Importe les cartes depuis JSON vers PostgreSQL."""
    
    # Charger les cartes
    with open("data/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
    
    # Connexion PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="timeline_ranger",
        user="postgres",
        password="password"
    )
    cur = conn.cursor()
    
    # Préparer les données
    values = []
    for card in cards:
        values.append((
            card["card_number"],
            card["card_type"],
            card["name"],
            json.dumps(card["data"], ensure_ascii=False)
        ))
    
    # Insérer
    insert_query = """
    INSERT INTO cards (card_number, card_type, name, data)
    VALUES %s
    ON CONFLICT (card_number) DO UPDATE
    SET card_type = EXCLUDED.card_type,
        name = EXCLUDED.name,
        data = EXCLUDED.data,
        updated_at = NOW()
    """
    
    execute_values(cur, insert_query, values)
    conn.commit()
    
    print(f"Imported {len(cards)} cards to PostgreSQL")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_cards_to_postgres()
```

## 🔄 Mise à Jour du Code

### Avant (Neo4j)

```python
# Ancien code avec Neo4j
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_card(card_number):
    with driver.session() as session:
        query = """
        MATCH (c:Card {card_number: $card_number})-[r]->(v)
        RETURN c, collect({rel: type(r), value: v.value}) as props
        """
        result = session.run(query, card_number=card_number)
        # Traiter le résultat...
```

### Après (PostgreSQL)

```python
# Nouveau code avec PostgreSQL
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://user:password@localhost/db")
Session = sessionmaker(bind=engine)

def get_card(card_number):
    with Session() as session:
        query = text("SELECT * FROM cards WHERE card_number = :card_number")
        result = session.execute(query, {"card_number": card_number}).fetchone()
        
        if result:
            return {
                "card_number": result.card_number,
                "card_type": result.card_type,
                "name": result.name,
                "data": result.data  # Déjà en dict Python
            }
        return None

def search_cards(card_type=None, name_pattern=None):
    with Session() as session:
        query = text("""
            SELECT * FROM cards
            WHERE (:card_type IS NULL OR card_type = :card_type)
            AND (:name_pattern IS NULL OR name ILIKE :name_pattern)
        """)
        results = session.execute(query, {
            "card_type": card_type,
            "name_pattern": f"%{name_pattern}%" if name_pattern else None
        }).fetchall()
        
        return [dict(row) for row in results]

def search_cards_by_property(property_key, property_value):
    with Session() as session:
        query = text("""
            SELECT * FROM cards
            WHERE data->>:property_key = :property_value
        """)
        results = session.execute(query, {
            "property_key": property_key,
            "property_value": property_value
        }).fetchall()
        
        return [dict(row) for row in results]
```

## 📊 Requêtes Comparatives

### Recherche par Type

**Neo4j** :
```cypher
MATCH (c:Card:Animal)
RETURN c
```

**PostgreSQL** :
```sql
SELECT * FROM cards WHERE card_type = 'Animal';
```

### Recherche par Propriété

**Neo4j** :
```cypher
MATCH (c:Card)-[:HAS_Continent_s_d_origine]->(v {value: "Afrique"})
RETURN c
```

**PostgreSQL** :
```sql
SELECT * FROM cards 
WHERE data->>'continent_s_d_origine' = 'Afrique';
-- ou avec index GIN
SELECT * FROM cards 
WHERE data @> '{"continent_s_d_origine": "Afrique"}'::jsonb;
```

### Recherche Complexe

**PostgreSQL** :
```sql
-- Cartes avec crédits > 20 et continent Afrique
SELECT * FROM cards
WHERE (data->>'credits')::int > 20
AND data->>'continent' = 'Afrique';
```

## ✅ Avantages de PostgreSQL

1. **Coût** : $0-7/mois vs $65+/mois pour Neo4j
2. **Simplicité** : SQL standard, plus facile à maintenir
3. **Performance** : Excellent pour ce cas d'usage
4. **Intégration** : Même base pour cartes, utilisateurs, parties
5. **JSONB** : Flexible comme Neo4j mais avec SQL

## 🚀 Plan d'Action

1. ✅ Exporter les cartes depuis l'ODS vers JSON
2. ✅ Créer le schéma PostgreSQL
3. ✅ Importer les cartes dans PostgreSQL
4. ✅ Mettre à jour le code (remplacer Neo4j)
5. ✅ Tester les requêtes
6. ✅ Déployer

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


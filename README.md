# Ark Nova - Graphe Neo4j

## 📋 Architecture du Graphe

### Principe Fondamental

Le graphe est construit à partir du fichier ODS `Ark_Nova_Mondes_marins_cartes_stats_FR.ods`, qui est **la seule et unique source de connaissance** pour l'instant.

### Structure du Graphe

#### 1. Nœuds Principaux (Feuilles ODS)

Chaque **feuille** du fichier ODS devient un **type de nœud principal** dans le graphe :
- `Animal` (feuille "Animal")
- `Mécène` (feuille "Mécène")
- `Projet_de_conservation` (feuille "Projet_de_conservation")
- `Décompte_final` (feuille "Décompte_final")

Chaque nœud hérite également du label `Card` et possède :
- `card_number` : **clé primaire** (numéro de carte unique)
- `sheet_name` : nom de la feuille d'origine

#### 2. Relations HAS_<nom_colonne>

Pour **chaque colonne** de chaque feuille, une relation est créée :
- Format : `HAS_<NomColonne>`
- Direction : `(:Card)-[:HAS_<NomColonne>]->(:Value_<NomColonne>)`

**Exemple** :
- Colonne "Nom Animal" → Relation `HAS_Nom_Animal`
- Colonne "Crédits" → Relation `HAS_Crédits`
- Colonne "Continent(s) d'origine" → Relation `HAS_Continent_s_d_origine`

#### 3. Nœuds de Valeurs

Pour **chaque colonne**, un type de nœud de valeur est créé :
- Format : `Value_<NomColonne>`
- Propriété : `value` (contient la valeur de la cellule)

**Règle importante** : Les valeurs vides (NaN, chaînes vides) sont remplacées par la valeur `"Inconnu"`.

#### 4. Clé Primaire

Le **numéro de carte** (`card_number`) est la clé primaire unique pour identifier chaque carte dans le graphe.

## 📊 Exemple de Structure

Pour une carte d'animal avec :
- Numéro : 1
- Nom : "Lion"
- Crédits : 15
- Continent : "Afrique"

Le graphe contiendra :

```
(:Card:Animal {card_number: 1, sheet_name: "Animal"})
  -[:HAS_Nom_Animal]->(:Value_Nom_Animal {value: "Lion"})
  -[:HAS_Crédits]->(:Value_Crédits {value: 15})
  -[:HAS_Continent_s_d_origine]->(:Value_Continent_s_d_origine {value: "Afrique"})
```

## 🚀 Installation et Utilisation

### Prérequis

- Python 3.9+
- Neo4j (Desktop, Community Edition ou Aura)
- Les dépendances Python (voir `requirements.txt`)

### Installation

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Configurer Neo4j** :

   Créer un fichier `.env` à la racine du dossier `ark_nova_clean` :
```env
NEO4J_URI=neo4j+s://c227c5ca.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=votre_mot_de_passe_aura
NEO4J_DATABASE=neo4j
```

   **Note** : L'URI par défaut est déjà configurée pour Neo4j Aura Instance01 (`c227c5ca`). 
   Il suffit de définir `NEO4J_PASSWORD` dans le fichier `.env` avec le mot de passe de votre instance Aura.
   
   Ou modifier directement les valeurs dans `config.py` si vous préférez.

3. **Lancer l'import** :
```bash
python import_ods_new_architecture.py
```

### Vérification

Une fois l'import terminé, vous pouvez vérifier le graphe dans Neo4j Browser :

```cypher
// Voir toutes les cartes
MATCH (c:Card)
RETURN c
LIMIT 25

// Compter les cartes par type
MATCH (c:Card)
RETURN labels(c) as type, count(*) as count

// Voir une carte avec ses relations
MATCH (c:Card {card_number: 341})-[r]->(v)
RETURN c, r, v
LIMIT 50
```

## 🔧 Fichiers

- `Ark_Nova_Mondes_marins_cartes_stats_FR.ods` : Source de données unique
- `config.py` : Configuration Neo4j
- `import_ods_new_architecture.py` : Script d'import
- `requirements.txt` : Dépendances Python

## 📝 Notes

- Les feuilles "Commentaires" et "FR-EN_Capacité-Corallien" sont ignorées lors de l'import
- Les noms de colonnes sont nettoyés pour créer des noms de relations valides (suppression des caractères spéciaux, remplacement des espaces par des underscores)
- Les valeurs numériques sont converties en chaînes pour les nœuds Value (pour simplifier le modèle)
- Les valeurs vides sont remplacées par `"Inconnu"`


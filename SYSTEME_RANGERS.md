# Système des Rangers de Couleurs - Documentation Complète

## 🎯 Vue d'Ensemble

Le système des **Rangers de Couleurs** remplace le système des **cartes Action** d'Ark Nova. Chaque joueur dispose de **5 Rangers** qui peuvent réaliser des **actions de couleur** correspondantes.

## 🔵⚫🟠🟢🟡 Les 5 Rangers

| Ranger | Couleur | Action Originale | Description |
|--------|---------|------------------|-------------|
| **Ranger Bleu** | 🔵 | ACTION MECENE | Spécialisé dans les actions de mécénat et sponsors |
| **Ranger Noir** | ⚫ | ACTION ANIMAUX | Spécialisé dans les actions liées aux animaux/troupes |
| **Ranger Orange** | 🟠 | ACTION CONSTRUCTION | Spécialisé dans les actions de construction |
| **Ranger Vert** | 🟢 | ACTION ASSOCIATION | Spécialisé dans les actions d'association et spécialistes |
| **Ranger Jaune** | 🟡 | ACTION CARTES | Spécialisé dans la gestion de cartes (pioche, défausse) |

## 🎴 Actions de Couleur

Chaque Ranger peut réaliser uniquement les **actions de sa couleur** :

### 🔵 Actions Bleues
- **Source** : Cartes Mécène
- **Ranger** : Ranger Bleu
- **Exemples** :
  - "Action Bleue : Fondation Wildlife"
  - "Action Bleue : Sponsor Industriel"
  - "Action Bleue : Mécène Scientifique"

### ⚫ Actions Noires
- **Source** : Cartes Animal
- **Ranger** : Ranger Noir
- **Exemples** :
  - "Action Noire : Lion"
  - "Action Noire : Éléphant"
  - "Action Noire : Tigre"

### 🟠 Actions Orange
- **Source** : Actions de Construction
- **Ranger** : Ranger Orange
- **Exemples** :
  - "Action Orange : Construire une garnison standard"
  - "Action Orange : Construire un bâtiment"
  - "Action Orange : Agrandir une garnison"

### 🟢 Actions Vertes
- **Source** : Actions d'Association
- **Ranger** : Ranger Vert
- **Exemples** :
  - "Action Verte : Engager un embassadeur"
  - "Action Verte : Activer une capacité"
  - "Action Verte : Augmenter la renommée"

### 🟡 Actions Jaunes
- **Source** : Actions de gestion de cartes
- **Ranger** : Ranger Jaune
- **Exemples** :
  - "Action Jaune : Piocher 2 cartes"
  - "Action Jaune : Défausser 1 carte"
  - "Action Jaune : Rejouer une carte"

## 🔄 Système de Rotation

### Mécanique
1. **Position initiale** : Chaque Ranger a une position de 1 à 5
2. **Puissance** : La position détermine la puissance (1 = faible, 5 = forte)
3. **Utilisation** : Le joueur choisit un Ranger et réalise une action de sa couleur
4. **Rotation** : Après utilisation, le Ranger revient en position 1
5. **Décalage** : Les autres Rangers montent d'une position

### Exemple de Rotation

**État initial** :
```
Position 1 : Ranger Jaune (puissance 1)
Position 2 : Ranger Bleu (puissance 2)
Position 3 : Ranger Noir (puissance 3)
Position 4 : Ranger Orange (puissance 4)
Position 5 : Ranger Vert (puissance 5)
```

**Le joueur utilise Ranger Noir (position 3)** :
```
Position 1 : Ranger Noir (revient en position 1)
Position 2 : Ranger Jaune (monte de 1)
Position 3 : Ranger Bleu (monte de 1)
Position 4 : Ranger Orange (monte de 1)
Position 5 : Ranger Vert (monte de 1)
```

## 🎮 Règles de Jeu

### Règles de Base
1. **Un Ranger ne peut réaliser que les actions de sa couleur**
2. **La puissance du Ranger** détermine l'efficacité de l'action
3. **Chaque action** a des prérequis (coût, conditions, etc.)
4. **La rotation** est automatique après utilisation

### Restrictions
- ❌ Un **Ranger Bleu** ne peut **pas** réaliser une **Action Noire**
- ❌ Un **Ranger Noir** ne peut **pas** réaliser une **Action Bleue**
- ✅ Un **Ranger Bleu** peut **seulement** réaliser des **Actions Bleues**
- ✅ Un **Ranger Noir** peut **seulement** réaliser des **Actions Noires**

## 📊 Impact de la Puissance

La **puissance du Ranger** (1-5) influence l'efficacité de l'action :

### Exemples

#### Action Bleue : Fondation Wildlife
- **Puissance 1** : Gain de 2 crédits
- **Puissance 2** : Gain de 3 crédits
- **Puissance 3** : Gain de 4 crédits
- **Puissance 4** : Gain de 5 crédits
- **Puissance 5** : Gain de 6 crédits

#### Action Jaune : Piocher des cartes
- **Puissance 1** : Piocher 1 carte
- **Puissance 2** : Piocher 2 cartes
- **Puissance 3** : Piocher 3 cartes
- **Puissance 4** : Piocher 4 cartes
- **Puissance 5** : Piocher 5 cartes

## 🎨 Interface Utilisateur

### Éléments Visuels
- **5 Rangers** affichés avec leurs couleurs respectives
- **Indicateurs de position** (1-5) pour chaque Ranger
- **Indicateurs de puissance** visuels (barres, étoiles, etc.)
- **Actions disponibles** filtrées par couleur
- **Animation de rotation** lors du changement de position

### Interactions
- **Clic sur un Ranger** : Affiche les actions disponibles de sa couleur
- **Clic sur une action** : Confirme l'utilisation avec le Ranger sélectionné
- **Prévisualisation** : Affiche l'effet avant confirmation
- **Animation** : Rotation automatique après utilisation

## 🔗 Intégration avec le Système

### Armures Méca
- Les **Rangers** opèrent sur des **armures méca** (anciens plateaux de jeu)
- Chaque **plateau de jeu différent** = **Une armure méca unique** à construire
- Les **garnisons** sont construites sur l'**armure méca** par le **Ranger Orange**
- Les **actions des Rangers** se déroulent sur l'**armure méca**

### Base de Données Neo4j
- **Nœuds Ranger** : Représentent les 5 Rangers
- **Nœuds Action** : Représentent les actions de couleur
- **Nœuds ArmureMeca** : Représentent les différentes armures méca disponibles
- **Relations** : Lient les Rangers aux actions de leur couleur
- **Relations** : Lient les Rangers aux armures méca
- **Propriétés** : Position, puissance, couleur

### Scripts de Conversion
- **Mapping des cartes** : Cartes Mécène → Actions Bleues
- **Mapping des cartes** : Cartes Animal → Actions Noires
- **Création des nœuds** : Rangers et Actions dans Neo4j
- **Création des relations** : Associations Ranger-Action

## 📝 Notes de Design

### Couleurs
- **Bleu** : Associé à l'eau, la stabilité, le mécénat
- **Noir** : Associé à la force, la puissance, les animaux
- **Orange** : Associé à l'énergie, la construction, le feu
- **Vert** : Associé à la nature, la croissance, l'association
- **Jaune** : Associé à la lumière, la connaissance, les cartes

### Thème
- **Rangers** : Représentent des personnages spécialisés
- **Actions** : Représentent les capacités des Rangers
- **Rotation** : Représentent le cycle de travail des Rangers

## 🚀 Prochaines Étapes

1. ✅ **Mapping des Rangers** : Définition des 5 Rangers
2. ✅ **Mapping des Actions** : Définition des actions de couleur
3. ⏳ **Adaptation de la base de données** : Création des nœuds et relations
4. ⏳ **Scripts de conversion** : Transformation des données
5. ⏳ **Interface utilisateur** : Implémentation visuelle
6. ⏳ **Tests** : Validation du système

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


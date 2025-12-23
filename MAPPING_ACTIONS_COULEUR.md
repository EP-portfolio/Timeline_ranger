# Mapping des Cartes Jouables → Actions de Couleur

Ce document détaille comment les cartes jouables d'Ark Nova deviennent des actions de couleur pour les Rangers.

## 🎯 Principe Fondamental

Chaque **carte jouable** est associée à un **Ranger de couleur** et devient une **action de couleur** que ce Ranger peut réaliser.

## 🔵 Actions Bleues (Ranger Bleu)

### Cartes Source
- **Cartes Mécène** → **Actions Bleues**
- **⚠️ Note importante** : Toutes les Actions Bleues ne permettent pas de poser des pièces d'armure
- Seules certaines cartes Mécène (avec effets de construction/bâtiment) deviennent des pièces d'armure
- Les autres Actions Bleues ont d'autres effets (revenus, bonus, etc.)
- **À vérifier** : Consulter la base de données ODS pour identifier les cartes qui permettent réellement de poser

### Mapping Détaillé
| Propriété Originale (Carte Mécène) | Propriété Nouvelle (Pièce d'armure) | Notes |
|-----------------------------------|-------------------------------------|-------|
| `Nom Mécène` | `Nom Pièce d'armure` | Nom de la pièce d'armure spéciale |
| `Niveau` | `Niveau Action` | Niveau de l'action (1-3) |
| `Condition(s) (icônes)` | `Condition(s) (icônes)` | Conditions requises |
| `Icône(s) obtenue(s)` | `Icône(s) obtenue(s)` | Icônes gagnées |
| `Points Attrait/Conservation/Réputation` | `Points de Dégâts/Nombre de Lasers/À DÉTERMINER` | Points accordés |
| `Effet unique immédiat (fond jaune)` | `Effet d'invocation (fond jaune)` | Effet immédiat |
| `Effet permanent/récurrent (fond bleu)` | `Effet quotidien (fond bleu)` | Effet récurrent |
| `Revenus (fond violet)` | `Or par jour (fond violet)` | Revenus générés |
| `Effet de fin de partie (fond marron)` | `Dernier souffle (fond marron)` | Effet fin de partie |

### Exemple
- **Carte Mécène** : "Fondation Wildlife" (Niveau 2)
- **Action Bleue** : "Action Bleue : Pièce d'armure - Fondation Wildlife" (Niveau 2)
- **Ranger** : Ranger Bleu peut poser cette pièce d'armure sur l'armure méca

## ⚫ Actions Noires (Ranger Noir)

### Cartes Source
- **Cartes Animal** → **Actions Noires** → **Installation d'armes**

### Mapping Détaillé
| Propriété Originale (Carte Animal) | Propriété Nouvelle (Arme) | Notes |
|-----------------------------------|---------------------------|-------|
| `Nom Animal` | `Nom Arme` | Nom de l'arme |
| `Taille` | `Taille Slot Requis` | Taille du slot nécessaire pour l'arme |
| `Enclos` | `Type Slot` | Type de slot requis (si applicable) |
| `Crédits` | `Or` | Coût en or |
| `Condition(s) (icônes)` | `Condition(s) (icônes)` | Conditions requises |
| `Catégorie(s) d'animal` | `Catégorie(s) de troupe` | Catégories |
| `Continent(s) d'origine` | `Plan(s) d'origine` | Plans d'origine |
| `Capacité` | `Bonus` | Capacité spéciale |
| `Points Attrait` | `Dégâts Physique` | Points de dégâts physique |
| `Points Conservation` | `Dégâts d'Armure` | Points de dégâts d'armure |
| `Points Réputation` | `Renommée` | Points de renommée |

### Exemple
- **Carte Animal** : "Lion" (Taille 3, Coût 15)
- **Action Noire** : "Action Noire : Installer Arme - Lion" (Taille slot 3, Coût 15)
- **Ranger** : Ranger Noir peut installer cette arme dans un **slot disponible** créé par le Ranger Orange
- **Prérequis** : Un slot de taille 3 doit avoir été construit par le Ranger Orange

## 🟠 Actions Orange (Ranger Orange)

### Actions Source
- **Actions de Construction** → **Actions Orange** → **Construction de parties d'armure**

### Mapping Détaillé
| Propriété Originale | Propriété Nouvelle | Notes |
|---------------------|-------------------|-------|
| Action de construction d'enclos | Action Orange : Construire partie d'armure | Construction de base |
| Action de construction de bâtiment | Action Orange : Construire partie spéciale | Construction avancée |
| Puissance de l'action | Puissance du Ranger | **Détermine le nombre de parties/slots créés** |
| Taille de construction | Taille de la partie d'armure | Taille de la partie construite |
| **Nouveau** | **Création de slots** | Le Ranger Orange crée des **slots pour armes** |

### Exemple
- **Action Construction** : "Construire un enclos standard (taille 2)"
- **Action Orange** : "Action Orange : Construire partie d'armure (taille 2) + créer 2 slots"
- **Ranger** : Ranger Orange peut construire des parties d'armure et créer des slots
- **Résultat** : Les slots créés peuvent être utilisés par le Ranger Noir pour installer des armes

## 🟢 Actions Vertes (Ranger Vert)

### Actions Source
- **Actions d'Association** → **Actions Vertes** → **Installation de lasers**

### Mapping Détaillé
| Propriété Originale | Propriété Nouvelle | Notes |
|---------------------|-------------------|-------|
| Engager un spécialiste | Action Verte : Installer laser | Installation de laser |
| Activer une capacité | Action Verte : Activer capacité laser | Activation de capacité |
| Puissance de l'action | Puissance du Ranger | **Détermine le nombre de lasers** |
| **Points verts** | **Nombre de lasers** | **Chaque point vert = 1 laser** |

### Exemple
- **Action Association** : "Engager un spécialiste" (puissance 3)
- **Action Verte** : "Action Verte : Installer 3 lasers" (puissance 3 = 3 lasers)
- **Ranger** : Ranger Vert peut installer des lasers sur l'armure méca
- **Règle importante** : **Chaque point vert (puissance) = 1 laser installé**
  - Puissance 1 = 1 laser
  - Puissance 2 = 2 lasers
  - Puissance 3 = 3 lasers
  - Puissance 4 = 4 lasers
  - Puissance 5 = 5 lasers

## 🟡 Actions Jaunes (Ranger Jaune)

### Actions Source
- **Actions de gestion de cartes** → **Actions Jaunes**

### Mapping Détaillé
| Propriété Originale | Propriété Nouvelle | Notes |
|---------------------|-------------------|-------|
| Piocher des cartes | Action Jaune : Piocher | Action directe |
| Défausser des cartes | Action Jaune : Défausser | Action directe |
| Rejouer une carte | Action Jaune : Rejouer | Action directe |
| Puissance de l'action | Puissance du Ranger | Détermine le nombre de cartes |

### Exemple
- **Action Cartes** : "Piocher 2 cartes"
- **Action Jaune** : "Action Jaune : Piocher 2 cartes"
- **Ranger** : Ranger Jaune peut réaliser cette action

## 🎮 Système de Jeu

### Règles de Base
1. **Un Ranger ne peut réaliser que les actions de sa couleur**
2. **La puissance du Ranger** (1-5) détermine l'efficacité de l'action
3. **Après utilisation**, le Ranger revient en position 1
4. **Les autres Rangers** montent d'une position

### Exemples de Gameplay

#### Exemple 1 : Ranger Bleu
- **Ranger Bleu** en position 3 (puissance 3)
- **Action Bleue disponible** : "Fondation Wildlife" (Niveau 2)
- Le joueur peut utiliser le **Ranger Bleu** pour réaliser cette **action bleue**
- Après utilisation, **Ranger Bleu** revient en position 1

#### Exemple 2 : Ranger Noir
- **Ranger Noir** en position 5 (puissance 5)
- **Action Noire disponible** : "Lion" (Coût 15)
- Le joueur peut utiliser le **Ranger Noir** pour réaliser cette **action noire**
- Après utilisation, **Ranger Noir** revient en position 1

## 📋 Tableau Récapitulatif

| Ranger | Couleur | Cartes/Actions Source | Actions de Couleur |
|--------|---------|----------------------|-------------------|
| **Ranger Bleu** | 🔵 Bleu | Cartes Mécène | Actions Bleues |
| **Ranger Noir** | ⚫ Noir | Cartes Animal | Actions Noires |
| **Ranger Orange** | 🟠 Orange | Actions Construction | Actions Orange |
| **Ranger Vert** | 🟢 Vert | Actions Association | Actions Vertes |
| **Ranger Jaune** | 🟡 Jaune | Actions Cartes | Actions Jaunes |

## 🔗 Intégration avec les Autres Mappings

Ce mapping s'intègre avec :
- **Mapping des Rangers** : Définit quels Rangers existent
- **Mapping des types de cartes** : Animal → Troupe, Mécène → Sort
- **Mapping des points** : Points Attrait → Points de Dégâts, Points Conservation → Nombre de Lasers
- **Mapping des ressources** : Crédits → Or

## 📝 Notes Importantes

1. **Les cartes jouables** deviennent des **actions de couleur** spécifiques
2. **Chaque action** est associée à un **Ranger de couleur**
3. **La couleur** est le filtre principal pour déterminer la compatibilité
4. **Le système de puissance** (1-5) s'applique à tous les Rangers

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


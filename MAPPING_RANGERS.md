# Mapping des Cartes Action → Rangers de Couleurs

Ce document définit le nouveau système de Rangers de couleurs qui remplace les cartes Action d'Ark Nova.

## 🎯 Vue d'Ensemble

Les **5 cartes Action** d'Ark Nova sont transformées en **5 Rangers de couleurs** avec un système de rotation similaire.

## 🔵 Mapping des Cartes Action → Rangers

| Carte Action Originale  | Ranger de Couleur | Description                                                     |
| ----------------------- | ----------------- | --------------------------------------------------------------- |
| **ACTION MECENE**       | **RANGER BLEU**   | Ranger spécialisé dans les pièces d'armure (bâtiments spéciaux) |
| **ACTION ANIMAUX**      | **RANGER NOIR**   | Ranger spécialisé dans l'installation d'armes dans les slots    |
| **ACTION CONSTRUCTION** | **RANGER ORANGE** | Ranger spécialisé dans la construction de parties d'armure méca |
| **ACTION ASSOCIATION**  | **RANGER VERT**   | Ranger spécialisé dans l'installation de lasers                 |
| **ACTION CARTES**       | **RANGER JAUNE**  | Ranger spécialisé dans les actions de gestion de cartes         |

## 🎴 Mapping des Cartes Jouables → Actions de Couleur

Les cartes jouables associées à chaque action deviennent des **actions de couleur** que le Ranger correspondant peut réaliser :

### 🔵 Actions Bleues (Ranger Bleu)
- **Cartes Mécène** → **Actions Bleues** → **Pièces d'armure**
- Le **Ranger Bleu** peut poser des **pièces d'armure** (anciennement bâtiments spéciaux via cartes Mécène)
- Les **actions bleues** permettent de placer des **pièces d'armure spéciales** sur l'armure méca
- Exemple : Une carte Mécène devient une "Action Bleue : Pièce d'armure [Nom]" jouable par le Ranger Bleu

### ⚫ Actions Noires (Ranger Noir)
- **Cartes Animal** → **Actions Noires** → **Installation d'armes**
- Le **Ranger Noir** peut installer des **armes dans les slots** construits par le Ranger Orange
- Les **actions noires** permettent d'installer des **armes** dans les **slots d'armure** disponibles
- Exemple : Une carte Animal devient une "Action Noire : Installer [Arme]" dans un slot disponible

### 🟠 Actions Orange (Ranger Orange)
- **Actions de Construction** → **Actions Orange** → **Construction de parties d'armure**
- Le **Ranger Orange** construit des **parties de l'armure méca** et crée des **slots pour armes**
- Les **actions orange** permettent de construire des **parties d'armure** et des **slots d'armes**
- Exemple : "Action Orange : Construire une partie d'armure + créer 2 slots"

### 🟢 Actions Vertes (Ranger Vert)
- **Actions d'Association** → **Actions Vertes** → **Installation de lasers**
- Le **Ranger Vert** installe des **lasers** sur l'armure méca
- **Chaque point vert** = **Un nouveau laser** à installer
- Les **actions vertes** permettent d'installer des **lasers** selon la puissance du Ranger
- Exemple : "Action Verte : Installer 3 lasers" (si le Ranger Vert est en position 3)

### 🟡 Actions Jaunes (Ranger Jaune)
- **Cartes liées à la gestion de cartes** → **Actions Jaunes**
- Le **Ranger Jaune** peut réaliser des **actions jaunes** (anciennement actions de gestion de cartes)
- Note : Actions de pioche, défausse, etc.

## 🔄 Système de Rotation

Le système de rotation fonctionne de la même manière que les cartes Action :

- Chaque **Ranger** a une **puissance de 1 à 5** selon sa position
- Après utilisation d'un Ranger, il revient en **position 1** (puissance minimale)
- Les autres Rangers montent d'une position, augmentant leur puissance
- La stratégie consiste à optimiser l'ordre d'utilisation des Rangers

## 📋 Structure des Actions de Couleur

Chaque **Action de Couleur** hérite des propriétés de la carte originale :

### Actions Bleues (ex-Cartes Mécène → Pièces d'armure)
- Nom du mécène → Nom de la pièce d'armure
- Niveau → Niveau de la pièce d'armure
- Effets → Effets de la pièce d'armure
- Points → Points accordés
- Revenus → Revenus générés (si applicable)

### Actions Noires (ex-Cartes Animal → Armes)
- Nom de l'animal → Nom de l'arme
- Taille → Taille de l'arme / Taille du slot requis
- Coût → Coût de l'arme
- Capacités → Capacités de l'arme
- Points → Points de dégâts accordés
- **Important** : L'arme doit être installée dans un **slot** créé par le Ranger Orange

### Actions Orange (Construction de parties d'armure)
- Action de construction → Construction de partie d'armure
- Puissance du Ranger → Nombre de parties / slots créés
- Coût → Coût de construction
- **Important** : Crée des **slots** pour que le Ranger Noir puisse installer des armes

### Actions Vertes (Installation de lasers)
- Action d'association → Installation de lasers
- Puissance du Ranger → Nombre de lasers installés
- **Important** : **Chaque point vert = 1 laser**
- Les lasers peuvent avoir des effets spéciaux selon le type

## 🎮 Implications pour le Jeu

### Interface Utilisateur
- **5 Rangers visuels** avec leurs couleurs respectives
- **Indicateurs de puissance** (1-5) pour chaque Ranger
- **Actions disponibles** filtrées par couleur selon le Ranger actif
- **Animation de rotation** lors du changement de position

### Mécaniques de Jeu
- Un **Ranger** ne peut réaliser que les **actions de sa couleur**
- La **puissance du Ranger** détermine l'efficacité de l'action
- **Rotation automatique** après utilisation d'un Ranger
- **Stratégie** : Optimiser l'ordre d'utilisation des Rangers

## 🔗 Relations avec les Autres Mappings

Ce mapping s'intègre avec :
- **Mapping des types de cartes** : Animal → Troupe, Mécène → Sort, etc.
- **Mapping des points** : Points Attrait → Points de Dégâts, Points Conservation → Nombre de Lasers
- **Mapping des continents** : Continents → Plans
- **Mapping des catégories** : Catégories d'animaux → Catégories de troupes

## 📝 Notes Importantes

1. **Les Rangers remplacent les cartes Action** mais conservent la mécanique de rotation
2. **Les cartes jouables** deviennent des **actions de couleur** spécifiques à chaque Ranger
3. **La couleur** est le filtre principal pour déterminer quelles actions un Ranger peut réaliser
4. **Le système de puissance** (1-5) reste identique au système original

## 🚀 Prochaines Étapes

1. ✅ Mapping des Rangers de couleurs (ce document)
2. ⏳ Mapping des cartes jouables vers actions de couleur
3. ⏳ Adaptation de l'interface utilisateur
4. ⏳ Mise à jour de la base de données Neo4j
5. ⏳ Scripts de conversion

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


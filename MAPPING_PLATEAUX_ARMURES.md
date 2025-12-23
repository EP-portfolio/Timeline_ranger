# Mapping des Plateaux de Jeu → Armures Méca

Ce document définit le mapping des différents plateaux de jeu d'Ark Nova vers les armures méca à construire dans Timeline Ranger.

## 🎯 Vue d'Ensemble

Dans Ark Nova, chaque joueur dispose d'un **plateau personnel** avec une grille pour placer des tuiles d'enclos. Dans Timeline Ranger, chaque **plateau de jeu différent** devient une **armure méca** que le joueur peut construire.

## 🛡️ Concept : Armures Méca

### Principe Fondamental
- **Chaque plateau de jeu différent** = **Une armure méca unique**
- Les armures méca sont des **structures à construire** sur lesquelles le joueur place ses garnisons
- Chaque armure méca a ses propres **caractéristiques** et **configurations de grille**

## 📋 Mapping Conceptuel

| Concept Original (Ark Nova) | Concept Nouveau (Timeline Ranger) | Description |
|------------------------------|-----------------------------------|-------------|
| **Plateau Personnel** | **Armure Méca** | Structure de base pour construire |
| **Grille du plateau** | **Grille de l'armure méca** | Espace de placement des garnisons |
| **Tuiles d'enclos** | **Tuiles de garnison** | Éléments placés sur l'armure méca |
| **Configuration du plateau** | **Configuration de l'armure méca** | Disposition et contraintes spécifiques |
| **Différents plateaux** | **Différentes armures méca** | Variantes disponibles |

## 🔧 Caractéristiques des Armures Méca

### Structure de Base
Chaque armure méca possède :
- **Grille de placement** : Espace pour placer les garnisons
- **Contraintes de taille** : Limites de construction
- **Zones spéciales** : Zones avec des effets particuliers
- **Points d'ancrage** : Emplacements pour les garnisons

### Types d'Armures Méca
Les différents plateaux d'Ark Nova deviennent différents types d'armures méca :
- **Armure Méca Standard** : Configuration de base
- **Armure Méca Avancée** : Configuration avec zones spéciales
- **Armure Méca Spécialisée** : Configuration optimisée pour certains types de garnisons
- *(Autres variantes selon les plateaux disponibles dans Ark Nova)*

## 🎮 Implications pour le Jeu

### Construction
- Le joueur **choisit** une armure méca au début de la partie
- L'armure méca détermine les **contraintes de placement** des garnisons
- Chaque armure méca a des **avantages spécifiques**

### Placement
- Les **garnisons** sont placées sur la **grille de l'armure méca**
- Les **contraintes** (taille, adjacence) s'appliquent selon la configuration
- Les **zones spéciales** de l'armure méca peuvent offrir des bonus

### Progression
- Les joueurs peuvent **débloquer** de nouvelles armures méca
- Chaque armure méca peut avoir des **niveaux d'amélioration**
- Les armures méca peuvent être **personnalisées** avec des modules

## 🔗 Intégration avec les Autres Systèmes

### Rangers
- Les **Rangers** utilisent l'armure méca comme base d'opérations
- Certains Rangers peuvent avoir des **affinités** avec certaines armures méca
- Les **actions des Rangers** se déroulent sur l'armure méca

### Garnisons
- Les **garnisons** sont construites sur l'armure méca
- Les **contraintes de placement** dépendent de la configuration de l'armure méca
- Les **troupes** sont placées dans les garnisons sur l'armure méca

### Actions Orange (Ranger Orange)
- Le **Ranger Orange** construit des **parties de l'armure méca**
- Les **actions orange** permettent de construire des **parties d'armure** et de créer des **slots pour armes**
- La **puissance du Ranger Orange** détermine le nombre de parties/slots créés
- Les **slots créés** peuvent ensuite être utilisés par le **Ranger Noir** pour installer des armes

### Actions Noires (Ranger Noir)
- Le **Ranger Noir** installe des **armes dans les slots** créés par le Ranger Orange
- Les **actions noires** permettent d'installer des **armes** dans les **slots disponibles**
- Les armes doivent correspondre à la **taille du slot** disponible

### Actions Bleues (Ranger Bleu)
- Le **Ranger Bleu** pose des **pièces d'armure spéciales** (anciennement bâtiments spéciaux)
- Les **actions bleues** permettent de placer des **pièces d'armure** avec des effets spéciaux
- Les pièces d'armure peuvent offrir des **bonus** ou des **effets permanents**

### Actions Vertes (Ranger Vert)
- Le **Ranger Vert** installe des **lasers** sur l'armure méca
- Les **actions vertes** permettent d'installer des **lasers** selon la puissance du Ranger
- **Chaque point vert (puissance) = 1 laser** installé

## 📊 Structure des Données

### Données à Créer
Pour chaque armure méca, nous devons définir :
- **Nom** : Nom de l'armure méca
- **Type** : Type d'armure méca (Standard, Avancée, etc.)
- **Grille** : Configuration de la grille (taille, forme)
- **Zones spéciales** : Emplacements avec effets particuliers
- **Contraintes** : Règles de placement spécifiques
- **Bonus** : Avantages de cette armure méca

### Format Suggéré
```json
{
  "armure_meca_id": 1,
  "nom": "Armure Méca Standard",
  "type": "Standard",
  "grille": {
    "largeur": 5,
    "hauteur": 5,
    "cases": [...]
  },
  "zones_speciales": [...],
  "contraintes": {...},
  "bonus": [...]
}
```

## 🚀 Prochaines Étapes

1. ✅ **Mapping conceptuel** : Plateau → Armure Méca (ce document)
2. ⏳ **Recherche** : Identifier tous les plateaux différents d'Ark Nova
3. ⏳ **Création des données** : Définir les caractéristiques de chaque armure méca
4. ⏳ **Intégration Neo4j** : Ajouter les armures méca à la base de données
5. ⏳ **Interface** : Implémenter la visualisation des armures méca

## 📝 Notes Importantes

1. **Chaque plateau différent** = **Une armure méca unique**
2. Les armures méca sont des **structures à construire** et non des cartes
3. Les **garnisons** sont placées **sur** l'armure méca
4. Les **Rangers** utilisent l'armure méca comme **base d'opérations**
5. Les armures méca peuvent avoir des **configurations différentes** selon le type

## 🎨 Thème Visuel

Les armures méca doivent avoir un style :
- **Mécanique** : Apparence robotique/cybernétique
- **Modulaire** : Structure composée de modules
- **Fonctionnel** : Design orienté vers la construction militaire
- **Personnalisable** : Possibilité d'ajouter des modules/améliorations

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


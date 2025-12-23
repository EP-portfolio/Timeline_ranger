# Mapping Final Complet - Ark Nova → New Ark Nova

Ce document contient le mapping complet et final de toutes les colonnes.

## 📋 Résumé des Mappings par Catégorie

### Rangers de Couleurs (Nouveau Système)
- `ACTION MECENE` → `RANGER BLEU`
- `ACTION ANIMAUX` → `RANGER NOIR`
- `ACTION CONSTRUCTION` → `RANGER ORANGE`
- `ACTION ASSOCIATION` → `RANGER VERT`
- `ACTION CARTES` → `RANGER JAUNE`

### Actions de Couleur (Cartes Jouables)
- `Cartes Mécène` → `Actions Bleues` (jouables par Ranger Bleu)
- `Cartes Animal` → `Actions Noires` (jouables par Ranger Noir)
- `Actions Construction` → `Actions Orange` (jouables par Ranger Orange)
- `Actions Association` → `Actions Vertes` (jouables par Ranger Vert)
- `Actions Cartes` → `Actions Jaunes` (jouables par Ranger Jaune)

### Types de Cartes
- `Animal` → `Troupe`
- `Mécène` → `Technologie` ✅ (Table `technologies` dans le schéma SQL)
- `Projet_de_conservation` → `Quête`
- `Décompte_final` → `Décompte_final` (conservé)

### Points et Scores (FINAL)
- `Points Attrait` → `Points de Dégâts`
- `Points Conservation` → `Nombre de Lasers`
- `Points Réputation` → `Points de Développement Technique`
- `Points Science` → `Nombre de Paires d'Ailes du Méca`
- `Points Attrait/Conservation/Réputation : Glossaire` → `Points de Dégâts/Nombre de Lasers/Points de Développement Technique : Glossaire`

### Capacités et Effets
- `Capacité` → `Bonus`
- `Effet unique immédiat (fond jaune)` → `Effet d'invocation (fond jaune)`
- `Effet unique immédiat : Glossaire` → `Effet d'invocation : Glossaire`
- `Effet permanent/récurrent (fond bleu)` → `Effet quotidien (fond bleu)`
- `Effet permanent/récurrent : Glossaire` → `Effet quotidien : Glossaire`
- `Effet (unique) de fin de partie [lors du décompte final] (fond marron)` → `Dernier souffle (fond marron)`
- `Effet (unique) de fin de partie [lors du décompte final] : Glossaire` → `Dernier souffle : Glossaire`
- `End Game Conservation Points (brown)` → `Dernier souffle`

### Ressources
- `Crédits` → `Or`
- `Revenus (fond violet)` → `Or par jour (fond violet)`
- `Revenus : Glossaire` → `Or par jour : Glossaire`

### Garnisons et Enclos
- `Enclos` → `Type Garnison`
- `Enclos standard (minimum)` → `Garnison standard (minimum)`
- `Enclos sans adjacence case` → `Garnison sans adjacence case`
- `Vivarium à reptiles` → `Usine à meca`
- `Grande volière` → `Jardin d'Eden`
- `Aquarium` → `Vaisseau du vide`
- `Parc animalier` → `Citadelle`

### Adjacences
- `Adjacent case Rocher` → `Adjacent case Lave`
- `Adjacent case Eau` → `Adjacent case Vide`
- `Adjacent case` → `Adjacent case` (conservé)

### Continents → Matières Premières (FINAL)
- `Afrique` → `Titanium` ✅
- `Amériques` → `Platine` ✅
- `Asie` → `Vibranium` ✅
- `Australie` → `Carbone` ✅
- `Europe` → `Kevlar` ✅

### Continents → Plans (ANCIEN - À vérifier si toujours utilisé)
- `Afrique` → `Tir`
- `Amériques` → `Tank`
- `Asie` → `Furtifs`
- `Australie` → `Soutien`
- `Europe` → `Corps à corps`

### Catégories d'Animaux → Types d'Armes/Munitions (FINAL - TOUS CONFIRMÉS)
- `Prédateur` → `Explosifs` ✅
- `Herbivore` → `Munitions Nucléaires` ✅
- `Animal domestique` → `Munitions Standard` ✅
- `Animal marin` → `Torpilles` ✅
- `Oiseau` → `Missiles Aériens` ✅
- `Ours` → `Armes Lourdes` ✅
- `Primate` → `Armes Intelligentes` ✅
- `Reptile` → `Armes Toxiques` ✅

### Catégories d'Animaux → Catégories de Troupes (ANCIEN - À vérifier si toujours utilisé)
- `Animal domestique` → `Péons`
- `Animal marin` → `Void`
- `Herbivore` → `Ent`
- `Oiseau` → `Ange`
- `Ours` → `Dragon`
- `Primate` → `Singe de l'espace`
- `Prédateur` → `Démons`
- `Reptile` → `Mecas`

### Décomptes Finaux
- `Nom Décompte final` → `Dernier souffle`
- `(Points de) Conservation` → `(Points de) Dégâts d'Armure`
- `Condition Points de Conservation` → `Condition Points de Dégâts d'Armure`
- `(Points de) Conservation (texte)` → `(Points de) Dégâts d'Armure (texte)`

### Quêtes
- `Récompense Condition Taille animal` → `Récompense Condition Taille troupe`

### Colonnes Conservées (structure, texte à adapter manuellement)
- `Condition(s) (icônes à gauche sur un bandeau rouge)`
- `Capacité solo ou mode limitant interactions (sur fond bleu clair)`
- `Niveau`
- `Icône(s) obtenue(s) (icônes en haut à droite)`
- `Icons Gained`
- `Instant Bonus (yellow)`
- `Continuing Bonus (blue/lavender)`
- `Type de condition (texte)`
- `Activity Required`
- `Prérequis (texte)`
- `Prérequis`
- `Prérequis Nb. icônes`
- `Prérequis Icônes`
- `Récompense(s)`
- `Récompense …`
- `Bonus (en bas à droite) gagné par le joueur posant la carte`
- `Autre Bonus Joueur`
- `Scoring Card Name`
- `Autres conditions`
- `Glossaire`

### Plateaux de Jeu → Armures Méca
- `Plateau Personnel` → `Armure Méca`
- `Grille du plateau` → `Grille de l'armure méca`
- `Tuiles d'enclos` → `Tuiles de garnison`
- `Configuration du plateau` → `Configuration de l'armure méca`
- `Différents plateaux` → `Différentes armures méca`

### Métadonnées Conservées
- `Vague`
- `Jeu de base`
- `Promo`
- `Jeu avec extension Mondes Marins` → `Jeu avec extension Plans`
- `Remplacée par extension Mondes Marins` → `Remplacée par extension Plans`

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


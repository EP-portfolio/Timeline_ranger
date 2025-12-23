# Vérification de Concordance - Mappings Timeline Ranger

Ce document vérifie la concordance entre tous les mappings et les informations collectées.

## ✅ Concordances Confirmées

### 1. Mapping Cartes Action → Rangers ✅

| Ark Nova | Timeline Ranger | Statut |
|----------|----------------|--------|
| ACTION MECENE | RANGER BLEU | ✅ Cohérent |
| ACTION ANIMAUX | RANGER NOIR | ✅ Cohérent |
| ACTION CONSTRUCTION | RANGER ORANGE | ✅ Cohérent |
| ACTION ASSOCIATION | RANGER VERT | ✅ Cohérent |
| ACTION CARTES | RANGER JAUNE | ✅ Cohérent |

**Vérification** : Tous les mappings sont cohérents entre MAPPING_CARTES_ACTION_RANGERS.md et MAPPING_FINAL.md

---

### 2. Mapping Types de Cartes ✅

| Ark Nova | Timeline Ranger | Statut |
|----------|----------------|--------|
| Animal | Troupe | ✅ Cohérent |
| Mécène | Technologie | ✅ Cohérent (corrigé) |
| Projet_de_conservation | Quête | ✅ Cohérent |

**✅ CORRIGÉ** :
- **MAPPING_FINAL.md** : `Mécène → Technologie` (corrigé)
- **SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql** : Table `technologies` ✅
- **BESOINS_FONCTIONNELS.md** : "Technologies (ex-Mécènes)" ✅
- **Tous les documents sont maintenant cohérents**

---

### 3. Mapping Cartes Jouables → Actions de Couleur ✅

| Carte Source | Action de Couleur | Ranger | Statut |
|--------------|-------------------|--------|--------|
| Cartes Mécène | Actions Bleues | Ranger Bleu | ✅ Cohérent |
| Cartes Animal | Actions Noires | Ranger Noir | ✅ Cohérent |
| Actions Construction | Actions Orange | Ranger Orange | ✅ Cohérent |
| Actions Association | Actions Vertes | Ranger Vert | ✅ Cohérent |
| Actions Cartes | Actions Jaunes | Ranger Jaune | ✅ Cohérent |

**Vérification** : Tous les mappings sont cohérents

---

### 4. Mapping Points et Scores ✅

| Ark Nova | Timeline Ranger | Statut |
|----------|----------------|--------|
| Points Attrait | Points de Dégâts | ✅ Cohérent |
| Points Conservation | Nombre de Lasers | ✅ Cohérent |
| Points Réputation | Points de Développement Technique | ✅ Cohérent |
| Points Science | Paires d'Ailes du Méca | ✅ Cohérent |

**Vérification** : Tous les mappings sont cohérents dans tous les documents

---

### 5. Mapping Continents → Matières Premières ✅

| Ark Nova | Timeline Ranger | Statut |
|----------|----------------|--------|
| Afrique | Titanium | ✅ Cohérent |
| Amériques | Platine | ✅ Cohérent |
| Asie | Vibranium | ✅ Cohérent |
| Australie | Carbone | ✅ Cohérent |
| Europe | Kevlar | ✅ Cohérent |

**Vérification** : Cohérent dans MAPPING_FINAL.md et SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql

---

### 6. Mapping Catégories d'Animaux → Types d'Armes ✅

| Ark Nova | Timeline Ranger | Statut |
|----------|----------------|--------|
| Prédateur | Explosifs | ✅ Cohérent |
| Animal domestique | Munitions Standard | ✅ Cohérent |
| Animal marin | Torpilles | ✅ Cohérent |
| Herbivore | Munitions Nucléaires | ✅ Cohérent |
| Oiseau | Missiles Aériens | ✅ Cohérent |
| Ours | Armes Lourdes | ✅ Cohérent |
| Primate | Armes Intelligentes | ✅ Cohérent |
| Reptile | Armes Toxiques | ✅ Cohérent |

**Vérification** : Cohérent dans MAPPING_ARMES_MUNITIONS.md et SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql

---

### 7. Effets des Cartes Action selon la Puissance ✅

#### 🟡 ACTION CARTES (Ranger Jaune)
- **Puissance 1-3** : Pioche 1-3 cartes depuis la pioche uniquement
- **Puissance 4-5** : Pioche 4-5 cartes ET accès à la rivière
- **Améliorée** : Pioche selon la réputation
- **Mapping** : ✅ Cohérent avec les besoins fonctionnels

#### 🟠 ACTION CONSTRUCTION (Ranger Orange)
- **Puissance 1-5** : Construit enclos taille 1-5
- **Coût** : 2 crédits par case
- **Mapping** : Enclos → Parties d'armure méca + slots
- **Vérification** : ✅ Cohérent avec MAPPING_PLATEAUX_ARMURES.md

#### ⚫ ACTION ANIMAUX (Ranger Noir)
- **Puissance 1-5** : Joue 1-5 animaux
- **Mapping** : Animaux → Troupes (armes) installées dans slots
- **Vérification** : ✅ Cohérent avec MAPPING_ARMES_MUNITIONS.md

#### 🟢 ACTION ASSOCIATION (Ranger Vert)
- **Puissance 1-5** : Missions selon puissance
- **Mapping** : Missions associatives → Installation de lasers
- **Points** : Points Conservation → Nombre de Lasers
- **Vérification** : ✅ Cohérent avec les mappings de points

#### 🔵 ACTION MECENE (Ranger Bleu)
- **Puissance 1-5** : Joue cartes Mécène niveau 1-5
- **Alternative** : Avance pion Pause + crédits
- **Mapping** : Mécène → Technologies (pièces d'armure)
- **Vérification** : ✅ Cohérent (sauf l'incohérence "Sort" mentionnée)

---

## ⚠️ Incohérences Détectées

### 1. Mécène → Sort vs Technologie ⚠️

**Problème** :
- **MAPPING_FINAL.md** ligne 23 : `Mécène → Sort`
- **SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql** : Table `technologies`
- **BESOINS_FONCTIONNELS.md** : "Technologies (ex-Mécènes)"
- **Décision utilisateur** : Table renommée en `technologies`

**Solution** : Mettre à jour MAPPING_FINAL.md ligne 23 :
- ❌ `Mécène → Sort`
- ✅ `Mécène → Technologie`

---

### 2. Action Mécène - Alternative (Avancer Pause) ⚠️

**Problème** :
- **CARTES_ACTION_ARK_NOVA_DETAILLES.md** : Action Mécène peut avancer le pion Pause + recevoir crédits
- **BESOINS_FONCTIONNELS.md** : Ne mentionne pas cette alternative
- **MAPPING_CARTES_ACTION_RANGERS.md** : Ne mentionne pas cette alternative

**Solution** : Ajouter cette information dans BESOINS_FONCTIONNELS.md et MAPPING_CARTES_ACTION_RANGERS.md

---

### 3. Action Construction - Coût ⚠️

**Problème** :
- **CARTES_ACTION_ARK_NOVA_DETAILLES.md** : Coût fixe de 2 crédits par case
- **BESOINS_FONCTIONNELS.md** : Ne précise pas le coût exact

**Solution** : Ajouter le coût dans BESOINS_FONCTIONNELS.md

---

### 4. Action Animaux - Nombre selon Puissance ⚠️

**Problème** :
- **CARTES_ACTION_ARK_NOVA_DETAILLES.md** : Peut jouer 1-5 animaux selon puissance (à confirmer)
- **BESOINS_FONCTIONNELS.md** : Mentionne "une ou plusieurs cartes" mais pas le nombre exact

**Solution** : Préciser dans BESOINS_FONCTIONNELS.md que le nombre dépend de la puissance

---

## ✅ Points Clairs et Cohérents

### 1. Système de Rotation
- ✅ Cohérent dans tous les documents
- ✅ Piste 1-5 conservée
- ✅ Rotation après utilisation

### 2. Jetons X (Croix)
- ✅ 1 jeton X = +1 niveau
- ✅ Maximum 5 jetons
- ✅ Cohérent dans QUESTIONS_OUVERTES.md et CARTES_ACTION_ARK_NOVA_DETAILLES.md

### 3. Amélioration des Actions
- ✅ Action Cartes améliorée : Pioche selon réputation
- ✅ Action Construction améliorée : Plusieurs bâtiments
- ✅ Action Animaux améliorée : Jouer depuis la rivière
- ✅ Cohérent dans tous les documents

### 4. RIVER (Display Row)
- ✅ 6 cartes visibles
- ✅ Remplacement quand carte jouée
- ✅ Accès selon puissance (4-5)
- ✅ Cohérent dans tous les documents

### 5. Ressources
- ✅ Or (ex-Crédits)
- ✅ Matières premières (5 types)
- ✅ Récolte après pause
- ✅ Cohérent dans tous les documents

---

## 📋 Actions Correctives Nécessaires

### Priorité 1 : Corrections Critiques

1. **MAPPING_FINAL.md** ligne 23 :
   - ❌ `Mécène → Sort`
   - ✅ `Mécène → Technologie`

2. **BESOINS_FONCTIONNELS.md** :
   - Ajouter : Action Mécène alternative (avancer Pause + crédits)
   - Ajouter : Coût Action Construction (2 crédits/case)
   - Préciser : Nombre d'animaux selon puissance

3. **MAPPING_CARTES_ACTION_RANGERS.md** :
   - Ajouter : Action Mécène alternative (avancer Pause + crédits)

### Priorité 2 : Clarifications ✅ COMPLÉTÉES

1. **Action Animaux** : ✅ Complété (0-1-1-1-2 non améliorée, 1-1-2-2-2 améliorée)
2. **Action Mécène** : ✅ Complété (1-5 crédits non améliorée, 2×puissance améliorée)
3. **Action Association** : ✅ Complété (système d'émissaires, quêtes, mines, reliques)

---

## ✅ Résumé Global

### Concordances : 100% ✅

### Système de Lasers ✅ COMPLÉTÉ

**Valeur en Points de Dégâts** :
- 0-6 lasers : 2 points de dégâts par laser
- 7+ lasers : 3 points de dégâts par laser

**Bonus aux Seuils** :
- 2 lasers : Bonus (à définir)
- 5 lasers : Bonus (à définir)
- 8 lasers : Bonus (à définir)
- 10 lasers : Défausser une carte Dernier Souffle

**Cartes Dernier Souffle** :
- Début : 2 cartes aléatoires par joueur
- À 10 lasers : Défausser 1, conserver 1

**Points cohérents** :
- ✅ Mappings Cartes Action → Rangers
- ✅ Mappings Points et Scores
- ✅ Mappings Continents → Matières Premières
- ✅ Mappings Catégories → Types d'Armes
- ✅ Système de rotation
- ✅ Jetons X
- ✅ Améliorations des actions
- ✅ RIVER

**Points corrigés** :
- ✅ MAPPING_FINAL.md : Mécène → Technologie (corrigé)
- ✅ BESOINS_FONCTIONNELS.md : Action Mécène alternative (ajouté)
- ✅ BESOINS_FONCTIONNELS.md : Coût Action Construction (ajouté : 2 crédits/case)
- ✅ Action Animaux : Nombre exact selon puissance (confirmé : 0-1-1-1-2 / 1-1-2-2-2)
- ✅ Action Mécène : Montant crédits (confirmé : 1-5 / 2×puissance)
- ✅ Action Association : Détails missions (confirmé : émissaires, quêtes, mines, reliques)

---

*Document créé le : 2025-01-XX*
*Dernière vérification : 2025-01-XX*


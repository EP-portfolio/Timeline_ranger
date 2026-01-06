# Déroulé Complet d'une Partie - Timeline Ranger

## 🎮 Vue d'Ensemble

Timeline Ranger est un jeu de stratégie multijoueur où chaque joueur construit et équipe une **armure méca** (ex-plateau de jeu) avec des armes, des pièces d'armure et des lasers. Le jeu se joue en tours alternés, chaque joueur utilisant ses **5 Rangers** (cartes Action) pour effectuer des actions.

---

## 📋 Phase 1 : Initialisation de la Partie

### 1.1 Création et Rejoindre une Partie
- Un joueur crée une partie (hôte)
- D'autres joueurs rejoignent avec un code
- Chaque joueur choisit une **armure méca** (plateau de jeu)

### 1.2 Démarrage de la Partie
- L'hôte démarre la partie
- **Ordre de jeu initial** : Déterminé aléatoirement

### 1.3 Distribution Initiale

**Pour chaque joueur :**

#### 🎴 Les 5 Rangers (Cartes Action)
- **Ranger Noir** (Animaux) : Toujours en **position 1**
- **4 autres Rangers** : Mélangés aléatoirement en positions 2-5
  - 🔵 **Ranger Bleu** (Mécène)
  - 🟠 **Ranger Orange** (Construction)
  - 🟢 **Ranger Vert** (Association)
  - 🟡 **Ranger Jaune** (Cartes)

**Important** : La **position** (1-5) détermine la **puissance** de l'action.

#### 📦 Cartes Initiales
- Chaque joueur reçoit **8 cartes** de départ
- Types de cartes :
  - **Troupes** (ex-Animaux) : Armes à installer dans les garnisons
  - **Technologies** (ex-Mécènes) : Pièces d'armure ou actions spéciales
  - **Quêtes** (ex-Projets de Conservation) : Objectifs à réaliser

#### 💰 Ressources Initiales
- **Or** : 25 pièces d'or (PO)
- **Matières premières** : 0 (Titanium, Platine, Vibranium, Carbone, Kevlar)
- **Émissaires** : 1 disponible
- **Jetons X** : 0

#### 🎯 Scores Initiaux
- **Points de dégâts** : 0
- **Lasers** : 0
- **Réputation** : 0 (Points de développement technique)
- **Paires d'ailes** : 0

#### 🗺️ Plateau de Jeu
- **Grille hexagonale** : 9 colonnes verticales (6-7 hexagones par colonne)
- **Terrains** : Terre craquelée (constructible), Rochers et Eau (inconstructibles)
- **Garnisons** : Aucune (à construire)
- **Armes** : Aucune (à installer)
- **Lasers** : Aucun (à installer)

### 1.4 Sélection de la Main Initiale
- Chaque joueur doit **sélectionner 4 cartes** parmi les 8 reçues
- Les 4 cartes non sélectionnées sont défaussées
- Une fois la sélection confirmée, la partie commence

---

## 🔄 Phase 2 : Déroulement d'un Tour

### 2.1 Structure d'un Tour

Un tour se déroule ainsi :

1. **C'est votre tour** : Le joueur actif peut effectuer une action
2. **Choisir un Ranger** : Sélectionner un Ranger selon sa position (1-5)
3. **Jouer l'action** : Effectuer l'action correspondante à la couleur du Ranger
4. **Rotation des Rangers** : Le Ranger joué revient en position 1, les autres avancent
5. **Passage au joueur suivant** : Le tour passe au prochain joueur dans l'ordre

### 2.2 Système de Rotation des Rangers

**Mécanique fondamentale** :

```
État initial :
Position 1 : Ranger Noir (puissance 1)
Position 2 : Ranger Bleu (puissance 2)
Position 3 : Ranger Orange (puissance 3)
Position 4 : Ranger Vert (puissance 4)
Position 5 : Ranger Jaune (puissance 5)
```

**Exemple : Jouer le Ranger Orange (position 3)**

```
Avant :
1. Noir (1)
2. Bleu (2)
3. Orange (3) ← Joué
4. Vert (4)
5. Jaune (5)

Après rotation :
1. Orange (1) ← Revient en position 1
2. Noir (2) ← Avance de 1
3. Bleu (3) ← Avance de 1
4. Vert (4) ← Reste (position > 3)
5. Jaune (5) ← Reste (position > 3)
```

**Règle importante** :
- Le Ranger joué **revient toujours en position 1**
- Les Rangers **avant** la position jouée **avancent d'une position**
- Les Rangers **après** la position jouée **restent à leur position**

---

## 🎴 Les 5 Actions de Couleur (Rangers)

### ⚫ ACTION ANIMAUX (Ranger Noir)

**Fonction** : Installer des **Troupes** (armes) dans les **garnisons** construites.

#### 📊 Puissance et Effets

**Ranger Non Amélioré** :
| Puissance | Nombre de Troupes | Bonus                  |
| --------- | ----------------- | ---------------------- |
| 1         | 0 (peut passer)   | -                      |
| 2         | 1 troupe          | -                      |
| 3         | 1 troupe          | -                      |
| 4         | 1 troupe          | -                      |
| 5         | 2 troupes         | +1 point de réputation |

**Ranger Amélioré** :
| Puissance | Nombre de Troupes | Bonus                  |
| --------- | ----------------- | ---------------------- |
| 1         | 1 troupe          | -                      |
| 2         | 1 troupe          | -                      |
| 3         | 2 troupes         | -                      |
| 4         | 2 troupes         | -                      |
| 5         | 2 troupes         | +1 point de réputation |

**Bonus amélioration** : Peut jouer des troupes directement depuis la rivière (cartes disponibles)

#### 🎯 Déroulé de l'Action

1. **Sélectionner une carte Troupe** dans votre main
2. **Vérifier les prérequis** :
   - Avoir une **garnison** (construction) de **taille ≥ taille de la troupe**
   - La garnison doit être **inoccupée** (pas d'arme déjà installée)
3. **Placer la troupe** dans la garnison
4. **Effets de la troupe** :
   - Ajoute des **points de dégâts** au score
   - Peut ajouter des **lasers**
   - Peut ajouter de la **réputation**
   - Peut ajouter des **paires d'ailes**
   - Peut avoir des **effets spéciaux** (bonus, effets quotidiens, etc.)

#### 💡 Exemple Concret

- Vous avez une garnison de taille 3 (3 hexagones)
- Vous jouez le Ranger Noir en position 4 (puissance 4)
- Vous sélectionnez "Explosifs - Canon Alpha" (taille 2)
- La troupe est installée dans la garnison
- Vous gagnez : 2 points de dégâts, 1 laser
- La garnison est maintenant occupée

---

### 🔵 ACTION MÉCÈNE (Ranger Bleu)

**Fonction** : Jouer des **Technologies** (pièces d'armure) OU gagner des **crédits** (or).

#### 📊 Puissance et Effets

**Ranger Non Amélioré** :
| Puissance | Option 1 (Carte)     | Option 2 (Crédits) |
| --------- | -------------------- | ------------------ |
| 1         | 1 carte niveau 1 max | 1 crédit           |
| 2         | 1 carte niveau 2 max | 2 crédits          |
| 3         | 1 carte niveau 3 max | 3 crédits          |
| 4         | 1 carte niveau 4 max | 4 crédits          |
| 5         | 1 carte niveau 5 max | 5 crédits          |

**Ranger Amélioré** :
| Puissance | Option 1 (Cartes)                   | Option 2 (Crédits) |
| --------- | ----------------------------------- | ------------------ |
| 1         | Plusieurs cartes (total niveau ≤ 2) | 2 crédits          |
| 2         | Plusieurs cartes (total niveau ≤ 3) | 4 crédits          |
| 3         | Plusieurs cartes (total niveau ≤ 4) | 6 crédits          |
| 4         | Plusieurs cartes (total niveau ≤ 5) | 8 crédits          |
| 5         | Plusieurs cartes (total niveau ≤ 6) | 10 crédits         |

**Exemple amélioré puissance 3** :
- Peut jouer : carte niveau 1 + niveau 2, OU carte niveau 3, OU carte niveau 2 + niveau 2, etc. (total ≤ 4)

#### 🎯 Déroulé de l'Action

**Option 1 : Jouer une carte Technologie**
1. **Sélectionner une carte Technologie** dans votre main
2. **Vérifier le niveau** : Le niveau de la carte doit être ≤ puissance du Ranger
3. **Payer le coût** : Coût en or (peut être réduit par les mines)
4. **Placer la technologie** :
   - Si **pièce d'armure** (`is_armor_piece = true`) : Placer sur le plateau
   - Si **action** (`is_armor_piece = false`) : Activer l'effet immédiatement
5. **Effets** :
   - Points de dégâts
   - Lasers
   - Réputation
   - Or par jour (revenus récurrents)
   - Effets spéciaux

**Option 2 : Gagner des crédits**
1. **Ne pas sélectionner de carte**
2. **Gagner des crédits** : Montant = puissance (non amélioré) ou 2×puissance (amélioré)
3. **Ajouter à l'or** disponible

#### 💡 Exemple Concret

- Vous jouez le Ranger Bleu en position 3 (puissance 3)
- **Option 1** : Vous jouez "Système - Laser" (niveau 2) → Coût 5 or → Gagnez 1 laser
- **Option 2** : Vous choisissez de gagner 3 crédits → Votre or passe de 20 à 23

---

### 🟠 ACTION CONSTRUCTION (Ranger Orange)

**Fonction** : Construire des **garnisons** (parties d'armure) sur la grille hexagonale.

#### 📊 Puissance et Effets

**Toutes Puissances (Amélioré ou Non)** :
| Puissance | Taille maximale tuile | Coût           |
| --------- | --------------------- | -------------- |
| 1         | Taille 1              | 2 crédits/case |
| 2         | Taille 2              | 2 crédits/case |
| 3         | Taille 3              | 2 crédits/case |
| 4         | Taille 4              | 2 crédits/case |
| 5         | Taille 5              | 2 crédits/case |

**Différence Amélioration** :
- **Non amélioré** : **1 seule tuile** par tour
- **Amélioré** : **Plusieurs tuiles** possibles (total taille ≤ puissance, pas de doublons de taille)

#### 🎯 Déroulé de l'Action

**Étape 1 : Jouer l'action Construction**
- Le Ranger Orange est joué (ex: position 4 = puissance 4)
- Les **tuiles disponibles** sont chargées (taille ≤ 4)

**Étape 2 : Sélectionner une tuile**
- Choisir parmi les tuiles disponibles :
  - **Taille 1** : Tuile Simple (1 hexagone, coût 2 PO)
  - **Taille 2** : Tuile Ligne 2 (2 hexagones, coût 4 PO)
  - **Taille 3** : Tuile Ligne 3 ou Tuile L (3 hexagones, coût 6 PO)
  - **Taille 4** : Tuile Ligne 4, Carré, ou T (4 hexagones, coût 8 PO)
  - **Taille 5** : Tuile Ligne 5 ou Croix (5 hexagones, coût 10 PO)

**Étape 3 : Rotation de la tuile**
- Faire pivoter la tuile (multiples de 60°)
- Chaque rotation = ±60°

**Étape 4 : Placement sur la grille**
- Cliquer sur un hexagone de la grille pour définir l'**ancrage** (position de référence)
- La tuile est placée avec tous ses hexagones
- **Validations** :
  - Tous les hexagones doivent être dans la grille
  - Tous les hexagones doivent être **constructibles** (pas de rocher/eau)
  - Aucun hexagone ne doit être déjà occupé par une garnison

**Étape 5 : Paiement**
- Débiter le coût en or (2 PO par case)

**Étape 6 : Finalisation**
- **Ranger non amélioré** : Le tour se termine automatiquement
- **Ranger amélioré** : Vous pouvez continuer à construire d'autres tuiles (jusqu'à épuisement du total)

#### 💡 Exemple Concret

- Vous jouez le Ranger Orange en position 4 (puissance 4)
- Vous sélectionnez une **Tuile Carré** (taille 4, coût 8 PO)
- Vous la faites pivoter de 60°
- Vous la placez sur la grille à la position (3, 2)
- Vous payez 8 PO
- La garnison est créée (4 hexagones)
- **Si amélioré** : Vous pouvez construire une autre tuile (ex: taille 1) dans le même tour

---

### 🟢 ACTION ASSOCIATION (Ranger Vert)

**Fonction** : Réaliser des **Quêtes** et obtenir des **mines** et **reliques**.

#### 📊 Puissance et Effets

**Ranger Non Amélioré** :
| Puissance | Quête                | Autres Effets                              |
| --------- | -------------------- | ------------------------------------------ |
| 1         | 1 quête niveau 1 max | -                                          |
| 2         | 1 quête niveau 2 max | +2 points de réputation                    |
| 3         | 1 quête niveau 3 max | Récupère une mine                          |
| 4         | 1 quête niveau 4 max | Récupère une relique                       |
| 5         | 1 quête niveau 5 max | Peut réaliser quête si conditions remplies |

**Ranger Amélioré** :
| Puissance | Quêtes                               | Autres Effets                                     |
| --------- | ------------------------------------ | ------------------------------------------------- |
| 0         | -                                    | Peut payer or pour obtenir 1 laser supplémentaire |
| 2         | Une ou plusieurs quêtes niveau 2 max | +2 points de réputation                           |
| 3         | Une ou plusieurs quêtes niveau 3 max | Récupère une mine                                 |
| 4         | Une ou plusieurs quêtes niveau 4 max | Récupère une relique                              |
| 5         | Une ou plusieurs quêtes niveau 5 max | Peut réaliser quête si conditions remplies        |

#### 🎯 Déroulé de l'Action

**Étape 1 : Sélectionner une Quête**
- Choisir une carte Quête dans votre main
- Vérifier le **niveau de la quête** ≤ puissance du Ranger

**Étape 2 : Vérifier les Conditions**
- Chaque quête a des **conditions** à remplir :
  - **Quête Maîtrise** : Ex: "Avoir 3 types d'armes différents"
  - **Quête Forteresse** : Ex: "Avoir 5 garnisons construites"
  - **Quête Environnement** : Ex: "Avoir 10 lasers installés"
  - **Quête Programme** : Ex: "Avoir 3 quêtes réalisées"

**Étape 3 : Utiliser des Émissaires**
- Certaines quêtes nécessitent des **émissaires**
- Chaque joueur commence avec **1 émissaire**
- Maximum **4 émissaires** (peut être augmenté via bonus)

**Étape 4 : Réaliser la Quête**
- Si les conditions sont remplies, la quête est réalisée
- **Récompenses** :
  - Points de réputation
  - Points de dégâts
  - Lasers
  - Autres bonus

**Étape 5 : Effets Spéciaux selon Puissance**
- **Puissance 2** : +2 points de réputation
- **Puissance 3** : Récupère une **mine** (choisir le matériau)
- **Puissance 4** : Récupère une **relique** (bonus spécial)
- **Puissance 5** : Peut réaliser quête même si conditions partiellement remplies

#### 🏭 Système des Mines

**Obtention** :
- Via Action Association puissance 3
- Choisir le matériau : Titanium, Platine, Vibranium, Carbone, Kevlar

**Effet** :
- Réduit de **3 PO** le coût des pièces d'armure composées de ce matériau
- **Permanent** pour toute la partie

**Limite** :
- **Standard** : Maximum **2 mines**
- **Avec amélioration** : Maximum **3-4 mines** (si Ranger Vert amélioré)

**Exemple** :
- Vous avez une mine de **Vibranium**
- Une pièce d'armure coûte normalement **10 PO** et nécessite du Vibranium
- Avec la mine : Coût réduit à **7 PO** (10 - 3)

#### 💡 Exemple Concret

- Vous jouez le Ranger Vert en position 3 (puissance 3)
- Vous sélectionnez "Quête - Diversité d'Armes" (niveau 2)
- Conditions : Avoir 3 types d'armes différents installés
- Vous avez : Explosifs, Munitions Standard, Torpilles → ✅ Conditions remplies
- Vous réalisez la quête → Gagnez 5 points de réputation
- **Bonus puissance 3** : Vous récupérez une mine → Vous choisissez **Vibranium**

---

### 🟡 ACTION CARTES (Ranger Jaune)

**Fonction** : **Piocher des cartes** depuis la pioche ou la rivière.

#### 📊 Puissance et Effets

**Ranger Non Amélioré** :
| Puissance | Cartes piochées | Accès Rivière |
| --------- | --------------- | ------------- |
| 1         | 1 carte         | Non           |
| 2         | 2 cartes        | Non           |
| 3         | 3 cartes        | Non           |
| 4         | 4 cartes        | Oui           |
| 5         | 5 cartes        | Oui           |

**Ranger Amélioré** :
- Pioche selon la **réputation** du joueur (au lieu de la puissance)
- Accès rivière selon réputation

#### 🎯 Déroulé de l'Action

**Étape 1 : Déterminer le nombre de cartes**
- **Non amélioré** : Nombre = puissance (1-5)
- **Amélioré** : Nombre = réputation (peut être > 5)

**Étape 2 : Choisir la source**
- **Puissance 1-3** (non amélioré) : Pioche uniquement
- **Puissance 4-5** (non amélioré) : Pioche OU Rivière
- **Amélioré** : Selon réputation

**Étape 3 : Piocher les cartes**
- Les cartes sont ajoutées à votre main
- Limite de main : Pas de limite (ou à définir)

#### 💡 Exemple Concret

- Vous jouez le Ranger Jaune en position 4 (puissance 4)
- Vous piochez **4 cartes** depuis la pioche
- OU vous prenez **1 carte** depuis la rivière (cartes visibles)
- Les cartes sont ajoutées à votre main

---

## 🔄 Système de Rotation et Puissance

### Principe Fondamental

**La position = La puissance** :
- Position 1 = Puissance 1 (faible)
- Position 5 = Puissance 5 (forte)

**Stratégie** :
- Utiliser un Ranger en position 5 donne une action **puissante** mais le fait revenir en position 1
- Utiliser un Ranger en position 1 donne une action **faible** mais permet de le faire monter rapidement

### Exemple de Cycle

```
Tour 1 : Jouer Ranger Orange (position 4) → Construire tuile taille 4
         → Orange revient en position 1

Tour 2 : Jouer Ranger Bleu (position 2) → Gagner 2 crédits
         → Bleu revient en position 1, Orange monte en position 2

Tour 3 : Jouer Ranger Orange (position 2) → Construire tuile taille 2
         → Orange revient en position 1, Bleu monte en position 2

Tour 4 : Jouer Ranger Orange (position 1) → Construire tuile taille 1
         → Orange reste en position 1, mais les autres Rangers montent
```

---

## 🎁 Système d'Amélioration des Rangers

### Obtention de l'Amélioration

**Bonus à 2 Lasers** :
- Quand un joueur atteint **2 lasers**, il reçoit un **bonus**
- **Choix** :
  - **Option 1** : Améliorer une carte Action (Ranger)
  - **Option 2** : Obtenir un nouvel émissaire

### Effets des Améliorations

#### ⚫ Ranger Noir Amélioré
- Peut jouer plus de troupes (1-1-2-2-2 au lieu de 0-1-1-1-2)
- Peut jouer depuis la **rivière** (cartes visibles)

#### 🔵 Ranger Bleu Amélioré
- Peut jouer **plusieurs cartes** (total niveau ≤ puissance+1)
- Peut gagner **2×puissance crédits** (au lieu de puissance)

#### 🟠 Ranger Orange Amélioré
- Peut construire **plusieurs tuiles** en un tour
- Contrainte : Total taille ≤ puissance, pas de doublons de taille

#### 🟢 Ranger Vert Amélioré
- Peut réaliser **plusieurs quêtes** en un tour
- Niveau 0 : Peut payer or pour obtenir 1 laser

#### 🟡 Ranger Jaune Amélioré
- Pioche selon la **réputation** (au lieu de la puissance)
- Peut piocher beaucoup plus de cartes si réputation élevée

---

## 🏭 Système des Mines

### Obtention
- Via **Action Association puissance 3**
- Choisir le matériau : Titanium, Platine, Vibranium, Carbone, Kevlar

### Effet
- Réduit de **3 PO** le coût des pièces d'armure de ce matériau
- **Permanent** pour toute la partie

### Limite
- **Standard** : Maximum **2 mines**
- **Avec amélioration Ranger Vert** : Maximum **3-4 mines**

### Exemple
- Mine de Vibranium → Toutes les pièces d'armure en Vibranium coûtent 3 PO de moins

---

## ⚡ Système des Lasers

### Obtention
- Via cartes **Troupes** (nombre_lasers)
- Via cartes **Technologies** (nombre_lasers)
- Via **Action Association améliorée niveau 0** (payer or)

### Calcul des Points de Dégâts
- **≤ 6 lasers** : 2 points de dégâts par laser
- **> 6 lasers** : 3 points de dégâts par laser

**Exemple** :
- 5 lasers → 5 × 2 = **10 points de dégâts**
- 8 lasers → 8 × 3 = **24 points de dégâts**

### Bonus aux Seuils

**2 Lasers** :
- Choisir : Améliorer un Ranger OU obtenir un émissaire

**5 Lasers** :
- Bonus à définir

**8 Lasers** :
- Bonus à définir

**10 Lasers** (Événement Global) :
- **Le premier joueur** à atteindre 10 lasers déclenche l'événement
- **TOUS les joueurs** doivent défausser une des deux cartes "Dernier Souffle"
- Chaque joueur choisit laquelle conserver

---

## 🎯 Système de Scores

### Points de Dégâts
- **Sources** :
  - Cartes Troupes installées (points_degats)
  - Cartes Technologies installées (points_degats)
  - **Lasers** : 2× (si ≤6) ou 3× (si >6)
  - Cartes sur le plateau avec bonus dégâts

### Réputation (Points de Développement Technique)
- **Sources** :
  - Cartes Troupes (points_developpement_technique)
  - Cartes Technologies (points_developpement_technique)
  - Action Association puissance 2 (+2)
  - Réalisation de quêtes

### Paires d'Ailes
- **Sources** :
  - Cartes Troupes (paires_ailes)
  - Cartes Technologies (paires_ailes)

### Score Final
- **Total** = Points de dégâts + Bonus finaux + Cartes Dernier Souffle

---

## 🔄 Déroulé Type d'une Partie

### Tour 1-5 : Développement Initial
- Construire des **garnisons** (Ranger Orange)
- Installer des **troupes** (Ranger Noir)
- Jouer des **technologies** (Ranger Bleu)
- Gagner de l'**or** (Ranger Bleu option crédits)
- Piocher des **cartes** (Ranger Jaune)

### Tour 6-15 : Expansion
- Construire plus de garnisons
- Installer plus de troupes
- Atteindre **2 lasers** → Améliorer un Ranger
- Réaliser des **quêtes** (Ranger Vert)
- Obtenir des **mines** (Ranger Vert puissance 3)

### Tour 16-25 : Optimisation
- Maximiser les points de dégâts
- Installer des lasers supplémentaires
- Réaliser des quêtes complexes
- Optimiser la rotation des Rangers

### Fin de Partie
- Un joueur atteint **10 lasers** → Événement Dernier Souffle
- Tous les joueurs défaussent une carte Dernier Souffle
- **Décompte final** :
  - Points de dégâts totaux
  - Bonus des cartes Dernier Souffle
  - Autres bonus finaux
- Le joueur avec le **score le plus élevé** gagne

---

## 🎮 Actions Spéciales

### Passer son Tour
- Si vous ne voulez pas jouer d'action
- Vous obtenez un **jeton X** (si passé au niveau 1)
- Les jetons X permettent d'augmenter la puissance d'une action de +1

### Utiliser un Jeton X
- Lors de l'utilisation d'un Ranger, vous pouvez utiliser un jeton X
- La puissance effective devient : **position + 1**
- Exemple : Ranger en position 2 + jeton X = puissance 3

---

## 📊 Stratégies de Jeu

### Stratégie Rapide
- Utiliser les Rangers en position 5 pour des actions puissantes
- Construire rapidement des garnisons
- Installer des troupes rapidement

### Stratégie Longue
- Faire monter les Rangers progressivement
- Accumuler des ressources
- Réaliser des quêtes complexes
- Optimiser les mines

### Stratégie Laser
- Maximiser les lasers rapidement
- Atteindre 10 lasers en premier
- Contrôler l'événement Dernier Souffle

---

## 🎯 Points Clés à Retenir

1. **La position = la puissance** : Plus un Ranger est en position haute, plus son action est puissante
2. **Rotation stratégique** : Jouer un Ranger le fait revenir en position 1, planifiez vos actions
3. **Amélioration** : Atteindre 2 lasers permet d'améliorer un Ranger (choix stratégique)
4. **Mines** : Réduisent les coûts des pièces d'armure (maximum 2, 3-4 si amélioré)
5. **Lasers** : Contribuent massivement aux points de dégâts (2× ou 3× selon nombre)
6. **Quêtes** : Nécessitent des émissaires et offrent de gros bonus
7. **Construction** : Nécessaire pour installer des troupes (garnisons = slots d'armes)

---

*Document créé le : 2025-01-XX*
*Description complète du déroulé d'une partie Timeline Ranger*


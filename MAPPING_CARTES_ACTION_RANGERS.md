# Mapping Cartes Action Ark Nova → Rangers de Couleur

## 📋 Tableau de Mapping Principal

| Carte Action Ark Nova | Ranger de Couleur | Couleur | Description |
|----------------------|-------------------|---------|-------------|
| **ACTION MECENE** | **RANGER BLEU** | 🔵 | Ranger spécialisé dans les pièces d'armure (bâtiments spéciaux) |
| **ACTION ANIMAUX** | **RANGER NOIR** | ⚫ | Ranger spécialisé dans l'installation d'armes dans les slots |
| **ACTION CONSTRUCTION** | **RANGER ORANGE** | 🟠 | Ranger spécialisé dans la construction de parties d'armure méca |
| **ACTION ASSOCIATION** | **RANGER VERT** | 🟢 | Ranger spécialisé dans l'installation de lasers |
| **ACTION CARTES** | **RANGER JAUNE** | 🟡 | Ranger spécialisé dans les actions de gestion de cartes |

## 🎴 Mapping des Cartes Jouables → Actions de Couleur

### 🔵 Ranger Bleu (ACTION MECENE)
- **Cartes source** : Cartes Mécène
- **Devient** : Actions Bleues
- **Permet de** :
  - **Carte non améliorée** :
    - **Option 1** : Jouer 1 carte Mécène niveau max = puissance (1-5)
    - **Option 2** : Gagner 1-5 crédits selon puissance
  - **Carte améliorée** :
    - **Option 1** : Jouer plusieurs cartes Mécène (total niveau max = puissance + 1)
      - Exemple puissance 3 : Peut jouer cartes niveau 1+2, ou 3, ou 2+2, etc. (total ≤ 4)
    - **Option 2** : Gagner 2 × le niveau de l'action (2, 4, 6, 8, 10 crédits)
  - Poser des pièces d'armure (anciennement bâtiments spéciaux)
  - Activer des effets de mécénat
- **Exemples** :
  - "Action Bleue : Fondation Wildlife" (niveau 2)
  - "Action Bleue : Jouer 2 cartes Mécène niveau 1+2" (améliorée, puissance 3)
  - "Action Bleue : Gagner 6 crédits" (améliorée, puissance 3)

### ⚫ Ranger Noir (ACTION ANIMAUX)
- **Cartes source** : Cartes Animal
- **Devient** : Actions Noires
- **Permet de** :
  - **Carte non améliorée** : 
    - Puissance 1 : 0 animal (peut passer)
    - Puissance 2-4 : 1 animal maximum
    - Puissance 5 : 2 animaux maximum + gagne 1 point de réputation
  - **Carte améliorée** :
    - Puissance 1-2 : 1 animal maximum
    - Puissance 3-5 : 2 animaux maximum
    - Puissance 5 : Gagne 1 point de réputation
  - Installer des armes dans les slots (anciennement placer des animaux)
  - Les armes doivent être installées dans des slots créés par le Ranger Orange
- **Exemples** :
  - "Action Noire : Installer arme Lion" (1 animal)
  - "Action Noire : Installer 2 armes" (puissance 5)
  - "Action Noire : Installer arme + gagner réputation" (puissance 5)

### 🟠 Ranger Orange (ACTION CONSTRUCTION)
- **Cartes source** : Actions de Construction
- **Devient** : Actions Orange
- **Permet de** :
  - Construire des parties d'armure méca
  - Créer des slots pour armes (pour que le Ranger Noir puisse installer des armes)
  - La puissance du Ranger détermine le nombre de parties/slots créés
- **Exemples** :
  - "Action Orange : Construire une garnison standard"
  - "Action Orange : Construire un bâtiment"
  - "Action Orange : Agrandir une garnison"

### 🟢 Ranger Vert (ACTION ASSOCIATION)
- **Cartes source** : Actions d'Association
- **Devient** : Actions Vertes
- **Système d'émissaires** : 1 au début, peut débloquer jusqu'à 3 supplémentaires (max 4)
- **Permet de** :
  - **Carte non améliorée** : Réaliser 1 quête niveau max = puissance
  - **Carte améliorée** : Réaliser une ou plusieurs quêtes niveau max = puissance
  - **Effets selon puissance** :
    - Niveau 2 : Gagne 2 points de réputation
    - Niveau 3 : Récupère une mine (réduit de 3 po les pièces d'armure de ce matériau)
    - Niveau 4 : Récupère une relique (bonus à définir)
    - Niveau 5 : Peut réaliser une quête si conditions remplies
    - Niveau 0 (améliorée) : Peut payer or pour obtenir un laser supplémentaire
- **Exemples** :
  - "Action Verte : Réaliser quête niveau 3"
  - "Action Verte : Gagner 2 points de réputation" (niveau 2)
  - "Action Verte : Récupérer mine Vibranium" (niveau 3)

### 🟡 Ranger Jaune (ACTION CARTES)
- **Cartes source** : Actions de gestion de cartes
- **Devient** : Actions Jaunes
- **Permet de** :
  - Piocher des cartes
  - Défausser des cartes
  - Gérer la main de cartes
  - La puissance du Ranger détermine le nombre de cartes piochées
- **Exemples** :
  - "Action Jaune : Piocher 2 cartes" (si Ranger Jaune en position 2)
  - "Action Jaune : Défausser 1 carte"
  - "Action Jaune : Rejouer une carte"

## 🔄 Système de Rotation (Identique à Ark Nova)

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

#### Action Verte : Installer des lasers
- **Puissance 1** : Installer 1 laser
- **Puissance 2** : Installer 2 lasers
- **Puissance 3** : Installer 3 lasers
- **Puissance 4** : Installer 4 lasers
- **Puissance 5** : Installer 5 lasers

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

## 🔗 Relations avec les Autres Mappings

### Types de Cartes
- **Cartes Mécène** → **Actions Bleues** (Ranger Bleu)
- **Cartes Animal** → **Actions Noires** (Ranger Noir)
- **Actions Construction** → **Actions Orange** (Ranger Orange)
- **Actions Association** → **Actions Vertes** (Ranger Vert)
- **Actions Cartes** → **Actions Jaunes** (Ranger Jaune)

### Points et Scores
- **Points Attrait** → **Points de Dégâts** (via Actions Noires - armes)
- **Points Conservation** → **Nombre de Lasers** (via Actions Vertes)
- **Points Réputation** → **Points de Développement Technique**
- **Points Science** → **Paires d'Ailes du Méca**

## 📝 Notes Importantes

1. **Les Rangers remplacent les cartes Action** mais conservent la mécanique de rotation
2. **Les cartes jouables** deviennent des **actions de couleur** spécifiques à chaque Ranger
3. **La couleur** est le filtre principal pour déterminer quelles actions un Ranger peut réaliser
4. **Le système de puissance** (1-5) reste identique au système original d'Ark Nova
5. **Le système de piste 1-5** est conservé : chaque Ranger a une position qui détermine sa puissance

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


# Système des Lasers - Timeline Ranger

Ce document détaille le système complet des lasers dans Timeline Ranger.

## 🎯 Vue d'Ensemble

Les **lasers** (ex-Points Conservation d'Ark Nova) sont obtenus via les troupes, technologies et actions. Ils génèrent des points de dégâts et offrent des bonus à certains seuils.

## 📊 Valeur des Lasers en Points de Dégâts

### Système de Points
- **0-6 lasers** : Chaque laser vaut **2 points de dégâts**
- **7+ lasers** : Chaque laser vaut **3 points de dégâts**

**Exemples** :
- 3 lasers = 3 × 2 = **6 points de dégâts**
- 6 lasers = 6 × 2 = **12 points de dégâts**
- 7 lasers = 7 × 3 = **21 points de dégâts**
- 10 lasers = 10 × 3 = **30 points de dégâts**

## 🎁 Bonus aux Seuils de Lasers

### Bonus à 2 Lasers
- **Seuil** : 2 lasers obtenus
- **Bonus** : Le joueur **choisit** entre :
  - **Option 1** : Améliorer une carte Action
  - **Option 2** : Obtenir un nouvel émissaire
- **Note** : Ce bonus est personnel (chaque joueur le reçoit quand il atteint 2 lasers)

### Bonus à 5 Lasers
- **Seuil** : 5 lasers obtenus
- **Bonus** : À définir (à préciser)

### Bonus à 8 Lasers
- **Seuil** : 8 lasers obtenus
- **Bonus** : À définir (à préciser)

### Seuil à 10 Lasers
- **Seuil** : **Le premier joueur** à atteindre 10 lasers
- **Action** : **TOUS les joueurs** doivent défausser **une des deux cartes "Dernier Souffle"**
- **Effet** : Chaque joueur choisit laquelle des deux cartes conserver
- **Note** : C'est un événement global qui affecte tous les joueurs, pas seulement celui qui atteint 10 lasers

## 🔄 Obtention des Lasers

### Sources de Lasers

1. **Troupes (ex-Animaux)** :
   - Les troupes déployées peuvent donner des lasers
   - Voir colonne `nombre_lasers` dans la table `troupes`

2. **Technologies (ex-Mécènes)** :
   - Les technologies peuvent donner des lasers
   - Voir colonne `nombre_lasers` dans la table `technologies`

3. **Action Association (Ranger Vert)** :
   - Niveau 0 (carte améliorée) : Peut payer or pour obtenir 1 laser supplémentaire

4. **Quêtes (ex-Projets de Conservation)** :
   - Les quêtes complétées peuvent donner des lasers
   - Voir colonne `nombre_lasers` dans la table `quetes`

## 📈 Calcul des Points de Dégâts Totaux

### Formule
```
Si lasers ≤ 6 :
    Points de dégâts des lasers = lasers × 2

Si lasers ≥ 7 :
    Points de dégâts des lasers = lasers × 3
```

### Exemple de Calcul Complet
Un joueur a :
- 15 points de dégâts de troupes
- 8 lasers obtenus

**Calcul** :
- Lasers : 8 × 3 = 24 points de dégâts (car 8 > 6)
- **Total** : 15 + 24 = **39 points de dégâts**

## 🎴 Cartes Dernier Souffle

### Distribution Initiale
- **Début de partie** : Chaque joueur reçoit **2 cartes "Dernier Souffle"** aléatoirement
- Ces cartes sont conservées jusqu'à ce que le joueur atteigne 10 lasers

### À 10 Lasers
- Le joueur doit **défausser une des deux cartes**
- Le joueur **choisit** laquelle conserver
- La carte conservée sera utilisée lors du décompte final

## 🔗 Relations avec les Autres Systèmes

### Mapping Ark Nova
- **Points Conservation** → **Nombre de Lasers**
- Les lasers sont obtenus de la même manière que les points de conservation dans Ark Nova

### Action Association
- Permet d'obtenir des lasers supplémentaires (niveau 0 améliorée)
- Les quêtes réalisées via Action Association peuvent donner des lasers

### Décompte Final
- Les lasers comptent dans le score final (points de dégâts)
- Les cartes Dernier Souffle conservées sont appliquées au décompte final

## 📝 Notes Importantes

1. **Seuils de bonus** : Les bonus à 2, 5, 8 lasers doivent être définis
2. **Choix de carte** : À 10 lasers, le joueur choisit quelle carte Dernier Souffle conserver
3. **Valeur variable** : La valeur des lasers change à partir de 7 lasers (2 → 3 points de dégâts)
4. **Cumul** : Les lasers s'accumulent tout au long de la partie

## ⚠️ Points à Définir

1. **Bonus à 5 lasers** : Quel est le bonus exact ?
2. **Bonus à 8 lasers** : Quel est le bonus exact ?
3. **Action Association niveau 0** : Quel est le coût exact en or pour obtenir 1 laser ?
4. **Amélioration d'une carte Action** : Quelles sont les conditions exactes pour améliorer une carte Action ?

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


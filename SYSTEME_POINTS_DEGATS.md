# Système de Points de Dégâts - Timeline Ranger

Ce document détaille le calcul complet des points de dégâts dans Timeline Ranger.

## 🎯 Vue d'Ensemble

Les **points de dégâts** (ex-Points Attrait d'Ark Nova) sont le score principal du jeu. Ils proviennent de plusieurs sources.

## 📊 Sources de Points de Dégâts

### 1. Troupes (ex-Animaux)
- **Source** : Cartes Troupes déployées sur l'Armure Méca
- **Colonne** : `points_degats` dans la table `troupes`
- **Calcul** : Somme des points de dégâts de toutes les troupes en jeu

### 2. Lasers (ex-Points Conservation)
- **Source** : Troupes, Technologies, Quêtes, Action Association
- **Valeur variable** :
  - **0-6 lasers** : Chaque laser vaut **2 points de dégâts**
  - **7+ lasers** : Chaque laser vaut **3 points de dégâts**
- **Calcul** :
  ```
  Si lasers ≤ 6 :
      Points de dégâts des lasers = lasers × 2
  Si lasers ≥ 7 :
      Points de dégâts des lasers = lasers × 3
  ```

### 3. Technologies (ex-Mécènes)
- **Source** : Cartes Technologies déployées
- **Colonne** : `points_degats` dans la table `technologies` (si applicable)
- **Note** : Toutes les technologies ne donnent pas nécessairement des points de dégâts

### 4. Autres Sources
- **Effets de cartes** : Certaines cartes peuvent donner des points de dégâts
- **Quêtes** : Certaines quêtes peuvent donner des points de dégâts
- **Bonus** : Bonus obtenus via les lasers (à 2, 5, 8 lasers)

## 🧮 Calcul Total des Points de Dégâts

### Formule Complète
```
Points de dégâts totaux = 
    Points de dégâts des troupes +
    Points de dégâts des lasers (calculés selon nombre) +
    Points de dégâts des technologies +
    Points de dégâts des autres sources
```

### Exemple de Calcul

**Joueur avec** :
- 3 troupes : 5 + 3 + 4 = **12 points de dégâts**
- 2 technologies : 2 + 1 = **3 points de dégâts**
- **8 lasers** obtenus

**Calcul des lasers** :
- 8 lasers > 6, donc : 8 × 3 = **24 points de dégâts**

**Total** :
- 12 (troupes) + 3 (technologies) + 24 (lasers) = **39 points de dégâts**

## 🎁 Bonus aux Seuils de Lasers

### Bonus à 2 Lasers
- **Seuil** : 2 lasers obtenus
- **Bonus** : Le joueur **choisit** entre :
  - **Option 1** : Améliorer une carte Action
  - **Option 2** : Obtenir un nouvel émissaire
- **Note** : Bonus personnel (chaque joueur le reçoit individuellement)

### Bonus à 5 Lasers
- **Seuil** : 5 lasers obtenus
- **Bonus** : À définir (peut donner des points de dégâts supplémentaires ?)

### Bonus à 8 Lasers
- **Seuil** : 8 lasers obtenus
- **Bonus** : À définir (peut donner des points de dégâts supplémentaires ?)

### Seuil à 10 Lasers
- **Seuil** : **Le premier joueur** à atteindre 10 lasers
- **Action** : **TOUS les joueurs** doivent défausser une des deux cartes "Dernier Souffle"
- **Effet** : Chaque joueur choisit quelle carte conserver pour le décompte final
- **Note** : Événement global qui affecte tous les joueurs simultanément

## 📈 Évolution de la Valeur des Lasers

### Tableau de Valeur

| Nombre de Lasers | Valeur par Laser | Total Points de Dégâts |
|------------------|------------------|------------------------|
| 1 | 2 | 2 |
| 2 | 2 | 4 |
| 3 | 2 | 6 |
| 4 | 2 | 8 |
| 5 | 2 | 10 |
| 6 | 2 | 12 |
| 7 | 3 | 21 |
| 8 | 3 | 24 |
| 9 | 3 | 27 |
| 10 | 3 | 30 |
| 11 | 3 | 33 |
| 12 | 3 | 36 |

**Seuil critique** : À partir de 7 lasers, chaque laser supplémentaire vaut 50% de plus (3 au lieu de 2)

## 🎯 Conditions de Fin de Partie

### Seuil Principal
- **120 points de dégâts** : Condition principale de fin de partie
- **Variantes** : 80 ou 100 points (configurables)

### Calcul au Moment de la Fin
- Les points de dégâts sont calculés en temps réel
- Quand un joueur atteint le seuil, la partie se termine
- Chaque autre joueur a droit à un dernier tour

## 🔄 Mise à Jour Continue

### Pendant la Partie
- Les points de dégâts sont recalculés après chaque action
- Les lasers sont comptabilisés en temps réel
- Les bonus aux seuils sont appliqués immédiatement

### Décompte Final
- Application des effets "Dernier Souffle" de toutes les cartes
- Calcul final des points de dégâts des lasers
- Addition de tous les points de dégâts

## 📝 Notes Importantes

1. **Valeur variable** : Les lasers valent plus à partir de 7 lasers (2 → 3 points de dégâts)
2. **Bonus** : Les bonus à 2, 5, 8 lasers doivent être définis
3. **Carte Dernier Souffle** : À 10 lasers, choix de la carte à conserver
4. **Cumul** : Tous les points de dégâts s'accumulent tout au long de la partie

## ⚠️ Points à Définir

1. **Bonus à 2 lasers** : Quel est le bonus exact ? (points de dégâts ? ressources ?)
2. **Bonus à 5 lasers** : Quel est le bonus exact ?
3. **Bonus à 8 lasers** : Quel est le bonus exact ?
4. **Action Association niveau 0** : Quel est le coût exact en or pour obtenir 1 laser ?

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


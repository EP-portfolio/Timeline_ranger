# Système de Réputation (Points de Développement Technique)

Ce document détaille le système complet de réputation dans Timeline Ranger.

## 🎯 Vue d'Ensemble

La **réputation** (ex-Points Réputation d'Ark Nova) est représentée par les **Points de Développement Technique** dans Timeline Ranger. Elle est gagnée via diverses actions et offre des bonus à certains seuils.

## 📊 Limite de Réputation

### Limite Standard
- **Maximum** : **9 points de réputation** (sans amélioration)
- **Blocage** : Le marqueur ne peut pas dépasser la case 9 sur la piste de réputation

### Dépassement de la Limite
- **Condition** : Améliorer la carte Action **"Cartes"** (Ranger Jaune)
- **Effet** : Permet de continuer à avancer sur la piste de réputation au-delà de la case 9
- **Maximum** : **15 points de réputation** (la piste s'étend jusqu'à la case 15)
- **À la case 15** : Si vous gagnez encore des points de réputation, vous pouvez choisir entre :
  - Gagner **1 point d'attrait** (1 point de dégâts)
  - Prendre la **tuile bonus** située à la fin de la piste (si elle est encore disponible)

## 🎁 Bonus de la Piste de Réputation

### Bonus aux Différents Seuils

Les bonus de réputation sont obtenus **immédiatement** en atteignant ou dépassant certaines cases sur la piste. Chaque bonus n'est attribué **qu'une seule fois**, lors du premier passage ou arrêt sur la case correspondante.

### Types de Bonus Disponibles

Les bonus peuvent inclure :
- **Points d'attrait** (points de dégâts)
- **Crédits** (or)
- **Jetons X** (croix)
- **Bénévoles** (émissaires)
- **Cartes** (pioche de cartes)
- **Améliorations d'actions**
- **Autres avantages spécifiques**

### Cases Spécifiques

**Note** : Les bonus exacts à chaque case (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) sont indiqués sur le **plateau de jeu** ou dans le **livret de règles officiel**. 

**À vérifier sur le plateau** :
- Chaque case de la piste de réputation indique le bonus obtenu
- Les bonus sont généralement visibles directement sur le plateau de jeu

### Case 15 (Maximum)

- **Limite** : La piste s'étend jusqu'à la case 15
- **Si réputation déjà à 15** : Si vous gagnez encore des points de réputation, vous pouvez choisir entre :
  - Gagner **1 point d'attrait** (1 point de dégâts)
  - Prendre la **tuile bonus** située à la fin de la piste (si elle est encore disponible)
- **Tuile bonus** : Une tuile bonus unique est disponible à la fin de la piste (premier arrivé, premier servi)

## 📈 Obtention de Réputation

### Sources de Réputation

1. **Action Animaux (Ranger Noir)** :
   - Puissance 5 : Gagne 1 point de réputation

2. **Action Association (Ranger Vert)** :
   - Puissance 2 : Gagne 2 points de réputation

3. **Cartes Troupes** :
   - Certaines troupes donnent des points de réputation
   - Voir colonne `points_developpement_technique` dans la table `troupes`

4. **Cartes Technologies** :
   - Certaines technologies donnent des points de réputation
   - Voir colonne `points_developpement_technique` dans la table `technologies`

5. **Quêtes** :
   - Certaines quêtes peuvent donner des points de réputation
   - Voir colonne `points_developpement_technique` dans la table `quetes`

## 🔄 Action Cartes Améliorée

### Effet Principal
- **Pioche** : Au lieu de piocher selon la **puissance** (1-5), pioche selon la **réputation**
- **Exemple** : Si réputation = 7, pioche 7 cartes (au lieu de la puissance)

### Effet Secondaire
- **Déblocage** : Permet de dépasser la limite de 9 points de réputation
- **Maximum** : **15 points de réputation** (la piste s'étend jusqu'à la case 15)
- **Portée de réputation** : Plus votre réputation est élevée, plus vous avez accès à des cartes situées loin dans la rivière

## 📝 Notes Importantes

1. **Limite standard** : 9 points de réputation maximum sans amélioration
2. **Amélioration nécessaire** : Améliorer la carte Action "Cartes" pour dépasser 9
3. **Bonus** : Les bonus de réputation sont obtenus à certains seuils (à définir)
4. **Stratégie** : L'amélioration de la carte "Cartes" est importante pour maximiser la réputation

## ⚠️ Points à Vérifier sur le Plateau

1. **Bonus de réputation** : Les bonus exacts à chaque case (1-15) sont indiqués sur le plateau de jeu
   - À vérifier directement sur le plateau de jeu Ark Nova
   - Chaque case montre le bonus obtenu (crédits, jetons X, points d'attrait, etc.)
2. **Maximum avec amélioration** : ✅ Confirmé - **15 points de réputation maximum**
3. **Timing des bonus** : ✅ Confirmé - Les bonus sont obtenus **immédiatement** en atteignant les cases

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


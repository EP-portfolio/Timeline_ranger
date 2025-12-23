# Décisions Prises - Timeline Ranger

Ce document récapitule toutes les décisions prises concernant les mécaniques de jeu et l'architecture technique.

## 🎮 Mécaniques de Jeu

### 1. Système de Tours ✅
- **Ordre initial** : Premier joueur choisi aléatoirement
- **Points initiaux** : 
  - Joueur 1 : 0 point
  - Joueur 2 : 1 point
  - Joueur 3 : 2 points
  - Joueur 4 : 3 points
- **Tour par tour** : Un seul joueur actif à la fois

### 2. Actions par Tour ✅
- **Action principale** : Une carte action par tour maximum
- **Actions supplémentaires** : Possibles via effets de cartes spécifiques
- **Système de piste 1-5** : 
  - Chaque joueur dispose de 5 cartes Action placées sur une piste numérotée de 1 à 5
  - La position détermine la puissance (1 = faible, 5 = forte)
  - Quand une carte est jouée : elle revient en position 1, les autres avancent d'une position
- **Jetons X (Croix)** : 
  - Obtenus lorsqu'un joueur atteint la fin de la piste de pause (symbole tasse)
  - Maximum 5 jetons X
  - Utilisables pour augmenter le niveau d'une action
  - (À préciser : combien de jetons pour augmenter de combien de niveaux ?)
- **Amélioration** : Les cartes Action peuvent être améliorées pour augmenter leur efficacité

### 3. Pioche et Distribution ✅
- **Début de partie** : 
  - Chaque joueur reçoit 8 cartes aléatoirement
  - Chaque joueur conserve 4 cartes (défausse 4)
- **RIVER (Display Row)** : 
  - Zone commune avec 6 cartes visibles
  - Cartes jouables sous certaines conditions
  - **Remplacement** : Quand une carte est jouée, elle est remplacée par une nouvelle carte de la pioche
- **Action Cartes améliorée** : Permet de piocher des cartes à hauteur de la réputation du joueur

### 4. Main de Cartes ✅
- **Pendant le jeu** : Pas de limite
- **À la pause** : Limite à 3 cartes (ou plus selon bonus)
- **Défausse** : Obligatoire pour les cartes excédentaires à la pause

### 5. Placement sur l'Armure Méca ✅
- **Première pièce** : Doit être sur une case du bord de l'armure
- **Pièces suivantes** : Doivent être adjacentes à une pièce existante
- **Exceptions** : Certaines cartes peuvent avoir des règles de placement spécifiques

### 6. Actions de Couleur ✅
- **Système de piste 1-5** : 
  - 5 cartes Action sur une piste numérotée
  - Position = puissance (1 = faible, 5 = forte)
  - Rotation : Carte jouée → position 1, autres avancent
- **Jetons X (Croix)** : 
  - Obtenus à la fin de la piste de pause (symbole tasse)
  - Maximum 5 jetons X
  - Utilisables pour augmenter le niveau d'une action
  - (À préciser : combien de jetons pour augmenter de combien ?)
- **Amélioration** : Les cartes Action peuvent être améliorées
- **Actions spéciales** :
  - MECENES, ANIMAUX, ASSOCIATION : Permettent de jouer une ou plusieurs cartes de ce type
  - Peuvent avoir d'autres effets

### 7. Effets de Cartes ✅
- **Effets d'invocation** : Appliqués immédiatement lors du placement
- **Effets après pause** : Activés après que la pause ait lieu (récolte)
- **Effets permanents/récurrents (fond bleu)** : Probablement activés à chaque pause ou à chaque tour (à confirmer)
- **Effets de dernier souffle** : Seulement en fin de partie
- **Activation manuelle** : À déterminer selon les cartes

### 8. Ressources ✅
- **Récolte** : Ressources gagnées après la pause (récurrent)
- **Montant de la récolte** : Dépend de l'attrait du zoo (piste d'attrait) - plus l'attrait est élevé, plus les revenus sont élevés
- **Action Income (Noire)** : Permet de gagner de l'or - montant probablement égal à la puissance de l'action (1-5 crédits selon position)
- **One-shot** : Ressources gagnées une seule fois via cartes/actions
- **Types** : Or, matières premières (titanium, platine, vibranium, carbone, kevlar)
- **À préciser** : Limite de ressources

### 9. Quêtes ✅
- **Types** : 
  - Quêtes de base (toujours disponibles sur le plateau principal)
  - Quêtes dans la pioche
- **Fonctionnement** : 
  - Les joueurs peuvent contribuer aux projets en remplissant les conditions
  - Gagnent des points de conservation
- **Ajout de nouveaux projets** : 
  - Possible d'ajouter de nouveaux projets
  - Retrait du plus ancien projet (selon espace disponible)
- **Plusieurs projets actifs** : Oui, simultanément
- **Récompenses** : 
  - Points de conservation (lasers) - toujours
  - Points de réputation (développement technique) - parfois

### 10. Conditions de Fin de Partie ✅
- **Condition principale (Ark Nova)** : Un joueur fait se croiser ses marqueurs sur les pistes d'Attrait et de Conservation
- **Condition principale (Timeline Ranger)** : Un joueur atteint 120 points de dégâts
- **Variantes** : 80 ou 100 points (configurables)
- **Dernier tour** : Chaque autre joueur a droit à un dernier tour
- **Décompte final** : 
  - Application des effets "Dernier Souffle" de toutes les cartes
  - Calcul : Attrait (points de dégâts) + Conservation (lasers)
- **Départage** :
  1. Nombre de quêtes réalisées
  2. Score de réputation (points de développement technique)

## 💻 Architecture Technique

### 11. Gestion de l'État ✅
- **Replay complet** : Gestion d'état de chaque action lors de chaque tour
- **Objectif** : Replay total de la partie
- **Implémentation** :
  - Sauvegarde complète de l'état après chaque action
  - Historique complet des actions avec timestamps
  - Versioning pour replay pas à pas
- **À définir** : Taille maximale de l'état JSON

### 12. WebSockets ⏳
- **À définir** : Stratégie de synchronisation
  - Push complet de l'état à chaque action ?
  - Push incrémental (deltas) ?
  - Polling en fallback ?
  - Gestion des reconnexions ?

### 13. Gestion des Conflits ✅
- **Tour par tour** : Pas d'actions simultanées
- **Implémentation** :
  - Verrouillage du tour (un seul joueur actif)
  - Rejet des actions des autres joueurs pendant le tour actif
  - File d'attente non nécessaire

### 14. Performance ⏳
- **À définir** : Contraintes de performance
  - Temps de réponse maximum pour une action ?
  - Nombre de parties simultanées supportées ?
  - Taille maximale d'une partie ?

### 15. Historique et Replay ✅
- **Replay souhaité** : Oui
- **Implémentation** :
  - Historique complet des actions
  - Possibilité de revoir une partie
  - Export des parties (à considérer)

## 🎨 UX/UI

### 16. Interface Utilisateur ⏳
- **À définir** : Priorités d'affichage
  - Vue principale : Plateau ou main ?
  - Informations des autres joueurs : Toujours visibles ?
  - Notifications : Comment afficher ?

### 17. Feedback Utilisateur ⏳
- **À définir** : Comment informer l'utilisateur
  - Messages d'erreur : Niveau de détail ?
  - Confirmations : Pour quelles actions ?
  - Animations : Souhaitées ?

## 📊 Données

### 18. Configuration des Armures Méca ⏳
- **À compléter** : Voir CONFIGURATIONS_PLATEAUX_ARMURES.md
  - Dimensions exactes
  - Cases bloquées
  - Zones spéciales
  - Capacités spéciales

### 19. Données des Cartes ⏳
- **À vérifier** : Dans la base de données
  - Effets de toutes les cartes
  - Coûts exacts
  - Prérequis

### 20. Statistiques ⏳
- **À définir** : Statistiques à tracker
  - Parties jouées/gagnées
  - Scores moyens
  - Cartes les plus jouées
  - Temps de partie moyen

---

## 📝 Légende

- ✅ **Décision prise** : Décision claire et implémentable
- ⏳ **À définir** : Nécessite encore une décision ou clarification
- 🔄 **Partiellement défini** : Décision partielle, détails à compléter

---

## 🚀 Prochaines Étapes

### Priorité 1 : Clarifications Restantes
1. Système de croix et augmentation de niveau (détails d'implémentation)
2. Mécanisme de remplacement des cartes dans la RIVER
3. Timing exact des effets quotidiens
4. Montant de l'Action Noire (fixe/variable)
5. Mécanisme d'activation des quêtes

### Priorité 2 : Architecture Technique
1. Stratégie WebSockets (push complet vs incrémental)
2. Contraintes de performance
3. Taille maximale de l'état JSON

### Priorité 3 : UX/UI
1. Priorités d'affichage
2. Feedback utilisateur
3. Animations

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


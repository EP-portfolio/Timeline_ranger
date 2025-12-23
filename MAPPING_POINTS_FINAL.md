# Mapping des Points - Version Finale

Ce document définit le mapping final et complet de tous les points d'Ark Nova vers Timeline Ranger.

## 🔢 Mapping Complet des Points

| Point Original | Point Nouveau | Description | Statut |
|----------------|---------------|-------------|--------|
| `Points Attrait` | `Points de Dégâts` | Points de dégâts générés | ✅ Confirmé |
| `Points Conservation` | `Nombre de Lasers` | Nombre de lasers installés | ✅ Confirmé |
| `Points Réputation` | `Points de Développement Technique` | Points de développement technologique | ✅ Confirmé |
| `Points Science` | `Nombre de Paires d'Ailes du Méca` | Nombre de paires d'ailes de l'armure méca | ✅ Confirmé |

## 📊 Détails par Type de Point

### ⚔️ Points Attrait → Points de Dégâts
- **Description** : Points de dégâts infligés par les armes et pièces d'armure
- **Source** : Armes (Actions Noires), Pièces d'armure (Actions Bleues)
- **Utilisation** : Accumulation pour atteindre l'objectif de fin de partie
- **Exemple** : Une arme avec 5 points d'attrait = 5 points de dégâts

### 🔫 Points Conservation → Nombre de Lasers
- **Description** : Nombre de lasers à installer sur l'armure méca
- **Source** : Cartes avec points de conservation
- **Utilisation** : Le Ranger Vert installe les lasers
- **Règle** : Chaque point de conservation = 1 laser supplémentaire
- **Exemple** : Une carte avec 3 points de conservation = 3 lasers à installer

### 🔬 Points Réputation → Points de Développement Technique
- **Description** : Points de développement technologique
- **Source** : Cartes avec points de réputation
- **Utilisation** : Déblocage de technologies, améliorations, recherches
- **Exemple** : 5 points de réputation = 5 points de développement technique

### 🦅 Points Science → Nombre de Paires d'Ailes du Méca
- **Description** : Nombre de paires d'ailes de l'armure méca
- **Source** : Cartes avec points de science
- **Utilisation** : Détermine la mobilité et les capacités aériennes du méca
- **Règle** : Chaque point de science = 1 paire d'ailes
- **Exemple** : 2 points de science = 2 paires d'ailes sur l'armure méca

## 🎮 Implications pour le Jeu

### Système de Dégâts
- Les **Points de Dégâts** sont générés par :
  - Les **armes** installées par le Ranger Noir
  - Les **pièces d'armure** posées par le Ranger Bleu
- L'objectif est d'accumuler des **Points de Dégâts**

### Système de Lasers
- Les **Lasers** sont installés par le **Ranger Vert**
- **Total lasers** = Puissance du Ranger Vert + Points de Conservation des cartes
- Chaque laser peut avoir des **effets spéciaux**

### Système de Développement Technique
- Les **Points de Développement Technique** permettent de :
  - Débloquer des **technologies**
  - Améliorer des **composants**
  - Rechercher des **capacités spéciales**
- Accumulation progressive pour progression

### Système d'Ailes
- Les **Paires d'Ailes** déterminent :
  - La **mobilité aérienne** de l'armure méca
  - Les **capacités de vol**
  - Les **bonus de mouvement**
- Plus de paires d'ailes = plus de mobilité

## 📋 Exemples de Conversion

### Exemple 1 : Carte Animal
- **Original** : Lion (Attrait: 5, Conservation: 2, Réputation: 0, Science: 0)
- **Nouveau** : Arme - Lion
  - Points de Dégâts: 5
  - Nombre de Lasers: 2
  - Points de Développement Technique: 0
  - Paires d'Ailes: 0

### Exemple 2 : Carte Mécène
- **Original** : Fondation (Attrait: 3, Conservation: 1, Réputation: 2, Science: 1)
- **Nouveau** : Pièce d'armure - Fondation
  - Points de Dégâts: 3
  - Nombre de Lasers: 1
  - Points de Développement Technique: 2
  - Paires d'Ailes: 1

## 🔗 Intégration avec les Autres Systèmes

### Rangers
- **Ranger Noir** : Installe des armes (Points de Dégâts)
- **Ranger Vert** : Installe des lasers (Points de Conservation)
- **Ranger Bleu** : Pose des pièces (Points de Dégâts, Développement Technique, Ailes)
- **Ranger Orange** : Construit des parties (peut générer des points)

### Armure Méca
- Les **Points de Dégâts** déterminent la puissance offensive
- Les **Lasers** sont installés sur l'armure méca
- Les **Points de Développement Technique** débloquent des améliorations
- Les **Paires d'Ailes** améliorent la mobilité

## 📝 Notes Importantes

1. **Points de Dégâts** : Générés par armes et pièces d'armure
2. **Nombre de Lasers** : Déterminé par Points de Conservation
3. **Points de Développement Technique** : Débloquent technologies
4. **Paires d'Ailes** : Améliorent la mobilité aérienne
5. **Tous les mappings sont confirmés** : Plus de "À DÉTERMINER"

## 🚀 Prochaines Étapes

1. ✅ **Mapping complet** : Tous les points sont mappés
2. ⏳ **Mise à jour** : Tous les documents de mapping
3. ⏳ **Intégration Neo4j** : Ajouter les nouveaux points
4. ⏳ **Système de jeu** : Implémenter les mécaniques
5. ⏳ **Documentation** : Créer des guides détaillés

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


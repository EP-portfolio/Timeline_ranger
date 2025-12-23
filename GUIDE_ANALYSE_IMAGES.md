# Guide d'Analyse des Images de Plateaux

Ce guide explique comment obtenir et analyser les images des plateaux d'Ark Nova pour extraire les configurations des grilles.

## 📋 Méthodes pour Obtenir les Images

### Méthode 1 : Téléchargement depuis BoardGameGeek

1. **Aller sur BoardGameGeek** :
   - URL : https://boardgamegeek.com/boardgame/285774/ark-nova
   - Naviguer vers la section "Images" ou "Files"

2. **Télécharger les images** :
   - Trouver les images des plateaux de jeu
   - Cliquer droit sur l'image → "Enregistrer l'image sous..."
   - Sauvegarder dans le dossier `images_plateaux/`

### Méthode 2 : Captures d'Écran depuis des Vidéos

1. **Rechercher des vidéos** :
   - YouTube : "Ark Nova gameplay", "Ark Nova review"
   - Chercher les moments où les plateaux sont visibles

2. **Faire des captures** :
   - Pause la vidéo sur un plan clair du plateau
   - Faire une capture d'écran
   - Sauvegarder dans `images_plateaux/`

### Méthode 3 : Scanner les Plateaux Physiques

Si vous avez accès aux plateaux physiques :

1. **Scanner ou photographier** :
   - Utiliser un scanner ou un appareil photo
   - Assurer un éclairage uniforme
   - Capturer le plateau en entier et bien à plat

2. **Nommer les fichiers** :
   - `plateau_A.jpg`
   - `plateau_0.jpg`
   - `plateau_1.jpg`
   - etc.

### Méthode 4 : Sites de Vente en Ligne

1. **Consulter les sites** :
   - Philibert : https://www.philibertnet.com
   - Autres boutiques spécialisées

2. **Télécharger les images produits** :
   - Les images produits sont souvent de bonne qualité
   - Sauvegarder dans `images_plateaux/`

## 🔧 Utilisation des Scripts

### Étape 1 : Préparer les Images

Placez toutes les images des plateaux dans le dossier `images_plateaux/` avec des noms descriptifs :
```
images_plateaux/
  ├── plateau_A.jpg
  ├── plateau_0.jpg
  ├── plateau_1.jpg
  ├── plateau_2.jpg
  └── ...
```

### Étape 2 : Installer les Dépendances

```bash
pip install -r requirements.txt
```

Les dépendances nécessaires :
- `opencv-python` : Traitement d'image
- `numpy` : Calculs numériques
- `Pillow` : Manipulation d'images
- `matplotlib` : Visualisation
- `requests` : Téléchargement

### Étape 3 : Analyser les Images

```bash
python analyser_images_plateaux.py
```

Le script va :
1. Chercher toutes les images dans `images_plateaux/`
2. Analyser chaque image pour détecter la grille
3. Identifier les zones spéciales (eau, rocher, etc.)
4. Générer un rapport dans `RAPPORT_ANALYSE_PLATEAUX.md`
5. Sauvegarder les résultats dans `resultats_analyse_plateaux.json`

### Étape 4 : Vérifier et Corriger

1. **Consulter le rapport** :
   - Ouvrir `RAPPORT_ANALYSE_PLATEAUX.md`
   - Vérifier les dimensions détectées
   - Vérifier les zones spéciales identifiées

2. **Corriger si nécessaire** :
   - Les détections automatiques peuvent être imprécises
   - Comparer avec les images originales
   - Modifier manuellement le fichier JSON si besoin

## 📊 Format des Résultats

### Fichier JSON (`resultats_analyse_plateaux.json`)

```json
{
  "plateau_A": {
    "nom_plateau": "plateau_A",
    "chemin_image": "images_plateaux/plateau_A.jpg",
    "dimensions_grille": [5, 5],
    "zones_speciales": [
      {
        "position": [2, 3],
        "type": "eau"
      }
    ],
    "image_shape": [1000, 1000]
  }
}
```

### Intégration avec les Configurations

Les résultats peuvent être intégrés dans `configurations_plateaux.json` :

```bash
python documenter_configurations_plateaux.py
```

Puis fusionner les résultats de l'analyse avec les configurations.

## ⚠️ Limitations

1. **Qualité des images** :
   - Les images de mauvaise qualité peuvent donner de mauvais résultats
   - Préférer des images haute résolution

2. **Détection automatique** :
   - La détection de grille peut être imprécise
   - Les zones spéciales peuvent être mal identifiées
   - Une vérification manuelle est recommandée

3. **Variations visuelles** :
   - Les différents plateaux peuvent avoir des designs différents
   - Certains peuvent nécessiter des ajustements dans le script

## 🔍 Améliorations Possibles

1. **Apprentissage automatique** :
   - Entraîner un modèle pour mieux détecter les grilles
   - Améliorer la reconnaissance des zones spéciales

2. **Interface graphique** :
   - Créer une interface pour valider/corriger les détections
   - Permettre l'annotation manuelle

3. **Reconnaissance de texte** :
   - Utiliser OCR pour lire les labels sur les plateaux
   - Identifier automatiquement le numéro du plateau

## 📝 Notes

- Les scripts sont conçus pour être flexibles et adaptables
- N'hésitez pas à modifier les paramètres de détection selon vos images
- Les résultats doivent toujours être vérifiés manuellement

---
*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


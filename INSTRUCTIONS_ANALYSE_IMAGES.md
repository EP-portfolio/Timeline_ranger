# Instructions pour Analyser les Images des Plateaux

## 🎯 Objectif

Analyser automatiquement les images des plateaux d'Ark Nova pour extraire :
- Les dimensions des grilles (largeur x hauteur)
- Les positions des cases bloquées
- Les zones spéciales (eau, rocher, grottes, etc.)

## 📥 Étape 1 : Obtenir les Images

### Option A : Télécharger depuis BoardGameGeek

1. Allez sur : https://boardgamegeek.com/boardgame/285774/ark-nova
2. Cliquez sur l'onglet "Images"
3. Recherchez les images des plateaux de jeu
4. Téléchargez les images et placez-les dans `images_plateaux/`

### Option B : Captures d'Écran depuis YouTube

1. Recherchez des vidéos de gameplay d'Ark Nova
2. Faites des captures d'écran des plateaux
3. Sauvegardez dans `images_plateaux/` avec des noms descriptifs

### Option C : Scanner/Photographier les Plateaux Physiques

Si vous avez le jeu :
1. Scannez ou photographiez chaque plateau
2. Assurez-vous que l'image est nette et bien éclairée
3. Sauvegardez dans `images_plateaux/`

## 📁 Structure des Fichiers

Créez cette structure :
```
TIMELINE_RANGER/
  ├── images_plateaux/
  │   ├── plateau_A.jpg
  │   ├── plateau_0.jpg
  │   ├── plateau_1.jpg
  │   ├── plateau_2.jpg
  │   └── ...
  ├── analyser_images_plateaux.py
  └── ...
```

## 🔧 Étape 2 : Installer les Dépendances

```bash
pip install opencv-python numpy Pillow matplotlib requests
```

Ou installez toutes les dépendances :
```bash
pip install -r requirements.txt
```

## 🚀 Étape 3 : Lancer l'Analyse

```bash
python analyser_images_plateaux.py
```

Le script va :
1. ✅ Chercher toutes les images dans `images_plateaux/`
2. ✅ Analyser chaque image pour détecter la grille
3. ✅ Identifier les zones spéciales
4. ✅ Générer un rapport Markdown
5. ✅ Sauvegarder les résultats en JSON

## 📊 Étape 4 : Consulter les Résultats

### Fichier de Rapport
Ouvrez `RAPPORT_ANALYSE_PLATEAUX.md` pour voir :
- Les dimensions détectées pour chaque plateau
- Les zones spéciales identifiées
- Les positions des zones

### Fichier JSON
Ouvrez `resultats_analyse_plateaux.json` pour les données structurées.

## 🔄 Étape 5 : Intégrer avec les Configurations

Une fois les analyses terminées, vous pouvez intégrer les résultats dans `configurations_plateaux.json` :

1. Ouvrez `resultats_analyse_plateaux.json`
2. Copiez les dimensions et zones spéciales
3. Collez dans `configurations_plateaux.json`
4. Ré-exécutez `documenter_configurations_plateaux.py` pour mettre à jour le Markdown

## ⚠️ Notes Importantes

1. **Qualité des images** :
   - Utilisez des images haute résolution pour de meilleurs résultats
   - Les images floues ou mal éclairées peuvent donner de mauvais résultats

2. **Vérification manuelle** :
   - Les détections automatiques peuvent être imprécises
   - Vérifiez toujours les résultats avec les images originales
   - Corrigez manuellement si nécessaire

3. **Nommage des fichiers** :
   - Utilisez des noms descriptifs : `plateau_A.jpg`, `plateau_1.jpg`, etc.
   - Évitez les espaces et caractères spéciaux

## 🐛 Dépannage

### Erreur : "Aucune image trouvée"
- Vérifiez que le dossier `images_plateaux/` existe
- Vérifiez que les images sont dans ce dossier
- Vérifiez les extensions de fichiers (.jpg, .png, etc.)

### Erreur : "Impossible de détecter la grille"
- L'image peut être de mauvaise qualité
- Essayez avec une image de meilleure résolution
- Vérifiez que l'image montre bien le plateau complet

### Erreur : "Module not found"
- Installez les dépendances : `pip install -r requirements.txt`

## 📝 Exemple de Résultat Attendu

```json
{
  "plateau_A": {
    "nom_plateau": "plateau_A",
    "dimensions_grille": [5, 5],
    "zones_speciales": [
      {"position": [2, 3], "type": "eau"},
      {"position": [4, 1], "type": "rocher"}
    ]
  }
}
```

## 🎯 Prochaines Étapes

Une fois les configurations extraites :
1. ✅ Valider les dimensions avec les règles du jeu
2. ✅ Vérifier les zones spéciales manuellement
3. ✅ Intégrer dans `configurations_plateaux.json`
4. ✅ Mettre à jour la documentation

---
*Pour toute question ou problème, consultez `GUIDE_ANALYSE_IMAGES.md`*


"""
Script pour analyser les images des plateaux d'Ark Nova et extraire les configurations des grilles.
Ce script peut traiter des images locales ou téléchargées depuis des URLs.
"""

import os
import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class AnalyseurPlateau:
    """Classe pour analyser les images de plateaux et extraire les configurations."""
    
    def __init__(self, dossier_images: str = "images_plateaux"):
        self.dossier_images = Path(dossier_images)
        self.dossier_images.mkdir(exist_ok=True)
        self.resultats = {}
    
    def telecharger_image(self, url: str, nom_fichier: str) -> Optional[str]:
        """Télécharge une image depuis une URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            chemin = self.dossier_images / nom_fichier
            with open(chemin, 'wb') as f:
                f.write(response.content)
            
            print(f"Image telechargee : {chemin}")
            return str(chemin)
        except Exception as e:
            print(f"Erreur lors du telechargement de {url}: {e}")
            return None
    
    def charger_image(self, chemin: str) -> Optional[np.ndarray]:
        """Charge une image depuis un fichier."""
        try:
            if not os.path.exists(chemin):
                print(f"Fichier non trouve : {chemin}")
                return None
            
            img = cv2.imread(chemin)
            if img is None:
                print(f"Impossible de charger l'image : {chemin}")
                return None
            
            return img
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
            return None
    
    def detecter_grille(self, image: np.ndarray) -> Optional[Dict]:
        """Détecte une grille dans l'image."""
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Appliquer un flou pour réduire le bruit
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Détecter les bords avec Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Détecter les lignes avec HoughLinesP
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                                minLineLength=50, maxLineGap=10)
        
        if lines is None:
            return None
        
        # Analyser les lignes pour trouver la grille
        lignes_horizontales = []
        lignes_verticales = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Détecter si la ligne est horizontale ou verticale
            if abs(y2 - y1) < 10:  # Ligne horizontale
                lignes_horizontales.append((y1 + y2) // 2)
            elif abs(x2 - x1) < 10:  # Ligne verticale
                lignes_verticales.append((x1 + x2) // 2)
        
        # Trier et dédupliquer
        lignes_horizontales = sorted(set(lignes_horizontales))
        lignes_verticales = sorted(set(lignes_verticales))
        
        if len(lignes_horizontales) < 2 or len(lignes_verticales) < 2:
            return None
        
        # Calculer les dimensions approximatives
        hauteur_approx = len(lignes_horizontales) - 1
        largeur_approx = len(lignes_verticales) - 1
        
        return {
            "lignes_horizontales": lignes_horizontales,
            "lignes_verticales": lignes_verticales,
            "dimensions_approx": (largeur_approx, hauteur_approx),
            "image_shape": image.shape[:2]
        }
    
    def analyser_zones_speciales(self, image: np.ndarray, grille_info: Dict) -> List[Dict]:
        """Analyse les zones spéciales dans l'image (eau, rocher, etc.)."""
        zones = []
        
        # Convertir en HSV pour une meilleure détection des couleurs
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Détecter les zones bleues (eau)
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Détecter les zones grises/brunes (rocher)
        lower_gray = np.array([0, 0, 50])
        upper_gray = np.array([180, 50, 200])
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
        
        # Analyser chaque case de la grille
        lignes_h = grille_info["lignes_horizontales"]
        lignes_v = grille_info["lignes_verticales"]
        
        for y_idx in range(len(lignes_h) - 1):
            for x_idx in range(len(lignes_v) - 1):
                y1, y2 = lignes_h[y_idx], lignes_h[y_idx + 1]
                x1, x2 = lignes_v[x_idx], lignes_v[x_idx + 1]
                
                # Extraire la région de la case
                region = image[y1:y2, x1:x2]
                region_hsv = hsv[y1:y2, x1:x2]
                
                # Vérifier la présence de zones spéciales
                zone_info = {
                    "position": (x_idx, y_idx),
                    "type": "normale"
                }
                
                # Détecter l'eau (bleu)
                blue_pixels = np.sum(cv2.inRange(region_hsv, lower_blue, upper_blue))
                if blue_pixels > (region.shape[0] * region.shape[1] * 0.1):
                    zone_info["type"] = "eau"
                
                # Détecter le rocher (gris/brun)
                gray_pixels = np.sum(cv2.inRange(region_hsv, lower_gray, upper_gray))
                if gray_pixels > (region.shape[0] * region.shape[1] * 0.3) and zone_info["type"] == "normale":
                    zone_info["type"] = "rocher"
                
                if zone_info["type"] != "normale":
                    zones.append(zone_info)
        
        return zones
    
    def analyser_plateau(self, chemin_image: str, nom_plateau: str) -> Dict:
        """Analyse complète d'un plateau."""
        print(f"\nAnalyse de {nom_plateau}...")
        
        image = self.charger_image(chemin_image)
        if image is None:
            return None
        
        # Détecter la grille
        grille_info = self.detecter_grille(image)
        if grille_info is None:
            print("Impossible de detecter la grille")
            return None
        
        print(f"Grille detectee : {grille_info['dimensions_approx']}")
        
        # Analyser les zones spéciales
        zones = self.analyser_zones_speciales(image, grille_info)
        print(f"Zones speciales detectees : {len(zones)}")
        
        resultat = {
            "nom_plateau": nom_plateau,
            "chemin_image": chemin_image,
            "dimensions_grille": grille_info["dimensions_approx"],
            "zones_speciales": zones,
            "image_shape": grille_info["image_shape"]
        }
        
        self.resultats[nom_plateau] = resultat
        return resultat
    
    def sauvegarder_resultats(self, fichier: str = "resultats_analyse_plateaux.json"):
        """Sauvegarde les résultats de l'analyse."""
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(self.resultats, f, ensure_ascii=False, indent=2)
        print(f"\nResultats sauvegardes dans {fichier}")
    
    def generer_rapport(self, fichier: str = "RAPPORT_ANALYSE_PLATEAUX.md"):
        """Génère un rapport Markdown des analyses."""
        with open(fichier, 'w', encoding='utf-8') as f:
            f.write("# Rapport d'Analyse des Plateaux\n\n")
            f.write("Ce rapport contient les résultats de l'analyse automatique des images de plateaux.\n\n")
            
            for nom, resultat in self.resultats.items():
                f.write(f"## {nom}\n\n")
                f.write(f"**Dimensions detectees** : {resultat['dimensions_grille'][0]} x {resultat['dimensions_grille'][1]} cases\n\n")
                f.write(f"**Taille de l'image** : {resultat['image_shape'][1]} x {resultat['image_shape'][0]} pixels\n\n")
                
                if resultat['zones_speciales']:
                    f.write("### Zones Speciales Detectees\n\n")
                    for zone in resultat['zones_speciales']:
                        f.write(f"- **{zone['type']}** à la position ({zone['position'][0]}, {zone['position'][1]})\n")
                else:
                    f.write("### Zones Speciales\n\n")
                    f.write("Aucune zone speciale detectee automatiquement.\n")
                
                f.write("\n---\n\n")
        
        print(f"Rapport genere : {fichier}")


def analyser_images_locales(dossier: str = "images_plateaux"):
    """Analyse toutes les images dans un dossier local."""
    analyseur = AnalyseurPlateau()
    
    dossier_path = Path(dossier)
    if not dossier_path.exists():
        print(f"Le dossier {dossier} n'existe pas.")
        print("Placez les images des plateaux dans ce dossier.")
        return
    
    # Rechercher les images
    extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    images = []
    for ext in extensions:
        images.extend(dossier_path.glob(f'*{ext}'))
        images.extend(dossier_path.glob(f'*{ext.upper()}'))
    
    if not images:
        print(f"Aucune image trouvee dans {dossier}")
        print("Placez les images des plateaux dans ce dossier avec des noms descriptifs.")
        return
    
    print(f"Trouve {len(images)} image(s) a analyser")
    
    for img_path in images:
        nom_plateau = img_path.stem
        analyseur.analyser_plateau(str(img_path), nom_plateau)
    
    # Sauvegarder les résultats
    analyseur.sauvegarder_resultats()
    analyseur.generer_rapport()


def telecharger_et_analyser(urls: Dict[str, str]):
    """Télécharge et analyse des images depuis des URLs."""
    analyseur = AnalyseurPlateau()
    
    for nom, url in urls.items():
        nom_fichier = f"{nom}.jpg"
        chemin = analyseur.telecharger_image(url, nom_fichier)
        
        if chemin:
            analyseur.analyser_plateau(chemin, nom)
    
    # Sauvegarder les résultats
    analyseur.sauvegarder_resultats()
    analyseur.generer_rapport()


if __name__ == "__main__":
    print("=== Analyseur d'Images de Plateaux Ark Nova ===\n")
    
    # Option 1 : Analyser les images locales
    print("Recherche d'images locales dans 'images_plateaux/'...")
    analyser_images_locales()
    
    # Option 2 : Télécharger depuis des URLs (exemple)
    # urls = {
    #     "plateau_A": "https://example.com/plateau_A.jpg",
    #     "plateau_1": "https://example.com/plateau_1.jpg",
    # }
    # telecharger_et_analyser(urls)
    
    print("\n[OK] Analyse terminee !")
    print("\nInstructions :")
    print("1. Placez les images des plateaux dans le dossier 'images_plateaux/'")
    print("2. Nommez les fichiers avec des noms descriptifs (ex: plateau_A.jpg, plateau_1.jpg)")
    print("3. Relancez ce script pour analyser les images")


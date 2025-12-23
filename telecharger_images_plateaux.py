"""
Script pour télécharger des images de plateaux depuis des sources en ligne.
Ce script recherche et télécharge des images de plateaux d'Ark Nova.
"""

import os
import requests
from pathlib import Path
from typing import List, Optional
import time

class TelechargeurImages:
    """Classe pour télécharger des images de plateaux."""
    
    def __init__(self, dossier: str = "images_plateaux"):
        self.dossier = Path(dossier)
        self.dossier.mkdir(exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def telecharger(self, url: str, nom_fichier: str) -> bool:
        """Télécharge une image depuis une URL."""
        try:
            print(f"Telechargement de {url}...")
            response = requests.get(url, headers=self.headers, timeout=15, stream=True)
            response.raise_for_status()
            
            chemin = self.dossier / nom_fichier
            with open(chemin, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  -> Sauvegarde dans {chemin}")
            return True
        except Exception as e:
            print(f"  -> Erreur : {e}")
            return False
    
    def telecharger_liste(self, urls: List[tuple]):
        """Télécharge une liste d'URLs."""
        print(f"\nTelechargement de {len(urls)} image(s)...\n")
        
        for url, nom_fichier in urls:
            self.telecharger(url, nom_fichier)
            time.sleep(1)  # Pause pour éviter de surcharger le serveur
        
        print(f"\n[OK] Telechargement termine !")
        print(f"Images sauvegardees dans : {self.dossier.absolute()}")


# URLs potentielles d'images de plateaux (à compléter avec de vraies URLs)
URLS_PLATEAUX = [
    # Format : (URL, nom_fichier)
    # Exemple :
    # ("https://example.com/plateau_A.jpg", "plateau_A.jpg"),
    # ("https://example.com/plateau_1.jpg", "plateau_1.jpg"),
]

def rechercher_images_bgg():
    """Recherche des images sur BoardGameGeek."""
    print("Recherche d'images sur BoardGameGeek...")
    print("Note : Les URLs exactes doivent etre trouvees manuellement sur BGG")
    print("Allez sur https://boardgamegeek.com/boardgame/285774/ark-nova")
    print("et consultez la section 'Images' pour trouver les URLs des plateaux")


if __name__ == "__main__":
    print("=== Telechargeur d'Images de Plateaux ===\n")
    
    telechargeur = TelechargeurImages()
    
    if URLS_PLATEAUX:
        telechargeur.telecharger_liste(URLS_PLATEAUX)
    else:
        print("Aucune URL configuree.")
        print("\nPour utiliser ce script :")
        print("1. Trouvez les URLs des images de plateaux")
        print("2. Ajoutez-les dans la liste URLS_PLATEAUX")
        print("3. Relancez le script")
        print("\nSources possibles :")
        print("- BoardGameGeek (section Images)")
        print("- Sites de vente en ligne (Philibert, etc.)")
        print("- Forums de joueurs")
        print("- YouTube (captures d'ecran)")
        
        rechercher_images_bgg()


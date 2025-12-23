"""
Script pour documenter les configurations des plateaux d'Ark Nova → Armures Méca
Ce script aide à structurer et valider les configurations des grilles.
"""

import json
from typing import Dict, List, Optional, Tuple

# Structure de base pour un plateau
PLATEAU_TEMPLATE = {
    "plateau_id": None,
    "nom_original": "",
    "nom_timeline_ranger": "",
    "type": "",  # Débutant, Standard, Avancé, Spécialisé
    "difficulte": "",  # Facile, Moyen, Difficile
    "grille": {
        "dimensions": {
            "largeur": None,
            "hauteur": None
        },
        "total_cases": None,
        "cases_utilisables": None,
        "cases_bloquees": [],  # Liste de tuples (x, y) ou coordonnées
        "zones_speciales": []  # Liste de dicts avec type, positions, effets
    },
    "capacite_speciale": {
        "nom": "",
        "description": "",
        "effet": ""
    },
    "bonus_initiaux": [],  # Liste de bonus
    "contraintes": {}  # Dict de contraintes spécifiques
}

# Liste des plateaux identifiés
PLATEAUX_IDENTIFIES = [
    {"id": "A", "nom": "Plateau A", "type": "Débutant", "armure": "Armure Méca Débutante"},
    {"id": "0", "nom": "Plateau 0", "type": "Standard", "armure": "Armure Méca Standard"},
    {"id": "1", "nom": "Plateau 1", "type": "Avancé", "armure": "Armure Méca Type 1"},
    {"id": "2", "nom": "Plateau 2", "type": "Avancé", "armure": "Armure Méca Type 2"},
    {"id": "3", "nom": "Plateau 3", "type": "Avancé", "armure": "Armure Méca Type 3"},
    {"id": "4", "nom": "Plateau 4", "type": "Avancé", "armure": "Armure Méca Type 4"},
    {"id": "5", "nom": "Plateau 5", "type": "Avancé", "armure": "Armure Méca Type 5"},
    {"id": "6", "nom": "Plateau 6", "type": "Avancé", "armure": "Armure Méca Type 6"},
    {"id": "7", "nom": "Plateau 7", "type": "Avancé", "armure": "Armure Méca Type 7"},
    {"id": "8", "nom": "Plateau 8", "type": "Avancé", "armure": "Armure Méca Type 8"},
    {"id": "11", "nom": "Plateau 11 : Grottes", "type": "Spécialisé", "armure": "Armure Méca Grottes"},
    {"id": "12", "nom": "Plateau 12 : Intelligence Artificielle", "type": "Spécialisé", "armure": "Armure Méca Intelligence Artificielle"},
    {"id": "13", "nom": "Plateau 13 : Planche à Dessin", "type": "Spécialisé", "armure": "Armure Méca Planche à Dessin"},
    {"id": "14", "nom": "Plateau 14 : Lagon", "type": "Spécialisé", "armure": "Armure Méca Lagon"},
    {"id": "T1", "nom": "Plateau Tournoi 1", "type": "Spécialisé", "armure": "Armure Méca Tournoi"},
]

def creer_plateau_vide(plateau_id: str, nom: str, armure: str, type_plateau: str) -> Dict:
    """Crée une structure vide pour un plateau."""
    plateau = PLATEAU_TEMPLATE.copy()
    plateau["plateau_id"] = plateau_id
    plateau["nom_original"] = nom
    plateau["nom_timeline_ranger"] = armure
    plateau["type"] = type_plateau
    
    if type_plateau == "Débutant":
        plateau["difficulte"] = "Facile"
    elif type_plateau == "Standard":
        plateau["difficulte"] = "Moyen"
    else:
        plateau["difficulte"] = "Difficile"
    
    return plateau

def valider_grille(grille: Dict) -> Tuple[bool, List[str]]:
    """Valide qu'une grille a toutes les informations nécessaires."""
    erreurs = []
    
    if grille["dimensions"]["largeur"] is None:
        erreurs.append("Largeur de la grille manquante")
    if grille["dimensions"]["hauteur"] is None:
        erreurs.append("Hauteur de la grille manquante")
    if grille["total_cases"] is None:
        erreurs.append("Nombre total de cases manquant")
    if grille["cases_utilisables"] is None:
        erreurs.append("Nombre de cases utilisables manquant")
    
    # Vérifier la cohérence
    if (grille["dimensions"]["largeur"] is not None and 
        grille["dimensions"]["hauteur"] is not None and
        grille["total_cases"] is not None):
        largeur = grille["dimensions"]["largeur"]
        hauteur = grille["dimensions"]["hauteur"]
        total_attendu = largeur * hauteur
        if grille["total_cases"] != total_attendu:
            erreurs.append(f"Incohérence : {largeur}x{hauteur} = {total_attendu} cases, mais total_cases = {grille['total_cases']}")
    
    return len(erreurs) == 0, erreurs

def generer_grille_vide(largeur: int, hauteur: int) -> List[List[str]]:
    """Génère une représentation textuelle d'une grille vide."""
    grille = []
    for y in range(hauteur):
        ligne = []
        for x in range(largeur):
            ligne.append(".")
        grille.append(ligne)
    return grille

def marquer_case_bloquee(grille: List[List[str]], x: int, y: int):
    """Marque une case comme bloquée dans la grille."""
    if 0 <= y < len(grille) and 0 <= x < len(grille[y]):
        grille[y][x] = "X"

def marquer_zone_speciale(grille: List[List[str]], x: int, y: int, type_zone: str):
    """Marque une zone spéciale dans la grille."""
    if 0 <= y < len(grille) and 0 <= x < len(grille[y]):
        symboles = {
            "eau": "~",
            "rocher": "#",
            "grotte": "C",
            "technologie": "T",
            "lagon": "L"
        }
        symbole = symboles.get(type_zone.lower(), "?")
        grille[y][x] = symbole

def afficher_grille(grille: List[List[str]]):
    """Affiche une grille de manière lisible."""
    print("  ", end="")
    for x in range(len(grille[0])):
        print(f"{x:2}", end="")
    print()
    for y, ligne in enumerate(grille):
        print(f"{y:2} ", end="")
        for case in ligne:
            print(f"{case:2}", end="")
        print()

def sauvegarder_configurations(plateaux: List[Dict], fichier: str = "configurations_plateaux.json"):
    """Sauvegarde les configurations dans un fichier JSON."""
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(plateaux, f, ensure_ascii=False, indent=2)
    print(f"Configurations sauvegardées dans {fichier}")

def charger_configurations(fichier: str = "configurations_plateaux.json") -> List[Dict]:
    """Charge les configurations depuis un fichier JSON."""
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Fichier {fichier} non trouvé. Création d'une nouvelle structure.")
        return []

def creer_tous_plateaux_vides() -> List[Dict]:
    """Crée des structures vides pour tous les plateaux identifiés."""
    plateaux = []
    for p in PLATEAUX_IDENTIFIES:
        plateau = creer_plateau_vide(p["id"], p["nom"], p["armure"], p["type"])
        plateaux.append(plateau)
    return plateaux

def exporter_markdown(plateaux: List[Dict], fichier: str = "CONFIGURATIONS_PLATEAUX_DETAILLES.md"):
    """Exporte les configurations en format Markdown."""
    with open(fichier, 'w', encoding='utf-8') as f:
        f.write("# Configurations Détaillées des Plateaux → Armures Méca\n\n")
        f.write("Ce document contient les configurations détaillées de chaque plateau.\n\n")
        
        for plateau in plateaux:
            f.write(f"## {plateau['nom_timeline_ranger']}\n\n")
            f.write(f"**ID** : {plateau['plateau_id']}\n\n")
            f.write(f"**Nom Original** : {plateau['nom_original']}\n\n")
            f.write(f"**Type** : {plateau['type']}\n\n")
            f.write(f"**Difficulté** : {plateau['difficulte']}\n\n")
            
            # Grille
            f.write("### Configuration de la Grille\n\n")
            grille = plateau['grille']
            if grille['dimensions']['largeur'] and grille['dimensions']['hauteur']:
                f.write(f"- **Dimensions** : {grille['dimensions']['largeur']} x {grille['dimensions']['hauteur']} cases\n")
            else:
                f.write("- **Dimensions** : À documenter\n")
            
            if grille['total_cases']:
                f.write(f"- **Total cases** : {grille['total_cases']}\n")
            else:
                f.write("- **Total cases** : À documenter\n")
            
            if grille['cases_utilisables']:
                f.write(f"- **Cases utilisables** : {grille['cases_utilisables']}\n")
            else:
                f.write("- **Cases utilisables** : À documenter\n")
            
            if grille['cases_bloquees']:
                f.write(f"- **Cases bloquées** : {len(grille['cases_bloquees'])} cases\n")
                f.write("  - Positions : " + ", ".join([f"({x}, {y})" for x, y in grille['cases_bloquees']]) + "\n")
            else:
                f.write("- **Cases bloquées** : Aucune (ou à documenter)\n")
            
            # Zones spéciales
            f.write("\n### Zones Spéciales\n\n")
            if grille['zones_speciales']:
                for zone in grille['zones_speciales']:
                    f.write(f"- **{zone.get('type', 'Zone')}** : {zone.get('description', '')}\n")
                    if zone.get('positions'):
                        f.write("  - Positions : " + ", ".join([f"({x}, {y})" for x, y in zone['positions']]) + "\n")
            else:
                f.write("- Aucune zone spéciale (ou à documenter)\n")
            
            # Capacité spéciale
            f.write("\n### Capacité Spéciale\n\n")
            cap = plateau['capacite_speciale']
            if cap.get('nom'):
                f.write(f"- **Nom** : {cap['nom']}\n")
                f.write(f"- **Description** : {cap.get('description', 'À documenter')}\n")
                f.write(f"- **Effet** : {cap.get('effet', 'À documenter')}\n")
            else:
                f.write("- À documenter\n")
            
            # Bonus initiaux
            if plateau.get('bonus_initiaux'):
                f.write("\n### Bonus Initiaux\n\n")
                for bonus in plateau['bonus_initiaux']:
                    f.write(f"- {bonus}\n")
            
            f.write("\n---\n\n")
    
    print(f"Documentation Markdown exportée dans {fichier}")

if __name__ == "__main__":
    print("=== Script de Documentation des Configurations de Plateaux ===\n")
    
    # Créer les structures vides pour tous les plateaux
    print("Création des structures vides pour tous les plateaux identifiés...")
    plateaux = creer_tous_plateaux_vides()
    
    # Sauvegarder en JSON
    sauvegarder_configurations(plateaux)
    
    # Exporter en Markdown
    exporter_markdown(plateaux)
    
    print("\n[OK] Structures creees avec succes !")
    print("\nProchaines etapes :")
    print("1. Ouvrir le fichier JSON pour remplir les configurations")
    print("2. Utiliser les fonctions de validation pour verifier la coherence")
    print("3. Re-exporter en Markdown une fois les configurations completees")


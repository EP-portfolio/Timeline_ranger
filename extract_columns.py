# -*- coding: utf-8 -*-
"""
Script pour extraire toutes les colonnes des feuilles du fichier ODS Ark Nova
"""
import pandas as pd
import os
import sys

# Forcer l'encodage UTF-8 pour la console Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def extract_columns_from_ods(ods_file: str):
    """Extrait toutes les colonnes des trois feuilles principales"""
    
    if not os.path.exists(ods_file):
        print(f"[ERREUR] Fichier ODS non trouve : {ods_file}")
        return
    
    # D'abord, lister toutes les feuilles disponibles
    print("=" * 80)
    print("FEUILLES DISPONIBLES DANS LE FICHIER ODS")
    print("=" * 80)
    try:
        xl_file = pd.ExcelFile(ods_file, engine='odf')
        sheet_names = xl_file.sheet_names
        print(f"\nFeuilles trouvees ({len(sheet_names)} feuilles) :")
        for i, sheet in enumerate(sheet_names, 1):
            print(f"  {i}. {sheet}")
    except Exception as e:
        print(f"[ERREUR] Impossible de lire les feuilles : {e}")
        return
    
    print("\n" + "=" * 80)
    print("EXTRACTION DES COLONNES DU FICHIER ODS ARK NOVA")
    print("=" * 80)
    
    # ============================================================================
    # FEUILLE 1 : ANIMAL (Cartes Animaux)
    # ============================================================================
    print("\n" + "=" * 80)
    print("FEUILLE : Animal (Cartes Animaux)")
    print("=" * 80)
    
    try:
        df_animal = pd.read_excel(ods_file, sheet_name=sheet_names[1], engine='odf')  # Index 1 = Animal
        print(f"\nNombre de lignes : {len(df_animal)}")
        print(f"\nCOLONNES ({len(df_animal.columns)} colonnes) :")
        print("-" * 80)
        for i, col in enumerate(df_animal.columns, 1):
            print(f"{i:2d}. {col}")
        
        # Afficher un exemple de ligne pour voir les valeurs
        if len(df_animal) > 0:
            print("\n" + "-" * 80)
            print("EXEMPLE DE PREMIERE LIGNE :")
            print("-" * 80)
            first_row = df_animal.iloc[0]
            for col in df_animal.columns:
                value = first_row[col]
                if pd.notna(value):
                    print(f"  {col}: {value}")
    except Exception as e:
        print(f"[ERREUR] Impossible de lire la feuille 'Animal': {e}")
        import traceback
        traceback.print_exc()
    
    # ============================================================================
    # FEUILLE 2 : MECENE (Cartes Meceenes)
    # ============================================================================
    print("\n" + "=" * 80)
    print("FEUILLE : Mecene (Cartes Meceenes)")
    print("=" * 80)
    
    try:
        df_mecene = pd.read_excel(ods_file, sheet_name=sheet_names[2], engine='odf')  # Index 2 = Mecene
        print(f"\n[OK] Feuille trouvee : '{sheet_names[2]}'")
        print(f"Nombre de lignes : {len(df_mecene)}")
        print(f"\nCOLONNES ({len(df_mecene.columns)} colonnes) :")
        print("-" * 80)
        for i, col in enumerate(df_mecene.columns, 1):
            print(f"{i:2d}. {col}")
        
        # Afficher un exemple de ligne
        if len(df_mecene) > 0:
            print("\n" + "-" * 80)
            print("EXEMPLE DE PREMIERE LIGNE :")
            print("-" * 80)
            first_row = df_mecene.iloc[0]
            for col in df_mecene.columns:
                value = first_row[col]
                if pd.notna(value):
                    print(f"  {col}: {value}")
    except Exception as e:
        print(f"[ERREUR] Impossible de lire la feuille Mecene: {e}")
        import traceback
        traceback.print_exc()
    
    # ============================================================================
    # FEUILLE 3 : PROJET_DE_CONSERVATION (Cartes Projets de Conservation)
    # ============================================================================
    print("\n" + "=" * 80)
    print("FEUILLE : Projet_de_conservation (Cartes Projets de Conservation)")
    print("=" * 80)
    
    try:
        df_projet = pd.read_excel(ods_file, sheet_name=sheet_names[3], engine='odf')  # Index 3 = Projet_de_conservation
        print(f"\n[OK] Feuille trouvee : '{sheet_names[3]}'")
        print(f"Nombre de lignes : {len(df_projet)}")
        print(f"\nCOLONNES ({len(df_projet.columns)} colonnes) :")
        print("-" * 80)
        for i, col in enumerate(df_projet.columns, 1):
            print(f"{i:2d}. {col}")
        
        # Afficher un exemple de ligne
        if len(df_projet) > 0:
            print("\n" + "-" * 80)
            print("EXEMPLE DE PREMIERE LIGNE :")
            print("-" * 80)
            first_row = df_projet.iloc[0]
            for col in df_projet.columns:
                value = first_row[col]
                if pd.notna(value):
                    print(f"  {col}: {value}")
    except Exception as e:
        print(f"[ERREUR] Impossible de lire la feuille Projet de Conservation: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("EXTRACTION TERMINEE")
    print("=" * 80)


if __name__ == "__main__":
    ods_file = "Ark_Nova_Mondes_marins_cartes_stats_FR.ods"
    
    if not os.path.exists(ods_file):
        print(f"[ERREUR] Fichier ODS non trouve : {ods_file}")
        print("Assurez-vous que le fichier est dans le meme dossier que le script.")
        exit(1)
    
    extract_columns_from_ods(ods_file)

"""
Script pour exécuter la migration SQL MIGRATION_ADD_COLUMNS_CARTES.sql
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du backend au PYTHONPATH
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.core.database import Database
from app.core.config import settings


def run_migration():
    """Exécute la migration SQL pour ajouter les colonnes manquantes."""
    
    print("=" * 80)
    print("EXÉCUTION DE LA MIGRATION : Ajout des colonnes manquantes")
    print("=" * 80)
    print()
    
    # Lire le fichier SQL
    migration_file = Path(__file__).parent / "MIGRATION_ADD_COLUMNS_CARTES.sql"
    
    if not migration_file.exists():
        print(f"[ERREUR] Fichier de migration non trouvé : {migration_file}")
        return False
    
    print(f"[INFO] Lecture du fichier : {migration_file}")
    with open(migration_file, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    # Initialiser la connexion à la base de données
    print(f"[INFO] Connexion à la base de données...")
    print(f"      Host: {settings.SUPABASE_HOST}")
    print(f"      Port: {settings.SUPABASE_PORT}")
    print(f"      Database: {settings.SUPABASE_DB}")
    print(f"      User: {settings.SUPABASE_USER}")
    print()
    
    try:
        Database.initialize()
        
        # Exécuter la migration
        print("[INFO] Exécution de la migration...")
        print()
        
        from psycopg2.extras import RealDictCursor
        
        with Database.get_connection() as conn:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Exécuter chaque commande SQL séparément
            # (psycopg2 ne supporte pas l'exécution de plusieurs commandes en une fois)
            commands = []
            current_command = []
            
            for line in sql_content.split('\n'):
                # Ignorer les lignes vides et les commentaires
                stripped = line.strip()
                if not stripped or stripped.startswith('--'):
                    continue
                
                current_command.append(line)
                
                # Si la ligne se termine par un point-virgule, c'est la fin d'une commande
                if stripped.endswith(';'):
                    command = '\n'.join(current_command)
                    if command.strip():
                        commands.append(command)
                    current_command = []
            
            # Exécuter toutes les commandes
            executed = 0
            for i, command in enumerate(commands, 1):
                try:
                    print(f"[{i}/{len(commands)}] Exécution de la commande...")
                    cur.execute(command)
                    executed += 1
                except Exception as e:
                    # Si la colonne existe déjà, ce n'est pas grave (IF NOT EXISTS)
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"      [WARN] Colonne/Index deja existant(e), ignore(e)")
                    else:
                        print(f"      [ERREUR] Erreur : {e}")
                        raise
            
            # Commit des changements
            conn.commit()
            print()
            print(f"[OK] Migration terminée avec succès !")
            print(f"     {executed}/{len(commands)} commandes exécutées")
            print()
            
            # Vérifier que les colonnes ont été ajoutées
            print("[INFO] Vérification des colonnes ajoutées...")
            print()
            
            # Vérifier troupes
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'troupes' 
                AND column_name IN ('effet_du_vide', 'conditions', 'vague', 'jeu_base', 'jeu_mondes_marins', 'promo')
                ORDER BY column_name
            """)
            troupes_cols = cur.fetchall()
            print("Table TROUPES :")
            if troupes_cols:
                for col in troupes_cols:
                    print(f"  [OK] {col['column_name']} ({col['data_type']})")
            else:
                print("  [WARN] Aucune colonne trouvee")
            
            # Vérifier technologies
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'technologies' 
                AND column_name IN ('conditions', 'vague', 'jeu_base', 'jeu_mondes_marins', 'promo', 'remplacee_par')
                ORDER BY column_name
            """)
            tech_cols = cur.fetchall()
            print()
            print("Table TECHNOLOGIES :")
            if tech_cols:
                for col in tech_cols:
                    print(f"  [OK] {col['column_name']} ({col['data_type']})")
            else:
                print("  [WARN] Aucune colonne trouvee")
            
            # Vérifier quetes
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'quetes' 
                AND column_name IN ('bonus', 'vague', 'jeu_base', 'jeu_mondes_marins', 'remplacee_par')
                ORDER BY column_name
            """)
            quetes_cols = cur.fetchall()
            print()
            print("Table QUETES :")
            if quetes_cols:
                for col in quetes_cols:
                    print(f"  [OK] {col['column_name']} ({col['data_type']})")
            else:
                print("  [WARN] Aucune colonne trouvee")
            
            cur.close()
        
        Database.close()
        print()
        print("=" * 80)
        print("MIGRATION REUSSIE [OK]")
        print("=" * 80)
        return True
        
    except Exception as e:
        print()
        print(f"[ERREUR] Erreur lors de la migration : {e}")
        print()
        import traceback
        traceback.print_exc()
        Database.close()
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)


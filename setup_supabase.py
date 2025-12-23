"""
Script d'aide pour configurer Supabase rapidement
Ce script vérifie la connexion et guide l'utilisateur
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Vérifie si le fichier .env existe."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("[ERREUR] Fichier .env non trouve !")
        print("\nCreation du fichier .env...")
        
        # Créer .env depuis .env.example
        example_file = Path('.env.example')
        if example_file.exists():
            with open(example_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("[OK] Fichier .env cree depuis .env.example")
            print("\n[IMPORTANT] Modifiez le fichier .env avec vos informations Supabase !")
            print("   - SUPABASE_HOST")
            print("   - SUPABASE_PASSWORD")
            return False
        else:
            print("[ERREUR] Fichier .env.example non trouve non plus !")
            return False
    
    return True

def check_env_variables():
    """Vérifie que les variables d'environnement sont définies."""
    load_dotenv()
    
    required_vars = [
        'SUPABASE_HOST',
        'SUPABASE_DB',
        'SUPABASE_USER',
        'SUPABASE_PASSWORD',
        'SUPABASE_PORT'
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('xxxxx') or value.startswith('votre_'):
            missing.append(var)
    
    if missing:
        print(f"[ERREUR] Variables d'environnement manquantes ou non configurees :")
        for var in missing:
            print(f"   - {var}")
        print("\n[IMPORTANT] Modifiez le fichier .env avec vos informations Supabase !")
        return False
    
    return True

def test_connection():
    """Teste la connexion à Supabase."""
    try:
        import psycopg2
        
        load_dotenv()
        
        conn = psycopg2.connect(
            host=os.getenv('SUPABASE_HOST'),
            database=os.getenv('SUPABASE_DB'),
            user=os.getenv('SUPABASE_USER'),
            password=os.getenv('SUPABASE_PASSWORD'),
            port=os.getenv('SUPABASE_PORT'),
            sslmode='require'
        )
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        cur.close()
        conn.close()
        
        print("[OK] Connexion a Supabase reussie !")
        print(f"   Version PostgreSQL : {version[0][:50]}...")
        return True
        
    except ImportError:
        print("[ERREUR] psycopg2-binary n'est pas installe")
        print("   Installez-le avec : pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"[ERREUR] Erreur de connexion : {e}")
        print("\nVérifiez :")
        print("   - Que vos credentials Supabase sont corrects dans .env")
        print("   - Que votre projet Supabase est actif")
        print("   - Que vous avez accès à Internet")
        return False

def check_schema():
    """Vérifie que le schéma est créé."""
    try:
        import psycopg2
        
        load_dotenv()
        
        conn = psycopg2.connect(
            host=os.getenv('SUPABASE_HOST'),
            database=os.getenv('SUPABASE_DB'),
            user=os.getenv('SUPABASE_USER'),
            password=os.getenv('SUPABASE_PASSWORD'),
            port=os.getenv('SUPABASE_PORT'),
            sslmode='require'
        )
        
        cur = conn.cursor()
        
        # Vérifier les tables principales
        required_tables = [
            'rangers', 'weapon_types', 'raw_materials', 
            'troupes', 'technologies', 'quetes'
        ]
        
        missing_tables = []
        for table in required_tables:
            cur.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """)
            exists = cur.fetchone()[0]
            if not exists:
                missing_tables.append(table)
        
        cur.close()
        conn.close()
        
        if missing_tables:
            print(f"[ERREUR] Tables manquantes : {', '.join(missing_tables)}")
            print("\n[IMPORTANT] Executez d'abord le schema SQL dans Supabase !")
            print("   1. Ouvrez Supabase SQL Editor")
            print("   2. Copiez le contenu de SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql")
            print("   3. Executez le script")
            return False
        
        print("[OK] Schema verifie : Toutes les tables existent")
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la verification du schema : {e}")
        return False

def main():
    """Fonction principale."""
    print("=" * 60)
    print("Configuration Supabase - Timeline Ranger")
    print("=" * 60)
    print()
    
    # Étape 1 : Vérifier .env
    print("Etape 1 : Verification du fichier .env...")
    if not check_env_file():
        print("\n[ERREUR] Configuration incomplete. Veuillez remplir le fichier .env")
        return
    
    # Étape 2 : Vérifier les variables
    print("\nEtape 2 : Verification des variables d'environnement...")
    if not check_env_variables():
        print("\n[ERREUR] Configuration incomplete. Veuillez remplir le fichier .env")
        return
    
    print("[OK] Variables d'environnement configurees")
    
    # Étape 3 : Tester la connexion
    print("\nEtape 3 : Test de connexion a Supabase...")
    if not test_connection():
        return
    
    # Étape 4 : Vérifier le schéma
    print("\nEtape 4 : Verification du schema...")
    if not check_schema():
        return
    
    # Tout est OK
    print("\n" + "=" * 60)
    print("[OK] Configuration Supabase complete !")
    print("=" * 60)
    print("\nProchaines etapes :")
    print("   1. Executer : python SCRIPT_IMPORT_MAPPED_DATA.py")
    print("   2. Verifier les donnees dans Supabase SQL Editor")
    print("   3. Commencer a developper le backend API")

if __name__ == "__main__":
    main()


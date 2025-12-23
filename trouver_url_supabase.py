"""
Script pour aider à trouver et configurer l'URL Supabase
"""

def extract_db_url_from_api_url(api_url):
    """Extrait l'URL de la base de données depuis l'URL API."""
    # Enlever https:// et .supabase.co
    if api_url.startswith('https://'):
        api_url = api_url[8:]
    if api_url.endswith('.supabase.co'):
        project_id = api_url[:-12]  # Enlever .supabase.co
        db_url = f"db.{project_id}.supabase.co"
        return db_url
    return None

def main():
    print("=" * 60)
    print("Aide pour Trouver l'URL Supabase")
    print("=" * 60)
    print()
    
    print("Dans Supabase, il y a deux types d'URLs :")
    print("1. URL API : https://xxxxx.supabase.co (pour l'API REST)")
    print("2. URL Database : db.xxxxx.supabase.co (pour PostgreSQL)")
    print()
    
    print("📋 Où trouver l'URL Database :")
    print("   1. Allez dans Settings → Database")
    print("   2. Cherchez 'Connection string' ou 'Connection info'")
    print("   3. L'URL commence par 'db.' et se termine par '.supabase.co'")
    print()
    
    # Demander l'URL API si disponible
    api_url = input("Si vous avez l'URL API (https://xxxxx.supabase.co), collez-la ici (ou Entrée pour ignorer) : ").strip()
    
    if api_url:
        db_url = extract_db_url_from_api_url(api_url)
        if db_url:
            print(f"\n[OK] URL Database calculee : {db_url}")
            print("\nVotre fichier .env devrait contenir :")
            print(f"SUPABASE_HOST={db_url}")
            print("SUPABASE_DB=postgres")
            print("SUPABASE_USER=postgres")
            print("SUPABASE_PASSWORD=votre_mot_de_passe")
            print("SUPABASE_PORT=5432")
        else:
            print("\n[ERREUR] Impossible d'extraire l'URL. Verifiez le format.")
    else:
        print("\n📝 Instructions manuelles :")
        print("   1. Allez dans Supabase → Settings → Database")
        print("   2. Copiez l'URL qui commence par 'db.'")
        print("   3. Collez-la dans votre fichier .env comme SUPABASE_HOST")
        print()
        print("   Format attendu : db.xxxxx.supabase.co")
    
    print("\n" + "=" * 60)
    print("💡 Astuce : L'URL Database est toujours :")
    print("   db.[PROJECT_ID].supabase.co")
    print("   où [PROJECT_ID] est l'ID de votre projet Supabase")
    print("=" * 60)

if __name__ == "__main__":
    main()


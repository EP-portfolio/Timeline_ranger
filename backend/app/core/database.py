"""
Gestion de la connexion à la base de données PostgreSQL (Supabase)
"""
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator, Optional
import os
from app.core.config import settings


class Database:
    """Gestionnaire de pool de connexions PostgreSQL."""
    
    _pool: Optional[pool.SimpleConnectionPool] = None
    
    @classmethod
    def initialize(cls):
        """Initialise le pool de connexions."""
        if cls._pool is None:
            try:
                # Utiliser le port du pooler (6543) ou port direct (5432)
                port = int(settings.SUPABASE_PORT)
                # Permet d'utiliser un host de pooler dédié ou forcer l'IPv4 si nécessaire
                host = settings.SUPABASE_POOLER_HOST or settings.SUPABASE_HOST
                hostaddr = settings.SUPABASE_HOST_IPV4
                cls._pool = psycopg2.pool.SimpleConnectionPool(
                    1,  # minconn
                    20,  # maxconn
                    host=host,
                    database=settings.SUPABASE_DB,
                    user=settings.SUPABASE_USER,
                    password=settings.SUPABASE_PASSWORD,
                    port=port,
                    hostaddr=hostaddr if hostaddr else None,
                    sslmode='require'  # Supabase requiert SSL
                )
                if cls._pool:
                    print(f"[OK] Pool de connexions PostgreSQL initialise (host {host}, port {port}, hostaddr {hostaddr})")
                else:
                    print("[ERREUR] Echec de l'initialisation du pool")
            except Exception as e:
                print(f"[ERREUR] Erreur lors de l'initialisation du pool : {e}")
                raise
    
    @classmethod
    def close(cls):
        """Ferme toutes les connexions du pool."""
        if cls._pool:
            cls._pool.closeall()
            print("[OK] Pool de connexions ferme")
    
    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator[psycopg2.extensions.connection, None, None]:
        """Obtient une connexion du pool (context manager)."""
        if cls._pool is None:
            cls.initialize()
        
        if cls._pool is None:
            raise Exception("Pool de connexions non initialisé")
        
        conn = None
        try:
            conn = cls._pool.getconn()
            if conn is None:
                raise Exception("Impossible d'obtenir une connexion du pool")
            yield conn
        except Exception as e:
            print(f"[ERREUR] Erreur lors de l'obtention de la connexion : {e}")
            raise
        finally:
            if conn and cls._pool:
                cls._pool.putconn(conn)
    
    @classmethod
    @contextmanager
    def get_cursor(cls, commit: bool = False) -> Generator[RealDictCursor, None, None]:
        """Obtient un curseur avec une connexion (context manager)."""
        with cls.get_connection() as conn:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cur
                if commit:
                    conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()


# Initialisation lazy : le pool sera créé à la première utilisation
# Cela évite de bloquer le démarrage si la DB n'est pas accessible immédiatement


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
                # Utiliser le host standard (le pooler utilise le même host)
                host = settings.SUPABASE_HOST

                # Forcer IPv4 en résolvant le host en IPv4
                import socket

                try:
                    # Résoudre le host en IPv4
                    ipv4 = socket.gethostbyname(host)
                    print(f"[INFO] Host {host} résolu en IPv4: {ipv4}")
                except socket.gaierror as e:
                    print(f"[ERREUR] Impossible de résoudre {host} en IPv4: {e}")
                    ipv4 = None

                cls._pool = psycopg2.pool.SimpleConnectionPool(
                    1,  # minconn
                    20,  # maxconn
                    host=host,
                    hostaddr=ipv4,  # Forcer IPv4 pour éviter les problèmes IPv6
                    database=settings.SUPABASE_DB,
                    user=settings.SUPABASE_USER,
                    password=settings.SUPABASE_PASSWORD,
                    port=port,
                    sslmode="require",  # Supabase requiert SSL
                )
                if cls._pool:
                    print(
                        f"[OK] Pool de connexions PostgreSQL initialise (host {host}, port {port}, hostaddr {hostaddr})"
                    )
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

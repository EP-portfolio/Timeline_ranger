"""
Modèles de données pour les utilisateurs (accès DB)
"""
from typing import Optional
from datetime import datetime
from app.core.database import Database


class UserModel:
    """Modèle pour gérer les utilisateurs dans la base de données."""
    
    @staticmethod
    def create(email: str, password_hash: str, username: Optional[str] = None) -> dict:
        """Crée un nouvel utilisateur."""
        with Database.get_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO users (email, password_hash, username)
                VALUES (%s, %s, %s)
                RETURNING id, email, username, created_at, last_login, is_active
            """, (email, password_hash, username))
            return dict(cur.fetchone())
    
    @staticmethod
    def get_by_email(email: str) -> Optional[dict]:
        """Récupère un utilisateur par email."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, email, password_hash, username, created_at, last_login, is_active
                FROM users
                WHERE email = %s
            """, (email,))
            result = cur.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[dict]:
        """Récupère un utilisateur par ID."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, email, password_hash, username, created_at, last_login, is_active
                FROM users
                WHERE id = %s
            """, (user_id,))
            result = cur.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def update_last_login(user_id: int):
        """Met à jour la date de dernière connexion."""
        with Database.get_cursor(commit=True) as cur:
            cur.execute("""
                UPDATE users
                SET last_login = NOW()
                WHERE id = %s
            """, (user_id,))


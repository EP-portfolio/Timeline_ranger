"""
Modèles de données pour les parties (accès DB)
"""
import secrets
from typing import Optional, List
from datetime import datetime
from app.core.database import Database


class GameModel:
    """Modèle pour gérer les parties dans la base de données."""
    
    @staticmethod
    def generate_code() -> str:
        """Génère un code unique pour une partie."""
        return secrets.token_urlsafe(6).upper()[:6]
    
    @staticmethod
    def create(host_id: int, max_players: int = 4) -> dict:
        """Crée une nouvelle partie."""
        code = GameModel.generate_code()
        # Vérifier l'unicité du code
        while GameModel.get_by_code(code):
            code = GameModel.generate_code()
        
        with Database.get_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO games (code, host_id, max_players, status, current_players)
                VALUES (%s, %s, %s, 'waiting', 1)
                RETURNING id, code, host_id, max_players, status, current_players, created_at, started_at, finished_at
            """, (code, host_id, max_players))
            return dict(cur.fetchone())
    
    @staticmethod
    def get_by_code(code: str) -> Optional[dict]:
        """Récupère une partie par code."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, code, host_id, max_players, status, current_players, created_at, started_at, finished_at
                FROM games
                WHERE code = %s
            """, (code,))
            result = cur.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_by_id(game_id: int) -> Optional[dict]:
        """Récupère une partie par ID."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, code, host_id, max_players, status, current_players, created_at, started_at, finished_at
                FROM games
                WHERE id = %s
            """, (game_id,))
            result = cur.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def list_waiting_games(limit: int = 20) -> List[dict]:
        """Liste les parties en attente."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, code, host_id, max_players, status, current_players, created_at
                FROM games
                WHERE status = 'waiting' AND current_players < max_players
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            return [dict(row) for row in cur.fetchall()]
    
    @staticmethod
    def update_status(game_id: int, status: str):
        """Met à jour le statut d'une partie."""
        with Database.get_cursor(commit=True) as cur:
            if status == 'started':
                cur.execute("""
                    UPDATE games
                    SET status = %s, started_at = NOW()
                    WHERE id = %s
                """, (status, game_id))
            else:
                cur.execute("""
                    UPDATE games
                    SET status = %s
                    WHERE id = %s
                """, (status, game_id))
    
    @staticmethod
    def increment_players(game_id: int):
        """Incrémente le nombre de joueurs."""
        with Database.get_cursor(commit=True) as cur:
            cur.execute("""
                UPDATE games
                SET current_players = current_players + 1
                WHERE id = %s
            """, (game_id,))


class GamePlayerModel:
    """Modèle pour gérer les joueurs dans les parties."""
    
    @staticmethod
    def create(game_id: int, user_id: int, player_number: int, armure_meca_id: Optional[int] = None) -> dict:
        """Ajoute un joueur à une partie."""
        with Database.get_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO game_players (game_id, user_id, player_number, armure_meca_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, game_id, user_id, player_number, armure_meca_id, score, 
                          total_points_degats, total_lasers, total_points_developpement_technique,
                          total_paires_ailes, status, joined_at
            """, (game_id, user_id, player_number, armure_meca_id))
            return dict(cur.fetchone())
    
    @staticmethod
    def get_by_game_and_user(game_id: int, user_id: int) -> Optional[dict]:
        """Récupère un joueur par partie et utilisateur."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, game_id, user_id, player_number, armure_meca_id, score,
                       total_points_degats, total_lasers, total_points_developpement_technique,
                       total_paires_ailes, status, joined_at
                FROM game_players
                WHERE game_id = %s AND user_id = %s
            """, (game_id, user_id))
            result = cur.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def list_by_game(game_id: int) -> List[dict]:
        """Liste tous les joueurs d'une partie."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT gp.id, gp.game_id, gp.user_id, gp.player_number, gp.armure_meca_id,
                       gp.score, gp.total_points_degats, gp.total_lasers,
                       gp.total_points_developpement_technique, gp.total_paires_ailes,
                       gp.status, gp.joined_at,
                       u.email, u.username
                FROM game_players gp
                JOIN users u ON gp.user_id = u.id
                WHERE gp.game_id = %s
                ORDER BY gp.player_number
            """, (game_id,))
            return [dict(row) for row in cur.fetchall()]
    
    @staticmethod
    def get_next_player_number(game_id: int) -> int:
        """Obtient le prochain numéro de joueur disponible."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT COALESCE(MAX(player_number), 0) + 1
                FROM game_players
                WHERE game_id = %s
            """, (game_id,))
            result = cur.fetchone()
            return result[0] if result else 1


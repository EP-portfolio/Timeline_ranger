"""
Modèle pour gérer l'état des parties dans la base de données
"""
from typing import Optional, Dict, Any
import json
from app.core.database import Database


class GameStateModel:
    """Modèle pour gérer l'état des parties."""
    
    @staticmethod
    def create(game_id: int, state_data: Dict[str, Any], turn_number: int = 0, current_player: Optional[int] = None) -> dict:
        """Crée un nouvel état de partie."""
        with Database.get_cursor(commit=True) as cur:
            cur.execute("""
                INSERT INTO game_states (game_id, turn_number, current_player, state_data)
                VALUES (%s, %s, %s, %s)
                RETURNING id, game_id, turn_number, current_player, state_data, created_at
            """, (game_id, turn_number, current_player, json.dumps(state_data)))
            result = cur.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_latest(game_id: int) -> Optional[dict]:
        """Récupère le dernier état d'une partie."""
        with Database.get_cursor() as cur:
            cur.execute("""
                SELECT id, game_id, turn_number, current_player, state_data, created_at
                FROM game_states
                WHERE game_id = %s
                ORDER BY created_at DESC
                LIMIT 1
            """, (game_id,))
            result = cur.fetchone()
            if result:
                state = dict(result)
                # Convertir state_data de JSON string à dict
                if isinstance(state["state_data"], str):
                    state["state_data"] = json.loads(state["state_data"])
                return state
            return None
    
    @staticmethod
    def update(game_id: int, state_data: Dict[str, Any], turn_number: int, current_player: Optional[int] = None):
        """Met à jour l'état d'une partie (crée un nouvel état)."""
        return GameStateModel.create(game_id, state_data, turn_number, current_player)


"""
Modèle pour gérer l'état des parties dans la base de données
"""
from typing import Optional, Dict, Any
import json
from datetime import datetime
from decimal import Decimal
from app.core.database import Database


class GameStateModel:
    """Modèle pour gérer l'état des parties."""
    
    @staticmethod
    def create(game_id: int, state_data: Dict[str, Any], turn_number: int = 0, current_player: Optional[int] = None) -> dict:
        """Crée un nouvel état de partie."""
        try:
            # Fonction helper pour sérialiser les types non-JSON
            def json_serializer(obj):
                """Sérialise les objets non-JSON en string."""
                if isinstance(obj, (datetime,)):
                    return obj.isoformat()
                elif isinstance(obj, (Decimal,)):
                    return float(obj)
                elif hasattr(obj, '__dict__'):
                    return str(obj)
                raise TypeError(f"Type {type(obj)} non sérialisable")
            
            # S'assurer que state_data est sérialisable en JSON
            json_str = json.dumps(state_data, default=json_serializer, ensure_ascii=False)
            print(f"[DEBUG] Sérialisation JSON réussie pour game_id {game_id}, taille: {len(json_str)} bytes")
        except (TypeError, ValueError) as e:
            import traceback
            print(f"[ERREUR] Erreur de sérialisation JSON pour game_id {game_id}: {e}")
            print(f"[DEBUG] Type de state_data: {type(state_data)}")
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            raise ValueError(f"Impossible de sérialiser l'état du jeu en JSON: {e}")
        
        try:
            with Database.get_cursor(commit=True) as cur:
                cur.execute("""
                    INSERT INTO game_states (game_id, turn_number, current_player, state_data)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, game_id, turn_number, current_player, state_data, created_at
                """, (game_id, turn_number, current_player, json_str))
                result = cur.fetchone()
                print(f"[DEBUG] État sauvegardé avec succès dans la DB pour game_id {game_id}")
                return dict(result) if result else None
        except Exception as e:
            print(f"[ERREUR] Erreur lors de l'insertion dans la DB pour game_id {game_id}: {e}")
            import traceback
            print(f"[DEBUG] Traceback DB: {traceback.format_exc()}")
            raise
    
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


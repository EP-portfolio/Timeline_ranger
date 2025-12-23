"""
Schémas Pydantic pour les parties
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class GameBase(BaseModel):
    """Schéma de base pour une partie."""
    max_players: int = 4
    status: str = "waiting"  # waiting, started, finished


class GameCreate(GameBase):
    """Schéma pour créer une partie."""
    pass


class GameResponse(GameBase):
    """Schéma de réponse pour une partie."""
    id: int
    code: str
    host_id: int
    current_players: int
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class GamePlayerBase(BaseModel):
    """Schéma de base pour un joueur dans une partie."""
    player_number: int
    armure_meca_id: Optional[int] = None


class GamePlayerResponse(GamePlayerBase):
    """Schéma de réponse pour un joueur."""
    id: int
    game_id: int
    user_id: int
    score: int
    total_points_degats: int
    total_lasers: int
    total_points_developpement_technique: int
    total_paires_ailes: int
    status: str
    joined_at: datetime
    
    class Config:
        from_attributes = True


class GameJoinRequest(BaseModel):
    """Schéma pour rejoindre une partie."""
    game_code: str
    armure_meca_id: Optional[int] = None


class GameStateResponse(BaseModel):
    """Schéma pour l'état d'une partie."""
    game_id: int
    turn_number: int
    current_player: Optional[int] = None
    state_data: dict
    
    class Config:
        from_attributes = True


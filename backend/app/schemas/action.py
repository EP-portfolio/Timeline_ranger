"""
Schémas Pydantic pour les actions de jeu
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ActionType(str, Enum):
    """Types d'actions disponibles"""
    PLAY_COLOR = "play_color"  # Jouer une action de couleur (Ranger)
    PLAY_CARD = "play_card"  # Jouer une carte (troupe/technologie)
    PASS = "pass"  # Passer son tour
    USE_EFFECT = "use_effect"  # Utiliser un effet de carte


class ColorAction(str, Enum):
    """Actions de couleur (Rangers)"""
    BLUE = "blue"  # Action Mécène
    BLACK = "black"  # Action Animaux
    ORANGE = "orange"  # Action Construction
    GREEN = "green"  # Action Association
    YELLOW = "yellow"  # Action Cartes


class PlayColorActionRequest(BaseModel):
    """Requête pour jouer une action de couleur"""
    color: ColorAction = Field(..., description="Couleur de l'action (Ranger)")
    power: int = Field(..., ge=1, le=5, description="Puissance de l'action (1-5)")
    use_x_token: bool = Field(default=False, description="Utiliser un jeton X pour augmenter la puissance")
    action_data: Optional[Dict[str, Any]] = Field(default=None, description="Données supplémentaires selon l'action")


class PlayCardActionRequest(BaseModel):
    """Requête pour jouer une carte"""
    card_id: int = Field(..., description="ID de la carte à jouer")
    card_type: str = Field(..., description="Type de carte (troupe/technology)")
    position_x: Optional[int] = Field(None, description="Position X sur le plateau")
    position_y: Optional[int] = Field(None, description="Position Y sur le plateau")
    action_data: Optional[Dict[str, Any]] = Field(default=None, description="Données supplémentaires")


class PassActionRequest(BaseModel):
    """Requête pour passer son tour"""
    reason: Optional[str] = Field(None, description="Raison du pass (optionnel)")


class GameActionResponse(BaseModel):
    """Réponse après une action"""
    success: bool = Field(..., description="Action réussie")
    message: str = Field(..., description="Message de confirmation")
    game_state: Optional[Dict[str, Any]] = Field(None, description="État du jeu après l'action")
    next_player: Optional[int] = Field(None, description="Numéro du prochain joueur")


class GameStateResponse(BaseModel):
    """État complet du jeu"""
    game_id: int
    status: str
    turn_number: int
    current_player: Optional[int] = None  # Peut être None si la partie n'est pas démarrée
    players: List[Dict[str, Any]]
    game_data: Dict[str, Any] = Field(..., description="Données complètes de l'état du jeu")
    # Inclut : Rangers, main, plateau, ressources, scores, etc.


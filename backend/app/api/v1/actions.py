"""
Routes pour les actions de jeu
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from app.schemas.action import (
    PlayColorActionRequest,
    PlayCardActionRequest,
    PassActionRequest,
    GameActionResponse,
    GameStateResponse,
    ColorAction
)
from app.models.game import GameModel, GamePlayerModel
from app.api.v1.auth import get_current_user
from app.services.game_logic import GameLogic
import json

router = APIRouter(prefix="/games", tags=["actions"])


def get_game_state(game_id: int) -> Dict[str, Any]:
    """
    Récupère l'état du jeu depuis la base de données
    
    Args:
        game_id: ID de la partie
        
    Returns:
        État du jeu
    """
    # Pour le POC, on stocke l'état dans game_states
    # À implémenter avec le modèle GameStateModel
    # Pour l'instant, on retourne un état basique
    game = GameModel.get_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partie non trouvée"
        )
    
    # Récupérer les joueurs
    players = GamePlayerModel.list_by_game(game_id)
    
    # Pour le POC, on initialise l'état si nécessaire
    # Dans une vraie implémentation, on récupérerait depuis game_states
    if game["status"] == "started":
        # Initialiser l'état si c'est le premier appel
        # (dans une vraie implémentation, on vérifierait si l'état existe)
        state = GameLogic.initialize_game(game_id, players)
        return state
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="La partie n'a pas encore été démarrée"
    )


@router.post("/{game_id}/actions/play-color", response_model=GameActionResponse)
async def play_color_action(
    game_id: int,
    action: PlayColorActionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Joue une action de couleur (Ranger)
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie"
        )
    
    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)
    
    # Vérifier que c'est le tour du joueur
    if game_state["current_player"] != player["player_number"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce n'est pas votre tour"
        )
    
    # Récupérer l'état du joueur
    player_state = game_state["players"][player["player_number"]]
    
    # Valider l'action
    is_valid, error_message = GameLogic.validate_color_action(
        color=action.color.value,
        power=action.power,
        player_state=player_state,
        action_data=action.action_data
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Appliquer l'action (logique simplifiée pour le POC)
    # Trouver le Ranger joué
    played_ranger = None
    for ranger in player_state["rangers"]:
        if ranger["color"] == action.color.value:
            played_ranger = ranger
            break
    
    # Faire tourner les Rangers
    player_state["rangers"] = GameLogic.rotate_ranger(
        player_state["rangers"],
        played_ranger["position"]
    )
    
    # Appliquer les effets selon l'action
    if action.color == ColorAction.BLUE:
        # Action Mécène
        if action.action_data and "gain_credits" in action.action_data:
            player_state["resources"]["or"] += action.action_data["gain_credits"]
        # TODO: Jouer une carte Mécène si demandé
    
    elif action.color == ColorAction.BLACK:
        # Action Animaux
        # TODO: Jouer des animaux selon la puissance
        pass
    
    elif action.color == ColorAction.ORANGE:
        # Action Construction
        if action.action_data and "size" in action.action_data:
            cost = action.action_data["size"] * 2
            player_state["resources"]["or"] -= cost
            # TODO: Ajouter la construction au plateau
    
    elif action.color == ColorAction.GREEN:
        # Action Association
        if action.action_data and "gain_reputation" in action.action_data:
            player_state["scores"]["reputation"] += action.action_data["gain_reputation"]
        # TODO: Réaliser des quêtes, récupérer mines/reliques
    
    elif action.color == ColorAction.YELLOW:
        # Action Cartes
        # TODO: Piocher des cartes
        pass
    
    # Passer au joueur suivant
    next_player = GameLogic.get_next_player(
        game_state["current_player"],
        game_state["player_order"]
    )
    game_state["current_player"] = next_player
    game_state["turn_number"] += 1
    
    # Sauvegarder l'état mis à jour
    from app.models.game_state import GameStateModel
    GameStateModel.update(
        game_id=game_id,
        state_data=game_state,
        turn_number=game_state["turn_number"],
        current_player=game_state["current_player"]
    )
    
    # Diffuser la mise à jour via WebSocket
    from app.api.v1.websocket import broadcast_game_state_update_sync
    try:
        broadcast_game_state_update_sync(game_id, game_state)
    except Exception as e:
        print(f"Erreur broadcast WebSocket: {e}")
    
    return GameActionResponse(
        success=True,
        message=f"Action {action.color.value} jouée avec succès",
        game_state=game_state,
        next_player=next_player
    )


@router.post("/{game_id}/actions/play-card", response_model=GameActionResponse)
async def play_card_action(
    game_id: int,
    action: PlayCardActionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Joue une carte (troupe ou technologie)
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie"
        )
    
    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)
    
    # Vérifier que c'est le tour du joueur
    if game_state["current_player"] != player["player_number"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce n'est pas votre tour"
        )
    
    # TODO: Vérifier que la carte est dans la main du joueur
    # TODO: Vérifier les prérequis (coût, matières premières)
    # TODO: Placer la carte sur le plateau
    # TODO: Appliquer les effets de la carte
    
    return GameActionResponse(
        success=True,
        message="Carte jouée avec succès",
        game_state=game_state
    )


@router.post("/{game_id}/actions/pass", response_model=GameActionResponse)
async def pass_action(
    game_id: int,
    action: PassActionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Passe son tour
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie"
        )
    
    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)
    
    # Vérifier que c'est le tour du joueur
    if game_state["current_player"] != player["player_number"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce n'est pas votre tour"
        )
    
    # Obtenir un jeton X (si on passe au niveau 1)
    # Pour le POC, on simplifie
    
    # Passer au joueur suivant
    next_player = GameLogic.get_next_player(
        game_state["current_player"],
        game_state["player_order"]
    )
    game_state["current_player"] = next_player
    game_state["turn_number"] += 1
    
    # Sauvegarder l'état mis à jour
    from app.models.game_state import GameStateModel
    GameStateModel.update(
        game_id=game_id,
        state_data=game_state,
        turn_number=game_state["turn_number"],
        current_player=game_state["current_player"]
    )
    
    # Diffuser la mise à jour via WebSocket
    from app.api.v1.websocket import broadcast_game_state_update_sync
    try:
        broadcast_game_state_update_sync(game_id, game_state)
    except Exception as e:
        print(f"Erreur broadcast WebSocket: {e}")
    
    return GameActionResponse(
        success=True,
        message="Tour passé",
        game_state=game_state,
        next_player=next_player
    )


@router.get("/{game_id}/state", response_model=GameStateResponse)
async def get_game_state_endpoint(
    game_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Récupère l'état complet du jeu
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie"
        )
    
    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)
    
    # Formater la réponse
    players_list = []
    for player_num, player_state in game_state["players"].items():
        players_list.append({
            "player_number": player_num,
            "user_id": player_state["user_id"],
            "scores": player_state["scores"],
            "resources": player_state["resources"],
        })
    
    return GameStateResponse(
        game_id=game_id,
        status=game_state["status"],
        turn_number=game_state["turn_number"],
        current_player=game_state["current_player"],
        players=players_list,
        game_data=game_state
    )


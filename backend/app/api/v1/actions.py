"""
Routes pour les actions de jeu
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import random
import json
from app.schemas.action import (
    PlayColorActionRequest,
    PlayCardActionRequest,
    PassActionRequest,
    SelectInitialHandRequest,
    ExchangeCardForXTokenRequest,
    GetConstructionTilesRequest,
    PlaceConstructionRequest,
    GameActionResponse,
    GameStateResponse,
    ColorAction,
)
from app.models.game import GameModel, GamePlayerModel
from app.api.v1.auth import get_current_user
from app.services.game_logic import GameLogic

router = APIRouter(prefix="/games", tags=["actions"])


def get_game_state(game_id: int) -> Dict[str, Any]:
    """
    Récupère l'état du jeu depuis la base de données

    Args:
        game_id: ID de la partie

    Returns:
        État du jeu (avec clés normalisées en int pour players)
    """
    from app.models.game_state import GameStateModel

    game = GameModel.get_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partie non trouvée"
        )

    # Récupérer les joueurs
    players = GamePlayerModel.list_by_game(game_id)

    # Si la partie n'est pas démarrée, retourner un état avec les Rangers initialisés
    # pour permettre la visualisation de l'interface même sans démarrer la partie
    if game["status"] != "started":
        from app.services.game_logic import GameLogic

        # Initialiser un état minimal avec les Rangers
        minimal_state = {
            "game_id": game_id,
            "status": "waiting",
            "turn_number": 0,
            "current_player": None,
            "player_order": [p["player_number"] for p in players],
            "players": {},
        }

        # Initialiser les Rangers et les ressources pour chaque joueur
        rangers = GameLogic.initialize_rangers()
        for p in players:
            minimal_state["players"][p["player_number"]] = {
                "player_id": p["id"],
                "user_id": p["user_id"],
                "player_number": p["player_number"],
                "armure_meca_id": p.get("armure_meca_id"),
                "rangers": [r.copy() for r in rangers],  # Copie pour chaque joueur
                "resources": {
                    "or": 0,
                    "titanium": 0,
                    "platine": 0,
                    "vibranium": 0,
                    "carbone": 0,
                    "kevlar": 0,
                },
                "scores": {
                    "points_degats": 0,
                    "lasers": 0,
                    "reputation": 0,
                    "paires_ailes": 0,
                },
                "emissaires": 1,  # Émissaire de départ
                "board": {
                    "garnisons": [],
                    "weapon_slots": [],
                    "weapons": [],
                    "armor_pieces": [],
                    "lasers": [],
                },
                "hand": [],
                "x_tokens": 0,
                "last_breath_cards": [],
            }

        return minimal_state

    # Essayer de récupérer l'état depuis la base de données
    saved_state = GameStateModel.get_latest(game_id)

    if saved_state and saved_state.get("state_data"):
        # Normaliser les clés de players (convertir strings en int si nécessaire)
        state = saved_state["state_data"]
        if "players" in state and state["players"]:
            # Vérifier si les clés sont des strings et les convertir en int
            first_key = next(iter(state["players"].keys()))
            if isinstance(first_key, str) and first_key.isdigit():
                normalized_players = {}
                for key, value in state["players"].items():
                    normalized_players[int(key)] = value
                state["players"] = normalized_players
        return state

    # Si aucun état n'existe mais la partie est démarrée, initialiser
    # (peut arriver si l'état n'a pas été sauvegardé correctement)
    state = GameLogic.initialize_game(game_id, players)

    # Sauvegarder l'état initial
    GameStateModel.create(
        game_id=game_id,
        state_data=state,
        turn_number=state.get("turn_number", 1),
        current_player=state.get("current_player"),
    )

    return state


@router.post("/{game_id}/actions/play-color", response_model=GameActionResponse)
async def play_color_action(
    game_id: int,
    action: PlayColorActionRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Joue une action de couleur (Ranger)
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie",
        )

    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)

    # Vérifier que c'est le tour du joueur
    if game_state["current_player"] != player["player_number"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ce n'est pas votre tour"
        )

    # Récupérer l'état du joueur
    player_num = player["player_number"]
    player_state = game_state["players"].get(player_num)
    if not player_state:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"État du joueur {player_num} non trouvé",
        )

    # Valider l'action
    is_valid, error_message = GameLogic.validate_color_action(
        color=action.color.value,
        power=action.power,
        player_state=player_state,
        action_data=action.action_data,
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_message
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
        player_state["rangers"], played_ranger["position"]
    )

    # Appliquer les effets selon l'action
    if action.color == ColorAction.BLUE:
        # Action Mécène
        if action.selected_card_id:
            # Jouer une carte Mécène
            # Retirer la carte de la main
            player_state["hand"] = [
                card
                for card in player_state.get("hand", [])
                if card["id"] != action.selected_card_id
            ]
            # TODO: Appliquer les effets de la carte Mécène
        elif action.action_data and "gain_credits" in action.action_data:
            # Gagner des crédits (pas de carte)
            player_state["resources"]["or"] += action.action_data["gain_credits"]

    elif action.color == ColorAction.BLACK:
        # Action Animaux - Jouer une carte Troupe
        if action.selected_card_id:
            # Retirer la carte de la main
            selected_card = None
            for card in player_state.get("hand", []):
                if card["id"] == action.selected_card_id:
                    selected_card = card
                    break

            if not selected_card:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Carte non trouvée dans votre main",
                )

            # Vérifier que c'est bien une carte Troupe
            if selected_card.get("type") != "troupe":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cette action nécessite une carte Troupe",
                )

            # Vérifier les prérequis : construction de taille >= taille troupe et inoccupée
            troupe_size = selected_card.get("size", 0)
            if troupe_size == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La carte Troupe doit avoir une taille valide",
                )

            # Chercher une construction (garnison) de taille suffisante et inoccupée
            board = player_state.get("board", {})
            garnisons = board.get("garnisons", [])
            weapons = board.get("weapons", [])

            # Trouver une garnison disponible (taille >= taille troupe et non occupée)
            available_garnison = None
            for garnison in garnisons:
                garnison_size = garnison.get("size", 0)
                garnison_id = garnison.get("id")

                # Vérifier si la garnison est occupée
                is_occupied = any(
                    weapon.get("garnison_id") == garnison_id for weapon in weapons
                )

                # Vérifier que la taille est suffisante et qu'elle n'est pas occupée
                if garnison_size >= troupe_size and not is_occupied:
                    available_garnison = garnison
                    break

            if not available_garnison:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vous devez avoir une construction (garnison) de taille {troupe_size} ou plus, inoccupée, pour poser cette troupe",
                )

            # Retirer la carte de la main
            player_state["hand"] = [
                card
                for card in player_state.get("hand", [])
                if card["id"] != action.selected_card_id
            ]

            # Ajouter la troupe au plateau dans la garnison
            new_weapon = {
                "id": f"weapon_{selected_card['id']}",
                "card_id": selected_card["id"],
                "card_name": selected_card["name"],
                "garnison_id": available_garnison["id"],
                "size": troupe_size,
                "weapon_type": selected_card.get("weapon_type"),
            }
            board["weapons"] = board.get("weapons", []) + [new_weapon]

            # Marquer la garnison comme occupée
            for garnison in board["garnisons"]:
                if garnison["id"] == available_garnison["id"]:
                    garnison["occupied"] = True
                    garnison["weapon_id"] = new_weapon["id"]
                    break

    elif action.color == ColorAction.ORANGE:
        # Action Construction
        # L'action Construction ne place pas directement la construction
        # Elle permet au joueur de choisir une tuile et de la placer
        # Le placement se fait via l'endpoint /place-construction
        # Initialiser les données du tour de construction
        orange_ranger = next(
            (r for r in player_state["rangers"] if r["color"] == "orange"), None
        )
        is_improved = orange_ranger.get("improved", False) if orange_ranger else False
        
        # Initialiser les données du tour de construction
        player_state["construction_turn_data"] = {
            "action_power": action.power,
            "constructions_placed": [],  # Liste des tailles construites dans ce tour
            "total_size_used": 0,
            "is_improved": is_improved,  # Ranger amélioré ou non
        }

    elif action.color == ColorAction.GREEN:
        # Action Association
        if action.action_data and "gain_reputation" in action.action_data:
            player_state["scores"]["reputation"] += action.action_data[
                "gain_reputation"
            ]

        # Gestion des mines
        if action.action_data and "acquire_mine" in action.action_data:
            mine_type = action.action_data.get(
                "mine_type"
            )  # Ex: "vibranium", "titanium", etc.
            if mine_type:
                # Compter les mines actuelles
                mines = player_state.get("mines", [])
                current_mine_count = len(mines)

                # Ajouter la nouvelle mine
                new_mine = {
                    "id": f"mine_{len(mines) + 1}_{random.randint(1000, 9999)}",
                    "type": mine_type,
                }
                mines.append(new_mine)
                player_state["mines"] = mines

                # Si c'est la 2ème mine, permettre l'amélioration d'un Ranger
                if current_mine_count == 1:  # On avait 1 mine, maintenant on en a 2
                    # Le joueur peut améliorer un Ranger (sera géré par un endpoint séparé)
                    player_state["can_improve_ranger"] = True
                    player_state["improve_ranger_pending"] = True

    elif action.color == ColorAction.YELLOW:
        # Action Cartes
        # TODO: Piocher des cartes
        pass

    # Passer au joueur suivant
    next_player = GameLogic.get_next_player(
        game_state["current_player"], game_state["player_order"]
    )
    game_state["current_player"] = next_player
    game_state["turn_number"] += 1

    # Sauvegarder l'état mis à jour
    from app.models.game_state import GameStateModel

    GameStateModel.update(
        game_id=game_id,
        state_data=game_state,
        turn_number=game_state["turn_number"],
        current_player=game_state["current_player"],
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
        next_player=next_player,
    )


@router.post("/{game_id}/actions/play-card", response_model=GameActionResponse)
async def play_card_action(
    game_id: int,
    action: PlayCardActionRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Joue une carte (troupe ou technologie)
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie",
        )

    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)

    # Vérifier que c'est le tour du joueur
    if game_state["current_player"] != player["player_number"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ce n'est pas votre tour"
        )

    # TODO: Vérifier que la carte est dans la main du joueur
    # TODO: Vérifier les prérequis (coût, matières premières)
    # TODO: Placer la carte sur le plateau
    # TODO: Appliquer les effets de la carte

    return GameActionResponse(
        success=True, message="Carte jouée avec succès", game_state=game_state
    )


@router.post("/{game_id}/actions/pass", response_model=GameActionResponse)
async def pass_action(
    game_id: int,
    action: PassActionRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Passe son tour
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie",
        )

    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)

    # Vérifier que c'est le tour du joueur
    if game_state["current_player"] != player["player_number"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Ce n'est pas votre tour"
        )

    # Obtenir un jeton X (si on passe au niveau 1)
    # Pour le POC, on simplifie

    # Passer au joueur suivant
    next_player = GameLogic.get_next_player(
        game_state["current_player"], game_state["player_order"]
    )
    game_state["current_player"] = next_player
    game_state["turn_number"] += 1

    # Sauvegarder l'état mis à jour
    from app.models.game_state import GameStateModel

    GameStateModel.update(
        game_id=game_id,
        state_data=game_state,
        turn_number=game_state["turn_number"],
        current_player=game_state["current_player"],
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
        next_player=next_player,
    )


@router.get("/{game_id}/state", response_model=GameStateResponse)
async def get_game_state_endpoint(
    game_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Récupère l'état complet du jeu
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie",
        )

    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)

    # Formater la réponse
    players_list = []
    for player_num, player_state in game_state["players"].items():
        players_list.append(
            {
                "player_number": player_num,
                "user_id": player_state["user_id"],
                "scores": player_state["scores"],
                "resources": player_state["resources"],
            }
        )

    return GameStateResponse(
        game_id=game_id,
        status=game_state["status"],
        turn_number=game_state["turn_number"],
        current_player=game_state["current_player"],
        players=players_list,
        game_data=game_state,
    )


@router.post(
    "/{game_id}/actions/select-initial-hand", response_model=GameActionResponse
)
async def select_initial_hand(
    game_id: int,
    selection: SelectInitialHandRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Sélectionne 4 cartes parmi les 8 initiales
    """
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie",
        )

    # Récupérer l'état du jeu
    game_state = get_game_state(game_id)

    # Vérifier que le joueur n'a pas déjà sélectionné
    player_num = player["player_number"]
    player_state = game_state["players"].get(player_num)
    if not player_state:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"État du joueur {player_num} non trouvé",
        )

    if player_state.get("hand_selected", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous avez déjà sélectionné vos cartes",
        )

    # Vérifier que les cartes sélectionnées sont dans initial_hand
    initial_hand = player_state.get("initial_hand", [])
    initial_card_ids = {card["id"] for card in initial_hand}
    selected_ids = set(selection.selected_card_ids)

    if not selected_ids.issubset(initial_card_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certaines cartes sélectionnées ne sont pas dans votre main initiale",
        )

    if len(selected_ids) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous devez sélectionner exactement 4 cartes",
        )

    # Sélectionner les 4 cartes
    selected_cards = [card for card in initial_hand if card["id"] in selected_ids]

    # Mettre à jour l'état du joueur
    player_state["hand"] = selected_cards
    player_state["hand_selected"] = True

    # Sauvegarder l'état mis à jour
    from app.models.game_state import GameStateModel

    GameStateModel.update(
        game_id=game_id,
        state_data=game_state,
        turn_number=game_state.get("turn_number", 1),
        current_player=game_state.get("current_player"),
    )

    # Diffuser la mise à jour via WebSocket
    from app.api.v1.websocket import broadcast_game_state_update_sync

    try:
        broadcast_game_state_update_sync(game_id, game_state)
    except Exception as e:
        print(f"Erreur broadcast WebSocket: {e}")

    return GameActionResponse(
        success=True,
        message="4 cartes sélectionnées avec succès",
        game_state=game_state,
    )

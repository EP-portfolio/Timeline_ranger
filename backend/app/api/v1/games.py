"""
Routes pour les parties
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.game import (
    GameCreate,
    GameResponse,
    GameJoinRequest,
    GamePlayerResponse,
    GameStateResponse,
)
from app.models.game import GameModel, GamePlayerModel
from app.models.user import UserModel
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/games", tags=["games"])


@router.post("", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(
    game_data: GameCreate, current_user: dict = Depends(get_current_user)
):
    """Crée une nouvelle partie."""
    game = GameModel.create(
        host_id=current_user["id"], max_players=game_data.max_players
    )

    # Ajouter le créateur comme premier joueur
    GamePlayerModel.create(
        game_id=game["id"], user_id=current_user["id"], player_number=1
    )

    return game


@router.get("", response_model=List[GameResponse])
async def list_games(limit: int = 20):
    """Liste les parties en attente."""
    games = GameModel.list_waiting_games(limit=limit)
    return games


@router.get("/{game_code}", response_model=GameResponse)
async def get_game(game_code: str):
    """Récupère une partie par code."""
    game = GameModel.get_by_code(game_code)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partie non trouvée"
        )
    return game


@router.get("/by-id/{game_id}", response_model=GameResponse)
async def get_game_by_id(game_id: int, current_user: dict = Depends(get_current_user)):
    """Récupère une partie par ID."""
    game = GameModel.get_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partie non trouvée"
        )
    return game


@router.post("/join", response_model=GamePlayerResponse)
async def join_game(
    join_data: GameJoinRequest, current_user: dict = Depends(get_current_user)
):
    """Rejoint une partie."""
    game = GameModel.get_by_code(join_data.game_code)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partie non trouvée"
        )

    if game["status"] != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cette partie n'accepte plus de nouveaux joueurs",
        )

    if game["current_players"] >= game["max_players"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La partie est complète"
        )

    # Vérifier si l'utilisateur n'est pas déjà dans la partie
    existing_player = GamePlayerModel.get_by_game_and_user(
        game["id"], current_user["id"]
    )
    if existing_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous êtes déjà dans cette partie",
        )

    # Ajouter le joueur
    player_number = GamePlayerModel.get_next_player_number(game["id"])
    player = GamePlayerModel.create(
        game_id=game["id"],
        user_id=current_user["id"],
        player_number=player_number,
        armure_meca_id=join_data.armure_meca_id,
    )

    # Incrémenter le nombre de joueurs
    GameModel.increment_players(game["id"])

    return player


@router.get("/{game_id}/players", response_model=List[GamePlayerResponse])
async def get_game_players(
    game_id: int, current_user: dict = Depends(get_current_user)
):
    """Récupère tous les joueurs d'une partie."""
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, current_user["id"])
    if not player:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas dans cette partie",
        )

    players = GamePlayerModel.list_by_game(game_id)
    return players


@router.post("/{game_id}/start")
async def start_game(game_id: int, current_user: dict = Depends(get_current_user)):
    """Démarre une partie (seul l'hôte peut le faire)."""
    game = GameModel.get_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partie non trouvée"
        )

    if game["host_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seul l'hôte peut démarrer la partie",
        )

    if game["status"] != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La partie a déjà été démarrée",
        )

    if game["current_players"] < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il faut au moins 1 joueur pour démarrer",
        )

    # Initialiser l'état du jeu
    from app.services.game_logic import GameLogic
    from app.models.game_state import GameStateModel
    import traceback
    from decimal import Decimal

    try:
        players = GamePlayerModel.list_by_game(game_id)
        if not players:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aucun joueur trouvé dans la partie",
            )

        # Normaliser les données des joueurs (convertir Decimal en int, datetime en string)
        normalized_players = []
        for p in players:
            normalized_player = {
                "id": int(p["id"]),
                "user_id": int(p["user_id"]),
                "player_number": int(p["player_number"]) if isinstance(p["player_number"], (int, Decimal)) else p["player_number"],
                "armure_meca_id": int(p["armure_meca_id"]) if p.get("armure_meca_id") else None,
            }
            # Vérifier que player_number est valide
            if normalized_player["player_number"] is None:
                raise ValueError(f"Joueur sans player_number valide: {p}")
            normalized_players.append(normalized_player)

        print(f"[DEBUG] Nombre de joueurs normalisés: {len(normalized_players)}")
        for p in normalized_players:
            print(f"[DEBUG] Joueur normalisé: {p}")

        # Initialiser l'état du jeu avec les joueurs normalisés
        game_state = GameLogic.initialize_game(game_id, normalized_players)
        print(f"[DEBUG] État du jeu initialisé avec succès")

        # Sauvegarder l'état initial AVANT de mettre à jour le statut
        # pour s'assurer que l'état est disponible quand le statut change
        print(f"[DEBUG] Tentative de sauvegarde de l'état pour game_id {game_id}")
        saved_state = GameStateModel.create(
            game_id=game_id,
            state_data=game_state,
            turn_number=game_state["turn_number"],
            current_player=game_state["current_player"],
        )
        print(f"[DEBUG] État sauvegardé: {saved_state is not None}")

        if saved_state is None:
            raise ValueError("Échec de la sauvegarde de l'état du jeu")

        # Mettre à jour le statut APRÈS la sauvegarde de l'état
        print(f"[DEBUG] Mise à jour du statut de la partie {game_id} à 'started'")
        GameModel.update_status(game_id, "started")
        print(f"[DEBUG] Statut mis à jour avec succès")

        # Vérifier que l'état est bien récupérable
        verification_state = GameStateModel.get_latest(game_id)
        if verification_state:
            print(
                f"[DEBUG] Vérification: État récupérable depuis DB, status: {verification_state.get('state_data', {}).get('status')}"
            )
        else:
            print(
                f"[WARN] Vérification: Impossible de récupérer l'état juste après sauvegarde"
            )

        # Ne pas retourner game_state complet pour éviter les réponses trop volumineuses
        # Le frontend récupérera l'état via /state
        return {
            "message": "Partie démarrée",
            "game_id": game_id,
            "status": "started",
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback

        error_traceback = traceback.format_exc()
        print(f"[ERREUR] Erreur lors du démarrage de la partie {game_id}: {e}")
        print(f"[TRACEBACK] {error_traceback}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du démarrage de la partie: {str(e)}",
        )

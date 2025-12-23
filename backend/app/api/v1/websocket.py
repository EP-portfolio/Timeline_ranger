"""
WebSocket endpoint pour la synchronisation temps réel
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import Dict, List, Set
import json
import asyncio
from app.api.v1.auth import get_current_user_from_token
from app.models.game import GameModel, GamePlayerModel

router = APIRouter()

# Gestion des connexions WebSocket actives
# Structure: {game_id: {player_id: [websocket1, websocket2, ...]}}
active_connections: Dict[int, Dict[int, List[WebSocket]]] = {}


class ConnectionManager:
    """Gère les connexions WebSocket pour les parties"""
    
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, List[WebSocket]]] = {}
    
    async def connect(self, websocket: WebSocket, game_id: int, player_id: int):
        """Connecte un joueur à une partie"""
        await websocket.accept()
        
        if game_id not in self.active_connections:
            self.active_connections[game_id] = {}
        
        if player_id not in self.active_connections[game_id]:
            self.active_connections[game_id][player_id] = []
        
        self.active_connections[game_id][player_id].append(websocket)
        print(f"✅ Joueur {player_id} connecté à la partie {game_id}")
    
    def disconnect(self, websocket: WebSocket, game_id: int, player_id: int):
        """Déconnecte un joueur d'une partie"""
        if game_id in self.active_connections:
            if player_id in self.active_connections[game_id]:
                if websocket in self.active_connections[game_id][player_id]:
                    self.active_connections[game_id][player_id].remove(websocket)
                
                # Nettoyer si plus de connexions pour ce joueur
                if not self.active_connections[game_id][player_id]:
                    del self.active_connections[game_id][player_id]
            
            # Nettoyer si plus de connexions pour cette partie
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
        
        print(f"❌ Joueur {player_id} déconnecté de la partie {game_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Envoie un message à une connexion spécifique"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Erreur envoi message personnel: {e}")
    
    async def broadcast_to_game(self, game_id: int, message: dict, exclude_player: int = None):
        """Diffuse un message à tous les joueurs d'une partie"""
        if game_id not in self.active_connections:
            return
        
        disconnected = []
        
        for player_id, websockets in self.active_connections[game_id].items():
            if exclude_player and player_id == exclude_player:
                continue
            
            for websocket in websockets:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    print(f"Erreur broadcast à joueur {player_id}: {e}")
                    disconnected.append((game_id, player_id, websocket))
        
        # Nettoyer les connexions déconnectées
        for game_id, player_id, websocket in disconnected:
            self.disconnect(websocket, game_id, player_id)
    
    async def broadcast_to_player(self, game_id: int, player_id: int, message: dict):
        """Envoie un message à un joueur spécifique (toutes ses connexions)"""
        if game_id not in self.active_connections:
            return
        
        if player_id not in self.active_connections[game_id]:
            return
        
        disconnected = []
        
        for websocket in self.active_connections[game_id][player_id]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Erreur envoi à joueur {player_id}: {e}")
                disconnected.append((game_id, player_id, websocket))
        
        # Nettoyer les connexions déconnectées
        for game_id, player_id, websocket in disconnected:
            self.disconnect(websocket, game_id, player_id)


manager = ConnectionManager()


async def verify_game_access(websocket: WebSocket, game_id: int, user_id: int) -> bool:
    """Vérifie que l'utilisateur a accès à la partie"""
    # Vérifier que la partie existe
    game = GameModel.get_by_id(game_id)
    if not game:
        await websocket.send_json({
            "type": "error",
            "message": "Partie non trouvée"
        })
        return False
    
    # Vérifier que l'utilisateur est dans la partie
    player = GamePlayerModel.get_by_game_and_user(game_id, user_id)
    if not player:
        await websocket.send_json({
            "type": "error",
            "message": "Vous n'êtes pas dans cette partie"
        })
        return False
    
    return True


@router.websocket("/ws/games/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    """
    Endpoint WebSocket pour une partie
    
    Authentification via query parameter: ?token=JWT_TOKEN
    """
    # Récupérer le token depuis les query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token manquant")
        return
    
    # Vérifier le token et récupérer l'utilisateur
    try:
        user = get_current_user_from_token(token)
        user_id = user["id"]
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token invalide")
        return
    
    # Vérifier l'accès à la partie
    if not await verify_game_access(websocket, game_id, user_id):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Accès refusé")
        return
    
    # Connecter le joueur
    await manager.connect(websocket, game_id, user_id)
    
    # Envoyer un message de bienvenue
    await manager.send_personal_message({
        "type": "connection",
        "message": "Connecté à la partie",
        "game_id": game_id,
        "user_id": user_id
    }, websocket)
    
    # Notifier les autres joueurs
    await manager.broadcast_to_game(game_id, {
        "type": "player_connected",
        "player_id": user_id,
        "game_id": game_id
    }, exclude_player=user_id)
    
    try:
        while True:
            # Recevoir les messages du client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                # Gérer différents types de messages
                if message_type == "ping":
                    # Keep-alive
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": message.get("timestamp")
                    }, websocket)
                
                elif message_type == "game_state_request":
                    # Demande de l'état du jeu
                    # TODO: Récupérer l'état depuis la base de données
                    await manager.send_personal_message({
                        "type": "game_state",
                        "message": "État du jeu (à implémenter)"
                    }, websocket)
                
                elif message_type == "action":
                    # Action de jeu (pourrait être utilisé pour des actions rapides)
                    # Pour le POC, on utilise les endpoints REST
                    await manager.broadcast_to_game(game_id, {
                        "type": "action_notification",
                        "player_id": user_id,
                        "action": message.get("action"),
                        "data": message.get("data")
                    })
                
                else:
                    # Message non reconnu
                    await manager.send_personal_message({
                        "type": "error",
                        "message": f"Type de message non reconnu: {message_type}"
                    }, websocket)
            
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Format JSON invalide"
                }, websocket)
            
            except Exception as e:
                print(f"Erreur traitement message: {e}")
                await manager.send_personal_message({
                    "type": "error",
                    "message": f"Erreur: {str(e)}"
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id, user_id)
        # Notifier les autres joueurs
        await manager.broadcast_to_game(game_id, {
            "type": "player_disconnected",
            "player_id": user_id,
            "game_id": game_id
        })
    
    except Exception as e:
        print(f"Erreur WebSocket: {e}")
        manager.disconnect(websocket, game_id, user_id)


def broadcast_game_state_update_sync(game_id: int, game_state: dict):
    """
    Fonction utilitaire pour diffuser une mise à jour d'état de jeu
    À appeler depuis les endpoints REST après une action
    Version synchrone qui crée une tâche asynchrone
    """
    import time
    try:
        # Essayer de récupérer la boucle d'événements
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Si la boucle tourne déjà, créer une tâche
            asyncio.create_task(manager.broadcast_to_game(game_id, {
                "type": "game_state_update",
                "game_id": game_id,
                "state": game_state,
                "timestamp": time.time()
            }))
        else:
            # Si la boucle ne tourne pas, l'exécuter
            loop.run_until_complete(manager.broadcast_to_game(game_id, {
                "type": "game_state_update",
                "game_id": game_id,
                "state": game_state,
                "timestamp": time.time()
            }))
    except RuntimeError:
        # Pas de boucle d'événements, en créer une nouvelle
        asyncio.run(manager.broadcast_to_game(game_id, {
            "type": "game_state_update",
            "game_id": game_id,
            "state": game_state,
            "timestamp": time.time()
        }))


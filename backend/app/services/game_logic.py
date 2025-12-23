"""
Logique métier du jeu Timeline Ranger
"""

from typing import Dict, List, Any, Optional
import random
from datetime import datetime


class GameLogic:
    """Classe pour gérer la logique métier du jeu"""

    @staticmethod
    def initialize_rangers() -> List[Dict[str, Any]]:
        """
        Initialise les 5 Rangers de base pour un joueur
        Le Ranger Animaux (noir) est toujours en position 1
        Les 4 autres Rangers sont mélangés aléatoirement dans les positions 2-5

        Returns:
            Liste des 5 Rangers avec leurs positions initiales (1-5)
        """
        # Ranger Animaux (noir) toujours en position 1
        animals_ranger = {
            "color": "black",
            "name": "Ranger Noir",
            "position": 1,
            "improved": False,
        }

        # Les 4 autres Rangers à mélanger aléatoirement
        other_rangers = [
            {"color": "blue", "name": "Ranger Bleu", "position": 0, "improved": False},
            {
                "color": "orange",
                "name": "Ranger Orange",
                "position": 0,
                "improved": False,
            },
            {"color": "green", "name": "Ranger Vert", "position": 0, "improved": False},
            {
                "color": "yellow",
                "name": "Ranger Jaune",
                "position": 0,
                "improved": False,
            },
        ]

        # Mélanger aléatoirement les 4 autres Rangers
        random.shuffle(other_rangers)

        # Assigner les positions 2-5 aux Rangers mélangés
        for i, ranger in enumerate(other_rangers, start=2):
            ranger["position"] = i

        # Retourner tous les Rangers : Animaux en 1, puis les 4 autres mélangés
        return [animals_ranger] + other_rangers

    @staticmethod
    def generate_initial_cards(count: int = 8) -> List[Dict[str, Any]]:
        """
        Génère des cartes initiales pour un joueur (POC avec cartes factices)
        
        Args:
            count: Nombre de cartes à générer (par défaut 8)
            
        Returns:
            Liste de cartes avec ID, nom, type, etc.
        """
        # Pour le POC, on génère des cartes factices
        # Plus tard, on récupérera les vraies cartes depuis la base de données
        card_types = ["troupe", "technology"]
        card_names = [
            "Explosif - Lion", "Explosif - Tigre", "Explosif - Ours",
            "Munition - Aigle", "Munition - Loup", "Munition - Renard",
            "Technologie - Armure", "Technologie - Bouclier", "Technologie - Laser",
            "Technologie - Radar", "Technologie - Propulseur", "Technologie - Réacteur"
        ]
        
        cards = []
        for i in range(count):
            card_type = random.choice(card_types)
            card_name = random.choice(card_names)
            cards.append({
                "id": f"card_{i}_{random.randint(1000, 9999)}",
                "name": card_name,
                "type": card_type,
                "cost": random.randint(1, 5),
                "size": random.randint(1, 3) if card_type == "troupe" else None,
            })
        
        return cards

    @staticmethod
    def initialize_game(game_id: int, players: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Initialise une nouvelle partie

        Args:
            game_id: ID de la partie
            players: Liste des joueurs avec leurs informations

        Returns:
            État initial du jeu
        """
        # Distribuer les cartes initiales (8 cartes, garder 4)
        # Chaque joueur reçoit 8 cartes et doit en garder 4

        # Initialiser les Rangers (5 cartes Action) pour chaque joueur
        # Les Rangers sont déjà initialisés avec les positions 1-5
        rangers = GameLogic.initialize_rangers()

        # Initialiser l'état pour chaque joueur
        players_state = {}
        for player in players:
            # Générer 8 cartes initiales pour chaque joueur
            initial_cards = GameLogic.generate_initial_cards(8)
            
            players_state[player["player_number"]] = {
                "player_id": player["id"],
                "user_id": player["user_id"],
                "player_number": player["player_number"],
                "armure_meca_id": player.get("armure_meca_id"),
                "rangers": rangers.copy(),
                "initial_hand": initial_cards,  # 8 cartes initiales à sélectionner
                "hand": [],  # Cartes en main après sélection (4 cartes)
                "hand_selected": False,  # Indique si le joueur a sélectionné ses 4 cartes
                "resources": {
                    "or": 0,  # Crédits
                    "titanium": 0,
                    "platine": 0,
                    "vibranium": 0,
                    "carbone": 0,
                    "kevlar": 0,
                },
                "scores": {
                    "points_degats": 0,
                    "lasers": 0,
                    "reputation": 0,  # Points de développement technique
                    "paires_ailes": 0,
                },
                "board": {
                    "garnisons": [],  # Parties d'armure construites
                    "weapon_slots": [],  # Slots pour armes
                    "weapons": [],  # Armes installées (troupes)
                    "armor_pieces": [],  # Pièces d'armure (technologies)
                    "lasers": [],  # Lasers installés
                },
                "emissaires": 1,  # Émissaires disponibles
                "x_tokens": 0,  # Jetons X (croix)
                "last_breath_cards": [],  # Cartes Dernier Souffle (2 au début)
            }

        # Déterminer l'ordre de jeu initial (aléatoire)
        player_numbers = [p["player_number"] for p in players]
        random.shuffle(player_numbers)

        game_state = {
            "game_id": game_id,
            "status": "started",
            "turn_number": 1,
            "current_player": player_numbers[0],  # Premier joueur
            "player_order": player_numbers,
            "players": players_state,
            "created_at": datetime.now().isoformat(),
        }

        return game_state

    @staticmethod
    def rotate_ranger(
        rangers: List[Dict[str, Any]], played_position: int
    ) -> List[Dict[str, Any]]:
        """
        Fait tourner les Rangers après qu'une action a été jouée

        Args:
            rangers: Liste des Rangers du joueur
            played_position: Position du Ranger joué (1-5)

        Returns:
            Liste des Rangers après rotation
        """
        # Le Ranger joué revient en position 1
        # Les autres avancent d'une position

        # Trouver le Ranger joué
        played_ranger = None
        for ranger in rangers:
            if ranger["position"] == played_position:
                played_ranger = ranger
                break

        if not played_ranger:
            return rangers

        # Nouvelle liste avec le Ranger joué en position 1
        new_rangers = [played_ranger.copy()]
        new_rangers[0]["position"] = 1

        # Les Rangers AVANT la position jouée avancent d'une position
        # Les Rangers APRÈS la position jouée restent à leur position
        for ranger in rangers:
            if ranger["position"] != played_position:
                new_ranger = ranger.copy()
                if new_ranger["position"] < played_position:
                    # Les Rangers avant le joué avancent d'une position
                    new_ranger["position"] += 1
                # Les Rangers après le joué gardent leur position (ne bougent pas)
                new_rangers.append(new_ranger)

        # Trier par position
        new_rangers.sort(key=lambda x: x["position"])

        return new_rangers

    @staticmethod
    def get_next_player(current_player: int, player_order: List[int]) -> int:
        """
        Détermine le prochain joueur

        Args:
            current_player: Numéro du joueur actuel
            player_order: Ordre des joueurs

        Returns:
            Numéro du prochain joueur
        """
        current_index = player_order.index(current_player)
        next_index = (current_index + 1) % len(player_order)
        return player_order[next_index]

    @staticmethod
    def validate_color_action(
        color: str,
        power: int,
        player_state: Dict[str, Any],
        action_data: Optional[Dict[str, Any]] = None,
    ) -> tuple[bool, str]:
        """
        Valide une action de couleur

        Args:
            color: Couleur de l'action
            power: Puissance de l'action
            player_state: État du joueur
            action_data: Données supplémentaires

        Returns:
            (is_valid, error_message)
        """
        # Vérifier que le joueur a le Ranger de cette couleur
        ranger = None
        for r in player_state["rangers"]:
            if r["color"] == color:
                ranger = r
                break

        if not ranger:
            return False, f"Vous n'avez pas le Ranger {color}"

        # Vérifier que la puissance correspond à la position du Ranger
        if ranger["position"] != power:
            # Vérifier si le joueur utilise un jeton X
            if action_data and action_data.get("use_x_token"):
                if player_state["x_tokens"] < 1:
                    return False, "Vous n'avez pas de jeton X"
                # Avec jeton X, on peut augmenter la puissance
                if power > ranger["position"] + 1:
                    return False, "Puissance trop élevée même avec jeton X"
            else:
                return (
                    False,
                    f"La puissance doit correspondre à la position du Ranger ({ranger['position']})",
                )

        # Validations spécifiques selon la couleur
        if color == "black":  # Action Animaux
            # Vérifier qu'on peut jouer des animaux selon la puissance
            # Pour le POC, on simplifie
            pass

        elif color == "blue":  # Action Mécène
            # Vérifier qu'on peut jouer une carte Mécène OU gagner des crédits
            if action_data:
                if "play_card" in action_data:
                    # Vérifier que la carte existe et est jouable
                    pass
                elif "gain_credits" in action_data:
                    # Vérifier le montant (1-5 selon puissance)
                    credits = action_data["gain_credits"]
                    if credits != power:
                        return (
                            False,
                            f"Montant de crédits incorrect (doit être {power})",
                        )

        elif color == "orange":  # Action Construction
            # Vérifier qu'on a assez d'or (2 crédits par case)
            if action_data and "size" in action_data:
                cost = action_data["size"] * 2
                if player_state["resources"]["or"] < cost:
                    return (
                        False,
                        f"Pas assez d'or (nécessite {cost}, vous avez {player_state['resources']['or']})",
                    )

        elif color == "green":  # Action Association
            # Vérifier qu'on a des émissaires si nécessaire
            if action_data and "use_emissaire" in action_data:
                if player_state["emissaires"] < 1:
                    return False, "Vous n'avez pas d'émissaire disponible"

        elif color == "yellow":  # Action Cartes
            # Pas de validation spéciale pour le POC
            pass

        return True, ""

    @staticmethod
    def calculate_laser_damage_points(lasers: int) -> int:
        """
        Calcule les points de dégâts des lasers

        Args:
            lasers: Nombre de lasers

        Returns:
            Points de dégâts
        """
        if lasers <= 6:
            return lasers * 2
        else:
            return lasers * 3

    @staticmethod
    def calculate_total_damage_points(player_state: Dict[str, Any]) -> int:
        """
        Calcule le total des points de dégâts d'un joueur

        Args:
            player_state: État du joueur

        Returns:
            Total des points de dégâts
        """
        total = player_state["scores"]["points_degats"]

        # Ajouter les points de dégâts des lasers
        lasers = player_state["scores"]["lasers"]
        total += GameLogic.calculate_laser_damage_points(lasers)

        # Ajouter les points de dégâts des cartes sur le plateau
        # (à implémenter selon les cartes posées)

        return total

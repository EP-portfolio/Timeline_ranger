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
        # Types de cartes selon le schéma SQL :
        # - troupe : Cartes Troupes (ex-Animaux) → Ranger Noir
        # - technology : Cartes Technologies (ex-Mécènes) → Ranger Bleu
        # - quete : Cartes Quêtes (ex-Projets de Conservation) → Ranger Vert

        # Dictionnaire associant chaque type à ses noms spécifiques
        # Les noms de Troupes utilisent le format: "{Type Arme} - {Nom Arme}"
        # Format mappé selon le schéma: weapon_type_code.replace('_', ' ').title() - nom_arme
        card_names_by_type = {
            "troupe": [
                # Explosifs (ex-Prédateurs)
                "Explosifs - Canon Alpha",
                "Explosifs - Lance-Grenades Beta",
                "Explosifs - Détonateur Gamma",
                # Munitions Standard (ex-Animaux domestiques)
                "Munitions Standard - Fusil M1",
                "Munitions Standard - Carabine M2",
                "Munitions Standard - Pistolet M3",
                # Torpilles (ex-Animaux marins)
                "Torpilles - Torpille T1",
                "Torpilles - Missile Sous-Marin T2",
                # Munitions Nucléaires (ex-Herbivores)
                "Munitions Nucléaires - Projectile N1",
                "Munitions Nucléaires - Ogive N2",
                # Missiles Aériens (ex-Oiseaux)
                "Missiles Aériens - Missile A1",
                "Missiles Aériens - Drone A2",
                # Armes Lourdes (ex-Ours)
                "Armes Lourdes - Canon Lourd L1",
                "Armes Lourdes - Mortier L2",
                # Armes Intelligentes (ex-Primates)
                "Armes Intelligentes - Système IA I1",
                "Armes Intelligentes - Robot I2",
                # Armes Toxiques (ex-Reptiles)
                "Armes Toxiques - Projectile Toxique X1",
                "Armes Toxiques - Gaz X2",
            ],
            "technology": [
                "Système - Armure",
                "Système - Bouclier",
                "Système - Laser",
                "Système - Radar",
                "Système - Propulseur",
                "Système - Réacteur",
                "Renfort - Fondation",
                "Blindage - Avancé",
            ],
            "quete": [
                "Quête - Diversité d'Armes",
                "Quête - Maîtrise Tactique",
                "Quête - Forteresse",
                "Quête - Environnement",
                "Quête - Programme",
            ],
        }

        card_types = ["troupe", "technology", "quete"]

        cards = []
        for i in range(count):
            card_type = random.choice(card_types)
            # Choisir un nom qui correspond au type sélectionné
            card_name = random.choice(card_names_by_type[card_type])

            # Base commune pour toutes les cartes
            # Pour le POC, on utilise des coûts basés sur la taille/type
            # Les vraies valeurs viendront de la base de données
            base_cost = (
                2 if card_type == "troupe" else 3 if card_type == "technology" else 1
            )

            card = {
                "id": f"card_{i}_{random.randint(1000, 9999)}",
                "name": card_name,
                "type": card_type,
                "cost": base_cost + random.randint(0, 2),  # Coût de base + variation
            }

            # Attributs spécifiques selon le type (selon le schéma SQL)
            if card_type == "troupe":
                # Extraire le type d'arme du nom (ex: "Explosifs - Canon Alpha" → "explosifs")
                weapon_type_code = card_name.split(" - ")[0].lower().replace(" ", "_")
                card.update(
                    {
                        "size": random.randint(1, 3),
                        "points_degats": random.randint(0, 3),
                        "nombre_lasers": random.randint(0, 2),
                        "points_developpement_technique": random.randint(0, 2),
                        "paires_ailes": random.randint(0, 1),
                        "raw_materials_required": [],  # Liste vide pour POC, sera remplie depuis la DB
                        "bonus": None,  # Capacité → Bonus
                        "effet_invocation": None,  # Effet unique immédiat
                        "effet_quotidien": None,  # Effet permanent/récurrent
                        "dernier_souffle": None,  # Effet de fin de partie
                        "weapon_type": weapon_type_code,  # Type d'arme (ex: "explosifs", "munitions_standard")
                    }
                )
            elif card_type == "technology":
                card.update(
                    {
                        "level": random.randint(1, 3),
                        "points_degats": random.randint(0, 2),
                        "nombre_lasers": random.randint(0, 1),
                        "points_developpement_technique": random.randint(0, 2),
                        "paires_ailes": random.randint(0, 1),
                        "or_par_jour": random.randint(0, 2),  # Revenus → Or par jour
                        "is_armor_piece": random.choice(
                            [True, False]
                        ),  # Pièce d'armure ou action
                        "armor_piece_type": (
                            random.choice(
                                ["Renfort", "Blindage", "Composant", "Dispositif"]
                            )
                            if random.choice([True, False])
                            else None
                        ),
                        "bonus": None,
                        "effet_invocation": None,
                        "effet_quotidien": None,
                        "dernier_souffle": None,
                    }
                )
            elif card_type == "quete":
                card.update(
                    {
                        "quest_type": random.choice(
                            ["maitrise", "forteresse", "environnement", "programme"]
                        ),
                        "condition_type": None,  # Type de condition
                        "conditions": {},  # Conditions détaillées
                        "rewards": {},  # Récompenses
                    }
                )

            cards.append(card)

        return cards

    @staticmethod
    def initialize_board_grid() -> Dict[str, Any]:
        """
        Initialise la grille hexagonale de base de l'armure méca
        La map est constituée de 9 colonnes VERTICALES contenant chacune 6 ou 7 emplacements
        Structure hexagonale : colonnes verticales avec décalage pour motif hexagonal
        Les cases rocher et eau sont inconstructibles

        Returns:
            Dictionnaire contenant la grille hexagonale avec terrains par défaut
        """
        hexagons = []

        # Structure : 9 colonnes VERTICALES (q = 0 à 8)
        # Chaque colonne a 6 ou 7 hexagones selon le motif hexagonal
        # Colonnes impaires (0, 2, 4, 6, 8) : 7 hexagones
        # Colonnes paires (1, 3, 5, 7) : 6 hexagones
        column_sizes = [7, 6, 7, 6, 7, 6, 7, 6, 7]  # 9 colonnes

        # Générer tous les hexagones de la grille
        # Système de coordonnées hexagonales axiales (q, r)
        # q = colonne (0-8), r = position dans la colonne
        for q in range(9):  # 9 colonnes verticales
            column_size = column_sizes[q]
            for r in range(column_size):
                # Déterminer le terrain par défaut
                # Par défaut : terre craquelée (constructible)
                # Les cases rocher et eau seront définies selon la configuration de l'armure méca
                terrain = "cracked_earth"  # Terre craquelée (constructible par défaut)
                constructible = True  # Constructible par défaut

                hexagons.append(
                    {
                        "q": q,
                        "r": r,
                        "x": 0,  # Sera calculé lors de l'affichage
                        "y": 0,  # Sera calculé lors de l'affichage
                        "terrain": terrain,
                        "constructible": constructible,  # True = constructible, False = inconstructible (rocher/eau)
                        "tokens": [],
                        "special_zone": None,
                        "garnison_id": None,
                        "weapon_id": None,
                    }
                )

        return {
            "columns": 9,  # 9 colonnes verticales
            "column_sizes": column_sizes,  # Taille de chaque colonne [7, 6, 7, 6, 7, 6, 7, 6, 7]
            "hexagons": hexagons,
        }

    @staticmethod
    def get_available_construction_tiles(max_size: int) -> List[Dict[str, Any]]:
        """
        Retourne les tuiles de construction disponibles selon la taille maximale

        Args:
            max_size: Taille maximale (niveau de l'action Construction)

        Returns:
            Liste des tuiles de construction disponibles (taille <= max_size)
        """
        # Définir toutes les tuiles de construction possibles
        # Chaque tuile a une forme définie par ses hexagones relatifs
        all_tiles = {
            1: [
                {
                    "id": "tile_1_single",
                    "size": 1,
                    "name": "Tuile Simple",
                    "shape": "single",
                    "hexagons": [{"q": 0, "r": 0}],  # 1 hexagone
                    "cost": 2,
                }
            ],
            2: [
                {
                    "id": "tile_2_line",
                    "size": 2,
                    "name": "Tuile Ligne 2",
                    "shape": "line",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                    ],  # 2 hexagones en ligne verticale
                    "cost": 4,
                }
            ],
            3: [
                {
                    "id": "tile_3_line",
                    "size": 3,
                    "name": "Tuile Ligne 3",
                    "shape": "line",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": 0, "r": 2},
                    ],  # 3 hexagones en ligne
                    "cost": 6,
                },
                {
                    "id": "tile_3_L",
                    "size": 3,
                    "name": "Tuile L",
                    "shape": "L",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": 1, "r": 1},
                    ],  # Forme L
                    "cost": 6,
                },
            ],
            4: [
                {
                    "id": "tile_4_line",
                    "size": 4,
                    "name": "Tuile Ligne 4",
                    "shape": "line",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": 0, "r": 2},
                        {"q": 0, "r": 3},
                    ],
                    "cost": 8,
                },
                {
                    "id": "tile_4_square",
                    "size": 4,
                    "name": "Tuile Carré",
                    "shape": "square",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 1, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": 1, "r": 1},
                    ],
                    "cost": 8,
                },
                {
                    "id": "tile_4_T",
                    "size": 4,
                    "name": "Tuile T",
                    "shape": "T",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": -1, "r": 1},
                        {"q": 1, "r": 1},
                    ],
                    "cost": 8,
                },
            ],
            5: [
                {
                    "id": "tile_5_line",
                    "size": 5,
                    "name": "Tuile Ligne 5",
                    "shape": "line",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": 0, "r": 2},
                        {"q": 0, "r": 3},
                        {"q": 0, "r": 4},
                    ],
                    "cost": 10,
                },
                {
                    "id": "tile_5_cross",
                    "size": 5,
                    "name": "Tuile Croix",
                    "shape": "cross",
                    "hexagons": [
                        {"q": 0, "r": 0},
                        {"q": 0, "r": 1},
                        {"q": -1, "r": 1},
                        {"q": 1, "r": 1},
                        {"q": 0, "r": 2},
                    ],
                    "cost": 10,
                },
            ],
        }

        # Retourner toutes les tuiles de taille <= max_size
        available_tiles = []
        for size in range(1, max_size + 1):
            if size in all_tiles:
                available_tiles.extend(all_tiles[size])

        return available_tiles

    @staticmethod
    def rotate_tile_hexagons(
        hexagons: List[Dict[str, int]], rotation: int
    ) -> List[Dict[str, int]]:
        """
        Fait pivoter une tuile d'un angle de 60° * rotation
        rotation = 1 : 60° vers la droite
        rotation = -1 : 60° vers la gauche
        rotation = 0 : pas de rotation

        Args:
            hexagons: Liste des hexagones relatifs de la tuile
            rotation: Nombre de rotations (1 = droite, -1 = gauche, 0 = aucune)

        Returns:
            Liste des hexagones après rotation
        """
        if rotation == 0:
            return hexagons

        # Rotation hexagonale : conversion (q, r) avec matrice de rotation
        # Rotation de 60° vers la droite : (q', r') = (-r, q + r)
        # Rotation de 60° vers la gauche : (q', r') = (q + r, -q)
        rotated = []
        for hex in hexagons:
            q, r = hex["q"], hex["r"]
            if rotation > 0:  # Rotation droite (60°)
                for _ in range(rotation):
                    q, r = -r, q + r
            else:  # Rotation gauche (-60°)
                for _ in range(-rotation):
                    q, r = q + r, -q
            rotated.append({"q": q, "r": r})

        return rotated

    @staticmethod
    def validate_tile_placement(
        grid_hexagons: List[Dict[str, Any]],
        tile_hexagons: List[Dict[str, int]],
        anchor_q: int,
        anchor_r: int,
        existing_garnisons: List[Dict[str, Any]],
    ) -> tuple[bool, str]:
        """
        Valide le placement d'une tuile sur la grille

        Args:
            grid_hexagons: Tous les hexagones de la grille
            tile_hexagons: Hexagones relatifs de la tuile (après rotation)
            anchor_q: Colonne d'ancrage (position de référence)
            anchor_r: Position dans la colonne d'ancrage
            existing_garnisons: Garnisons déjà placées

        Returns:
            (is_valid, error_message)
        """
        # Calculer les positions absolues de tous les hexagones de la tuile
        tile_positions = []
        for hex_rel in tile_hexagons:
            abs_q = anchor_q + hex_rel["q"]
            abs_r = anchor_r + hex_rel["r"]
            tile_positions.append((abs_q, abs_r))

        # Vérifier que tous les hexagones de la tuile sont dans la grille
        grid_dict = {(h["q"], h["r"]): h for h in grid_hexagons}

        for q, r in tile_positions:
            if (q, r) not in grid_dict:
                return False, f"L'hexagone ({q}, {r}) est hors de la grille"

            hex = grid_dict[(q, r)]

            # Vérifier que l'hexagone est constructible
            if not hex.get("constructible", True):
                return (
                    False,
                    f"L'hexagone ({q}, {r}) n'est pas constructible (rocher ou eau)",
                )

            # Vérifier que l'hexagone n'est pas déjà occupé par une garnison
            if hex.get("garnison_id") is not None:
                return False, f"L'hexagone ({q}, {r}) est déjà occupé par une garnison"

        return True, "Placement valide"

    @staticmethod
    def initialize_game(game_id: int, players: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Initialise une nouvelle partie

        Args:
            game_id: ID de la partie
            players: Liste des joueurs avec leurs informations (normalisés)

        Returns:
            État initial du jeu
        """
        # Initialiser les Rangers (5 cartes Action) pour chaque joueur
        rangers = GameLogic.initialize_rangers()

        # Initialiser l'état pour chaque joueur
        players_state = {}
        for player in players:
            # S'assurer que player_number est un int
            player_number = int(player["player_number"])
            
            # Générer 8 cartes initiales pour chaque joueur
            initial_cards = GameLogic.generate_initial_cards(8)

            players_state[player_number] = {
                "player_id": int(player["id"]),
                "user_id": int(player["user_id"]),
                "player_number": player_number,
                "armure_meca_id": int(player["armure_meca_id"]) if player.get("armure_meca_id") else None,
                "rangers": [r.copy() for r in rangers],  # Deep copy des Rangers
                "initial_hand": initial_cards,  # 8 cartes initiales à sélectionner
                "hand": [],  # Cartes en main après sélection (4 cartes)
                "hand_selected": False,  # Indique si le joueur a sélectionné ses 4 cartes
                "resources": {
                    "or": 25,  # Pièces d'or (PO) - Les joueurs commencent avec 25 PO
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
                    # Grille hexagonale de base de l'armure méca
                    "grid": GameLogic.initialize_board_grid(),
                    "garnisons": [],
                    "weapon_slots": [],
                    "weapons": [],
                    "armor_pieces": [],
                    "lasers": [],
                    "tokens": [],
                    "special_zones": [],
                },
                "emissaires": 1,
                "x_tokens": 0,
                "last_breath_cards": [],
                "mines": [],
                "can_improve_ranger": False,
                "improve_ranger_pending": False,
                "construction_turn_data": {
                    "action_power": None,
                    "constructions_placed": [],
                    "total_size_used": 0,
                    "is_improved": False,
                },
            }

        # Déterminer l'ordre de jeu initial (aléatoire)
        player_numbers = [int(p["player_number"]) for p in players]
        random.shuffle(player_numbers)

        game_state = {
            "game_id": int(game_id),
            "status": "started",
            "turn_number": 1,
            "current_player": player_numbers[0] if player_numbers else None,
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

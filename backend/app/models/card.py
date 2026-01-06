"""
Modèles pour récupérer les cartes depuis la base de données
"""
from typing import Dict, List, Any, Optional
from app.core.database import Database
import json


class TroupeModel:
    """Modèle pour les cartes Troupes (ex-Animaux)"""
    
    @staticmethod
    def get_random(count: int = 1) -> List[Dict[str, Any]]:
        """Récupère des cartes Troupes aléatoires depuis la DB"""
        try:
            with Database.get_cursor() as cur:
                cur.execute("""
                    SELECT 
                        t.id, t.card_number, t.original_name, t.mapped_name,
                        t.weapon_type_id, t.size, t.cost,
                        t.points_degats, t.nombre_lasers, 
                        t.points_developpement_technique, t.paires_ailes,
                        t.raw_materials_required, t.bonus, t.effet_invocation,
                        t.effet_quotidien, t.dernier_souffle,
                        t.type_garnison, t.garnison_standard_minimum,
                        t.garnison_sans_adjacence, t.adjacent_lave, t.adjacent_vide,
                        t.original_data,
                        wt.code as weapon_type_code, wt.name as weapon_type_name
                    FROM troupes t
                    LEFT JOIN weapon_types wt ON t.weapon_type_id = wt.id
                    ORDER BY RANDOM()
                    LIMIT %s
                """, (count,))
                results = cur.fetchall()
                
                cards = []
                for row in results:
                    card = dict(row)
                    # Convertir JSONB en dict Python
                    if card.get('raw_materials_required'):
                        if isinstance(card['raw_materials_required'], str):
                            card['raw_materials_required'] = json.loads(card['raw_materials_required'])
                    if card.get('original_data'):
                        if isinstance(card['original_data'], str):
                            card['original_data'] = json.loads(card['original_data'])
                    # Ajouter le type pour le frontend
                    card['type'] = 'troupe'
                    card['id'] = f"troupe_{card['id']}"
                    cards.append(card)
                
                return cards
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les troupes depuis la DB: {e}")
            return []


class TechnologyModel:
    """Modèle pour les cartes Technologies (ex-Mécènes)"""
    
    @staticmethod
    def get_random(count: int = 1) -> List[Dict[str, Any]]:
        """Récupère des cartes Technologies aléatoires depuis la DB"""
        try:
            with Database.get_cursor() as cur:
                cur.execute("""
                    SELECT 
                        id, card_number, original_name, mapped_name,
                        is_armor_piece, armor_piece_type, level,
                        points_degats, nombre_lasers,
                        points_developpement_technique, paires_ailes,
                        cost, or_par_jour, bonus, effet_invocation,
                        effet_quotidien, dernier_souffle, original_data
                    FROM technologies
                    ORDER BY RANDOM()
                    LIMIT %s
                """, (count,))
                results = cur.fetchall()
                
                cards = []
                for row in results:
                    card = dict(row)
                    # Convertir JSONB en dict Python
                    if card.get('original_data'):
                        if isinstance(card['original_data'], str):
                            card['original_data'] = json.loads(card['original_data'])
                    # Pour les technologies, cost = niveau requis du Ranger Bleu (level)
                    # Le level est le niveau de la carte elle-même
                    card['type'] = 'technology'
                    card['id'] = f"technology_{card['id']}"
                    # Le nom doit être unique, utiliser mapped_name
                    card['name'] = card['mapped_name']
                    # Pour les technologies, le cost représente le niveau requis (level)
                    if card.get('level'):
                        card['cost'] = card['level']  # Niveau requis = level de la carte
                    cards.append(card)
                
                return cards
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les technologies depuis la DB: {e}")
            return []


class QueteModel:
    """Modèle pour les cartes Quêtes (ex-Projets de Conservation)"""
    
    @staticmethod
    def get_random(count: int = 1) -> List[Dict[str, Any]]:
        """Récupère des cartes Quêtes aléatoires depuis la DB"""
        try:
            with Database.get_cursor() as cur:
                cur.execute("""
                    SELECT 
                        id, card_number, original_name, mapped_name,
                        quest_type, condition_type, conditions, rewards,
                        original_data
                    FROM quetes
                    ORDER BY RANDOM()
                    LIMIT %s
                """, (count,))
                results = cur.fetchall()
                
                cards = []
                for row in results:
                    card = dict(row)
                    # Convertir JSONB en dict Python
                    if card.get('conditions'):
                        if isinstance(card['conditions'], str):
                            card['conditions'] = json.loads(card['conditions'])
                    if card.get('rewards'):
                        if isinstance(card['rewards'], str):
                            card['rewards'] = json.loads(card['rewards'])
                    if card.get('original_data'):
                        if isinstance(card['original_data'], str):
                            card['original_data'] = json.loads(card['original_data'])
                    card['type'] = 'quete'
                    card['id'] = f"quete_{card['id']}"
                    card['name'] = card['mapped_name']
                    cards.append(card)
                
                return cards
        except Exception as e:
            print(f"[ERREUR] Impossible de récupérer les quêtes depuis la DB: {e}")
            return []


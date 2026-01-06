"""
Script pour importer les données mappées depuis l'ODS vers PostgreSQL
Ce script applique TOUS les mappings Timeline Ranger lors de l'import
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values, Json
import json
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import os
from dotenv import load_dotenv
import numpy as np

# Charger les variables d'environnement
load_dotenv()

# Mapping des catégories d'animaux vers types d'armes
WEAPON_TYPE_MAPPING = {
    'Prédateur': 'explosifs',
    'Animal domestique': 'munitions_standard',
    'Animal marin': 'torpilles',
    'Herbivore': 'munitions_nucleaires',
    'Oiseau': 'missiles_aeriens',
    'Ours': 'armes_lourdes',
    'Primate': 'armes_intelligentes',
    'Reptile': 'armes_toxiques'
}

# Mapping des continents vers matières premières
RAW_MATERIAL_MAPPING = {
    'Afrique': 'titanium',
    'Amériques': 'platine',
    'Asie': 'vibranium',
    'Australie': 'carbone',
    'Europe': 'kevlar'
}

# Mapping des points
POINTS_MAPPING = {
    'Points Attrait': 'points_degats',
    'Points Conservation': 'nombre_lasers',
    'Points Réputation': 'points_developpement_technique',
    'Points Science': 'paires_ailes'
}

# Mapping des ressources
RESOURCES_MAPPING = {
    'Crédits': 'cost',
    'Revenus (fond violet)': 'or_par_jour'
}

class TimelineRangerImporter:
    """Importateur pour Timeline Ranger avec tous les mappings."""
    
    def __init__(self, db_config: Optional[Dict] = None):
        # Si db_config n'est pas fourni, utiliser les variables d'environnement
        if db_config is None:
            db_config = {
                'host': os.getenv('SUPABASE_HOST', 'localhost'),
                'database': os.getenv('SUPABASE_DB', 'postgres'),
                'user': os.getenv('SUPABASE_USER', 'postgres'),
                'password': os.getenv('SUPABASE_PASSWORD', 'password'),
                'port': os.getenv('SUPABASE_PORT', '5432'),
                'sslmode': 'require'  # Supabase requiert SSL
            }
        
        self.conn = psycopg2.connect(**db_config)
        self.cur = self.conn.cursor()
        self.weapon_type_cache = {}
        self.raw_material_cache = {}
        self._load_caches()
    
    def _safe_int(self, value, default=0):
        """Convertit une valeur en int de manière sécurisée."""
        if pd.isna(value) or value is None:
            return default
        if isinstance(value, (int, float)):
            if np.isnan(value):
                return default
            try:
                return int(value)
            except (ValueError, OverflowError):
                return default
        if isinstance(value, str):
            # Essayer d'extraire un nombre de la chaîne
            import re
            numbers = re.findall(r'-?\d+', value)
            if numbers:
                try:
                    return int(numbers[0])
                except (ValueError, OverflowError):
                    return default
            return default
        return default
    
    def _clean_dict_for_json(self, data: dict) -> dict:
        """Nettoie un dictionnaire en remplaçant NaN/None par None pour JSON."""
        cleaned = {}
        for key, value in data.items():
            if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
                cleaned[key] = None
            elif isinstance(value, dict):
                cleaned[key] = self._clean_dict_for_json(value)
            elif isinstance(value, list):
                cleaned[key] = [self._clean_dict_for_json(item) if isinstance(item, dict) 
                               else (None if (pd.isna(item) or (isinstance(item, float) and np.isnan(item))) else item)
                               for item in value]
            else:
                cleaned[key] = value
        return cleaned
    
    def _load_caches(self):
        """Charge les caches des types d'armes et matières premières."""
        # Cache des types d'armes
        self.cur.execute("SELECT id, code FROM weapon_types")
        for row in self.cur.fetchall():
            self.weapon_type_cache[row[1]] = row[0]
        
        # Cache des matières premières
        self.cur.execute("SELECT id, code FROM raw_materials")
        for row in self.cur.fetchall():
            self.raw_material_cache[row[1]] = row[0]
    
    def get_weapon_type_id(self, category: str) -> Optional[int]:
        """Obtient l'ID du type d'arme depuis la catégorie."""
        if not category:
            return None
        
        # Gérer les catégories combinées (ex: "Prédateur ; Ours")
        categories = [c.strip() for c in category.split(';')]
        primary_category = categories[0]
        
        weapon_code = WEAPON_TYPE_MAPPING.get(primary_category)
        if weapon_code:
            return self.weapon_type_cache.get(weapon_code)
        return None
    
    def get_raw_materials(self, continents: str) -> List[Dict]:
        """Obtient les matières premières depuis les continents."""
        if not continents:
            return []
        
        materials = []
        continent_list = [c.strip() for c in continents.split(';')]
        
        for continent in continent_list:
            material_code = RAW_MATERIAL_MAPPING.get(continent)
            if material_code and material_code in self.raw_material_cache:
                materials.append({
                    'material_id': self.raw_material_cache[material_code],
                    'quantity': 1
                })
        
        return materials
    
    def map_points(self, row: pd.Series) -> Dict:
        """Mappe les points selon le mapping Timeline Ranger."""
        points = {
            'points_degats': 0,
            'nombre_lasers': 0,
            'points_developpement_technique': 0,
            'paires_ailes': 0
        }
        
        # Points Attrait → Points de Dégâts
        if 'Points Attrait' in row and pd.notna(row['Points Attrait']):
            points['points_degats'] = int(row['Points Attrait'])
        
        # Points Conservation → Nombre de Lasers
        if 'Points Conservation' in row and pd.notna(row['Points Conservation']):
            points['nombre_lasers'] = self._safe_int(row.get('Points Conservation', 0), 0)
        
        # Points Réputation → Points de Développement Technique
        if 'Points Réputation' in row and pd.notna(row['Points Réputation']):
            points['points_developpement_technique'] = self._safe_int(row.get('Points Réputation', 0), 0)
        
        # Points Science → Paires d'Ailes
        if 'Points Science' in row and pd.notna(row['Points Science']):
            points['paires_ailes'] = self._safe_int(row.get('Points Science', 0), 0)
        
        return points
    
    def get_mapped_name(self, original_name: str, card_type: str, row: pd.Series) -> str:
        """Obtient le nom mappé depuis les fichiers de mapping."""
        # Charger les fichiers de mapping
        mapping_files = {
            'Animal': 'MAPPING_NOMS_COMPLET.md',  # Ou fichiers spécifiques
            'Mécène': 'MAPPING_NOMS_MECENES.md',
            'Projet_de_conservation': 'MAPPING_NOMS_PROJETS_CONSERVATION.md'
        }
        
        # Pour l'instant, utiliser le nom original avec préfixe
        if card_type == 'Animal':
            category = row.get('Catégorie', '')
            weapon_type = WEAPON_TYPE_MAPPING.get(category.split(';')[0].strip(), 'Arme')
            return f"{weapon_type.title()} - {original_name}"
        elif card_type == 'Mécène':
            # Vérifier si c'est une pièce d'armure ou une action
            # Pour l'instant, utiliser "Système" par défaut
            return f"Système {original_name}"
        elif card_type == 'Projet_de_conservation':
            return f"Quête : {original_name}"
        
        return original_name
    
    def parse_enclos(self, row: pd.Series) -> Dict:
        """Parse les colonnes d'enclos pour déterminer type_garnison, garnison_standard_minimum, adjacences."""
        result = {
            'type_garnison': None,
            'garnison_standard_minimum': False,
            'garnison_sans_adjacence': False,
            'adjacent_lave': False,
            'adjacent_vide': False
        }
        
        # Enclos standard (minimum)
        if pd.notna(row.get('Enclos standard (minimum)')):
            result['garnison_standard_minimum'] = True
        
        # Enclos sans adjacence case
        if pd.notna(row.get('Enclos sans adjacence case')):
            result['garnison_sans_adjacence'] = True
        
        # Adjacent case Rocher → adjacent_lave
        if pd.notna(row.get('Adjacent case Rocher')):
            result['adjacent_lave'] = True
        
        # Adjacent case Eau → adjacent_vide
        if pd.notna(row.get('Adjacent case Eau')):
            result['adjacent_vide'] = True
        
        # Type de garnison (Vivarium, Grande volière, Aquarium, Parc animalier)
        if pd.notna(row.get('Vivarium à reptiles')):
            result['type_garnison'] = 'Vivarium'
        elif pd.notna(row.get('Grande volière')):
            result['type_garnison'] = 'Grande volière'
        elif pd.notna(row.get('Aquarium')):
            result['type_garnison'] = 'Aquarium'
        elif pd.notna(row.get('Parc animalier')):
            result['type_garnison'] = 'Parc animalier'
        elif pd.notna(row.get('Enclos')):
            # Parser "Enclos" pour déterminer le type
            enclos = str(row.get('Enclos', ''))
            if 'Parc' in enclos:
                result['type_garnison'] = 'Parc animalier'
            elif 'Aquarium' in enclos:
                result['type_garnison'] = 'Aquarium'
            elif 'Volière' in enclos:
                result['type_garnison'] = 'Grande volière'
            elif 'Vivarium' in enclos:
                result['type_garnison'] = 'Vivarium'
        
        return result
    
    def parse_conditions(self, row: pd.Series, column_name: str) -> Optional[Dict]:
        """Parse les conditions depuis une colonne."""
        if pd.isna(row.get(column_name)):
            return None
        
        conditions_text = str(row.get(column_name, ''))
        if not conditions_text or conditions_text.strip() == '':
            return None
        
        # Pour l'instant, stocker le texte brut dans un JSONB
        # On pourra parser plus tard selon les besoins
        return {
            'texte': conditions_text,
            'raw': conditions_text
        }
    
    def import_troupes(self, ods_file: str):
        """Importe les troupes (ex-Animaux) depuis l'ODS."""
        print("Import des troupes (Animaux)...")
        
        df = pd.read_excel(ods_file, sheet_name='Animal', engine='odf')
        
        troupes = []
        for _, row in df.iterrows():
            card_number = self._safe_int(row.get('N° Carte', 0), 0)
            if card_number == 0:
                continue  # Ignorer les lignes sans numéro de carte
            
            # Nom Animal → mapped_name (nom mappé)
            original_name = str(row.get('Nom Animal', ''))
            if not original_name or original_name.strip() == '':
                continue
            
            # Obtenir le nom mappé depuis la catégorie
            category = str(row.get('Catégorie(s) d\'animal (icônes en haut à droite)', ''))
            weapon_type_code = WEAPON_TYPE_MAPPING.get(category.split(';')[0].strip(), 'Arme')
            mapped_name = f"{weapon_type_code.replace('_', ' ').title()} - {original_name}"
            
            # Obtenir le type d'arme
            weapon_type_id = self.get_weapon_type_id(category)
            
            # Mapper les points (utiliser les colonnes individuelles)
            points = {
                'points_degats': self._safe_int(row.get('Points Attrait', 0), 0),
                'nombre_lasers': self._safe_int(row.get('Points Conservation', 0), 0),
                'points_developpement_technique': self._safe_int(row.get('Points Réputation', 0), 0),
                'paires_ailes': 0  # Points Science n'existe pas dans cette feuille
            }
            
            # Obtenir les matières premières depuis Continent(s) d'origine
            continents = str(row.get('Continent(s) d\'origine (icônes en haut à droite)', ''))
            raw_materials = self.get_raw_materials(continents)
            
            # Parser les informations d'enclos
            enclos_info = self.parse_enclos(row)
            
            # Conditions
            conditions = self.parse_conditions(row, 'Condition(s) (icônes à gauche sur un bandeau rouge)')
            
            # Créer l'objet troupe
            troupe = {
                'card_number': card_number,
                'original_name': original_name,
                'mapped_name': mapped_name,
                'weapon_type_id': weapon_type_id,
                'size': self._safe_int(row.get('Taille', 0), None) if pd.notna(row.get('Taille')) else None,
                'cost': self._safe_int(row.get('Crédits', 0), 0),
                'points_degats': points['points_degats'],
                'nombre_lasers': points['nombre_lasers'],
                'points_developpement_technique': points['points_developpement_technique'],
                'paires_ailes': points['paires_ailes'],
                'raw_materials_required': Json(raw_materials),
                'original_data': Json(self._clean_dict_for_json(row.to_dict())),
                'bonus': str(row.get('Capacité', '')) if pd.notna(row.get('Capacité')) else None,
                'effet_du_vide': str(row.get('Effet Corallien', '')) if pd.notna(row.get('Effet Corallien')) else None,
                'effet_invocation': None,  # Pas dans cette feuille
                'effet_quotidien': None,  # Pas dans cette feuille
                'dernier_souffle': None,  # Pas dans cette feuille
                'type_garnison': enclos_info['type_garnison'],
                'garnison_standard_minimum': enclos_info['garnison_standard_minimum'],
                'garnison_sans_adjacence': enclos_info['garnison_sans_adjacence'],
                'adjacent_lave': enclos_info['adjacent_lave'],
                'adjacent_vide': enclos_info['adjacent_vide'],
                'conditions': Json(conditions) if conditions else None,
                'vague': str(row.get('Vague', '')) if pd.notna(row.get('Vague')) else None,
                'jeu_base': True if pd.notna(row.get('Jeu de base')) else False,
                'jeu_mondes_marins': True if pd.notna(row.get('Jeu avec extension Mondes Marins')) else False,
                'promo': True if pd.notna(row.get('Promo')) else False,
            }
            
            troupes.append(troupe)
        
        # Insérer dans PostgreSQL
        insert_query = """
        INSERT INTO troupes (
            card_number, original_name, mapped_name, weapon_type_id, size, cost,
            points_degats, nombre_lasers, points_developpement_technique, paires_ailes,
            raw_materials_required, original_data, bonus, effet_du_vide,
            type_garnison, garnison_standard_minimum, garnison_sans_adjacence,
            adjacent_lave, adjacent_vide, conditions, vague, jeu_base,
            jeu_mondes_marins, promo
        ) VALUES %s
        ON CONFLICT (card_number) DO UPDATE
        SET mapped_name = EXCLUDED.mapped_name,
            weapon_type_id = EXCLUDED.weapon_type_id,
            size = EXCLUDED.size,
            cost = EXCLUDED.cost,
            points_degats = EXCLUDED.points_degats,
            nombre_lasers = EXCLUDED.nombre_lasers,
            points_developpement_technique = EXCLUDED.points_developpement_technique,
            paires_ailes = EXCLUDED.paires_ailes,
            raw_materials_required = EXCLUDED.raw_materials_required,
            original_data = EXCLUDED.original_data,
            bonus = EXCLUDED.bonus,
            effet_du_vide = EXCLUDED.effet_du_vide,
            type_garnison = EXCLUDED.type_garnison,
            garnison_standard_minimum = EXCLUDED.garnison_standard_minimum,
            garnison_sans_adjacence = EXCLUDED.garnison_sans_adjacence,
            adjacent_lave = EXCLUDED.adjacent_lave,
            adjacent_vide = EXCLUDED.adjacent_vide,
            conditions = EXCLUDED.conditions,
            vague = EXCLUDED.vague,
            jeu_base = EXCLUDED.jeu_base,
            jeu_mondes_marins = EXCLUDED.jeu_mondes_marins,
            promo = EXCLUDED.promo,
            updated_at = NOW()
        """
        
        values = [(
            t['card_number'], t['original_name'], t['mapped_name'], t['weapon_type_id'],
            t['size'], t['cost'], t['points_degats'], t['nombre_lasers'],
            t['points_developpement_technique'], t['paires_ailes'],
            t['raw_materials_required'], t['original_data'], t['bonus'],
            t['effet_du_vide'], t['type_garnison'], t['garnison_standard_minimum'],
            t['garnison_sans_adjacence'], t['adjacent_lave'], t['adjacent_vide'],
            t['conditions'], t['vague'], t['jeu_base'],
            t['jeu_mondes_marins'], t['promo']
        ) for t in troupes]
        
        execute_values(self.cur, insert_query, values)
        self.conn.commit()
        
        print(f"[OK] {len(troupes)} troupes importees")
    
    def parse_points_combined(self, row: pd.Series) -> Dict:
        """Parse la colonne 'Points Attrait/Conservation/Réputation' combinée."""
        points = {
            'points_degats': 0,
            'nombre_lasers': 0,
            'points_developpement_technique': 0,
            'paires_ailes': 0
        }
        
        # Essayer d'abord les colonnes individuelles
        if 'Points Attrait' in row and pd.notna(row.get('Points Attrait')):
            points['points_degats'] = self._safe_int(row.get('Points Attrait', 0), 0)
        
        if 'Points Conservation' in row and pd.notna(row.get('Points Conservation')):
            points['nombre_lasers'] = self._safe_int(row.get('Points Conservation', 0), 0)
        
        if 'Points Réputation' in row and pd.notna(row.get('Points Réputation')):
            points['points_developpement_technique'] = self._safe_int(row.get('Points Réputation', 0), 0)
        
        # Si la colonne combinée existe, essayer de la parser
        if 'Points Attrait/Conservation/Réputation' in row and pd.notna(row.get('Points Attrait/Conservation/Réputation')):
            combined = str(row.get('Points Attrait/Conservation/Réputation', ''))
            # Parser le format "X Attrait, Y Conservation, Z Réputation"
            # À adapter selon le format réel
        
        return points
    
    def import_technologies(self, ods_file: str):
        """Importe les technologies (ex-Mécènes) depuis l'ODS."""
        print("Import des technologies (Mécènes)...")
        
        # Essayer différentes variantes du nom de feuille
        sheet_names = ['Mécène', 'Mcne', 'Mecene']
        df = None
        
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(ods_file, sheet_name=sheet_name, engine='odf')
                break
            except:
                continue
        
        if df is None:
            print("[ERREUR] Impossible de trouver la feuille Mecene")
            return
        
        technologies = []
        for _, row in df.iterrows():
            card_number = self._safe_int(row.get('N° Carte', 0), 0)
            if card_number == 0:
                continue
            
            original_name = str(row.get('Nom Mécène', ''))
            if not original_name or original_name.strip() == '':
                continue
            
            # Nom mappé (utiliser original_name directement comme mapped_name pour l'instant)
            mapped_name = original_name
            
            # Déterminer si c'est une pièce d'armure ou une action
            # (basé sur l'effet - à adapter selon vos critères)
            is_armor_piece = False  # À déterminer selon les effets
            armor_piece_type = None
            
            # Niveau → niveau requis du Ranger Bleu
            level = self._safe_int(row.get('Niveau', 0), None) if pd.notna(row.get('Niveau')) else None
            
            # Mapper les points (utiliser la fonction combinée)
            points = self.parse_points_combined(row)
            
            # Conditions
            conditions = self.parse_conditions(row, 'Condition(s) (icônes à gauche sur un bandeau rouge)')
            
            # Icône(s) obtenue(s) → bonus
            bonus = str(row.get('Icône(s) obtenue(s) (icônes en haut à droite)', '')) if pd.notna(row.get('Icône(s) obtenue(s) (icônes en haut à droite)')) else None
            
            technology = {
                'card_number': card_number,
                'original_name': original_name,
                'mapped_name': mapped_name,
                'is_armor_piece': is_armor_piece,
                'armor_piece_type': armor_piece_type,
                'level': level,
                'points_degats': points['points_degats'],
                'nombre_lasers': points['nombre_lasers'],
                'points_developpement_technique': points['points_developpement_technique'],
                'paires_ailes': points['paires_ailes'],
                'cost': level,  # Pour technologies, cost = niveau requis (level)
                'or_par_jour': self._safe_int(row.get('Revenus (fond violet)', 0), 0),
                'bonus': bonus,
                'effet_invocation': str(row.get('Effet unique immédiat (fond jaune)', '')) if pd.notna(row.get('Effet unique immédiat (fond jaune)')) else None,
                'effet_quotidien': str(row.get('Effet permanent/récurrent (fond bleu)', '')) if pd.notna(row.get('Effet permanent/récurrent (fond bleu)')) else None,
                'dernier_souffle': str(row.get('Effet (unique) de fin de partie [lors du décompte final] (fond marron)', '')) if pd.notna(row.get('Effet (unique) de fin de partie [lors du décompte final] (fond marron)')) else None,
                'conditions': Json(conditions) if conditions else None,
                'original_data': Json(self._clean_dict_for_json(row.to_dict())),
                'vague': str(row.get('Vague', '')) if pd.notna(row.get('Vague')) else None,
                'jeu_base': True if pd.notna(row.get('Jeu de base')) else False,
                'jeu_mondes_marins': True if pd.notna(row.get('Jeu avec extension Mondes Marins')) else False,
                'promo': True if pd.notna(row.get('Promo')) else False,
                'remplacee_par': self._safe_int(row.get('Remplacée par extension Mondes Marins', 0), None) if pd.notna(row.get('Remplacée par extension Mondes Marins')) else None,
            }
            
            technologies.append(technology)
        
        # Insérer dans PostgreSQL
        insert_query = """
        INSERT INTO technologies (
            card_number, original_name, mapped_name, is_armor_piece, armor_piece_type,
            level, points_degats, nombre_lasers, points_developpement_technique,
            paires_ailes, cost, or_par_jour, original_data
        ) VALUES %s
        ON CONFLICT (card_number) DO UPDATE
        SET mapped_name = EXCLUDED.mapped_name,
            is_armor_piece = EXCLUDED.is_armor_piece,
            armor_piece_type = EXCLUDED.armor_piece_type,
            level = EXCLUDED.level,
            points_degats = EXCLUDED.points_degats,
            nombre_lasers = EXCLUDED.nombre_lasers,
            points_developpement_technique = EXCLUDED.points_developpement_technique,
            paires_ailes = EXCLUDED.paires_ailes,
            cost = EXCLUDED.cost,
            or_par_jour = EXCLUDED.or_par_jour,
            original_data = EXCLUDED.original_data,
            updated_at = NOW()
        """
        
        values = [(
            t['card_number'], t['original_name'], t['mapped_name'],
            t['is_armor_piece'], t['armor_piece_type'], t['level'],
            t['points_degats'], t['nombre_lasers'], t['points_developpement_technique'],
            t['paires_ailes'], t['cost'], t['or_par_jour'], t['original_data']
        ) for t in technologies]
        
        execute_values(self.cur, insert_query, values)
        self.conn.commit()
        
        print(f"[OK] {len(technologies)} technologies importees")
    
    def parse_recompenses(self, row: pd.Series) -> Dict:
        """Parse les récompenses depuis les colonnes Récompense(s)."""
        rewards = {
            'conservation': None,
            'condition_taille_animal': None,
            'reputation': None,
            'autre': None,
            'texte_complet': None
        }
        
        # Récompense(s) - texte complet
        if pd.notna(row.get('Récompense(s)')):
            rewards['texte_complet'] = str(row.get('Récompense(s)', ''))
        
        # Récompense Conservation
        if pd.notna(row.get('Récompense Conservation')):
            rewards['conservation'] = str(row.get('Récompense Conservation', ''))
        
        # Récompense Condition Taille animal
        if pd.notna(row.get('Récompense Condition Taille animal')):
            rewards['condition_taille_animal'] = str(row.get('Récompense Condition Taille animal', ''))
        
        # Récompense Réputation
        if pd.notna(row.get('Récompense Réputation')):
            rewards['reputation'] = str(row.get('Récompense Réputation', ''))
        
        # Récompense …
        if pd.notna(row.get('Récompense …')):
            rewards['autre'] = str(row.get('Récompense …', ''))
        
        return rewards
    
    def parse_prerequis(self, row: pd.Series) -> Dict:
        """Parse tous les prérequis depuis les colonnes Prérequis*."""
        prerequis = {
            'texte': None,
            'nb_icones': None,
            'icones': None,
            'categorie_continent_animal': None,
            'zoo_partenaire': None,
            'specific_requirements': None
        }
        
        # Prérequis (texte) → conditions détaillées
        if pd.notna(row.get('Prérequis (texte)')):
            prerequis['texte'] = str(row.get('Prérequis (texte)', ''))
        
        # Prérequis Nb. icônes
        if pd.notna(row.get('Prérequis Nb. icônes')):
            prerequis['nb_icones'] = str(row.get('Prérequis Nb. icônes', ''))
        
        # Prérequis Icônes
        if pd.notna(row.get('Prérequis Icônes')):
            prerequis['icones'] = str(row.get('Prérequis Icônes', ''))
        
        # Prérequis Catégorie/Continent Animal
        if pd.notna(row.get('Prérequis Catégorie/Continent Animal')):
            prerequis['categorie_continent_animal'] = str(row.get('Prérequis Catégorie/Continent Animal', ''))
        
        # Prérequis Zoo partenaire
        if pd.notna(row.get('Prérequis Zoo partenaire')):
            prerequis['zoo_partenaire'] = str(row.get('Prérequis Zoo partenaire', ''))
        
        # Specific Requirements
        if pd.notna(row.get('Specific Requirements')):
            prerequis['specific_requirements'] = str(row.get('Specific Requirements', ''))
        
        return prerequis
    
    def import_quetes(self, ods_file: str):
        """Importe les quêtes (ex-Projets de Conservation) depuis l'ODS."""
        print("Import des quêtes (Projets de Conservation)...")
        
        sheet_names = ['Projet_de_conservation', 'Projet de conservation', 'Projet']
        df = None
        
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(ods_file, sheet_name=sheet_name, engine='odf')
                break
            except:
                continue
        
        if df is None:
            print("[ERREUR] Impossible de trouver la feuille Projet de Conservation")
            return
        
        quetes = []
        for _, row in df.iterrows():
            card_number = self._safe_int(row.get('N° Carte', 0), 0)
            if card_number == 0:
                continue
            
            original_name = str(row.get('Nom Projet de conservation', ''))
            if not original_name or original_name.strip() == '':
                continue
            
            mapped_name = f"Quête : {original_name}"
            
            # Parser les prérequis (conditions)
            prerequis = self.parse_prerequis(row)
            
            # Parser les récompenses
            recompenses = self.parse_recompenses(row)
            
            # Bonus (en bas à droite) gagné par le joueur posant la carte
            bonus = str(row.get('Bonus (en bas à droite) gagné par le joueur posant la carte', '')) if pd.notna(row.get('Bonus (en bas à droite) gagné par le joueur posant la carte')) else None
            
            quete = {
                'card_number': card_number,
                'original_name': original_name,
                'mapped_name': mapped_name,
                'quest_type': 'maitrise',  # À déterminer selon le type (Activity Required)
                'condition_type': str(row.get('Type de condition (texte)', '')) if pd.notna(row.get('Type de condition (texte)', None)) else None,
                'conditions': Json(prerequis),
                'rewards': Json(recompenses),
                'bonus': bonus,
                'original_data': Json(self._clean_dict_for_json(row.to_dict())),
                'vague': str(row.get('Vague', '')) if pd.notna(row.get('Vague')) else None,
                'jeu_base': True if pd.notna(row.get('Jeu de base')) else False,
                'jeu_mondes_marins': True if pd.notna(row.get('Jeu avec extension Mondes Marins')) else False,
                'remplacee_par': self._safe_int(row.get('Remplacée par extension Mondes Marins', 0), None) if pd.notna(row.get('Remplacée par extension Mondes Marins')) else None,
            }
            
            quetes.append(quete)
        
        # Dédupliquer par card_number (garder le dernier)
        seen = {}
        for q in quetes:
            seen[q['card_number']] = q
        quetes_unique = list(seen.values())
        
        # Insérer dans PostgreSQL
        insert_query = """
        INSERT INTO quetes (
            card_number, original_name, mapped_name, quest_type,
            condition_type, conditions, rewards, bonus, original_data,
            vague, jeu_base, jeu_mondes_marins, remplacee_par
        ) VALUES %s
        ON CONFLICT (card_number) DO UPDATE
        SET mapped_name = EXCLUDED.mapped_name,
            quest_type = EXCLUDED.quest_type,
            condition_type = EXCLUDED.condition_type,
            conditions = EXCLUDED.conditions,
            rewards = EXCLUDED.rewards,
            bonus = EXCLUDED.bonus,
            original_data = EXCLUDED.original_data,
            vague = EXCLUDED.vague,
            jeu_base = EXCLUDED.jeu_base,
            jeu_mondes_marins = EXCLUDED.jeu_mondes_marins,
            remplacee_par = EXCLUDED.remplacee_par,
            updated_at = NOW()
        """
        
        values = [(
            q['card_number'], q['original_name'], q['mapped_name'],
            q['quest_type'], q['condition_type'], q['conditions'],
            q['rewards'], q['bonus'], q['original_data'],
            q['vague'], q['jeu_base'], q['jeu_mondes_marins'], q['remplacee_par']
        ) for q in quetes_unique]
        
        execute_values(self.cur, insert_query, values)
        self.conn.commit()
        
        print(f"[OK] {len(quetes_unique)} quetes importees (apres deduplication)")
    
    def create_color_actions(self):
        """Crée les actions de couleur depuis les troupes et technologies."""
        print("Création des actions de couleur...")
        
        # Actions Noires depuis les troupes
        self.cur.execute("""
            INSERT INTO color_actions (ranger_id, action_type, source_type, source_id, name, description)
            SELECT 
                r.id,
                'black',
                'troupe',
                t.id,
                t.mapped_name,
                CONCAT('Installer ', t.mapped_name, ' dans un slot')
            FROM troupes t
            CROSS JOIN rangers r
            WHERE r.color = 'black'
            ON CONFLICT DO NOTHING
        """)
        
        # Actions Bleues depuis les technologies
        self.cur.execute("""
            INSERT INTO color_actions (ranger_id, action_type, source_type, source_id, name, description)
            SELECT 
                r.id,
                'blue',
                'technology',
                t.id,
                t.mapped_name,
                CONCAT('Utiliser ', t.mapped_name)
            FROM technologies t
            CROSS JOIN rangers r
            WHERE r.color = 'blue'
            ON CONFLICT DO NOTHING
        """)
        
        self.conn.commit()
        print("[OK] Actions de couleur creees")
    
    def close(self):
        """Ferme la connexion."""
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    # Configuration : Utiliser les variables d'environnement (.env)
    # Ou fournir une config manuelle si nécessaire
    db_config = None  # Utilisera les variables d'environnement
    
    # Pour une config manuelle (optionnel) :
    # db_config = {
    #     'host': 'db.xxxxx.supabase.co',
    #     'database': 'postgres',
    #     'user': 'postgres',
    #     'password': 'votre_mot_de_passe',
    #     'port': '5432',
    #     'sslmode': 'require'
    # }
    
    ods_file = "Ark_Nova_Mondes_marins_cartes_stats_FR.ods"
    
    if not os.path.exists(ods_file):
        print(f"[ERREUR] Erreur : Fichier ODS non trouve : {ods_file}")
        print("Assurez-vous que le fichier est dans le même dossier que le script.")
        exit(1)
    
    importer = TimelineRangerImporter(db_config)
    
    try:
        # Importer les données
        importer.import_troupes(ods_file)
        importer.import_technologies(ods_file)
        importer.import_quetes(ods_file)
        
        # Créer les actions de couleur
        importer.create_color_actions()
        
        print("\n[OK] Import termine avec succes !")
        
    except Exception as e:
        print(f"[ERREUR] Erreur lors de l'import : {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        importer.close()


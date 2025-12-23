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
    
    def import_troupes(self, ods_file: str):
        """Importe les troupes (ex-Animaux) depuis l'ODS."""
        print("Import des troupes (Animaux)...")
        
        df = pd.read_excel(ods_file, sheet_name='Animal', engine='odf')
        
        troupes = []
        for _, row in df.iterrows():
            card_number = self._safe_int(row.get('N° Carte', 0), 0)
            original_name = str(row.get('Nom', ''))
            
            # Obtenir le nom mappé
            category = str(row.get('Catégorie', ''))
            weapon_type_code = WEAPON_TYPE_MAPPING.get(category.split(';')[0].strip(), 'Arme')
            mapped_name = f"{weapon_type_code.replace('_', ' ').title()} - {original_name}"
            
            # Obtenir le type d'arme
            weapon_type_id = self.get_weapon_type_id(category)
            
            # Mapper les points
            points = self.map_points(row)
            
            # Obtenir les matières premières
            continents = str(row.get('Continent(s) d\'origine', ''))
            raw_materials = self.get_raw_materials(continents)
            
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
                'effet_invocation': str(row.get('Effet unique immédiat (fond jaune)', '')) if pd.notna(row.get('Effet unique immédiat (fond jaune)', None)) else None,
                'effet_quotidien': str(row.get('Effet permanent/récurrent (fond bleu)', '')) if pd.notna(row.get('Effet permanent/récurrent (fond bleu)', None)) else None,
                'dernier_souffle': str(row.get('Effet (unique) de fin de partie [lors du décompte final] (fond marron)', '')) if pd.notna(row.get('Effet (unique) de fin de partie [lors du décompte final] (fond marron)', None)) else None,
            }
            
            troupes.append(troupe)
        
        # Insérer dans PostgreSQL
        insert_query = """
        INSERT INTO troupes (
            card_number, original_name, mapped_name, weapon_type_id, size, cost,
            points_degats, nombre_lasers, points_developpement_technique, paires_ailes,
            raw_materials_required, original_data, bonus, effet_invocation,
            effet_quotidien, dernier_souffle
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
            effet_invocation = EXCLUDED.effet_invocation,
            effet_quotidien = EXCLUDED.effet_quotidien,
            dernier_souffle = EXCLUDED.dernier_souffle,
            updated_at = NOW()
        """
        
        values = [(
            t['card_number'], t['original_name'], t['mapped_name'], t['weapon_type_id'],
            t['size'], t['cost'], t['points_degats'], t['nombre_lasers'],
            t['points_developpement_technique'], t['paires_ailes'],
            t['raw_materials_required'], t['original_data'], t['bonus'],
            t['effet_invocation'], t['effet_quotidien'], t['dernier_souffle']
        ) for t in troupes]
        
        execute_values(self.cur, insert_query, values)
        self.conn.commit()
        
        print(f"[OK] {len(troupes)} troupes importees")
    
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
            original_name = str(row.get('Nom', ''))
            
            # Déterminer si c'est une pièce d'armure ou une action
            # (basé sur l'effet - à adapter selon vos critères)
            is_armor_piece = False  # À déterminer selon les effets
            armor_piece_type = None
            
            # Nom mappé
            mapped_name = f"Système {original_name}"  # Par défaut
            
            # Mapper les points
            points = self.map_points(row)
            
            technology = {
                'card_number': card_number,
                'original_name': original_name,
                'mapped_name': mapped_name,
                'is_armor_piece': is_armor_piece,
                'armor_piece_type': armor_piece_type,
                'level': self._safe_int(row.get('Niveau', 0), None) if pd.notna(row.get('Niveau')) else None,
                'points_degats': points['points_degats'],
                'nombre_lasers': points['nombre_lasers'],
                'points_developpement_technique': points['points_developpement_technique'],
                'paires_ailes': points['paires_ailes'],
                'cost': self._safe_int(row.get('Crédits', 0), 0),
                'or_par_jour': self._safe_int(row.get('Revenus (fond violet)', 0), 0),
                'original_data': Json(self._clean_dict_for_json(row.to_dict())),
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
            original_name = str(row.get('Nom', ''))
            mapped_name = f"Quête : {original_name}"
            
            quete = {
                'card_number': card_number,
                'original_name': original_name,
                'mapped_name': mapped_name,
                'quest_type': 'maitrise',  # À déterminer selon le type
                'condition_type': str(row.get('Type de condition (texte)', '')) if pd.notna(row.get('Type de condition (texte)', None)) else None,
                'conditions': Json({}),
                'rewards': Json({}),
                'original_data': Json(self._clean_dict_for_json(row.to_dict())),
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
            condition_type, conditions, rewards, original_data
        ) VALUES %s
        ON CONFLICT (card_number) DO UPDATE
        SET mapped_name = EXCLUDED.mapped_name,
            quest_type = EXCLUDED.quest_type,
            condition_type = EXCLUDED.condition_type,
            conditions = EXCLUDED.conditions,
            rewards = EXCLUDED.rewards,
            original_data = EXCLUDED.original_data,
            updated_at = NOW()
        """
        
        values = [(
            q['card_number'], q['original_name'], q['mapped_name'],
            q['quest_type'], q['condition_type'], q['conditions'],
            q['rewards'], q['original_data']
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


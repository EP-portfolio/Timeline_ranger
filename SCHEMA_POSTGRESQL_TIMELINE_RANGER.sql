-- ============================================================================
-- Schéma PostgreSQL pour Timeline Ranger
-- Ce schéma reflète TOUS les mappings Ark Nova → Timeline Ranger
-- ============================================================================

-- ============================================================================
-- 1. RANGERS DE COULEURS
-- ============================================================================

CREATE TABLE rangers (
    id SERIAL PRIMARY KEY,
    color VARCHAR(20) UNIQUE NOT NULL,  -- 'blue', 'black', 'orange', 'green', 'yellow'
    name VARCHAR(100) NOT NULL,  -- 'Ranger Bleu', 'Ranger Noir', etc.
    original_action VARCHAR(50),  -- 'ACTION MECENE', 'ACTION ANIMAUX', etc.
    description TEXT,
    role TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insertion des 5 Rangers
INSERT INTO rangers (color, name, original_action, description, role) VALUES
('blue', 'Ranger Bleu', 'ACTION MECENE', 'Ranger spécialisé dans les pièces d''armure', 'Pose des pièces d''armure spéciales'),
('black', 'Ranger Noir', 'ACTION ANIMAUX', 'Ranger spécialisé dans l''installation d''armes', 'Installe des armes dans les slots'),
('orange', 'Ranger Orange', 'ACTION CONSTRUCTION', 'Ranger spécialisé dans la construction', 'Construit des parties d''armure méca et crée des slots'),
('green', 'Ranger Vert', 'ACTION ASSOCIATION', 'Ranger spécialisé dans l''installation de lasers', 'Installe des lasers sur l''armure méca'),
('yellow', 'Ranger Jaune', 'ACTION CARTES', 'Ranger spécialisé dans la gestion de cartes', 'Actions de gestion de cartes');

-- ============================================================================
-- 2. TYPES D'ARMES/MUNITIONS (Mapping Catégories d'Animaux)
-- ============================================================================

CREATE TABLE weapon_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,  -- 'explosifs', 'munitions_standard', etc.
    name VARCHAR(100) NOT NULL,  -- 'Explosifs', 'Munitions Standard', etc.
    original_category VARCHAR(50),  -- 'Prédateur', 'Animal domestique', etc.
    description TEXT,
    characteristics JSONB,  -- Caractéristiques spéciales
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insertion des types d'armes
INSERT INTO weapon_types (code, name, original_category, description) VALUES
('explosifs', 'Explosifs', 'Prédateur', 'Armes explosives et dévastatrices'),
('munitions_standard', 'Munitions Standard', 'Animal domestique', 'Munitions de base, polyvalentes'),
('torpilles', 'Torpilles', 'Animal marin', 'Armes sous-marines, projectiles aquatiques'),
('munitions_nucleaires', 'Munitions Nucléaires', 'Herbivore', 'Armes nucléaires, projectiles radioactifs'),
('missiles_aeriens', 'Missiles Aériens', 'Oiseau', 'Armes volantes, projectiles guidés'),
('armes_lourdes', 'Armes Lourdes', 'Ours', 'Armes de gros calibre, canons lourds'),
('armes_intelligentes', 'Armes Intelligentes', 'Primate', 'Armes guidées IA, systèmes autonomes'),
('armes_toxiques', 'Armes Toxiques', 'Reptile', 'Armes chimiques, venins, acides');

-- ============================================================================
-- 3. MATIÈRES PREMIÈRES (Mapping Continents)
-- ============================================================================

CREATE TABLE raw_materials (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,  -- 'titanium', 'platine', etc.
    name VARCHAR(100) NOT NULL,  -- 'Titanium', 'Platine', etc.
    original_continent VARCHAR(50),  -- 'Afrique', 'Amériques', etc.
    description TEXT,
    characteristics JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insertion des matières premières
INSERT INTO raw_materials (code, name, original_continent, description) VALUES
('titanium', 'Titanium', 'Afrique', 'Métal léger et résistant'),
('platine', 'Platine', 'Amériques', 'Métal précieux et résistant'),
('vibranium', 'Vibranium', 'Asie', 'Matériau ultra-résistant et léger'),
('carbone', 'Carbone', 'Australie', 'Matériau léger et flexible'),
('kevlar', 'Kevlar', 'Europe', 'Matériau composite résistant');

-- ============================================================================
-- 4. ARMURES MÉCA (Mapping Plateaux de Jeu)
-- ============================================================================

CREATE TABLE armures_meca (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,  -- 'plateau_A', 'plateau_1', etc.
    name VARCHAR(100) NOT NULL,  -- 'Armure Méca Débutante', etc.
    original_plateau VARCHAR(50),  -- 'Plateau A', 'Plateau 1', etc.
    type VARCHAR(50),  -- 'Débutant', 'Standard', 'Avancé', 'Spécialisé'
    difficulty VARCHAR(20),  -- 'Facile', 'Moyen', 'Difficile'
    configuration JSONB,  -- Configuration de la grille, zones spéciales, etc.
    special_ability JSONB,  -- Capacité spéciale
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 5. CARTES - TROUPES (Mapping Animaux → Armes)
-- ============================================================================

CREATE TABLE troupes (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,  -- Numéro original de la carte
    original_name VARCHAR(255) NOT NULL,  -- Nom original (ex: "Lion")
    mapped_name VARCHAR(255) NOT NULL,  -- Nom mappé (ex: "Explosif - Lion")
    weapon_type_id INTEGER REFERENCES weapon_types(id),  -- Type d'arme/munition
    size INTEGER,  -- Taille (ex: 1, 2, 3, 4, 5)
    cost INTEGER,  -- Coût en Or (ex-Crédits)
    
    -- Points mappés
    points_degats INTEGER DEFAULT 0,  -- Points Attrait → Points de Dégâts
    nombre_lasers INTEGER DEFAULT 0,  -- Points Conservation → Nombre de Lasers
    points_developpement_technique INTEGER DEFAULT 0,  -- Points Réputation → Points de Développement Technique
    paires_ailes INTEGER DEFAULT 0,  -- Points Science → Nombre de Paires d'Ailes
    
    -- Matières premières requises
    raw_materials_required JSONB,  -- [{material_id: 1, quantity: 2}, ...]
    
    -- Propriétés originales (pour référence)
    original_data JSONB,  -- Toutes les données originales de l'ODS
    
    -- Capacités et effets
    bonus TEXT,  -- Capacité → Bonus
    effet_invocation TEXT,  -- Effet unique immédiat → Effet d'invocation
    effet_quotidien TEXT,  -- Effet permanent/récurrent → Effet quotidien
    dernier_souffle TEXT,  -- Effet de fin de partie → Dernier souffle
    
    -- Garnisons
    type_garnison VARCHAR(100),  -- Enclos → Type Garnison
    garnison_standard_minimum BOOLEAN DEFAULT FALSE,
    garnison_sans_adjacence BOOLEAN DEFAULT FALSE,
    
    -- Adjacences mappées
    adjacent_lave BOOLEAN DEFAULT FALSE,  -- Adjacent case Rocher → Adjacent case Lave
    adjacent_vide BOOLEAN DEFAULT FALSE,  -- Adjacent case Eau → Adjacent case Vide
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_troupes_weapon_type ON troupes(weapon_type_id);
CREATE INDEX idx_troupes_card_number ON troupes(card_number);
CREATE INDEX idx_troupes_mapped_name ON troupes(mapped_name);

-- ============================================================================
-- 6. CARTES - TECHNOLOGIES (Mapping Mécènes → Pièces d'Armure)
-- ============================================================================

CREATE TABLE technologies (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,
    original_name VARCHAR(255) NOT NULL,  -- Nom original (ex: "Fondation Wildlife")
    mapped_name VARCHAR(255) NOT NULL,  -- Nom mappé (ex: "Système Fondation Wildlife" ou "Renfort Fondation")
    is_armor_piece BOOLEAN DEFAULT FALSE,  -- True si c'est une pièce d'armure, False si c'est une action
    armor_piece_type VARCHAR(50),  -- 'Renfort', 'Blindage', 'Composant', 'Dispositif' (si is_armor_piece = true)
    level INTEGER,  -- Niveau
    
    -- Points mappés
    points_degats INTEGER DEFAULT 0,
    nombre_lasers INTEGER DEFAULT 0,
    points_developpement_technique INTEGER DEFAULT 0,
    paires_ailes INTEGER DEFAULT 0,
    
    -- Ressources
    cost INTEGER,  -- Coût en Or (ex-Crédits)
    or_par_jour INTEGER,  -- Revenus → Or par jour
    
    -- Propriétés originales
    original_data JSONB,
    
    -- Effets
    bonus TEXT,
    effet_invocation TEXT,
    effet_quotidien TEXT,
    dernier_souffle TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_technologies_card_number ON technologies(card_number);
CREATE INDEX idx_technologies_is_armor_piece ON technologies(is_armor_piece);

-- ============================================================================
-- 7. CARTES - QUÊTES (Mapping Projets de Conservation)
-- ============================================================================

CREATE TABLE quetes (
    id SERIAL PRIMARY KEY,
    card_number INTEGER UNIQUE NOT NULL,
    original_name VARCHAR(255) NOT NULL,  -- Nom original (ex: "ESPÈCES DIVERSIFIÉES")
    mapped_name VARCHAR(255) NOT NULL,  -- Nom mappé (ex: "Quête : Diversité d'Armes")
    quest_type VARCHAR(50),  -- 'maitrise', 'forteresse', 'environnement', 'programme'
    condition_type VARCHAR(100),  -- Type de condition
    conditions JSONB,  -- Conditions détaillées
    rewards JSONB,  -- Récompenses
    original_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quetes_card_number ON quetes(card_number);
CREATE INDEX idx_quetes_quest_type ON quetes(quest_type);

-- ============================================================================
-- 8. ACTIONS DE COULEUR
-- ============================================================================

CREATE TABLE color_actions (
    id SERIAL PRIMARY KEY,
    ranger_id INTEGER REFERENCES rangers(id),
    action_type VARCHAR(50) NOT NULL,  -- 'blue', 'black', 'orange', 'green', 'yellow'
    source_type VARCHAR(50),  -- 'troupe', 'technology', 'construction', 'association', 'cartes'
    source_id INTEGER,  -- ID de la carte source (troupe, technology, etc.)
    name VARCHAR(255) NOT NULL,
    description TEXT,
    power_required INTEGER,  -- Puissance minimale du Ranger requise
    effects JSONB,  -- Effets de l'action
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_color_actions_ranger ON color_actions(ranger_id);
CREATE INDEX idx_color_actions_type ON color_actions(action_type);

-- ============================================================================
-- 9. UTILISATEURS
-- ============================================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- ============================================================================
-- 10. PARTIES
-- ============================================================================

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,  -- Code pour rejoindre
    host_id INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'waiting',  -- 'waiting', 'playing', 'finished'
    max_players INTEGER DEFAULT 4,
    current_players INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    finished_at TIMESTAMP
);

-- ============================================================================
-- 11. JOUEURS DANS UNE PARTIE
-- ============================================================================

CREATE TABLE game_players (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    user_id INTEGER REFERENCES users(id),
    player_number INTEGER,  -- 1, 2, 3, 4
    armure_meca_id INTEGER REFERENCES armures_meca(id),  -- Armure méca choisie
    score INTEGER DEFAULT 0,
    
    -- Scores détaillés
    total_points_degats INTEGER DEFAULT 0,
    total_lasers INTEGER DEFAULT 0,
    total_points_developpement_technique INTEGER DEFAULT 0,
    total_paires_ailes INTEGER DEFAULT 0,
    
    status VARCHAR(20) DEFAULT 'active',  -- 'active', 'disconnected', 'eliminated'
    joined_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 12. ÉTAT DE LA PARTIE
-- ============================================================================

CREATE TABLE game_states (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    turn_number INTEGER DEFAULT 0,
    current_player INTEGER,  -- player_number
    state_data JSONB,  -- État complet de la partie (Rangers, actions, etc.)
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 13. STATISTIQUES UTILISATEURS
-- ============================================================================

CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    favorite_armure_id INTEGER REFERENCES armures_meca(id),
    favorite_weapon_type_id INTEGER REFERENCES weapon_types(id),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 14. GARNISONS (Mapping Enclos)
-- ============================================================================

CREATE TABLE garnisons (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    position_x INTEGER NOT NULL,
    position_y INTEGER NOT NULL,
    type_garnison VARCHAR(100),  -- Type de garnison
    troupe_id INTEGER REFERENCES troupes(id),  -- Troupe installée (si applicable)
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 15. SLOTS D'ARMES (Créés par Ranger Orange)
-- ============================================================================

CREATE TABLE weapon_slots (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    position_x INTEGER NOT NULL,
    position_y INTEGER NOT NULL,
    size INTEGER NOT NULL,  -- Taille du slot (1-5)
    troupe_id INTEGER REFERENCES troupes(id),  -- Arme installée (si applicable)
    created_at TIMESTAMP DEFAULT NOW(),
    installed_at TIMESTAMP
);

-- ============================================================================
-- 16. PIÈCES D'ARMURE (Posées par Ranger Bleu)
-- ============================================================================

CREATE TABLE armor_pieces (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    technology_id INTEGER REFERENCES technologies(id),  -- Technologie utilisée (pièce d'armure)
    position_x INTEGER,
    position_y INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 17. LASERS (Installés par Ranger Vert)
-- ============================================================================

CREATE TABLE lasers (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    position_x INTEGER,
    position_y INTEGER,
    laser_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- 18. ACTIONS EFFECTUÉES DANS UNE PARTIE
-- ============================================================================

CREATE TABLE game_actions (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    player_id INTEGER REFERENCES game_players(id),
    turn_number INTEGER NOT NULL,
    ranger_id INTEGER REFERENCES rangers(id),
    color_action_id INTEGER REFERENCES color_actions(id),
    action_data JSONB,  -- Détails de l'action
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_game_actions_game ON game_actions(game_id);
CREATE INDEX idx_game_actions_turn ON game_actions(turn_number);

-- ============================================================================
-- VUES UTILES
-- ============================================================================

-- Vue des troupes avec leurs types d'armes
CREATE VIEW v_troupes_with_weapons AS
SELECT 
    t.*,
    wt.name as weapon_type_name,
    wt.code as weapon_type_code
FROM troupes t
LEFT JOIN weapon_types wt ON t.weapon_type_id = wt.id;

-- Vue des actions disponibles par Ranger
CREATE VIEW v_actions_by_ranger AS
SELECT 
    r.color as ranger_color,
    r.name as ranger_name,
    ca.*,
    CASE 
        WHEN ca.source_type = 'troupe' THEN t.mapped_name
        WHEN ca.source_type = 'technology' THEN tech.mapped_name
        ELSE ca.name
    END as source_name
FROM color_actions ca
JOIN rangers r ON ca.ranger_id = r.id
LEFT JOIN troupes t ON ca.source_type = 'troupe' AND ca.source_id = t.id
LEFT JOIN technologies tech ON ca.source_type = 'technology' AND ca.source_id = tech.id;

-- ============================================================================
-- FONCTIONS UTILES
-- ============================================================================

-- Fonction pour obtenir les actions disponibles pour un Ranger
CREATE OR REPLACE FUNCTION get_actions_for_ranger(ranger_color VARCHAR)
RETURNS TABLE (
    action_id INTEGER,
    action_name VARCHAR,
    action_type VARCHAR,
    power_required INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ca.id,
        ca.name,
        ca.action_type,
        ca.power_required
    FROM color_actions ca
    JOIN rangers r ON ca.ranger_id = r.id
    WHERE r.color = ranger_color;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Trigger pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_troupes_updated_at BEFORE UPDATE ON troupes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_technologies_updated_at BEFORE UPDATE ON technologies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quetes_updated_at BEFORE UPDATE ON quetes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- FIN DU SCHÉMA
-- ============================================================================


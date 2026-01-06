-- ============================================================================
-- Migration : Ajout des colonnes manquantes pour le nouveau mapping Ark Nova
-- ============================================================================
-- Ce script ajoute les colonnes nécessaires pour le nouveau mapping complet
-- des cartes Ark Nova vers Timeline Ranger

-- ============================================================================
-- 1. TABLE TROUPES (Cartes Animaux)
-- ============================================================================

-- Effet du vide : Effet spécial des cartes Coralliennes (extension Mondes Marins)
-- Exemple : "Quand vous jouez cette carte, si vous avez X cases vides, gagnez Y"
ALTER TABLE troupes ADD COLUMN IF NOT EXISTS effet_du_vide TEXT;

-- Conditions : Conditions pour jouer la carte (stockées en JSONB)
-- Exemple : {"texte": "Mécène II", "icones_requises": ["Recherche"]}
ALTER TABLE troupes ADD COLUMN IF NOT EXISTS conditions JSONB;

-- Vague : Numéro de vague de sortie de la carte (pour filtrage)
-- Exemple : "1", "2", "3" (pour les extensions)
ALTER TABLE troupes ADD COLUMN IF NOT EXISTS vague VARCHAR(50);

-- Jeu de base : Indique si la carte est disponible dans le jeu de base
ALTER TABLE troupes ADD COLUMN IF NOT EXISTS jeu_base BOOLEAN DEFAULT TRUE;

-- Jeu avec extension Mondes Marins : Indique si la carte est disponible avec l'extension
ALTER TABLE troupes ADD COLUMN IF NOT EXISTS jeu_mondes_marins BOOLEAN DEFAULT FALSE;

-- Promo : Indique si c'est une carte promotionnelle
ALTER TABLE troupes ADD COLUMN IF NOT EXISTS promo BOOLEAN DEFAULT FALSE;

-- ============================================================================
-- 2. TABLE TECHNOLOGIES (Cartes Mécènes)
-- ============================================================================

-- Conditions : Conditions pour jouer la carte (stockées en JSONB)
-- Exemple : {"texte": "Mécène II", "icones_requises": ["Recherche"]}
ALTER TABLE technologies ADD COLUMN IF NOT EXISTS conditions JSONB;

-- Vague : Numéro de vague de sortie de la carte
ALTER TABLE technologies ADD COLUMN IF NOT EXISTS vague VARCHAR(50);

-- Jeu de base : Indique si la carte est disponible dans le jeu de base
ALTER TABLE technologies ADD COLUMN IF NOT EXISTS jeu_base BOOLEAN DEFAULT TRUE;

-- Jeu avec extension Mondes Marins : Indique si la carte est disponible avec l'extension
ALTER TABLE technologies ADD COLUMN IF NOT EXISTS jeu_mondes_marins BOOLEAN DEFAULT FALSE;

-- Promo : Indique si c'est une carte promotionnelle
ALTER TABLE technologies ADD COLUMN IF NOT EXISTS promo BOOLEAN DEFAULT FALSE;

-- Remplacée par extension Mondes Marins : Numéro de carte qui remplace celle-ci
-- Exemple : Si cette carte est remplacée par la carte 201 dans l'extension
ALTER TABLE technologies ADD COLUMN IF NOT EXISTS remplacee_par INTEGER;

-- ============================================================================
-- 3. TABLE QUETES (Cartes Projets de Conservation)
-- ============================================================================

-- Bonus : Bonus gagné par le joueur posant la carte
-- Exemple : "+2 réputation", "Piochez 1 carte"
ALTER TABLE quetes ADD COLUMN IF NOT EXISTS bonus TEXT;

-- Vague : Numéro de vague de sortie de la carte
ALTER TABLE quetes ADD COLUMN IF NOT EXISTS vague VARCHAR(50);

-- Jeu de base : Indique si la carte est disponible dans le jeu de base
ALTER TABLE quetes ADD COLUMN IF NOT EXISTS jeu_base BOOLEAN DEFAULT TRUE;

-- Jeu avec extension Mondes Marins : Indique si la carte est disponible avec l'extension
ALTER TABLE quetes ADD COLUMN IF NOT EXISTS jeu_mondes_marins BOOLEAN DEFAULT FALSE;

-- Remplacée par extension Mondes Marins : Numéro de carte qui remplace celle-ci
ALTER TABLE quetes ADD COLUMN IF NOT EXISTS remplacee_par INTEGER;

-- ============================================================================
-- INDEX pour améliorer les performances
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_troupes_vague ON troupes(vague);
CREATE INDEX IF NOT EXISTS idx_troupes_jeu_base ON troupes(jeu_base);
CREATE INDEX IF NOT EXISTS idx_troupes_promo ON troupes(promo);

CREATE INDEX IF NOT EXISTS idx_technologies_vague ON technologies(vague);
CREATE INDEX IF NOT EXISTS idx_technologies_jeu_base ON technologies(jeu_base);
CREATE INDEX IF NOT EXISTS idx_technologies_promo ON technologies(promo);

CREATE INDEX IF NOT EXISTS idx_quetes_vague ON quetes(vague);
CREATE INDEX IF NOT EXISTS idx_quetes_jeu_base ON quetes(jeu_base);

-- ============================================================================
-- COMMENTAIRES pour documentation
-- ============================================================================

COMMENT ON COLUMN troupes.effet_du_vide IS 'Effet spécial des cartes Coralliennes (extension Mondes Marins) - se déclenche selon les cases vides';
COMMENT ON COLUMN troupes.conditions IS 'Conditions pour jouer la carte (JSONB) - ex: {"texte": "Mécène II", "icones_requises": ["Recherche"]}';
COMMENT ON COLUMN troupes.vague IS 'Numéro de vague de sortie de la carte (pour filtrage par extension)';
COMMENT ON COLUMN troupes.jeu_base IS 'True si la carte est disponible dans le jeu de base Ark Nova';
COMMENT ON COLUMN troupes.jeu_mondes_marins IS 'True si la carte est disponible avec l''extension Mondes Marins';
COMMENT ON COLUMN troupes.promo IS 'True si c''est une carte promotionnelle';

COMMENT ON COLUMN technologies.conditions IS 'Conditions pour jouer la carte (JSONB) - ex: {"texte": "Mécène II"}';
COMMENT ON COLUMN technologies.remplacee_par IS 'Numéro de carte qui remplace celle-ci dans l''extension Mondes Marins';

COMMENT ON COLUMN quetes.bonus IS 'Bonus gagné par le joueur posant la carte (ex: "+2 réputation")';
COMMENT ON COLUMN quetes.remplacee_par IS 'Numéro de carte qui remplace celle-ci dans l''extension Mondes Marins';


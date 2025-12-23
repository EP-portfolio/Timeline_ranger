-- Script de vérification du schéma Supabase
-- Exécutez ces requêtes dans Supabase SQL Editor pour vérifier que tout est créé

-- 1. Vérifier que les tables principales existent
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- 2. Vérifier les Rangers (devrait retourner 5 lignes)
SELECT * FROM rangers ORDER BY id;

-- 3. Vérifier les Types d'Armes (devrait retourner 8 lignes)
SELECT * FROM weapon_types ORDER BY id;

-- 4. Vérifier les Matières Premières (devrait retourner 5 lignes)
SELECT * FROM raw_materials ORDER BY id;

-- 5. Vérifier les Index
SELECT 
    tablename,
    indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 6. Vérifier les Vues
SELECT 
    table_name as view_name
FROM information_schema.views
WHERE table_schema = 'public'
ORDER BY table_name;

-- 7. Compter le nombre total de tables
SELECT COUNT(*) as total_tables
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE';

-- 8. Vérifier les contraintes (Foreign Keys)
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_schema = 'public'
ORDER BY tc.table_name;



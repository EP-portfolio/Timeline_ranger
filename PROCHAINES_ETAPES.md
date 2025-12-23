# Prochaines Étapes - Timeline Ranger Online

## 📊 État Actuel du Projet

### ✅ Ce qui est Fait

1. **Mapping Complet** :
   - ✅ Tous les mappings Ark Nova → Timeline Ranger documentés
   - ✅ Noms des cartes mappés
   - ✅ Points, catégories, continents mappés
   - ✅ Rangers de couleurs définis

2. **Base de Données** :
   - ✅ Schéma PostgreSQL complet avec tous les mappings
   - ✅ Script d'import avec transformations
   - ✅ Structure pour jeu multijoueur

3. **Architecture** :
   - ✅ Architecture low-cost définie (Supabase/Vercel)
   - ✅ Plan de développement détaillé
   - ✅ Checklist complète

### ⏳ Ce qui Reste à Faire

1. **Backend API** : À créer
2. **Frontend** : À créer
3. **Déploiement** : À configurer
4. **Tests** : À effectuer

## 🎯 Prochaines Étapes Prioritaires

### Phase 1 : Setup et Test de la Base de Données (1-2 jours)

**Objectif** : Vérifier que le schéma et l'import fonctionnent correctement

#### Étape 1.1 : Configurer PostgreSQL Localement
- [ ] Installer PostgreSQL (ou utiliser Docker)
- [ ] Créer la base de données `timeline_ranger`
- [ ] Exécuter le schéma SQL
- [ ] Vérifier que les tables sont créées

#### Étape 1.2 : Tester l'Import
- [ ] Configurer le script d'import (connexion DB)
- [ ] Exécuter l'import depuis l'ODS
- [ ] Vérifier les données importées
- [ ] Corriger les erreurs éventuelles

#### Étape 1.3 : Créer Supabase (Alternative Cloud)
- [ ] Créer un compte Supabase (gratuit)
- [ ] Créer un projet
- [ ] Exécuter le schéma SQL dans Supabase
- [ ] Tester l'import dans Supabase

**Livrables** :
- ✅ Base de données fonctionnelle
- ✅ Données importées et vérifiées
- ✅ Connexion Supabase configurée

---

### Phase 2 : Backend API de Base (3-5 jours)

**Objectif** : Créer l'API FastAPI avec authentification et gestion des parties

#### Étape 2.1 : Structure du Projet Backend
- [ ] Créer le dossier `backend/`
- [ ] Structure FastAPI de base
- [ ] Configuration (`.env`, `config.py`)
- [ ] Connexion PostgreSQL/Supabase

#### Étape 2.2 : Authentification
- [ ] Modèle User (SQLAlchemy)
- [ ] Route `POST /api/auth/register`
- [ ] Route `POST /api/auth/login`
- [ ] JWT tokens
- [ ] Middleware d'authentification

#### Étape 2.3 : API des Cartes
- [ ] Route `GET /api/troupes` (liste)
- [ ] Route `GET /api/troupes/{id}`
- [ ] Route `GET /api/technologies` (liste)
- [ ] Route `GET /api/technologies/{id}`
- [ ] Route `GET /api/quetes` (liste)
- [ ] Filtres et recherche

#### Étape 2.4 : API des Parties
- [ ] Route `POST /api/games/create`
- [ ] Route `POST /api/games/join`
- [ ] Route `GET /api/games/list`
- [ ] Route `GET /api/games/{id}`

**Livrables** :
- ✅ API FastAPI fonctionnelle
- ✅ Authentification opérationnelle
- ✅ CRUD des cartes et parties

---

### Phase 3 : WebSocket et Synchronisation (3-4 jours)

**Objectif** : Communication temps réel pour les parties

#### Étape 3.1 : Setup WebSocket
- [ ] Route WebSocket `/ws/game/{game_id}`
- [ ] Gestionnaire de connexions
- [ ] Système de rooms

#### Étape 3.2 : Événements de Partie
- [ ] Événement `player_joined`
- [ ] Événement `player_action`
- [ ] Événement `game_state_update`
- [ ] Événement `turn_change`

#### Étape 3.3 : Synchronisation
- [ ] Sauvegarde de l'état de partie
- [ ] Broadcast des actions
- [ ] Gestion des déconnexions

**Livrables** :
- ✅ WebSocket fonctionnel
- ✅ Parties synchronisées en temps réel

---

### Phase 4 : Frontend de Base (4-5 jours)

**Objectif** : Interface utilisateur pour authentification et lobby

#### Étape 4.1 : Setup Frontend
- [ ] Créer projet React/Vue
- [ ] Configuration build
- [ ] Client API (Axios)
- [ ] Client WebSocket

#### Étape 4.2 : Pages d'Authentification
- [ ] Page Login
- [ ] Page Register
- [ ] Gestion des tokens
- [ ] Redirection

#### Étape 4.3 : Lobby
- [ ] Page Lobby
- [ ] Liste des parties
- [ ] Créer une partie
- [ ] Rejoindre une partie

**Livrables** :
- ✅ Frontend fonctionnel
- ✅ Authentification complète
- ✅ Lobby opérationnel

---

### Phase 5 : Interface de Jeu (5-7 jours)

**Objectif** : Interface complète pour jouer

#### Étape 5.1 : Layout de Jeu
- [ ] Layout principal
- [ ] Composant Rangers
- [ ] Composant Armure Méca
- [ ] Composant Main de cartes

#### Étape 5.2 : Interactions
- [ ] Sélection de Ranger
- [ ] Affichage des actions
- [ ] Exécution d'actions
- [ ] Feedback visuel

#### Étape 5.3 : Logique de Jeu
- [ ] Rotation des Rangers
- [ ] Validation des actions
- [ ] Calcul des scores
- [ ] Fin de partie

**Livrables** :
- ✅ Interface de jeu complète
- ✅ Toutes les interactions fonctionnelles

---

## 🚀 Plan d'Action Immédiat (Cette Semaine)

### Jour 1-2 : Setup Base de Données
1. **Aujourd'hui** :
   - [ ] Installer PostgreSQL localement (ou Docker)
   - [ ] Créer la base de données
   - [ ] Exécuter le schéma SQL
   - [ ] Vérifier les tables

2. **Demain** :
   - [ ] Configurer le script d'import
   - [ ] Importer les données depuis l'ODS
   - [ ] Vérifier les données importées
   - [ ] Créer compte Supabase et tester

### Jour 3-5 : Backend API de Base
3. **Jour 3** :
   - [ ] Créer structure backend FastAPI
   - [ ] Configuration et connexion DB
   - [ ] Route de test

4. **Jour 4** :
   - [ ] Authentification (register/login)
   - [ ] JWT tokens
   - [ ] Tests d'authentification

5. **Jour 5** :
   - [ ] API des cartes (troupes, technologies, quêtes)
   - [ ] API des parties (create, join, list)
   - [ ] Tests des routes

### Semaine 2 : WebSocket et Frontend
- WebSocket et synchronisation
- Frontend de base (auth + lobby)

### Semaine 3 : Interface de Jeu
- Interface complète
- Logique de jeu

---

## 📋 Checklist Immédiate

### À Faire MAINTENANT

1. **Setup PostgreSQL** :
   ```bash
   # Option 1 : Installer PostgreSQL
   # Option 2 : Utiliser Docker
   docker run --name postgres-timeline -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
   
   # Créer la base
   psql -U postgres -c "CREATE DATABASE timeline_ranger;"
   ```

2. **Exécuter le Schéma** :
   ```bash
   psql -U postgres -d timeline_ranger -f SCHEMA_POSTGRESQL_TIMELINE_RANGER.sql
   ```

3. **Tester l'Import** :
   ```bash
   # Modifier SCRIPT_IMPORT_MAPPED_DATA.py avec vos credentials
   python SCRIPT_IMPORT_MAPPED_DATA.py
   ```

4. **Vérifier les Données** :
   ```sql
   -- Vérifier les Rangers
   SELECT * FROM rangers;
   
   -- Vérifier les Troupes
   SELECT COUNT(*) FROM troupes;
   
   -- Vérifier les Technologies
   SELECT COUNT(*) FROM technologies;
   ```

---

## 🎯 Objectif MVP (Minimum Viable Product)

**Pour avoir un prototype fonctionnel** :

1. ✅ Base de données avec données importées
2. ✅ API backend avec auth + parties
3. ✅ WebSocket de base
4. ✅ Frontend auth + lobby
5. ✅ Interface de jeu minimale

**Durée estimée** : 3-4 semaines

---

## 💡 Recommandation

**Commencer par** :
1. **Setup PostgreSQL** (aujourd'hui)
2. **Tester l'import** (demain)
3. **Créer le backend de base** (cette semaine)

Une fois la base de données fonctionnelle et les données importées, vous pourrez :
- Voir les données mappées en action
- Tester les requêtes
- Développer l'API avec des données réelles

---

*Document créé le : 2025-01-XX*
*Dernière mise à jour : 2025-01-XX*


"""
Script de test pour vérifier que les endpoints fonctionnent
À exécuter avec : python -m pytest backend/test_endpoints.py -v
Ou directement : python backend/test_endpoints.py
"""
import requests
import json
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Variables globales pour stocker les tokens et IDs
auth_token: Optional[str] = None
user1_token: Optional[str] = None
user2_token: Optional[str] = None
game_id: Optional[int] = None
game_code: Optional[str] = None


def print_response(response, title: str):
    """Affiche la réponse de manière lisible"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def test_health_check():
    """Test du health check"""
    print("🔍 Test 1: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    assert response.status_code == 200
    print("✅ Health check OK\n")


def test_register_user1():
    """Test d'inscription utilisateur 1"""
    global user1_token
    print("🔍 Test 2: Inscription Utilisateur 1")
    data = {
        "email": "test1@example.com",
        "password": "test123456",
        "username": "testuser1"
    }
    response = requests.post(f"{API_BASE}/auth/register", json=data)
    print_response(response, "Inscription Utilisateur 1")
    assert response.status_code in [200, 201, 400]  # 400 si déjà existant
    print("✅ Inscription OK\n")


def test_register_user2():
    """Test d'inscription utilisateur 2"""
    global user2_token
    print("🔍 Test 3: Inscription Utilisateur 2")
    data = {
        "email": "test2@example.com",
        "password": "test123456",
        "username": "testuser2"
    }
    response = requests.post(f"{API_BASE}/auth/register", json=data)
    print_response(response, "Inscription Utilisateur 2")
    assert response.status_code in [200, 201, 400]  # 400 si déjà existant
    print("✅ Inscription OK\n")


def test_login_user1():
    """Test de connexion utilisateur 1"""
    global user1_token
    print("🔍 Test 4: Connexion Utilisateur 1")
    data = {
        "email": "test1@example.com",
        "password": "test123456"
    }
    response = requests.post(f"{API_BASE}/auth/login", data=data)
    print_response(response, "Connexion Utilisateur 1")
    assert response.status_code == 200
    user1_token = response.json()["access_token"]
    print(f"✅ Token obtenu: {user1_token[:20]}...\n")


def test_login_user2():
    """Test de connexion utilisateur 2"""
    global user2_token
    print("🔍 Test 5: Connexion Utilisateur 2")
    data = {
        "email": "test2@example.com",
        "password": "test123456"
    }
    response = requests.post(f"{API_BASE}/auth/login", data=data)
    print_response(response, "Connexion Utilisateur 2")
    assert response.status_code == 200
    user2_token = response.json()["access_token"]
    print(f"✅ Token obtenu: {user2_token[:20]}...\n")


def test_get_current_user():
    """Test de récupération du profil utilisateur"""
    global user1_token
    print("🔍 Test 6: Profil Utilisateur")
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.get(f"{API_BASE}/auth/me", headers=headers)
    print_response(response, "Profil Utilisateur")
    assert response.status_code == 200
    print("✅ Profil OK\n")


def test_create_game():
    """Test de création d'une partie"""
    global user1_token, game_id, game_code
    print("🔍 Test 7: Création d'une Partie")
    headers = {"Authorization": f"Bearer {user1_token}"}
    data = {"max_players": 4}
    response = requests.post(f"{API_BASE}/games", json=data, headers=headers)
    print_response(response, "Création Partie")
    assert response.status_code == 201
    game_id = response.json()["id"]
    game_code = response.json()["code"]
    print(f"✅ Partie créée: ID={game_id}, Code={game_code}\n")


def test_list_games():
    """Test de liste des parties"""
    print("🔍 Test 8: Liste des Parties")
    response = requests.get(f"{API_BASE}/games")
    print_response(response, "Liste des Parties")
    assert response.status_code == 200
    print("✅ Liste OK\n")


def test_get_game():
    """Test de récupération d'une partie"""
    global game_code
    print("🔍 Test 9: Récupération Partie")
    response = requests.get(f"{API_BASE}/games/{game_code}")
    print_response(response, "Récupération Partie")
    assert response.status_code == 200
    print("✅ Récupération OK\n")


def test_join_game():
    """Test de rejoindre une partie"""
    global user2_token, game_code
    print("🔍 Test 10: Rejoindre une Partie")
    headers = {"Authorization": f"Bearer {user2_token}"}
    data = {"game_code": game_code}
    response = requests.post(f"{API_BASE}/games/join", json=data, headers=headers)
    print_response(response, "Rejoindre Partie")
    assert response.status_code == 200
    print("✅ Rejoindre OK\n")


def test_get_game_players():
    """Test de récupération des joueurs"""
    global user1_token, game_id
    print("🔍 Test 11: Liste des Joueurs")
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.get(f"{API_BASE}/games/{game_id}/players", headers=headers)
    print_response(response, "Liste des Joueurs")
    assert response.status_code == 200
    print("✅ Liste Joueurs OK\n")


def test_start_game():
    """Test de démarrage d'une partie"""
    global user1_token, game_id
    print("🔍 Test 12: Démarrer une Partie")
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.post(f"{API_BASE}/games/{game_id}/start", headers=headers)
    print_response(response, "Démarrer Partie")
    assert response.status_code == 200
    print("✅ Démarrage OK\n")


def test_get_game_state():
    """Test de récupération de l'état du jeu"""
    global user1_token, game_id
    print("🔍 Test 13: État du Jeu")
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.get(f"{API_BASE}/games/{game_id}/state", headers=headers)
    print_response(response, "État du Jeu")
    assert response.status_code == 200
    state = response.json()
    print(f"✅ État récupéré: Tour {state['turn_number']}, Joueur actif: {state['current_player']}\n")


def test_play_color_action():
    """Test de jouer une action de couleur"""
    global user1_token, game_id
    print("🔍 Test 14: Jouer une Action de Couleur")
    headers = {"Authorization": f"Bearer {user1_token}"}
    data = {
        "color": "blue",
        "power": 1,
        "use_x_token": False,
        "action_data": {
            "gain_credits": 1
        }
    }
    response = requests.post(
        f"{API_BASE}/games/{game_id}/actions/play-color",
        json=data,
        headers=headers
    )
    print_response(response, "Jouer Action de Couleur")
    assert response.status_code == 200
    print("✅ Action jouée OK\n")


def test_pass_action():
    """Test de passer son tour"""
    global user2_token, game_id
    print("🔍 Test 15: Passer son Tour")
    headers = {"Authorization": f"Bearer {user2_token}"}
    data = {"reason": "Test"}
    response = requests.post(
        f"{API_BASE}/games/{game_id}/actions/pass",
        json=data,
        headers=headers
    )
    print_response(response, "Passer Tour")
    assert response.status_code == 200
    print("✅ Pass OK\n")


def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("🧪 DÉBUT DES TESTS DES ENDPOINTS")
    print("="*60 + "\n")
    
    try:
        test_health_check()
        test_register_user1()
        test_register_user2()
        test_login_user1()
        test_login_user2()
        test_get_current_user()
        test_create_game()
        test_list_games()
        test_get_game()
        test_join_game()
        test_get_game_players()
        test_start_game()
        test_get_game_state()
        test_play_color_action()
        test_pass_action()
        
        print("\n" + "="*60)
        print("✅ TOUS LES TESTS SONT PASSÉS !")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ ERREUR: {e}\n")
    except Exception as e:
        print(f"\n❌ ERREUR INATTENDUE: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n⚠️  Assurez-vous que le serveur backend est démarré sur http://localhost:8000")
    print("   Commande: cd backend && uvicorn app.main:app --reload\n")
    input("Appuyez sur Entrée pour continuer...")
    run_all_tests()


import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { gamesAPI } from '../services/api'
import './Home.css'

const Home = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleCreateGame = async () => {
    try {
      const response = await gamesAPI.create({ max_players: 4 })
      navigate(`/games/${response.data.id}`)
    } catch (error) {
      console.error('Erreur création partie:', error)
      alert('Erreur lors de la création de la partie')
    }
  }

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Timeline Ranger</h1>
        <div className="user-info">
          <span>Bonjour, {user?.username || user?.email}</span>
          <button onClick={logout} className="logout-button">
            Déconnexion
          </button>
        </div>
      </header>

      <main className="home-main">
        <div className="home-content">
          <h2>Bienvenue dans Timeline Ranger</h2>
          <p>Créez ou rejoignez une partie pour commencer à jouer</p>

          <div className="action-buttons">
            <button onClick={handleCreateGame} className="primary-button">
              Créer une Partie
            </button>
            <button onClick={() => navigate('/games')} className="secondary-button">
              Voir les Parties
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Home


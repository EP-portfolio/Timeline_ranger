import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { gamesAPI } from '../services/api'
import './Games.css'

const Games = () => {
  const [games, setGames] = useState([])
  const [loading, setLoading] = useState(true)
  const [gameCode, setGameCode] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    loadGames()
    // Rafraîchir toutes les 5 secondes
    const interval = setInterval(loadGames, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadGames = async () => {
    try {
      const response = await gamesAPI.list()
      setGames(response.data)
    } catch (error) {
      console.error('Erreur chargement parties:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleJoinByCode = async () => {
    if (!gameCode.trim()) {
      alert('Veuillez entrer un code de partie')
      return
    }

    try {
      const response = await gamesAPI.get(gameCode)
      navigate(`/games/${response.data.id}`)
    } catch (error) {
      alert('Partie non trouvée')
    }
  }

  const handleJoinGame = (gameId) => {
    navigate(`/games/${gameId}`)
  }

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
    <div className="games-container">
      <header className="games-header">
        <h1>Parties Disponibles</h1>
        <button onClick={handleCreateGame} className="create-button">
          Créer une Partie
        </button>
      </header>

      <main className="games-main">
        <div className="join-by-code">
          <h2>Rejoindre par Code</h2>
          <div className="code-input-group">
            <input
              type="text"
              placeholder="Code de partie"
              value={gameCode}
              onChange={(e) => setGameCode(e.target.value.toUpperCase())}
              maxLength={6}
            />
            <button onClick={handleJoinByCode}>Rejoindre</button>
          </div>
        </div>

        <div className="games-list">
          <h2>Parties en Attente</h2>
          {loading ? (
            <div className="loading">Chargement...</div>
          ) : games.length === 0 ? (
            <div className="no-games">Aucune partie en attente</div>
          ) : (
            <div className="games-grid">
              {games.map((game) => (
                <div key={game.id} className="game-card">
                  <div className="game-info">
                    <h3>Partie {game.code}</h3>
                    <p>
                      {game.current_players} / {game.max_players} joueurs
                    </p>
                  </div>
                  <button
                    onClick={() => handleJoinGame(game.id)}
                    disabled={game.current_players >= game.max_players}
                    className="join-button"
                  >
                    {game.current_players >= game.max_players ? 'Complet' : 'Rejoindre'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default Games


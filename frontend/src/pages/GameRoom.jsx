import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { gamesAPI, actionsAPI } from '../services/api'
import wsService from '../services/websocket'
import { useAuth } from '../contexts/AuthContext'
import './GameRoom.css'

const GameRoom = () => {
  const { id } = useParams()
  const { user } = useAuth()
  const [gameState, setGameState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [wsConnected, setWsConnected] = useState(false)

  useEffect(() => {
    loadGameState()

    // Connexion WebSocket
    const token = localStorage.getItem('token')
    if (token) {
      wsService.connect(parseInt(id), token)

      wsService.on('connected', () => {
        setWsConnected(true)
      })

      wsService.on('disconnected', () => {
        setWsConnected(false)
      })

      wsService.on('game_state_update', (message) => {
        if (message.state) {
          setGameState(message.state)
        }
      })

      wsService.on('player_connected', (message) => {
        console.log('Joueur connecté:', message)
        loadGameState()
      })

      wsService.on('player_disconnected', (message) => {
        console.log('Joueur déconnecté:', message)
        loadGameState()
      })
    }

    // Keep-alive ping toutes les 30 secondes
    const pingInterval = setInterval(() => {
      if (wsService.isConnected()) {
        wsService.ping()
      }
    }, 30000)

    return () => {
      clearInterval(pingInterval)
      wsService.disconnect()
    }
  }, [id])

  const loadGameState = async () => {
    try {
      const response = await gamesAPI.getState(id)
      setGameState(response.data.game_data)
      setError('')
    } catch (error) {
      console.error('Erreur chargement état:', error)
      setError('Erreur lors du chargement de l\'état du jeu')
    } finally {
      setLoading(false)
    }
  }

  const handlePlayColor = async (color, power) => {
    try {
      const response = await actionsAPI.playColor(id, {
        color,
        power,
        use_x_token: false,
        action_data: color === 'blue' ? { gain_credits: power } : {},
      })
      // L'état sera mis à jour via WebSocket
    } catch (error) {
      console.error('Erreur action:', error)
      alert(error.response?.data?.detail || 'Erreur lors de l\'action')
    }
  }

  const handlePass = async () => {
    try {
      await actionsAPI.pass(id, {})
      // L'état sera mis à jour via WebSocket
    } catch (error) {
      console.error('Erreur pass:', error)
      alert(error.response?.data?.detail || 'Erreur lors du pass')
    }
  }

  if (loading) {
    return <div className="game-room-loading">Chargement...</div>
  }

  if (error) {
    return <div className="game-room-error">{error}</div>
  }

  if (!gameState) {
    return <div className="game-room-error">État du jeu non disponible</div>
  }

  const currentPlayerState = gameState.players[gameState.current_player]
  const isMyTurn = currentPlayerState?.user_id === user?.id

  return (
    <div className="game-room">
      <header className="game-room-header">
        <h1>Partie {id}</h1>
        <div className="connection-status">
          <span className={wsConnected ? 'connected' : 'disconnected'}>
            {wsConnected ? '🟢 Connecté' : '🔴 Déconnecté'}
          </span>
        </div>
      </header>

      <div className="game-room-content">
        <div className="game-info">
          <h2>Tour {gameState.turn_number}</h2>
          <p>Joueur actif: {gameState.current_player}</p>
          {isMyTurn && <p className="your-turn">C'est votre tour !</p>}
        </div>

        <div className="rangers-section">
          <h3>Rangers (Actions de Couleur)</h3>
          <div className="rangers-grid">
            {currentPlayerState?.rangers?.map((ranger) => (
              <div key={ranger.color} className="ranger-card">
                <div className="ranger-color" style={{ backgroundColor: getColorHex(ranger.color) }}>
                  {ranger.name}
                </div>
                <div className="ranger-position">Position: {ranger.position}</div>
                {isMyTurn && (
                  <button
                    onClick={() => handlePlayColor(ranger.color, ranger.position)}
                    className="play-action-button"
                  >
                    Jouer (Puissance {ranger.position})
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="actions-section">
          <h3>Actions</h3>
          {isMyTurn ? (
            <button onClick={handlePass} className="pass-button">
              Passer mon Tour
            </button>
          ) : (
            <p className="waiting">En attente du joueur {gameState.current_player}...</p>
          )}
        </div>

        <div className="players-section">
          <h3>Joueurs</h3>
          <div className="players-list">
            {Object.values(gameState.players).map((player) => (
              <div key={player.player_number} className="player-card">
                <h4>Joueur {player.player_number}</h4>
                <p>Or: {player.resources?.or || 0}</p>
                <p>Points de dégâts: {player.scores?.points_degats || 0}</p>
                <p>Lasers: {player.scores?.lasers || 0}</p>
                <p>Réputation: {player.scores?.reputation || 0}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

function getColorHex(color) {
  const colors = {
    blue: '#3b82f6',
    black: '#1f2937',
    orange: '#f97316',
    green: '#10b981',
    yellow: '#eab308',
  }
  return colors[color] || '#666'
}

export default GameRoom


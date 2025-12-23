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
  const [gameInfo, setGameInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [wsConnected, setWsConnected] = useState(false)

  useEffect(() => {
    loadGameState()
    loadGameInfo()

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
      console.log('Réponse API:', response.data) // Debug
      
      // Vérifier que game_data existe
      if (!response.data || !response.data.game_data) {
        console.error('Structure de réponse invalide:', response.data)
        setError('Structure de réponse invalide du serveur')
        return
      }
      
      setGameState(response.data.game_data)
      setError('')
    } catch (error) {
      console.error('Erreur chargement état:', error)
      console.error('Détails erreur:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
      })
      setError(
        error.response?.data?.detail || 
        error.message || 
        'Erreur lors du chargement de l\'état du jeu'
      )
    } finally {
      setLoading(false)
    }
  }

  const loadGameInfo = async () => {
    try {
      // Récupérer les infos de la partie pour savoir si on est l'hôte
      const response = await gamesAPI.get(id)
      setGameInfo(response.data)
    } catch (error) {
      console.error('Erreur chargement infos partie:', error)
    }
  }

  const handleStartGame = async () => {
    try {
      await gamesAPI.start(id)
      loadGameState() // Recharger l'état après démarrage
      loadGameInfo()
    } catch (error) {
      console.error('Erreur démarrage partie:', error)
      alert(error.response?.data?.detail || 'Erreur lors du démarrage de la partie')
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

  // Note: On affiche l'interface même si la partie est en "waiting"
  // pour permettre la visualisation des Rangers et de l'interface

  const currentPlayerState = gameState.current_player 
    ? gameState.players?.[gameState.current_player] 
    : null
  const myPlayerState = Object.values(gameState.players || {}).find(
    (p) => p.user_id === user?.id
  )
  const isMyTurn = gameState.current_player !== null && 
                   gameState.current_player !== undefined &&
                   currentPlayerState?.user_id === user?.id

  return (
    <div className="game-room">
      <header className="game-room-header">
        <h1>Partie {id}</h1>
        <div className="header-right">
          {gameState?.status === 'waiting' && gameInfo?.host_id === user?.id && (
            <button onClick={handleStartGame} className="start-game-button">
              Démarrer la Partie
            </button>
          )}
          {gameState?.status === 'waiting' && (
            <span className="waiting-badge">⏳ En attente</span>
          )}
          <div className="connection-status">
            <span className={wsConnected ? 'connected' : 'disconnected'}>
              {wsConnected ? '🟢 Connecté' : '🔴 Déconnecté'}
            </span>
          </div>
        </div>
      </header>

      <div className="game-room-content">
        {/* Zone principale : RIVER (en haut) */}
        <div className="river-section">
          <h2>RIVER</h2>
          <div className="river-content">
            {/* Colonne de gauche : Image MECA */}
            <div className="meca-section">
              <h3>IMAGE MECA</h3>
              {myPlayerState?.armure_meca_id && (
                <div className="meca-info">
                  <p>Armure MECA #{myPlayerState.armure_meca_id}</p>
                </div>
              )}
            </div>

            {/* Zone centrale : Image de la Map/Armure */}
            <div className="map-armor-section">
              <div className="map-armor-placeholder">
                <p>IMAGE DE LA MAP/ARMURE</p>
                {myPlayerState?.board && (
                  <div className="board-info">
                    <p>Garnisons: {myPlayerState.board.garnisons?.length || 0}</p>
                    <p>Armes: {myPlayerState.board.weapons?.length || 0}</p>
                    <p>Pièces d'armure: {myPlayerState.board.armor_pieces?.length || 0}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Colonne de droite : Récapitulatif */}
            <div className="recap-section">
              <h3>RECAP</h3>
              <div className="recap-content">
                <div className="recap-item">
                  <span className="recap-label">Tour:</span>
                  <span className="recap-value">{gameState.turn_number}</span>
                </div>
                <div className="recap-item">
                  <span className="recap-label">Joueur actif:</span>
                  <span className="recap-value">{gameState.current_player}</span>
                </div>
                {myPlayerState && (
                  <>
                    <div className="recap-item">
                      <span className="recap-label">Or:</span>
                      <span className="recap-value">{myPlayerState.resources?.or || 0}</span>
                    </div>
                    <div className="recap-item">
                      <span className="recap-label">Lasers:</span>
                      <span className="recap-value">{myPlayerState.scores?.lasers || 0}</span>
                    </div>
                    <div className="recap-item">
                      <span className="recap-label">Réputation:</span>
                      <span className="recap-value">{myPlayerState.scores?.reputation || 0}</span>
                    </div>
                    <div className="recap-item">
                      <span className="recap-label">Émissaires:</span>
                      <span className="recap-value">{myPlayerState.emissaires || 0}</span>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Jauge de dégâts */}
        {myPlayerState && (
          <div className="damage-gauge-section">
            <h3>JAUGE DÉGÂTS</h3>
            <div className="damage-gauge">
              <div className="gauge-bar">
                <div
                  className="gauge-fill"
                  style={{
                    width: `${Math.min((myPlayerState.scores?.points_degats || 0) / 100, 1) * 100}%`,
                  }}
                />
              </div>
              <span className="gauge-value">
                {myPlayerState.scores?.points_degats || 0} / 100
              </span>
            </div>
          </div>
        )}

        {/* Cartes Action (Rangers) en bas */}
        <div className="action-cards-section">
          <h3>CARTES ACTION</h3>
          <div className="rangers-grid">
            {myPlayerState?.rangers?.map((ranger) => (
              <div key={ranger.color} className="ranger-card">
                <div
                  className="ranger-color"
                  style={{ backgroundColor: getColorHex(ranger.color) }}
                >
                  <div className="ranger-name">{ranger.name}</div>
                  <div className="ranger-position">Position {ranger.position}</div>
                  {ranger.improved && <div className="ranger-improved">★ Amélioré</div>}
                </div>
                {gameState?.status === 'started' && isMyTurn && (
                  <button
                    onClick={() => handlePlayColor(ranger.color, ranger.position)}
                    className="play-action-button"
                    disabled={!isMyTurn}
                  >
                    Jouer (Niveau {ranger.position})
                  </button>
                )}
                {gameState?.status === 'waiting' && (
                  <div className="play-action-button disabled">
                    En attente du démarrage
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="actions-section">
          {gameState?.status === 'waiting' ? (
            <p className="waiting">La partie n'a pas encore démarré. {gameInfo?.host_id === user?.id ? 'Cliquez sur "Démarrer la Partie" pour commencer.' : 'En attente du démarrage...'}</p>
          ) : isMyTurn ? (
            <button onClick={handlePass} className="pass-button">
              Passer mon Tour
            </button>
          ) : (
            <p className="waiting">En attente du joueur {gameState.current_player}...</p>
          )}
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


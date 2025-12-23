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
  const [selectedCards, setSelectedCards] = useState([])
  const [selectedAction, setSelectedAction] = useState(null) // { color, power } ou null
  const [selectedCardFromHand, setSelectedCardFromHand] = useState(null)

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
      // Récupérer les infos de la partie par ID pour savoir si on est l'hôte
      const response = await gamesAPI.getById(id)
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

  const handlePlayColor = (color, power) => {
    // Au lieu de jouer directement, on sélectionne l'action pour afficher les cartes jouables
    setSelectedAction({ color, power })
    setSelectedCardFromHand(null)
  }

  const handleSelectCardFromHand = (cardId) => {
    setSelectedCardFromHand(cardId)
  }

  const handleConfirmActionWithCard = async () => {
    if (!selectedAction) return

    // Action Noire (Animaux) nécessite obligatoirement une carte Troupe
    if (selectedAction.color === 'black' && !selectedCardFromHand) {
      alert('Vous devez sélectionner une carte Troupe pour jouer l\'action Animaux')
      return
    }

    // Action Bleue peut être jouée avec ou sans carte
    // Les autres actions (Orange, Vert, Jaune) ne nécessitent pas de carte

    try {
      const actionData = {}
      if (selectedAction.color === 'blue' && !selectedCardFromHand) {
        // Si pas de carte sélectionnée pour bleu, gagner des crédits
        actionData.gain_credits = selectedAction.power
      }

      await actionsAPI.playColor(id, {
        color: selectedAction.color,
        power: selectedAction.power,
        use_x_token: false,
        selected_card_id: selectedCardFromHand || null,
        action_data: actionData,
      })

      // Réinitialiser la sélection
      setSelectedAction(null)
      setSelectedCardFromHand(null)
      // L'état sera mis à jour via WebSocket
    } catch (error) {
      console.error('Erreur action:', error)
      alert(error.response?.data?.detail || 'Erreur lors de l\'action')
    }
  }

  const handleCancelAction = () => {
    setSelectedAction(null)
    setSelectedCardFromHand(null)
  }

  // Filtrer les cartes jouables selon l'action sélectionnée
  const getPlayableCards = () => {
    if (!selectedAction || !myPlayerState?.hand) return []

    const { color } = selectedAction

    // Bleu (Mécène) : peut jouer des cartes Mécène ou gagner des crédits
    // Pour le POC, on considère toutes les cartes comme jouables avec bleu
    if (color === 'blue') {
      return myPlayerState.hand
    }

    // Noir (Animaux) : peut jouer des cartes Troupe
    if (color === 'black') {
      return myPlayerState.hand.filter(card => card.type === 'troupe')
    }

    // Orange, Vert, Jaune : pas de cartes à jouer pour l'instant
    return []
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

  const handleCardSelect = (cardId) => {
    if (!myPlayerState?.initial_hand || myPlayerState.hand_selected) return

    setSelectedCards(prev => {
      if (prev.includes(cardId)) {
        return prev.filter(id => id !== cardId)
      } else if (prev.length < 4) {
        return [...prev, cardId]
      }
      return prev
    })
  }

  const handleConfirmHandSelection = async () => {
    if (selectedCards.length !== 4) {
      alert('Vous devez sélectionner exactement 4 cartes')
      return
    }

    try {
      await actionsAPI.selectInitialHand(id, { selected_card_ids: selectedCards })
      setSelectedCards([])
      loadGameState()
    } catch (error) {
      console.error('Erreur sélection cartes:', error)
      alert(error.response?.data?.detail || 'Erreur lors de la sélection des cartes')
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
                {gameState?.status === 'started' && isMyTurn && myPlayerState?.hand_selected && (
                  <button
                    onClick={() => handlePlayColor(ranger.color, ranger.position)}
                    className="play-action-button"
                    disabled={selectedAction !== null}
                  >
                    Jouer (Niveau {ranger.position})
                  </button>
                )}
                {gameState?.status === 'started' && isMyTurn && !myPlayerState?.hand_selected && (
                  <div className="play-action-button disabled">
                    Sélectionnez d'abord vos cartes
                  </div>
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

        {/* Sélection de cartes initiales */}
        {gameState?.status === 'started' && myPlayerState && !myPlayerState.hand_selected && myPlayerState.initial_hand?.length > 0 && (
          <div className="initial-hand-selection">
            <h3>Sélectionnez 4 cartes parmi les 8 ({selectedCards.length}/4)</h3>
            <div className="cards-grid">
              {myPlayerState.initial_hand.map((card) => (
                <div
                  key={card.id}
                  className={`card-item ${selectedCards.includes(card.id) ? 'selected' : ''}`}
                  onClick={() => handleCardSelect(card.id)}
                  style={{ backgroundColor: getCardColorByType(card.type) }}
                >
                  <div className="card-name">{card.name}</div>
                  <div className="card-type">{card.type}</div>
                  <div className="card-cost">Coût: {card.cost}</div>
                  {card.size && <div className="card-size">Taille: {card.size}</div>}
                </div>
              ))}
            </div>
            <button
              onClick={handleConfirmHandSelection}
              className="confirm-hand-button"
              disabled={selectedCards.length !== 4}
            >
              Confirmer la sélection (4 cartes)
            </button>
          </div>
        )}

        {/* Sélection de carte pour l'action */}
        {selectedAction && (
          <div className="card-selection-for-action">
            <h3>
              Action {selectedAction.color === 'blue' ? 'Mécène' :
                selectedAction.color === 'black' ? 'Animaux' :
                  selectedAction.color === 'orange' ? 'Construction' :
                    selectedAction.color === 'green' ? 'Association' : 'Cartes'}
              (Niveau {selectedAction.power})
            </h3>
            <p className="selection-instruction">
              {selectedAction.color === 'blue' && 'Sélectionnez une carte Mécène ou gagnez des crédits'}
              {selectedAction.color === 'black' && 'Sélectionnez une carte Troupe à jouer'}
              {selectedAction.color === 'orange' && 'Action Construction (pas de carte nécessaire)'}
              {selectedAction.color === 'green' && 'Action Association (pas de carte nécessaire)'}
              {selectedAction.color === 'yellow' && 'Action Cartes (pas de carte nécessaire)'}
            </p>

            {getPlayableCards().length > 0 && (
              <div className="playable-cards-section">
                <h4>Cartes jouables :</h4>
                <div className="cards-grid">
                  {getPlayableCards().map((card) => (
                    <div
                      key={card.id}
                      className={`card-item ${selectedCardFromHand === card.id ? 'selected' : ''}`}
                      onClick={() => handleSelectCardFromHand(card.id)}
                      style={{ backgroundColor: getCardColorByType(card.type) }}
                    >
                      <div className="card-name">{card.name}</div>
                      <div className="card-type">{card.type}</div>
                      <div className="card-cost">Coût: {card.cost}</div>
                      {card.size && <div className="card-size">Taille: {card.size}</div>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {selectedAction.color === 'blue' && (
              <div className="action-options">
                <button
                  className={`option-button ${!selectedCardFromHand ? 'selected' : ''}`}
                  onClick={() => setSelectedCardFromHand(null)}
                >
                  Gagner {selectedAction.power} crédits (pas de carte)
                </button>
              </div>
            )}

            <div className="action-confirm-buttons">
              <button
                onClick={handleConfirmActionWithCard}
                className="confirm-action-button"
                disabled={selectedAction.color === 'black' && !selectedCardFromHand}
              >
                Confirmer l'action
              </button>
              <button
                onClick={handleCancelAction}
                className="cancel-action-button"
              >
                Annuler
              </button>
            </div>
          </div>
        )}

        {/* Cartes en main (après sélection) */}
        {myPlayerState?.hand_selected && myPlayerState.hand?.length > 0 && !selectedAction && (
          <div className="hand-section">
            <h3>Mes Cartes en Main ({myPlayerState.hand.length})</h3>
            <div className="cards-grid">
              {myPlayerState.hand.map((card) => (
                <div 
                  key={card.id} 
                  className="card-item"
                  style={{ backgroundColor: getCardColorByType(card.type) }}
                >
                  <div className="card-name">{card.name}</div>
                  <div className="card-type">{card.type}</div>
                  <div className="card-cost">Coût: {card.cost}</div>
                  {card.size && <div className="card-size">Taille: {card.size}</div>}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="actions-section">
          {gameState?.status === 'waiting' ? (
            <p className="waiting">La partie n'a pas encore démarré. {gameInfo?.host_id === user?.id ? 'Cliquez sur "Démarrer la Partie" pour commencer.' : 'En attente du démarrage...'}</p>
          ) : isMyTurn && myPlayerState?.hand_selected ? (
            <button onClick={handlePass} className="pass-button">
              Passer mon Tour
            </button>
          ) : gameState?.status === 'started' && !myPlayerState?.hand_selected ? (
            <p className="waiting">Veuillez d'abord sélectionner vos 4 cartes</p>
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

function getCardColorByType(cardType) {
  // Mapping des types de cartes aux couleurs des Rangers
  const cardTypeColors = {
    troupe: '#1f2937',      // Noir - Ranger Animaux
    technology: '#f97316',  // Orange - Ranger Construction
    mecenes: '#3b82f6',     // Bleu - Ranger Mécène (si on a des cartes Mécène spécifiques)
  }
  return cardTypeColors[cardType] || '#2a2a2a' // Par défaut gris foncé
}

export default GameRoom


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
  // États pour l'action Construction
  const [availableTiles, setAvailableTiles] = useState([]) // Tuiles disponibles selon le niveau
  const [selectedTile, setSelectedTile] = useState(null) // Tuile choisie
  const [tileRotation, setTileRotation] = useState(0) // Rotation de la tuile (multiples de 60°)
  const [previewPosition, setPreviewPosition] = useState(null) // { q, r } pour prévisualisation

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
      setLoading(true)
      const response = await gamesAPI.getState(id)
      console.log('Réponse API complète:', response)
      console.log('Réponse API data:', response.data) // Debug

      // Vérifier que game_data existe
      if (!response.data) {
        console.error('Pas de data dans la réponse:', response)
        setError('Pas de données dans la réponse du serveur')
        setLoading(false)
        return
      }

      if (!response.data.game_data) {
        console.error('Structure de réponse invalide - pas de game_data:', response.data)
        setError('Structure de réponse invalide du serveur (pas de game_data)')
        setLoading(false)
        return
      }

      const gameData = response.data.game_data
      console.log('Game data chargé:', {
        status: gameData.status,
        turn_number: gameData.turn_number,
        current_player: gameData.current_player,
        players_count: Object.keys(gameData.players || {}).length
      })

      setGameState(gameData)
      setError('')
    } catch (error) {
      console.error('Erreur chargement état:', error)
      console.error('Détails erreur:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        stack: error.stack
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

  const handlePlayColor = async (color, power) => {
    // Au lieu de jouer directement, on sélectionne l'action pour afficher les cartes jouables
    setSelectedAction({ color, power })
    setSelectedCardFromHand(null)

    // Si c'est l'action Construction, charger les tuiles disponibles
    if (color === 'orange') {
      try {
        const response = await actionsAPI.getConstructionTiles(id, power)
        setAvailableTiles(response.data.tiles || [])
        setSelectedTile(null)
        setTileRotation(0)
        setPreviewPosition(null)
      } catch (error) {
        console.error('Erreur chargement tuiles:', error)
        alert(error.response?.data?.detail || 'Erreur lors du chargement des tuiles')
      }
    }
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

    // Action Verte (Association) nécessite obligatoirement une carte Quête
    if (selectedAction.color === 'green' && !selectedCardFromHand) {
      alert('Vous devez sélectionner une carte Quête pour jouer l\'action Association')
      return
    }

    // Action Bleue peut être jouée avec ou sans carte (technologie ou crédits)
    // Les autres actions (Orange, Jaune) ne nécessitent pas de carte

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
    setSelectedTile(null)
    setTileRotation(0)
    setPreviewPosition(null)
  }

  const handleSelectTile = (tile) => {
    setSelectedTile(tile)
    setTileRotation(0)
    setPreviewPosition(null)
  }

  const handleRotateTile = (direction) => {
    setTileRotation(prev => {
      const newRotation = prev + direction
      // Limiter la rotation entre -5 et 5 (équivalent à -300° et +300°)
      if (newRotation < -5) return -5
      if (newRotation > 5) return 5
      return newRotation
    })
  }

  const handlePlaceConstruction = async () => {
    if (!selectedAction || !selectedTile || !previewPosition) {
      alert('Veuillez sélectionner une tuile et un emplacement')
      return
    }

    try {
      await actionsAPI.placeConstruction(id, {
        tile_id: selectedTile.id,
        anchor_q: previewPosition.q,
        anchor_r: previewPosition.r,
        rotation: tileRotation,
        finish_construction_turn: false, // Le joueur peut continuer si le Ranger est amélioré
      })

      // Réinitialiser après placement
      setSelectedTile(null)
      setTileRotation(0)
      setPreviewPosition(null)
      // Ne pas réinitialiser selectedAction si le Ranger est amélioré et peut continuer
      // L'état sera mis à jour via WebSocket
    } catch (error) {
      console.error('Erreur placement construction:', error)
      alert(error.response?.data?.detail || 'Erreur lors du placement de la construction')
    }
  }

  // Filtrer les cartes jouables selon l'action sélectionnée
  const getPlayableCards = () => {
    if (!selectedAction || !myPlayerState?.hand) return []

    const { color, power } = selectedAction

    // Bleu (Mécène) : peut jouer des cartes Technologie dont le niveau requis (cost) <= puissance du Ranger
    if (color === 'blue') {
      const playableCards = myPlayerState.hand.filter(card => {
        // Pour les technologies, le "cost" représente le niveau requis du Ranger Bleu
        if (card.type === 'technology') {
          const levelRequired = card.cost || card.level || 0
          // Le niveau requis doit être <= puissance du Ranger Bleu
          const isPlayable = levelRequired <= power
          console.log(`[DEBUG] Carte ${card.name} (type: ${card.type}): niveau requis=${levelRequired}, Ranger Bleu niveau=${power}, jouable=${isPlayable}`)
          return isPlayable
        }
        // Les autres types de cartes ne sont pas jouables avec l'action Bleue
        return false
      })
      console.log(`[DEBUG] Action Bleue niveau ${power}: ${playableCards.length} carte(s) technologie jouable(s) sur ${myPlayerState.hand.filter(c => c.type === 'technology').length} technologie(s) en main`)
      return playableCards
    }

    // Noir (Animaux) : peut jouer des cartes Troupe
    if (color === 'black') {
      return myPlayerState.hand.filter(card => card.type === 'troupe')
    }

    // Vert (Association) : peut jouer des cartes Quête
    if (color === 'green') {
      return myPlayerState.hand.filter(card => card.type === 'quete')
    }

    // Orange, Jaune : pas de cartes à jouer
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
              <div className="hex-grid-container">
                {myPlayerState?.board?.grid?.hexagons ? (
                  <HexGrid
                    hexagons={myPlayerState.board.grid.hexagons}
                    garnisons={myPlayerState.board.garnisons || []}
                    weapons={myPlayerState.board.weapons || []}
                    tokens={myPlayerState.board.tokens || []}
                    specialZones={myPlayerState.board.special_zones || []}
                    selectedAction={selectedAction}
                    selectedTile={selectedTile}
                    setPreviewPosition={setPreviewPosition}
                  />
                ) : (
                  <div className="map-armor-placeholder">
                    <p>Chargement de la grille...</p>
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
                  <CardDetail card={card} />
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
              {selectedAction.color === 'blue' && 'Sélectionnez une carte Technologie (Mécène) ou gagnez des crédits'}
              {selectedAction.color === 'black' && 'Sélectionnez une carte Troupe à jouer'}
              {selectedAction.color === 'orange' && 'Sélectionnez une tuile de construction, puis son emplacement'}
              {selectedAction.color === 'green' && 'Sélectionnez une carte Quête à réaliser'}
              {selectedAction.color === 'yellow' && 'Action Cartes (pas de carte nécessaire)'}
            </p>

            {selectedAction.color === 'blue' && (
              <div className="playable-cards-section">
                {getPlayableCards().length > 0 ? (
                  <>
                    <h4>Cartes Technologie jouables (niveau requis ≤ {selectedAction.power}) :</h4>
                    <div className="cards-grid">
                      {getPlayableCards().map((card) => {
                        const levelRequired = card.cost || card.level || 0
                        return (
                          <div
                            key={card.id}
                            className={`card-item ${selectedCardFromHand === card.id ? 'selected' : ''}`}
                            onClick={() => handleSelectCardFromHand(card.id)}
                            style={{ backgroundColor: getCardColorByType(card.type) }}
                            title={`Niveau requis: ${levelRequired} (Ranger Bleu niveau ${selectedAction.power})`}
                          >
                            <CardDetail card={card} />
                          </div>
                        )
                      })}
                    </div>
                  </>
                ) : (
                  <div className="no-playable-cards">
                    <p>⚠️ Aucune carte Technologie jouable avec le Ranger Bleu niveau {selectedAction.power}</p>
                    <p className="hint">Les cartes Technologie nécessitent un niveau de Ranger Bleu supérieur ou égal à leur niveau requis.</p>
                  </div>
                )}
              </div>
            )}

            {selectedAction.color !== 'blue' && getPlayableCards().length > 0 && (
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
                      <CardDetail card={card} />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {selectedAction.color !== 'blue' && getPlayableCards().length === 0 && (
              <div className="no-playable-cards">
                <p>⚠️ Aucune carte jouable pour cette action</p>
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

            {/* Section spéciale pour l'action Construction */}
            {selectedAction.color === 'orange' ? (
              <div className="construction-section">
                {/* Sélection de la tuile */}
                {!selectedTile ? (
                  <div className="tiles-selection">
                    <h4>Tuiles disponibles (taille ≤ {selectedAction.power})</h4>
                    {availableTiles.length > 0 ? (
                      <div className="tiles-grid">
                        {availableTiles.map((tile) => (
                          <div
                            key={tile.id}
                            className="tile-preview"
                            onClick={() => handleSelectTile(tile)}
                          >
                            <div className="tile-name">{tile.name}</div>
                            <div className="tile-size">Taille: {tile.size}</div>
                            <div className="tile-cost">Coût: {tile.cost} PO</div>
                            <div className="tile-shape">Forme: {tile.shape}</div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p>Chargement des tuiles...</p>
                    )}
                  </div>
                ) : (
                  <div className="tile-placement">
                    <div className="selected-tile-info">
                      <h4>Tuile sélectionnée: {selectedTile.name}</h4>
                      <p>Taille: {selectedTile.size} | Coût: {selectedTile.cost} PO</p>
                      <div className="rotation-controls">
                        <button onClick={() => handleRotateTile(-1)} className="rotate-button">
                          ↺ Gauche (-60°)
                        </button>
                        <span>Rotation: {tileRotation * 60}°</span>
                        <button onClick={() => handleRotateTile(1)} className="rotate-button">
                          ↻ Droite (+60°)
                        </button>
                      </div>
                    </div>
                    <p className="placement-instruction">
                      Cliquez sur la grille pour choisir l'emplacement de la tuile
                    </p>
                    {previewPosition && (
                      <div className="placement-confirm">
                        <p>Position: ({previewPosition.q}, {previewPosition.r})</p>
                        <button
                          onClick={handlePlaceConstruction}
                          className="confirm-placement-button"
                        >
                          Valider le placement ({selectedTile.cost} PO)
                        </button>
                      </div>
                    )}
                    <button
                      onClick={() => {
                        setSelectedTile(null)
                        setTileRotation(0)
                        setPreviewPosition(null)
                      }}
                      className="cancel-tile-button"
                    >
                      Choisir une autre tuile
                    </button>
                  </div>
                )}
                <button onClick={handleCancelAction} className="cancel-action-button">
                  Annuler l'action
                </button>
              </div>
            ) : (
              <div className="action-confirm-buttons">
                <button
                  onClick={handleConfirmActionWithCard}
                  className="confirm-action-button"
                  disabled={(selectedAction.color === 'black' || selectedAction.color === 'green') && !selectedCardFromHand}
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
            )}
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
                  <CardDetail card={card} />
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
  // Basé sur le schéma SQL : troupes, technologies, quetes
  const cardTypeColors = {
    troupe: '#1f2937',      // Noir - Ranger Animaux (Action Animaux)
    technology: '#3b82f6',  // Bleu - Ranger Mécène (Action Mécène - pièces d'armure)
    quete: '#10b981',       // Vert - Ranger Association (Action Association - quêtes)
    mecenes: '#3b82f6',     // Bleu - Ranger Mécène (alias pour technologies)
  }
  return cardTypeColors[cardType] || '#2a2a2a' // Par défaut gris foncé
}

// Composant pour afficher tous les détails d'une carte
function CardDetail({ card }) {
  return (
    <>
      <div className="card-header">
        <div className="card-name">{card.name}</div>
        <div className="card-type">{card.type}</div>
        {card.is_factice && (
          <div className="card-factice-badge">⚠️ CARTE FACTICE</div>
        )}
      </div>
      
      <div className="card-body">
        {/* Coût ou Niveau requis selon le type de carte */}
        {card.type === 'technology' && card.cost !== undefined && card.cost !== null && (
          <div className="card-section">
            <div className="card-level-required">🔵 Niveau requis: {card.cost}</div>
          </div>
        )}
        
        {card.type !== 'technology' && card.cost !== undefined && card.cost !== null && (
          <div className="card-section">
            <div className="card-cost">{card.cost} PO</div>
          </div>
        )}

        {/* Niveau (pour technologies - affiché en badge) */}
        {card.level && (
          <div className="card-level">Niveau {card.level}</div>
        )}

        {/* Taille (pour troupes) */}
        {card.size !== undefined && card.size !== null && (
          <div className="card-section">
            <div className="card-size">Taille: {card.size}</div>
          </div>
        )}

        {/* Statistiques */}
        <div className="card-stats">
          {card.points_degats !== undefined && card.points_degats !== null && card.points_degats > 0 && (
            <div className="card-stat">
              <span className="card-stat-label">Dégâts:</span>
              <span className="card-stat-value stat-damage">⚔️ {card.points_degats}</span>
            </div>
          )}
          
          {card.nombre_lasers !== undefined && card.nombre_lasers !== null && card.nombre_lasers > 0 && (
            <div className="card-stat">
              <span className="card-stat-label">Lasers:</span>
              <span className="card-stat-value stat-laser">🔵 {card.nombre_lasers}</span>
            </div>
          )}
          
          {card.points_developpement_technique !== undefined && card.points_developpement_technique !== null && card.points_developpement_technique > 0 && (
            <div className="card-stat">
              <span className="card-stat-label">Réputation:</span>
              <span className="card-stat-value stat-reputation">⭐ {card.points_developpement_technique}</span>
            </div>
          )}
          
          {card.paires_ailes !== undefined && card.paires_ailes !== null && card.paires_ailes > 0 && (
            <div className="card-stat">
              <span className="card-stat-label">Ailes:</span>
              <span className="card-stat-value stat-wings">🪽 {card.paires_ailes}</span>
            </div>
          )}
          
          {card.or_par_jour !== undefined && card.or_par_jour !== null && card.or_par_jour > 0 && (
            <div className="card-stat">
              <span className="card-stat-label">Or/jour:</span>
              <span className="card-stat-value stat-gold">💰 {card.or_par_jour}</span>
            </div>
          )}
        </div>

        {/* Matières premières requises */}
        {card.raw_materials_required && Array.isArray(card.raw_materials_required) && card.raw_materials_required.length > 0 && (
          <div className="card-materials">
            <div className="card-section-title">Matériaux requis</div>
            {card.raw_materials_required.map((material, idx) => (
              <div key={idx} className="card-material-item">
                • {material.material_name || material.material_id}: {material.quantity}
              </div>
            ))}
          </div>
        )}

        {/* Type d'arme (pour troupes) */}
        {card.weapon_type && (
          <div className="card-section">
            <div className="card-section-title">Type d'arme</div>
            <div className="card-material-item">{card.weapon_type}</div>
          </div>
        )}

        {/* Type de pièce d'armure (pour technologies) */}
        {card.armor_piece_type && (
          <div className="card-section">
            <div className="card-section-title">Type de pièce</div>
            <div className="card-material-item">{card.armor_piece_type}</div>
          </div>
        )}

        {/* Type de quête (pour quêtes) */}
        {card.quest_type && (
          <div className="card-section">
            <div className="card-section-title">Type de quête</div>
            <div className="card-material-item">{card.quest_type}</div>
          </div>
        )}

        {/* Conditions (pour quêtes) */}
        {card.conditions && typeof card.conditions === 'object' && Object.keys(card.conditions).length > 0 && (
          <div className="card-conditions">
            <div className="card-section-title">Conditions</div>
            {Object.entries(card.conditions).map(([key, value], idx) => (
              <div key={idx} className="card-condition-item">
                {key}: {typeof value === 'object' ? JSON.stringify(value) : value}
              </div>
            ))}
          </div>
        )}

        {/* Récompenses (pour quêtes) */}
        {card.rewards && typeof card.rewards === 'object' && Object.keys(card.rewards).length > 0 && (
          <div className="card-section">
            <div className="card-section-title">Récompenses</div>
            {Object.entries(card.rewards).map(([key, value], idx) => (
              <div key={idx} className="card-material-item">
                {key}: {typeof value === 'object' ? JSON.stringify(value) : value}
              </div>
            ))}
          </div>
        )}

        {/* Effets */}
        <div className="card-effects">
          {card.bonus && (
            <div className="card-effect">
              <div className="card-effect-title">Bonus</div>
              <div className="card-effect-text">{card.bonus}</div>
            </div>
          )}
          
          {card.effet_invocation && (
            <div className="card-effect">
              <div className="card-effect-title">Effet d'invocation</div>
              <div className="card-effect-text">{card.effet_invocation}</div>
            </div>
          )}
          
          {card.effet_quotidien && (
            <div className="card-effect">
              <div className="card-effect-title">Effet quotidien</div>
              <div className="card-effect-text">{card.effet_quotidien}</div>
            </div>
          )}
          
          {card.dernier_souffle && (
            <div className="card-effect">
              <div className="card-effect-title">Dernier souffle</div>
              <div className="card-effect-text">{card.dernier_souffle}</div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

// Composant pour afficher la grille hexagonale
function HexGrid({ hexagons, garnisons, weapons, tokens, specialZones, selectedAction, selectedTile, setPreviewPosition }) {
  // Calculer les positions des hexagones pour l'affichage
  const hexSize = 30 // Taille d'un hexagone en pixels
  const hexWidth = hexSize * 2
  const hexHeight = Math.sqrt(3) * hexSize

  // Fonction pour convertir coordonnées hexagonales (q, r) en coordonnées pixel
  // Structure : 9 colonnes verticales (q = 0-8), chaque colonne a 6 ou 7 hexagones
  const hexToPixel = (q, r) => {
    // Pour une grille hexagonale en colonnes verticales
    // Les colonnes impaires sont décalées
    const offsetX = hexSize * Math.sqrt(3) * q
    const offsetY = hexSize * (1.5 * r + (q % 2) * 0.75) // Décalage pour colonnes paires/impaires
    return { x: offsetX + 50, y: offsetY + 50 } // Offset pour centrer
  }

  // Obtenir le terrain d'un hexagone
  const getTerrainColor = (terrain, constructible) => {
    if (!constructible) {
      if (terrain === 'water') return '#3b82f6' // Bleu pour l'eau
      if (terrain === 'rock') return '#6b7280' // Gris pour les rochers
    }
    return '#92400e' // Marron pour la terre craquelée (constructible)
  }

  // Vérifier si un hexagone a une garnison
  const getGarnisonForHex = (q, r) => {
    return garnisons.find(g =>
      g.hexagons?.some(h => h.q === q && h.r === r)
    )
  }

  // Vérifier si un hexagone a une arme
  const getWeaponForHex = (q, r) => {
    const garnison = getGarnisonForHex(q, r)
    if (garnison && garnison.weapon_id) {
      return weapons.find(w => w.id === garnison.weapon_id)
    }
    return null
  }

  return (
    <div className="hex-grid-wrapper">
      <svg
        className="hex-grid-svg"
        viewBox="0 0 800 600"
        preserveAspectRatio="xMidYMid meet"
      >
        {hexagons.map((hex, index) => {
          const { x, y } = hexToPixel(hex.q, hex.r)
          const terrainColor = getTerrainColor(hex.terrain, hex.constructible)
          const garnison = getGarnisonForHex(hex.q, hex.r)
          const weapon = getWeaponForHex(hex.q, hex.r)

          // Points pour dessiner l'hexagone
          const points = []
          for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i
            const px = x + hexSize * Math.cos(angle)
            const py = y + hexSize * Math.sin(angle)
            points.push(`${px},${py}`)
          }

          return (
            <g key={`hex-${hex.q}-${hex.r}`}>
              <polygon
                points={points.join(' ')}
                fill={terrainColor}
                stroke={hex.constructible ? '#666' : '#444'}
                strokeWidth={1}
                opacity={hex.constructible ? 0.8 : 0.5}
                className="hex-cell"
                onClick={() => {
                  // Si on est en mode placement de tuile, définir la position de prévisualisation
                  if (selectedAction?.color === 'orange' && selectedTile) {
                    setPreviewPosition({ q: hex.q, r: hex.r })
                  }
                }}
                style={{
                  cursor: selectedAction?.color === 'orange' && selectedTile ? 'pointer' : 'default',
                }}
              />
              {garnison && (
                <circle
                  cx={x}
                  cy={y}
                  r={hexSize * 0.6}
                  fill="#10b981"
                  opacity={0.3}
                  className="garnison-marker"
                />
              )}
              {weapon && (
                <circle
                  cx={x}
                  cy={y}
                  r={hexSize * 0.4}
                  fill="#1f2937"
                  opacity={0.7}
                  className="weapon-marker"
                />
              )}
              {/* Afficher les coordonnées pour debug (seulement quelques hexagones) */}
              {hex.q < 3 && hex.r < 2 && (
                <text
                  x={x}
                  y={y + 4}
                  fontSize="8"
                  fill="#fff"
                  textAnchor="middle"
                  className="hex-coords"
                >
                  {hex.q},{hex.r}
                </text>
              )}
            </g>
          )
        })}
      </svg>
    </div>
  )
}

export default GameRoom


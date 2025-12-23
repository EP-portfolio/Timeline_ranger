/**
 * Service WebSocket pour la synchronisation temps réel
 */

class WebSocketService {
  constructor() {
    this.ws = null
    this.gameId = null
    this.token = null
    this.listeners = new Map()
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectDelay = 1000
  }

  connect(gameId, token) {
    this.gameId = gameId
    this.token = token

    // Détecter automatiquement l'URL WebSocket (ws:// pour HTTP, wss:// pour HTTPS)
    const getWebSocketUrl = () => {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
      // Convertir l'URL API en URL WebSocket
      const baseUrl = apiUrl.replace('/api/v1', '').replace('http://', 'ws://').replace('https://', 'wss://')
      return baseUrl
    }

    const wsUrl = `${getWebSocketUrl()}/ws/games/${gameId}?token=${token}`
    
    try {
      this.ws = new WebSocket(wsUrl)

      this.ws.onopen = () => {
        console.log('✅ WebSocket connecté')
        this.reconnectAttempts = 0
        this.emit('connected')
      }

      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          this.handleMessage(message)
        } catch (error) {
          console.error('Erreur parsing message WebSocket:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('❌ Erreur WebSocket:', error)
        this.emit('error', error)
      }

      this.ws.onclose = () => {
        console.log('❌ WebSocket fermé')
        this.emit('disconnected')
        this.attemptReconnect()
      }
    } catch (error) {
      console.error('Erreur connexion WebSocket:', error)
      this.attemptReconnect()
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts}...`)
      setTimeout(() => {
        if (this.gameId && this.token) {
          this.connect(this.gameId, this.token)
        }
      }, this.reconnectDelay * this.reconnectAttempts)
    } else {
      console.error('Impossible de se reconnecter au WebSocket')
      this.emit('reconnect_failed')
    }
  }

  handleMessage(message) {
    const type = message.type
    this.emit(type, message)
    
    // Émettre aussi un événement générique
    this.emit('message', message)
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket non connecté, message non envoyé:', message)
    }
  }

  // Méthodes utilitaires
  ping() {
    this.send({
      type: 'ping',
      timestamp: Date.now(),
    })
  }

  requestGameState() {
    this.send({
      type: 'game_state_request',
    })
  }

  // Gestion des listeners
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event)
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach((callback) => {
        try {
          callback(data)
        } catch (error) {
          console.error(`Erreur dans callback pour ${event}:`, error)
        }
      })
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.gameId = null
    this.token = null
    this.listeners.clear()
    this.reconnectAttempts = 0
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN
  }
}

// Instance singleton
const wsService = new WebSocketService()

export default wsService


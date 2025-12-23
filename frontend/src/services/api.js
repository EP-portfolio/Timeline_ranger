import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Log pour debug (uniquement en développement)
if (import.meta.env.DEV) {
  console.log('🔗 API URL:', API_BASE_URL)
}

// Créer une instance axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 secondes de timeout
})

// Intercepteur pour ajouter le token à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Log des erreurs pour debug
    console.error('❌ Erreur API:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data,
    })

    if (error.response?.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }

    // Gestion des erreurs réseau
    if (error.code === 'ECONNABORTED' || error.message === 'Network Error') {
      console.error('🌐 Erreur réseau - Vérifier CORS et URL API')
    }

    return Promise.reject(error)
  }
)

// Auth
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (formData) =>
    api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  getCurrentUser: () => api.get('/auth/me'),
}

// Games
export const gamesAPI = {
  create: (data) => api.post('/games', data),
  list: () => api.get('/games'),
  get: (code) => api.get(`/games/${code}`),
  join: (data) => api.post('/games/join', data),
  getPlayers: (gameId) => api.get(`/games/${gameId}/players`),
  start: (gameId) => api.post(`/games/${gameId}/start`),
  getState: (gameId) => api.get(`/games/${gameId}/state`),
}

// Actions
export const actionsAPI = {
  playColor: (gameId, data) => api.post(`/games/${gameId}/actions/play-color`, data),
  playCard: (gameId, data) => api.post(`/games/${gameId}/actions/play-card`, data),
  pass: (gameId, data) => api.post(`/games/${gameId}/actions/pass`, data),
}

export default api


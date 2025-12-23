import { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Vérifier si l'utilisateur est déjà connecté
    const token = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (token && savedUser) {
      try {
        setUser(JSON.parse(savedUser))
        // Vérifier que le token est toujours valide
        authAPI
          .getCurrentUser()
          .then((response) => {
            setUser(response.data)
            localStorage.setItem('user', JSON.stringify(response.data))
          })
          .catch(() => {
            // Token invalide, déconnexion
            logout()
          })
          .finally(() => setLoading(false))
      } catch (error) {
        logout()
        setLoading(false)
      }
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (email, password) => {
    try {
      const formData = new FormData()
      formData.append('username', email) // OAuth2 utilise 'username' pour l'email
      formData.append('password', password)

      const response = await authAPI.login(formData)
      const { access_token, user: userData } = response.data

      // Si user n'est pas dans la réponse, le récupérer avec /me
      let finalUserData = userData
      if (!finalUserData) {
        localStorage.setItem('token', access_token)
        const userResponse = await authAPI.getCurrentUser()
        finalUserData = userResponse.data
      }

      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(finalUserData))
      setUser(finalUserData)

      return { success: true }
    } catch (error) {
      console.error('Erreur login:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.message || 'Erreur de connexion',
      }
    }
  }

  const register = async (email, password, username) => {
    try {
      const response = await authAPI.register({ email, password, username })
      const userData = response.data

      // Connecter automatiquement après inscription
      const loginResult = await login(email, password)
      return loginResult
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || "Erreur d'inscription",
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth doit être utilisé dans un AuthProvider')
  }
  return context
}


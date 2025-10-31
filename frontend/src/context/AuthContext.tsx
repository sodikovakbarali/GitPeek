import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { getCurrentUser, logout as apiLogout } from '../lib/api'

interface User {
  login: string
  avatar_url: string
  name: string
}

interface AuthContextType {
  user: User | null
  sessionId: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (sessionId: string) => void
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(
    () => localStorage.getItem('session_id')
  )
  const [isLoading, setIsLoading] = useState(true)

  const refreshUser = async () => {
    if (!sessionId) {
      setUser(null)
      setIsLoading(false)
      return
    }

    try {
      const userData = await getCurrentUser()
      setUser(userData)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      // Clear invalid session
      localStorage.removeItem('session_id')
      setSessionId(null)
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    refreshUser()
  }, [sessionId])

  const login = (newSessionId: string) => {
    localStorage.setItem('session_id', newSessionId)
    setSessionId(newSessionId)
  }

  const logout = async () => {
    try {
      if (sessionId) {
        await apiLogout()
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('session_id')
      setSessionId(null)
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        sessionId,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}


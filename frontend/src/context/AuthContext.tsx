import { createContext, useContext, useState, ReactNode } from 'react'
import { api } from '../services/api'

interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'agent' | 'user'
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  async function login(email: string, password: string) {
    const { data } = await api.post('/api/auth/login', { email, password })
    localStorage.setItem('access_token', data.access_token)
    const me = await api.get('/api/auth/me')
    setUser(me.data)
  }

  function logout() {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { Spinner } from '../components/ui/Spinner'
import { useAuth } from '../context/AuthContext'
import { handleAuthCallback } from '../lib/api'

export default function AuthCallback() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { login } = useAuth()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const code = searchParams.get('code')

    if (!code) {
      setError('No authorization code received')
      setTimeout(() => navigate('/'), 3000)
      return
    }

    async function authenticate() {
      try {
        const response = await handleAuthCallback(code!)
        login(response.session_id)
        navigate('/')
      } catch (err) {
        console.error('Auth callback error:', err)
        setError('Authentication failed. Please try again.')
        setTimeout(() => navigate('/'), 3000)
      }
    }

    authenticate()
  }, [searchParams, navigate, login])

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] space-y-4">
        <div className="text-destructive text-lg font-medium">{error}</div>
        <p className="text-muted-foreground">Redirecting to home...</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] space-y-4">
      <Spinner size="lg" />
      <p className="text-muted-foreground">Completing authentication...</p>
    </div>
  )
}


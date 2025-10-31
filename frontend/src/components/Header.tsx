import { Moon, Sun, Github, LogOut } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'
import { useAuth } from '../context/AuthContext'
import { Button } from './ui/Button'
import { initiateGitHubLogin } from '../lib/api'

export default function Header() {
  const { theme, toggleTheme } = useTheme()
  const { user, isAuthenticated, logout } = useAuth()

  const handleLogin = async () => {
    try {
      const authUrl = await initiateGitHubLogin()
      window.location.href = authUrl
    } catch (error) {
      console.error('Login error:', error)
    }
  }

  return (
    <header className="border-b bg-card">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Github className="h-6 w-6 text-primary" />
          <h1 className="text-2xl font-bold">GitPeek</h1>
        </div>

        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {theme === 'light' ? (
              <Moon className="h-5 w-5" />
            ) : (
              <Sun className="h-5 w-5" />
            )}
          </Button>

          {isAuthenticated && user ? (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <img
                  src={user.avatar_url}
                  alt={user.login}
                  className="h-8 w-8 rounded-full"
                />
                <span className="text-sm font-medium">{user.login}</span>
              </div>
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          ) : (
            <Button onClick={handleLogin} size="sm">
              <Github className="h-4 w-4 mr-2" />
              Login with GitHub
            </Button>
          )}
        </div>
      </div>
    </header>
  )
}


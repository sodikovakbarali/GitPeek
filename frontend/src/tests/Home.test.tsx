import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Home from '../pages/Home'
import { AuthProvider } from '../context/AuthContext'
import { ThemeProvider } from '../context/ThemeContext'

// Mock the API
vi.mock('../lib/api', () => ({
  getUserActivity: vi.fn(),
  TimeRange: {},
}))

const AllProviders = ({ children }: { children: React.ReactNode }) => (
  <BrowserRouter>
    <ThemeProvider>
      <AuthProvider>
        {children}
      </AuthProvider>
    </ThemeProvider>
  </BrowserRouter>
)

describe('Home', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders hero section', () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    )

    expect(screen.getByText(/peek into github activity/i)).toBeInTheDocument()
  })

  it('renders search bar', () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    )

    expect(screen.getByPlaceholderText(/enter github username/i)).toBeInTheDocument()
  })

  it('shows empty state initially', () => {
    render(
      <AllProviders>
        <Home />
      </AllProviders>
    )

    expect(screen.getByText(/enter a github username to view their activity/i)).toBeInTheDocument()
  })
})


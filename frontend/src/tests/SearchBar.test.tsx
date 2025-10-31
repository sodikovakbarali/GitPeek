import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import SearchBar from '../components/SearchBar'

describe('SearchBar', () => {
  it('renders search input and button', () => {
    const mockSearch = vi.fn()
    render(<SearchBar onSearch={mockSearch} />)

    expect(screen.getByPlaceholderText(/enter github username/i)).toBeInTheDocument()
    expect(screen.getByText('Search')).toBeInTheDocument()
  })

  it('handles form submission', () => {
    const mockSearch = vi.fn()
    render(<SearchBar onSearch={mockSearch} />)

    const input = screen.getByPlaceholderText(/enter github username/i)
    const button = screen.getByText('Search')

    fireEvent.change(input, { target: { value: 'testuser' } })
    fireEvent.click(button)

    expect(mockSearch).toHaveBeenCalledWith('testuser', 'week')
  })

  it('does not submit empty username', () => {
    const mockSearch = vi.fn()
    render(<SearchBar onSearch={mockSearch} />)

    const button = screen.getByText('Search')
    fireEvent.click(button)

    expect(mockSearch).not.toHaveBeenCalled()
  })

  it('updates time range', () => {
    const mockSearch = vi.fn()
    render(<SearchBar onSearch={mockSearch} />)

    const input = screen.getByPlaceholderText(/enter github username/i)
    const select = screen.getByRole('combobox')
    const button = screen.getByText('Search')

    fireEvent.change(input, { target: { value: 'testuser' } })
    fireEvent.change(select, { target: { value: 'month' } })
    fireEvent.click(button)

    expect(mockSearch).toHaveBeenCalledWith('testuser', 'month')
  })
})


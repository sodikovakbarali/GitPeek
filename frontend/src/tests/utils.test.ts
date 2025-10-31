import { describe, it, expect } from 'vitest'
import { cn, formatDate, formatDateTime, truncateText } from '../lib/utils'

describe('utils', () => {
  describe('cn', () => {
    it('merges class names', () => {
      const result = cn('class1', 'class2')
      expect(result).toContain('class1')
      expect(result).toContain('class2')
    })

    it('handles conditional classes', () => {
      const result = cn('class1', false && 'class2', 'class3')
      expect(result).toContain('class1')
      expect(result).not.toContain('class2')
      expect(result).toContain('class3')
    })
  })

  describe('formatDate', () => {
    it('formats date string', () => {
      const date = '2024-01-15T12:00:00Z'
      const result = formatDate(date)
      expect(result).toMatch(/Jan/)
      expect(result).toMatch(/15/)
      expect(result).toMatch(/2024/)
    })
  })

  describe('formatDateTime', () => {
    it('formats datetime string', () => {
      const date = '2024-01-15T12:30:00Z'
      const result = formatDateTime(date)
      expect(result).toMatch(/Jan/)
      expect(result).toMatch(/15/)
      expect(result).toMatch(/2024/)
    })
  })

  describe('truncateText', () => {
    it('truncates long text', () => {
      const text = 'This is a very long text that should be truncated'
      const result = truncateText(text, 20)
      expect(result.length).toBeLessThanOrEqual(23) // 20 + '...'
      expect(result).toContain('...')
    })

    it('does not truncate short text', () => {
      const text = 'Short text'
      const result = truncateText(text, 20)
      expect(result).toBe(text)
      expect(result).not.toContain('...')
    })
  })
})


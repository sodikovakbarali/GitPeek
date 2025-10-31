import { useState, FormEvent } from 'react'
import { Search } from 'lucide-react'
import { Input } from './ui/Input'
import { Select } from './ui/Select'
import { Button } from './ui/Button'
import { TimeRange } from '../lib/api'

interface SearchBarProps {
  onSearch: (username: string, timeRange: TimeRange) => void
  isLoading?: boolean
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [username, setUsername] = useState('')
  const [timeRange, setTimeRange] = useState<TimeRange>('week')

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (username.trim()) {
      onSearch(username.trim(), timeRange)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl mx-auto">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <Input
            type="text"
            placeholder="Enter GitHub username..."
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={isLoading}
            className="w-full"
          />
        </div>

        <Select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value as TimeRange)}
          disabled={isLoading}
          className="sm:w-40"
        >
          <option value="day">Past Day</option>
          <option value="week">Past Week</option>
          <option value="month">Past Month</option>
          <option value="year">Past Year</option>
        </Select>

        <Button type="submit" disabled={isLoading || !username.trim()}>
          <Search className="h-4 w-4 mr-2" />
          Search
        </Button>
      </div>
    </form>
  )
}


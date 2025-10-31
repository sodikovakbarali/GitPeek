import { useState } from 'react'
import { AlertCircle } from 'lucide-react'
import SearchBar from '../components/SearchBar'
import UserStats from '../components/UserStats'
import ActivityChart from '../components/ActivityChart'
import RepositoryList from '../components/RepositoryList'
import CommitList from '../components/CommitList'
import { Spinner } from '../components/ui/Spinner'
import { useAuth } from '../context/AuthContext'
import { getUserActivity, TimeRange, UserActivity } from '../lib/api'

export default function Home() {
  const { isAuthenticated } = useAuth()
  const [activity, setActivity] = useState<UserActivity | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (username: string, timeRange: TimeRange) => {
    setIsLoading(true)
    setError(null)
    setActivity(null)

    try {
      const data = await getUserActivity(username, timeRange, isAuthenticated)
      setActivity(data)
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message)
      } else {
        setError('Failed to fetch user activity. Please try again.')
      }
      console.error('Search error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4 py-12">
        <h2 className="text-4xl font-bold tracking-tight">
          Peek into GitHub Activity
        </h2>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          View any GitHub user's repositories and commits over time. Login to see
          private repositories too.
        </p>
      </div>

      {/* Search Bar */}
      <SearchBar onSearch={handleSearch} isLoading={isLoading} />

      {/* Loading State */}
      {isLoading && (
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <Spinner size="lg" />
          <p className="text-muted-foreground">Loading activity...</p>
        </div>
      )}

      {/* Error State */}
      {error && !isLoading && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-6 flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-destructive">Error</h3>
            <p className="text-sm text-destructive/90 mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Results */}
      {activity && !isLoading && (
        <div className="space-y-6">
          {/* User Header */}
          <div className="flex items-center gap-4 p-6 bg-card rounded-lg border">
            {activity.avatar_url && (
              <img
                src={activity.avatar_url}
                alt={activity.username}
                className="h-16 w-16 rounded-full"
              />
            )}
            <div>
              <h3 className="text-2xl font-bold">{activity.username}</h3>
              <p className="text-muted-foreground">
                GitHub Activity Overview
              </p>
            </div>
          </div>

          {/* Stats */}
          <UserStats activity={activity} />

          {/* Activity Chart */}
          <ActivityChart data={activity.activity_chart} />

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <RepositoryList repositories={activity.repositories} />
            <CommitList commits={activity.commits} />
          </div>
        </div>
      )}

      {/* Empty State */}
      {!activity && !isLoading && !error && (
        <div className="text-center py-12 text-muted-foreground">
          <p>Enter a GitHub username to view their activity</p>
        </div>
      )}
    </div>
  )
}


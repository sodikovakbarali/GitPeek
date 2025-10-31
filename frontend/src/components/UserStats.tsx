import { GitCommit, FolderGit } from 'lucide-react'
import { UserActivity } from '../lib/api'
import { Card, CardContent } from './ui/Card'

interface UserStatsProps {
  activity: UserActivity
}

export default function UserStats({ activity }: UserStatsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Total Commits
              </p>
              <p className="text-3xl font-bold">{activity.total_commits}</p>
            </div>
            <GitCommit className="h-8 w-8 text-muted-foreground" />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Repositories
              </p>
              <p className="text-3xl font-bold">{activity.repositories.length}</p>
            </div>
            <FolderGit className="h-8 w-8 text-muted-foreground" />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Time Range
              </p>
              <p className="text-3xl font-bold capitalize">{activity.time_range}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}


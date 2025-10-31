import { GitCommit, ExternalLink } from 'lucide-react'
import { Commit } from '../lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card'
import { formatDateTime, truncateText } from '../lib/utils'

interface CommitListProps {
  commits: Commit[]
}

export default function CommitList({ commits }: CommitListProps) {
  if (!commits || commits.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Commits</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">
            No commits found for this time period
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Commits ({commits.length})</CardTitle>
        <CardDescription>Latest commits across all repositories</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {commits.map((commit) => (
            <div
              key={commit.sha}
              className="flex items-start gap-3 p-3 border rounded-lg hover:bg-accent transition-colors"
            >
              <GitCommit className="h-5 w-5 text-primary mt-0.5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <p className="font-medium text-sm">
                    {truncateText(commit.message, 80)}
                  </p>
                  <a
                    href={commit.html_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-primary flex-shrink-0"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </div>
                <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                  <span>{commit.repository}</span>
                  <span>•</span>
                  <span>{formatDateTime(commit.date)}</span>
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  <code className="bg-muted px-1.5 py-0.5 rounded">
                    {commit.sha.substring(0, 7)}
                  </code>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}


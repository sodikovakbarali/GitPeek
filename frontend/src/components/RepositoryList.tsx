import { Star, GitFork, ExternalLink } from 'lucide-react'
import { Repository } from '../lib/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/Card'

interface RepositoryListProps {
  repositories: Repository[]
}

export default function RepositoryList({ repositories }: RepositoryListProps) {
  if (!repositories || repositories.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Repositories</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground text-center py-8">
            No repositories found
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Repositories ({repositories.length})</CardTitle>
        <CardDescription>Most recently updated repositories</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {repositories.map((repo) => (
            <div
              key={repo.id}
              className="flex items-start justify-between p-4 border rounded-lg hover:bg-accent transition-colors"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <a
                    href={repo.html_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-primary hover:underline"
                  >
                    {repo.name}
                  </a>
                  {repo.private && (
                    <span className="text-xs bg-muted px-2 py-1 rounded">
                      Private
                    </span>
                  )}
                  <ExternalLink className="h-3 w-3 text-muted-foreground" />
                </div>
                {repo.description && (
                  <p className="text-sm text-muted-foreground mt-1">
                    {repo.description}
                  </p>
                )}
                <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                  {repo.language && (
                    <span className="flex items-center gap-1">
                      <span className="w-3 h-3 rounded-full bg-primary"></span>
                      {repo.language}
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <Star className="h-4 w-4" />
                    {repo.stars}
                  </span>
                  <span className="flex items-center gap-1">
                    <GitFork className="h-4 w-4" />
                    {repo.forks}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}


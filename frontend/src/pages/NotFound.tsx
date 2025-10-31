import { Link } from 'react-router-dom'
import { Button } from '../components/ui/Button'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] space-y-4 text-center">
      <h1 className="text-6xl font-bold">404</h1>
      <h2 className="text-2xl font-semibold">Page Not Found</h2>
      <p className="text-muted-foreground max-w-md">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/">
        <Button>Go Back Home</Button>
      </Link>
    </div>
  )
}


import { Link } from 'react-router-dom'

function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <p className="text-gray-400 mb-6">Page not found</p>
        <Link to="/" className="px-4 py-2 bg-primary text-black rounded-lg">Go Home</Link>
      </div>
    </div>
  )
}

export default NotFound

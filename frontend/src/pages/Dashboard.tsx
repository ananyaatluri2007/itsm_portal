import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Welcome, {user?.name}</h1>
        <button onClick={logout} className="text-sm text-red-600">
          Log out
        </button>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => navigate('/tickets')}
          className="bg-slate-800 text-white px-4 py-2 rounded hover:bg-slate-700"
        >
          View Incident Queue
        </button>
        <button
          onClick={() => navigate('/tickets/new')}
          className="bg-white border px-4 py-2 rounded hover:bg-slate-50"
        >
          Raise New Ticket
        </button>
      </div>

      <p className="text-slate-500 mt-6 text-sm">
        Next up: Asset Registry page and dashboard KPI charts.
      </p>
    </div>
  )
}

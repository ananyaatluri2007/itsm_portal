import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Welcome, {user?.name}</h1>
        <button onClick={logout} className="text-sm text-red-600">
          Log out
        </button>
      </div>
      <p className="text-slate-600">
        This is your dashboard placeholder. Next: build the Asset Registry and
        Incident Queue pages here.
      </p>
    </div>
  )
}

import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { listTickets, Ticket } from '../../services/tickets'
import SLABadge from '../../components/tickets/SLABadge'
import PriorityBadge from '../../components/tickets/PriorityBadge'

export default function IncidentQueue() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [statusFilter, setStatusFilter] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    setLoading(true)
    listTickets({
      status: statusFilter || undefined,
      priority: priorityFilter || undefined,
    })
      .then(setTickets)
      .finally(() => setLoading(false))
  }, [statusFilter, priorityFilter])

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Incident Queue</h1>
        <button
          onClick={() => navigate('/tickets/new')}
          className="bg-slate-800 text-white px-4 py-2 rounded hover:bg-slate-700"
        >
          Raise New Ticket
        </button>
      </div>

      <div className="flex gap-3 mb-4">
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="border rounded px-3 py-2 text-sm"
        >
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="pending_user">Pending User</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          className="border rounded px-3 py-2 text-sm"
        >
          <option value="">All Priorities</option>
          <option value="P1">P1 - Critical</option>
          <option value="P2">P2 - High</option>
          <option value="P3">P3 - Medium</option>
          <option value="P4">P4 - Low</option>
        </select>
      </div>

      {loading ? (
        <p className="text-slate-500">Loading tickets…</p>
      ) : tickets.length === 0 ? (
        <p className="text-slate-500">No tickets yet — raise your first incident.</p>
      ) : (
        <table className="w-full bg-white rounded shadow-sm overflow-hidden">
          <thead className="bg-slate-50 text-left text-xs text-slate-500 uppercase">
            <tr>
              <th className="p-3">Ticket ID</th>
              <th className="p-3">Title</th>
              <th className="p-3">Priority</th>
              <th className="p-3">Status</th>
              <th className="p-3">SLA</th>
              <th className="p-3">Created</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map((t) => (
              <tr
                key={t.id}
                onClick={() => navigate(`/tickets/${t.id}`)}
                className="border-t hover:bg-slate-50 cursor-pointer text-sm"
              >
                <td className="p-3 font-medium">{t.ticket_number}</td>
                <td className="p-3">{t.title}</td>
                <td className="p-3"><PriorityBadge priority={t.priority} /></td>
                <td className="p-3 capitalize">{t.status.replace('_', ' ')}</td>
                <td className="p-3"><SLABadge slaDueAt={t.sla_due_at} status={t.status} /></td>
                <td className="p-3 text-slate-500">
                  {new Date(t.created_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

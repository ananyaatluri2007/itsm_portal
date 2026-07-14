import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTicket, updateStatus, getComments, addComment, Ticket, Comment } from '../../services/tickets'
import SLABadge from '../../components/tickets/SLABadge'
import PriorityBadge from '../../components/tickets/PriorityBadge'
import { useAuth } from '../../context/AuthContext'

const STATUSES = ['open', 'in_progress', 'pending_user', 'resolved', 'closed']

export default function TicketDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [comments, setComments] = useState<Comment[]>([])
  const [newComment, setNewComment] = useState('')
  const [loading, setLoading] = useState(true)

  async function load() {
    if (!id) return
    const [t, c] = await Promise.all([getTicket(id), getComments(id)])
    setTicket(t)
    setComments(c)
    setLoading(false)
  }

  useEffect(() => {
    load()
  }, [id])

  async function handleStatusChange(status: string) {
    if (!id) return
    const updated = await updateStatus(id, status)
    setTicket(updated)
  }

  async function handleAddComment(e: React.FormEvent) {
    e.preventDefault()
    if (!id || !newComment.trim()) return
    const c = await addComment(id, newComment)
    setComments([...comments, c])
    setNewComment('')
  }

  if (loading || !ticket) return <div className="p-8 text-slate-500">Loading ticket…</div>

  const canManage = user?.role === 'admin' || user?.role === 'agent'

  return (
    <div className="p-8 max-w-3xl">
      <button onClick={() => navigate('/tickets')} className="text-sm text-slate-500 mb-4">
        ← Back to queue
      </button>

      <div className="bg-white rounded shadow-sm p-6 mb-6">
        <div className="flex justify-between items-start mb-2">
          <div>
            <p className="text-xs text-slate-400">{ticket.ticket_number}</p>
            <h1 className="text-xl font-semibold">{ticket.title}</h1>
          </div>
          <div className="flex gap-2">
            <PriorityBadge priority={ticket.priority} />
            <SLABadge slaDueAt={ticket.sla_due_at} status={ticket.status} />
          </div>
        </div>
        <p className="text-slate-600 mt-3">{ticket.description}</p>

        {canManage && (
          <div className="mt-4">
            <label className="block text-sm text-slate-600 mb-1">Status</label>
            <select
              value={ticket.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              className="border rounded px-3 py-2 text-sm"
            >
              {STATUSES.map((s) => (
                <option key={s} value={s}>{s.replace('_', ' ')}</option>
              ))}
            </select>
          </div>
        )}
        {!canManage && (
          <p className="mt-4 text-sm text-slate-500 capitalize">
            Status: {ticket.status.replace('_', ' ')}
          </p>
        )}
      </div>

      <div className="bg-white rounded shadow-sm p-6">
        <h2 className="font-semibold mb-4">Comments</h2>
        <div className="space-y-3 mb-4">
          {comments.length === 0 && (
            <p className="text-sm text-slate-400">No comments yet.</p>
          )}
          {comments.map((c) => (
            <div key={c.id} className="border-l-2 border-slate-200 pl-3 text-sm">
              <p className="text-slate-700">{c.body}</p>
              <p className="text-xs text-slate-400 mt-1">
                {new Date(c.created_at).toLocaleString()}
                {c.is_internal && ' · internal note'}
              </p>
            </div>
          ))}
        </div>
        <form onSubmit={handleAddComment} className="flex gap-2">
          <input
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Add a comment…"
            className="flex-1 border rounded px-3 py-2 text-sm"
          />
          <button type="submit" className="bg-slate-800 text-white px-4 py-2 rounded text-sm">
            Post
          </button>
        </form>
      </div>
    </div>
  )
}

interface Props {
  slaDueAt: string | null
  status: string
}

export default function SLABadge({ slaDueAt, status }: Props) {
  if (!slaDueAt || status === 'resolved' || status === 'closed') {
    return <span className="text-xs text-slate-400">—</span>
  }

  const due = new Date(slaDueAt).getTime()
  const now = Date.now()
  const msRemaining = due - now
  const hoursRemaining = msRemaining / (1000 * 60 * 60)

  let color = 'bg-green-100 text-green-700'
  let label = `${Math.max(0, Math.round(hoursRemaining))}h left`

  if (msRemaining < 0) {
    color = 'bg-red-100 text-red-700'
    label = 'Breached'
  } else if (hoursRemaining < 4) {
    color = 'bg-amber-100 text-amber-700'
  }

  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${color}`}>{label}</span>
  )
}

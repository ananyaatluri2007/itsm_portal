const COLORS: Record<string, string> = {
  P1: 'bg-red-100 text-red-700',
  P2: 'bg-orange-100 text-orange-700',
  P3: 'bg-yellow-100 text-yellow-700',
  P4: 'bg-slate-100 text-slate-700',
}

export default function PriorityBadge({ priority }: { priority: string }) {
  return (
    <span className={`px-2 py-1 rounded text-xs font-medium ${COLORS[priority] || COLORS.P4}`}>
      {priority}
    </span>
  )
}

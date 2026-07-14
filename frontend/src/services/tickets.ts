import { api } from './api'

export interface Ticket {
  id: string
  ticket_number: string
  title: string
  description: string
  category_id: number | null
  priority: string
  status: string
  reporter_id: string
  assigned_to: string | null
  asset_id: string | null
  sla_due_at: string | null
  created_at: string
}

export interface Category {
  id: number
  name: string
}

export interface Comment {
  id: string
  author_id: string
  body: string
  is_internal: boolean
  created_at: string
}

export async function listTickets(params?: { status?: string; priority?: string }) {
  const { data } = await api.get<Ticket[]>('/api/tickets', { params })
  return data
}

export async function getTicket(id: string) {
  const { data } = await api.get<Ticket>(`/api/tickets/${id}`)
  return data
}

export async function createTicket(payload: {
  title: string
  description: string
  category_id: number | null
  priority: string
}) {
  const { data } = await api.post<Ticket>('/api/tickets', payload)
  return data
}

export async function updateStatus(id: string, status: string) {
  const { data } = await api.patch<Ticket>(`/api/tickets/${id}/status`, { status })
  return data
}

export async function getComments(id: string) {
  const { data } = await api.get<Comment[]>(`/api/tickets/${id}/comments`)
  return data
}

export async function addComment(id: string, body: string, is_internal = false) {
  const { data } = await api.post<Comment>(`/api/tickets/${id}/comments`, { body, is_internal })
  return data
}

export async function listCategories() {
  const { data } = await api.get<Category[]>('/api/categories')
  return data
}

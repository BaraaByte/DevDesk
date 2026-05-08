import { create } from 'zustand'

interface SystemStats {
  cpu: number
  ram: number
  ram_total: number
  disk: number
  disk_total: number
  disk_used: number
  timestamp: string
}

interface Note {
  id: string
  text: string
  createdAt: string
}

interface SystemStore {
  stats: SystemStats | null
  notes: Note[]
  theme: 'dark' | 'light'
  loading: boolean
  error: string | null
  setTheme: (theme: 'dark' | 'light') => void
  addNote: (text: string) => void
  removeNote: (id: string) => void
  updateStats: (stats: SystemStats) => void
  fetchStats: () => Promise<void>
  fetchNotes: () => Promise<void>
  saveNote: (text: string) => Promise<void>
  deleteNote: (id: string) => Promise<void>
}

// API base URL
const API_BASE = 'http://127.0.0.1:8000'

// API functions
const apiRequest = async (endpoint: string, options?: RequestInit) => {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`)
  }

  return response.json()
}

export const useSystemStore = create<SystemStore>((set, get) => ({
  stats: null,
  notes: [],
  theme: 'dark',
  loading: false,
  error: null,

  setTheme: (theme) => set({ theme }),

  addNote: (text) => {
    const note = { id: Date.now().toString(), text, createdAt: new Date().toISOString() }
    set((state) => ({ notes: [note, ...state.notes] }))
  },

  removeNote: (id) => set((state) => ({
    notes: state.notes.filter((note) => note.id !== id),
  })),

  updateStats: (stats) => set({ stats }),

  fetchStats: async () => {
    try {
      set({ loading: true, error: null })
      const stats = await apiRequest('/api/stats')
      set({ stats, loading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to fetch stats', loading: false })
    }
  },

  fetchNotes: async () => {
    try {
      set({ loading: true, error: null })
      const notes = await apiRequest('/api/notes')
      set({ notes, loading: false })
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to fetch notes', loading: false })
    }
  },

  saveNote: async (text: string) => {
    try {
      set({ loading: true, error: null })
      const newNote = await apiRequest('/api/notes', {
        method: 'POST',
        body: JSON.stringify({ text }),
      })
      set((state) => ({ notes: [newNote, ...state.notes], loading: false }))
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to save note', loading: false })
    }
  },

  deleteNote: async (id: string) => {
    try {
      set({ loading: true, error: null })
      await apiRequest(`/api/notes/${id}`, {
        method: 'DELETE',
      })
      set((state) => ({
        notes: state.notes.filter((note) => note.id !== id),
        loading: false
      }))
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to delete note', loading: false })
    }
  },
}))

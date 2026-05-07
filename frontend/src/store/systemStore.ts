import { create } from 'zustand'

interface SystemStats {
  cpu: number
  ram: number
  ram_total: number
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
  setTheme: (theme: 'dark' | 'light') => void
  addNote: (text: string) => void
  removeNote: (id: string) => void
  updateStats: (stats: SystemStats) => void
}

// Mock data generator
const generateMockStats = (): SystemStats => ({
  cpu: Math.floor(Math.random() * 80) + 10,
  ram: Math.floor(Math.random() * 8) + 2,
  ram_total: 16,
  timestamp: new Date().toISOString(),
})

export const useSystemStore = create<SystemStore>((set) => ({
  stats: generateMockStats(),
  notes: [
    { id: '1', text: 'Setup DevDesk project ✓', createdAt: new Date().toISOString() },
    { id: '2', text: 'Build modern frontend', createdAt: new Date().toISOString() },
  ],
  theme: 'dark',

  setTheme: (theme) => set({ theme }),

  addNote: (text) => set((state) => ({
    notes: [
      { id: Date.now().toString(), text, createdAt: new Date().toISOString() },
      ...state.notes,
    ],
  })),

  removeNote: (id) => set((state) => ({
    notes: state.notes.filter((note) => note.id !== id),
  })),

  updateStats: (stats) => set({ stats }),
}))

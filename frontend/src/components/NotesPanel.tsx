import { useState, useEffect, memo, useCallback } from 'react'
import styled from '@emotion/styled'
import { useSystemStore } from '../store/systemStore'
import { useDebounce } from '../hooks/useDebounce'

const Container = styled.div<{ isDark: boolean }>`
  background: ${props => props.isDark ? 'rgba(30, 30, 30, 0.8)' : 'rgba(255, 255, 255, 0.8)'};
  border: 1px solid ${props => props.isDark ? 'rgba(102, 255, 204, 0.2)' : 'rgba(102, 255, 204, 0.3)'};
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  height: 400px;
  transition: all 0.3s ease;

  &:hover {
    border-color: ${props => props.isDark ? 'rgba(102, 255, 204, 0.5)' : 'rgba(102, 255, 204, 0.6)'};
  }
`

const Header = styled.div`
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.7;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`

const AddButton = styled.button`
  background: linear-gradient(135deg, #66ffcc 0%, #66ff99 100%);
  border: none;
  color: #000;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 255, 204, 0.3);
  }
`

const InputContainer = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
`

const Input = styled.input<{ isDark: boolean }>`
  flex: 1;
  background: ${props => props.isDark ? 'rgba(0, 0, 0, 0.3)' : 'rgba(255, 255, 255, 0.5)'};
  border: 1px solid ${props => props.isDark ? 'rgba(102, 255, 204, 0.2)' : 'rgba(102, 255, 204, 0.3)'};
  border-radius: 6px;
  padding: 8px 12px;
  color: ${props => props.isDark ? '#fff' : '#000'};
  font-size: 13px;
  
  &:focus {
    outline: none;
    border-color: rgba(102, 255, 204, 0.6);
    box-shadow: 0 0 0 2px rgba(102, 255, 204, 0.1);
  }

  &::placeholder {
    opacity: 0.5;
  }
`

const NotesList = styled.div`
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;

  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(102, 255, 204, 0.3);
    border-radius: 3px;
  }
`

const NoteItem = styled.div<{ isDark: boolean }>`
  background: ${props => props.isDark ? 'rgba(0, 0, 0, 0.3)' : 'rgba(102, 255, 204, 0.1)'};
  border: 1px solid ${props => props.isDark ? 'rgba(102, 255, 204, 0.2)' : 'rgba(102, 255, 204, 0.3)'};
  border-radius: 8px;
  padding: 12px;
  font-size: 13px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.3s ease;

  &:hover {
    border-color: rgba(102, 255, 204, 0.5);
    background: ${props => props.isDark ? 'rgba(102, 255, 204, 0.05)' : 'rgba(102, 255, 204, 0.15)'};
  }
`

const NoteText = styled.div`
  flex: 1;
  word-break: break-word;
  line-height: 1.5;
`

const DeleteButton = styled.button`
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.3s ease;
  padding: 0;
  font-size: 16px;

  &:hover {
    opacity: 1;
  }
`

const EmptyState = styled.div`
  font-size: 13px;
  opacity: 0.5;
  text-align: center;
  padding: 40px 20px;
`

interface NotesPanelProps {
  isDark: boolean
}

const NotesPanel = memo(function NotesPanel({ isDark }: NotesPanelProps) {
  const notes = useSystemStore((state) => state.notes)
  const fetchNotes = useSystemStore((state) => state.fetchNotes)
  const saveNote = useSystemStore((state) => state.saveNote)
  const deleteNote = useSystemStore((state) => state.deleteNote)
  const [input, setInput] = useState('')

  // Fetch notes on mount
  useEffect(() => {
    fetchNotes()
  }, [fetchNotes])

  const handleAdd = useCallback(async () => {
    if (input.trim()) {
      await saveNote(input.trim())
      setInput('')
    }
  }, [input, saveNote])

  const handleDelete = useCallback(async (id: string) => {
    await deleteNote(id)
  }, [deleteNote])

  const debouncedHandleAdd = useDebounce(handleAdd, 300)

  return (
    <Container isDark={isDark}>
      <Header>
        Quick Notes
        <AddButton onClick={handleAdd}>+ Add</AddButton>
      </Header>
      <InputContainer>
        <Input
          isDark={isDark}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAdd()}
          placeholder="Add a note..."
        />
      </InputContainer>
      {notes.length > 0 ? (
        <NotesList>
          {notes.map((note) => (
            <NoteItem key={note.id} isDark={isDark}>
              <NoteText>{note.text}</NoteText>
              <DeleteButton onClick={() => handleDelete(note.id)}>✕</DeleteButton>
            </NoteItem>
          ))}
        </NotesList>
      ) : (
        <EmptyState>No notes yet. Add one above! 📝</EmptyState>
      )}
    </Container>
  )
})

export default NotesPanel

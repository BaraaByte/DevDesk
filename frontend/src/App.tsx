import { useState } from 'react'
import styled from '@emotion/styled'
import CPUMonitor from './components/CPUMonitor'
import RAMMonitor from './components/RAMMonitor'
import TimeDisplay from './components/TimeDisplay'
import NotesPanel from './components/NotesPanel'
import ThemeToggle from './components/ThemeToggle'
import { useSystemStore } from './store/systemStore'

const AppContainer = styled.div<{ isDark: boolean }>`
  width: 100vw;
  height: 100vh;
  background: ${props => props.isDark 
    ? 'linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)'
    : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)'};
  color: ${props => props.isDark ? '#ffffff' : '#000000'};
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  padding: 24px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: auto auto 1fr;
  grid-gap: 20px;
  transition: background 0.5s ease;
  overflow: hidden;
`

const Header = styled.div`
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
`

const Title = styled.h1`
  font-size: 32px;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #61dafb 0%, #35baf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
`

const StatsGrid = styled.div`
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
`

const NotesContainer = styled.div`
  grid-column: 1 / -1;
  grid-row: 3;
  max-height: 450px;
`

function App() {
  const [isDark, setIsDark] = useState(true)
  const theme = useSystemStore((state) => state.theme)
  const setTheme = useSystemStore((state) => state.setTheme)

  const handleThemeToggle = () => {
    const newTheme = isDark ? 'light' : 'dark'
    setIsDark(!isDark)
    setTheme(newTheme)
  }

  return (
    <AppContainer isDark={isDark}>
      <Header>
        <Title>⚡ DevDesk</Title>
        <ThemeToggle isDark={isDark} onToggle={handleThemeToggle} />
      </Header>

      <StatsGrid>
        <CPUMonitor isDark={isDark} />
        <RAMMonitor isDark={isDark} />
        <TimeDisplay isDark={isDark} />
      </StatsGrid>

      <NotesContainer>
        <NotesPanel isDark={isDark} />
      </NotesContainer>
    </AppContainer>
  )
}

export default App

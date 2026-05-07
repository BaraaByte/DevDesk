import styled from '@emotion/styled'

const Button = styled.button<{ isDark: boolean }>`
  background: ${props => props.isDark ? 'rgba(97, 218, 251, 0.1)' : 'rgba(255, 193, 7, 0.1)'};
  border: 1px solid ${props => props.isDark ? 'rgba(97, 218, 251, 0.3)' : 'rgba(255, 193, 7, 0.3)'};
  font-size: 20px;
  cursor: pointer;
  padding: 10px 14px;
  border-radius: 8px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    background: ${props => props.isDark ? 'rgba(97, 218, 251, 0.2)' : 'rgba(255, 193, 7, 0.2)'};
    border-color: ${props => props.isDark ? 'rgba(97, 218, 251, 0.5)' : 'rgba(255, 193, 7, 0.5)'};
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
`

interface ThemeToggleProps {
  isDark: boolean
  onToggle: () => void
}

export default function ThemeToggle({ isDark, onToggle }: ThemeToggleProps) {
  return (
    <Button isDark={isDark} onClick={onToggle} title="Toggle theme">
      {isDark ? '☀️' : '🌙'}
    </Button>
  )
}

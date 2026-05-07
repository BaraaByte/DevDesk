import { useState, useEffect } from 'react'
import styled from '@emotion/styled'

const Container = styled.div<{ isDark: boolean }>`
  background: ${props => props.isDark ? 'rgba(30, 30, 30, 0.8)' : 'rgba(255, 255, 255, 0.8)'};
  border: 1px solid ${props => props.isDark ? 'rgba(255, 193, 7, 0.2)' : 'rgba(255, 193, 7, 0.3)'};
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  transition: all 0.3s ease;

  &:hover {
    border-color: ${props => props.isDark ? 'rgba(255, 193, 7, 0.5)' : 'rgba(255, 193, 7, 0.6)'};
    box-shadow: 0 8px 32px ${props => props.isDark ? 'rgba(255, 193, 7, 0.1)' : 'rgba(255, 193, 7, 0.15)'};
  }
`

const Time = styled.div`
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 12px;
  font-family: 'Courier New', monospace;
  background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`

const DateText = styled.div`
  font-size: 13px;
  opacity: 0.7;
  letter-spacing: 0.5px;
`

interface TimeDisplayProps {
  isDark: boolean
}

export default function TimeDisplay({ isDark }: TimeDisplayProps) {
  const [time, setTime] = useState<string>('')
  const [date, setDate] = useState<string>('')

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setTime(now.toLocaleTimeString('en-US', { hour12: false }))
      setDate(now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }))
    }

    updateTime()
    const interval = setInterval(updateTime, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <Container isDark={isDark}>
      <Time>{time}</Time>
      <DateText>{date}</DateText>
    </Container>
  )
}

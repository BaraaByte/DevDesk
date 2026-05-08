import { useEffect } from 'react'
import styled from '@emotion/styled'
import { useSystemStore } from '../store/systemStore'

const Container = styled.div<{ isDark: boolean }>`
  background: ${props => props.isDark ? 'rgba(30, 30, 30, 0.8)' : 'rgba(255, 255, 255, 0.8)'};
  border: 1px solid ${props => props.isDark ? 'rgba(97, 218, 251, 0.2)' : 'rgba(97, 218, 251, 0.3)'};
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;

  &:hover {
    border-color: ${props => props.isDark ? 'rgba(97, 218, 251, 0.5)' : 'rgba(97, 218, 251, 0.6)'};
    box-shadow: 0 8px 32px ${props => props.isDark ? 'rgba(97, 218, 251, 0.1)' : 'rgba(97, 218, 251, 0.15)'};
  }
`

const Label = styled.div`
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.7;
  margin-bottom: 12px;
`

const Value = styled.div`
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #61dafb 0%, #35baf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`

const ProgressBar = styled.div<{ isDark: boolean }>`
  height: 4px;
  background: ${props => props.isDark ? 'rgba(97, 218, 251, 0.1)' : 'rgba(97, 218, 251, 0.2)'};
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
`

const ProgressFill = styled.div<{ percentage: number }>`
  height: 100%;
  width: ${props => props.percentage}%;
  background: linear-gradient(90deg, #61dafb 0%, #35baf6 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
`

const Status = styled.div`
  font-size: 11px;
  opacity: 0.6;
`

interface CPUMonitorProps {
  isDark: boolean
}

export default function CPUMonitor({ isDark }: CPUMonitorProps) {
  const stats = useSystemStore((state) => state.stats)
  const fetchStats = useSystemStore((state) => state.fetchStats)

  // Fetch real stats on mount and periodically
  useEffect(() => {
    fetchStats()
    const interval = setInterval(fetchStats, 2000)
    return () => clearInterval(interval)
  }, [fetchStats])

  const cpuPercentage = stats?.cpu || 0

  return (
    <Container isDark={isDark}>
      <Label>CPU Usage</Label>
      <Value>{cpuPercentage.toFixed(1)}%</Value>
      <ProgressBar isDark={isDark}>
        <ProgressFill percentage={cpuPercentage} />
      </ProgressBar>
      <Status>
        {cpuPercentage < 30 && '📈 Idle'}
        {cpuPercentage >= 30 && cpuPercentage < 60 && '⚡ Active'}
        {cpuPercentage >= 60 && cpuPercentage < 85 && '🔥 Heavy'}
        {cpuPercentage >= 85 && '🚨 Critical'}
      </Status>
    </Container>
  )
}

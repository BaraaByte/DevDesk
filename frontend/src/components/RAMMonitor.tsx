import { useEffect } from 'react'
import styled from '@emotion/styled'
import { useSystemStore } from '../store/systemStore'

const Container = styled.div<{ isDark: boolean }>`
  background: ${props => props.isDark ? 'rgba(30, 30, 30, 0.8)' : 'rgba(255, 255, 255, 0.8)'};
  border: 1px solid ${props => props.isDark ? 'rgba(168, 237, 234, 0.2)' : 'rgba(168, 237, 234, 0.3)'};
  border-radius: 12px;
  padding: 20px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;

  &:hover {
    border-color: ${props => props.isDark ? 'rgba(168, 237, 234, 0.5)' : 'rgba(168, 237, 234, 0.6)'};
    box-shadow: 0 8px 32px ${props => props.isDark ? 'rgba(168, 237, 234, 0.1)' : 'rgba(168, 237, 234, 0.15)'};
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
  margin-bottom: 8px;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`

const Details = styled.div`
  font-size: 13px;
  opacity: 0.7;
  margin-bottom: 16px;
`

const ProgressBar = styled.div<{ isDark: boolean }>`
  height: 4px;
  background: ${props => props.isDark ? 'rgba(168, 237, 234, 0.1)' : 'rgba(168, 237, 234, 0.2)'};
  border-radius: 2px;
  overflow: hidden;
`

const ProgressFill = styled.div<{ percentage: number }>`
  height: 100%;
  width: ${props => props.percentage}%;
  background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
  border-radius: 2px;
  transition: width 0.3s ease;
`

interface RAMMonitorProps {
  isDark: boolean
}

export default function RAMMonitor({ isDark }: RAMMonitorProps) {
  const stats = useSystemStore((state) => state.stats)
  const fetchStats = useSystemStore((state) => state.fetchStats)

  // Fetch real stats on mount and periodically
  useEffect(() => {
    fetchStats()
    const interval = setInterval(fetchStats, 2500)
    return () => clearInterval(interval)
  }, [fetchStats])

  const ramUsed = stats?.ram || 0
  const ramTotal = stats?.ram_total || 16
  const ramPercentage = (ramUsed / ramTotal) * 100

  return (
    <Container isDark={isDark}>
      <Label>RAM Usage</Label>
      <Value>{ramUsed.toFixed(1)} GB</Value>
      <Details>of {ramTotal.toFixed(1)} GB ({ramPercentage.toFixed(1)}%)</Details>
      <ProgressBar isDark={isDark}>
        <ProgressFill percentage={ramPercentage} />
      </ProgressBar>
    </Container>
  )
}

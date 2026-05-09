# DevDesk Development Guide

## Project Architecture Overview

```
Frontend (React) ←→ REST API ←→ Backend (Flask) ← → System APIs
     Vite               Polling           psutil
  TypeScript          Updates           Linux APIs
  Emotion CSS                          GitHub API
```

## Frontend Architecture

### Component Hierarchy
```
App (Main Dashboard)
├── Header
│   ├── Title
│   └── ThemeToggle
├── StatsGrid
│   ├── CPUMonitor
│   ├── RAMMonitor
│   └── TimeDisplay
└── NotesPanel
```

### State Management (Zustand)
```
useSystemStore
├── stats (System metrics)
├── loading (Loading state)
├── error (Error state)
└── fetchStats() (Action)
```

### Styling Approach
- **Emotion (CSS-in-JS)**: Dynamic, theme-aware styling
- **No external CSS frameworks**: Pure custom components
- **Theme switching**: Dark/Light mode via React state

## Backend Architecture

### API Endpoints

#### REST Endpoints
- `GET /health` - Health check
- `GET /api/stats` - Current system statistics
- `GET /api/info` - Static system information

#### WebSocket
- `WS /ws/stats` - Real-time stats streaming (500ms updates)

### System Monitoring
```
monitor.py (SystemMonitor)
├── get_stats() → CPU%, RAM usage, timestamp
├── get_system_info() → OS, CPU count, boot time
├── get_cpu_per_core() → Per-core usage
└── get_process_info() → Specific process metrics
```

### Data Flow
```
Frontend
  ↓ (fetch on mount)
Backend /api/stats
  ↓ (psutil calls)
System kernel (/proc)
  ↓ (response)
Frontend update store
  ↓ (re-render)
UI update
```

## Key Technologies & Why

### Frontend
| Tech | Why | Alternative |
|------|-----|-------------|
| React | Popular, component-based, great tooling | Vue, Svelte |
| Vite | Lightning fast builds, ES modules | Webpack, Parcel |
| TypeScript | Type safety, better DX | JavaScript |
| Zustand | Lightweight state, no boilerplate | Redux, Recoil |
| Emotion | Dynamic theming, CSS-in-JS | Styled-components, Tailwind |

### Backend
| Tech | Why | Alternative |
|------|-----|-------------|
| Flask | Lightweight, familiar, easy to extend | FastAPI, Django |
| psutil | Cross-platform system info | Reading /proc directly |
| SQLAlchemy | ORM for SQLite storage | Raw SQL, Peewee |
| Polling | Simple, reliable backend updates | WebSockets, SSE |

## Performance Considerations

### Frontend
- ✅ Component memoization for large lists
- ✅ CSS-in-JS with emotion (scoped styles)
- ✅ Lazy loading plugins
- ⚠️ Monitor bundle size (target < 200KB)

### Backend
- ✅ Async/await for non-blocking I/O
- ✅ WebSocket for efficient updates (vs polling)
- ✅ Connection pooling for external APIs
- ⚠️ CPU polling interval: 100ms (trade-off: accuracy vs load)

## System Integration Points

### Linux Integration
1. **Process filesystem** (`/proc/stat`, `/proc/meminfo`)
   - psutil abstracts away; direct access possible
   - No root required for basic stats

2. **D-Bus** (for future music controls)
   - System service API
   - Control media players, get notifications

3. **Environment** (for system info)
   - `$HOME`, `$USER`, `$DISPLAY`
   - Terminal integration via PTY

### GitHub Integration (Future)
- OAuth 2.0 for authentication
- REST API for repo/PR data
- GraphQL for complex queries

## Database Considerations

### Current (MVP)
- ✅ No database needed
- ✅ Notes stored in localStorage
- ✅ System stats are real-time only

### Future
- Optional SQLite for stats history
- IndexedDB for browser-side caching
- User preferences in database

## Testing Strategy

### Frontend
```bash
npm run test  # Jest + React Testing Library
```

### Backend
```bash
pytest tests/  # pytest backend suite
```

## Deployment

### Development
```bash
# Terminal 1 - Backend
cd backend && python app.py

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

### Production
```bash
# Backend
gunicorn -w 4 app:app

# Frontend
npm run build  # Creates dist/ folder
# Serve dist/ via nginx or similar
```

## Debugging Tips

### Frontend
- React DevTools Chrome extension
- Browser DevTools (Network, Console)
- Zustand DevTools for state inspection

### Backend
- Flask development server logs
- Python debugger: `import pdb; pdb.set_trace()`
- Use `flask shell` or `python app.py` for debugging

## File Organization

### Adding a New Feature

1. **Frontend Component**
   ```
   src/components/NewWidget.tsx
   ```

2. **Backend Endpoint**
   ```
   backend/new_module.py
   Update backend/app.py or backend/routes.py with @app.route()
   ```

3. **Type Safety**
   ```
   src/types/new.ts (Frontend)
   src/models.py → NewModel (Backend)
   ```

4. **Styling**
   ```
   Use styled from '@emotion/styled' in component
   No separate CSS files needed
   ```

## Common Tasks

### Add a New Monitor
1. Add method to `SystemMonitor` class
2. Add endpoint in `main.py`
3. Create React component in `src/components/`
4. Add to UI in `App.tsx`

### Change Update Frequency
- Frontend: Modify interval in `useEffect` of component
- WebSocket: Change `asyncio.sleep()` value in `/ws/stats`

### Add a New Theme
- Modify theme colors in component `styled` definitions
- Connect to global theme state (future enhancement)

## Next Steps for Development

1. Add authentication (JWT tokens)
2. Implement plugin system
3. Add GitHub integration
4. Create terminal widget
5. Build analytics dashboard
6. Docker containerization
7. Deployment to cloud platform

---

**Questions?** Check existing code, open an issue, or ask in discussions!

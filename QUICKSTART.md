# Quick Start Guide

## 🚀 Get DevDesk Running in 5 Minutes

### Option 1: Automated Setup (Recommended)

```bash
cd devdesk
chmod +x setup.sh
./setup.sh
```

Then follow the instructions at the end.

### Option 2: Manual Setup

#### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python app.py
```

Backend will be available at: `http://localhost:8000`

#### 2. Frontend Setup (new terminal)
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### 3. Access the Dashboard

Open your browser and go to: **http://localhost:5173**

---

## 📊 What You'll See (MVP v1.0)

✅ **CPU Usage** - Real-time CPU percentage with visual progress bar
✅ **RAM Usage** - Memory usage in GB with percentage
✅ **Current Time** - Live clock showing system time
✅ **Quick Notes** - Text area for jotting down ideas (auto-saved to localStorage)
✅ **Theme Toggle** - Switch between dark and light themes

---

## 🔌 API Endpoints

All API requests go to: `http://localhost:8000`

### Health Check
```bash
curl http://localhost:8000/health
```

### Get System Stats
```bash
curl http://localhost:8000/api/stats
```

Response:
```json
{
  "cpu": 45.2,
  "ram": 8.5,
  "ram_total": 16.0,
  "timestamp": "2026-05-07T14:32:45.123456"
}
```

### Real-Time Stats (WebSocket)
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/stats');
ws.onmessage = (event) => {
  const stats = JSON.parse(event.data);
  console.log('CPU:', stats.cpu, '%');
};
```

---

## 🛠️ Common Commands

### Frontend
```bash
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run type-check  # Check TypeScript
```

### Backend
```bash
python app.py              # Run backend server
```

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=8001 python app.py
```

### "Port 5173 already in use"
```bash
# Use a different port
npm run dev -- --port 5174
```

### "psutil not installed"
```bash
cd backend
source venv/bin/activate
pip install psutil
```

### WebSocket connection refused
- Make sure both frontend and backend are running
- Check firewall settings
- Verify no proxy is blocking WebSocket

---

## 📁 Project Structure Reference

```
devdesk/
├── frontend/           # React + Vite app
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── store/       # Zustand store
│   │   ├── styles/      # CSS
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/            # Flask server
│   ├── app.py           # Flask app entry point
│   ├── models.py        # Database models and ORM
│   ├── routes.py        # API route definitions
│   ├── config.py        # Configuration and CORS settings
│   ├── utils.py         # System monitoring helpers
│   └── requirements.txt
├── plugins/            # Plugin examples
├── screenshots/        # App screenshots
├── README.md
└── setup.sh
```

---

## 🚀 Next Steps

1. **Add a new widget** → See DEVELOPMENT.md
2. **Create a plugin** → See plugins/PLUGIN_GUIDE.md
3. **Deploy to cloud** → Coming soon!
4. **Contribute** → See CONTRIBUTING.md

---

## 💡 Pro Tips

- **Auto-save notes**: Your notes are saved to browser localStorage instantly
- **Dark mode**: Click the theme toggle (☀️/🌙) in the top right
- **API testing**: Visit http://localhost:8000/docs for interactive API explorer
- **Real-time updates**: Stats update every 500ms via WebSocket
- **No database needed**: MVP uses only in-memory data and browser storage

---

**Happy coding! 🎉**

Questions? Open an issue on GitHub!

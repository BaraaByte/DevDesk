# DevDesk Backend

Modern Flask API backend for DevDesk system monitoring dashboard.

## Architecture

```
backend/
├── app.py              # Flask application factory
├── config.py           # Environment configuration
├── models.py           # SQLAlchemy database models
├── routes.py           # API endpoints (blueprints)
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── devdesk.db         # SQLite database (auto-created)
```

## Features

- **Modern Flask Setup** with blueprints and app factory pattern
- **SQLite Database** with SQLAlchemy ORM
- **CORS Enabled** for frontend integration
- **System Monitoring** API endpoints:
  - `GET /api/health` - Health check
  - `GET /api/stats/current` - Real-time system stats
  - `GET /api/stats/history` - Historical statistics
  - `GET /api/stats/summary` - Hourly summary stats
  - `GET /api/logs` - System event logs
  - `POST /api/logs` - Create event log

## Database Models

### SystemStats
- Stores CPU, RAM, and Disk usage metrics
- Timestamped entries for historical tracking
- Auto-converts to JSON format

### SystemLog
- Event logging (high_cpu, high_ram, etc.)
- Severity levels: info, warning, critical
- Queryable by event type or severity

## Setup & Run

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run development server
python app.py

# Server runs on http://localhost:8000
# API available at http://localhost:8000/api
```

## Configuration

Environment-based config in `config.py`:
- **Development**: Debug enabled, SQLite in memory
- **Testing**: Testing mode with in-memory DB
- **Production**: Requires SECRET_KEY env variable

Edit `.env` to customize settings.

## API Usage

### Get Current Stats
```bash
curl http://localhost:8000/api/stats/current
```

Response:
```json
{
  "cpu": 45.2,
  "ram": 8.5,
  "ram_total": 16,
  "ram_percent": 53.1,
  "disk": 62.4,
  "disk_used": 500.0,
  "disk_total": 800.0,
  "timestamp": "2026-05-07T22:36:45.123456"
}
```

### Get Stats Summary (Last Hour)
```bash
curl http://localhost:8000/api/stats/summary
```

Response:
```json
{
  "avg_cpu": 42.5,
  "avg_ram": 50.3,
  "peak_cpu": 78.9,
  "peak_ram": 65.2,
  "sample_count": 60
}
```

## Development

- Uses Flask 3.0 with SQLAlchemy 2.0
- Automatic database initialization
- Exception handling with proper HTTP status codes
- Type hints ready for enhancement
- Easy to extend with more models and routes

## Next Steps

- [ ] Add authentication/JWT
- [ ] Add database migrations (Alembic)
- [ ] Add more system metrics (network, processes)
- [ ] Add alerting system
- [ ] Add frontend integration

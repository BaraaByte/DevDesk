# DevDesk Backend

Modern Flask API backend for DevDesk system monitoring dashboard.

## Features

- **System Monitoring**: Real-time CPU, RAM, and Disk usage
- **Notes API**: CRUD operations for quick notes
- **Tasks API**: Task management (extensible)
- **SQLite Database**: Simple, file-based database
- **CORS Enabled**: Ready for frontend integration
- **Modular Architecture**: Easy to extend with new features
- **Health Check**: API status monitoring
- **Environment Configuration**: Development/Production support

## Project Structure

```
backend/
├── app.py              # Flask app factory and entry point
├── config.py           # Configuration management
├── models.py           # Database models (Note, Task)
├── routes.py           # API routes and blueprints
├── utils.py            # Helper functions (system stats)
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── devdesk_dev.db     # SQLite database (auto-created)
```

## Architecture

### Modular Design
- **app.py**: Application factory pattern for easy configuration
- **config.py**: Centralized configuration for different environments
- **models.py**: SQLAlchemy models for database tables
- **routes.py**: API routes organized with Flask blueprints
- **utils.py**: Reusable utility functions for system monitoring

### Expandability
The modular structure makes it easy to add:
- New API endpoints (add to `routes.py`)
- New database models (add to `models.py`)
- New utility functions (add to `utils.py`)
- New features like GitHub activity, weather, music controls, plugins

## API Endpoints

### System Stats
- `GET /api/stats` - Get current system statistics
  ```json
  {
    "cpu": 5.2,
    "ram": 4.4,
    "ram_total": 14.9,
    "disk": 69.4,
    "disk_used": 25.7,
    "disk_total": 39.1,
    "timestamp": "2026-05-08T17:49:39.230289"
  }
  ```

### Notes
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
  ```json
  {
    "text": "My note"
  }
  ```
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note

### Tasks
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- (PUT/DELETE endpoints coming soon)

### Health
- `GET /api/health` - Health check
- `GET /` - API info and available endpoints

## Setup & Run

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Create Virtual Environment**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```bash
   python app.py
   ```

   The API will be available at `http://127.0.0.1:8000`

### Configuration

Edit `.env` file to configure:
- `FLASK_ENV`: development/production/testing
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Custom database URL (optional)

### Using the API

```bash
# Get system stats
curl http://127.0.0.1:8000/api/stats

# List notes
curl http://127.0.0.1:8000/api/notes

# Create a note
curl -X POST http://127.0.0.1:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"text":"My important note"}'

# Delete a note
curl -X DELETE http://127.0.0.1:8000/api/notes/1
```

## Development

### Database Management
- Database is automatically created on first run
- SQLite file: `devdesk_dev.db`
- Use Flask shell for database management:
  ```bash
  flask shell
  >>> from models import db, Note
  >>> Note.query.all()
  ```

### Adding New Endpoints

1. Create a model in `models.py`
2. Add routes in `routes.py`
3. Use utilities from `utils.py` if needed
4. Update this README

### Example: Adding a New Feature

```python
# 1. Add model in models.py
class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # ...

# 2. Add routes in routes.py
@api_bp.route('/features', methods=['GET'])
def list_features():
    features = Feature.query.all()
    return jsonify([f.to_dict() for f in features])
```

## Dependencies

- **Flask 3.0.0**: Web framework
- **Flask-SQLAlchemy 3.1.1**: ORM and database management
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **psutil 5.9.6**: System and process utilities
- **python-dotenv 1.0.0**: Environment variable management

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Change port
```

### Database Errors
Delete `devdesk_dev.db` to reset:
```bash
rm devdesk_dev.db
python app.py  # Will recreate on startup
```

### CORS Issues
Check that frontend URL is in `CORS_ORIGINS` in `config.py`

## v1.0 Status

✅ Complete:
- System monitoring (CPU, RAM, Disk)
- Notes CRUD operations
- Task model foundation
- Modular architecture
- Environment configuration
- CORS support
- Error handling

🚀 Future Features:
- GitHub activity integration
- Weather information
- Music player controls
- Plugin system
- Custom themes
- Real-time notifications

pip install -r requirements.txt

# Run the server
python app.py

# Server runs on http://localhost:8000
```

## Database

The app automatically creates `devdesk.db` SQLite database with a `notes` table.

## Example API Usage

```bash
# Get system stats
curl http://localhost:8000/api/stats

# Get notes
curl http://localhost:8000/api/notes

# Create note
curl -X POST http://localhost:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello DevDesk!"}'
```

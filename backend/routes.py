"""API routes for DevDesk"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Note, Task
from utils import get_system_stats

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')


def register_routes(app):
    """Register all routes with the app"""
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'name': app.config.get('API_NAME', 'DevDesk API'),
            'version': app.config.get('API_VERSION', '1.0.0'),
            'status': 'running',
            'endpoints': {
                'health': '/api/health',
                'stats': '/api/stats',
                'notes': '/api/notes',
                'tasks': '/api/tasks',
            }
        })

    @api_bp.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat()
        })

    # ==================== STATS ENDPOINTS ====================

    @api_bp.route('/stats', methods=['GET'])
    def get_stats():
        """Get current system statistics"""
        try:
            stats = get_system_stats()
            stats['timestamp'] = datetime.utcnow().isoformat()
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ==================== NOTES ENDPOINTS ====================

    @api_bp.route('/notes', methods=['GET'])
    def list_notes():
        """Get all notes"""
        try:
            notes = Note.query.order_by(Note.created_at.desc()).all()
            return jsonify([note.to_dict() for note in notes])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @api_bp.route('/notes', methods=['POST'])
    def create_note():
        """Create a new note"""
        try:
            data = request.get_json()
            if not data or 'text' not in data:
                return jsonify({'error': 'Note text is required'}), 400

            if not data['text'].strip():
                return jsonify({'error': 'Note text cannot be empty'}), 400

            note = Note(text=data['text'].strip())
            from models import db
            db.session.add(note)
            db.session.commit()

            return jsonify(note.to_dict()), 201

        except Exception as e:
            from models import db
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @api_bp.route('/notes/<int:note_id>', methods=['GET'])
    def get_note(note_id):
        """Get a specific note"""
        try:
            note = Note.query.get_or_404(note_id)
            return jsonify(note.to_dict())
        except Exception as e:
            return jsonify({'error': str(e)}), 404

    @api_bp.route('/notes/<int:note_id>', methods=['PUT'])
    def update_note(note_id):
        """Update a note"""
        try:
            note = Note.query.get_or_404(note_id)
            data = request.get_json()

            if 'text' in data:
                if not data['text'].strip():
                    return jsonify({'error': 'Note text cannot be empty'}), 400
                note.text = data['text'].strip()

            from models import db
            db.session.commit()
            return jsonify(note.to_dict())

        except Exception as e:
            from models import db
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @api_bp.route('/notes/<int:note_id>', methods=['DELETE'])
    def delete_note(note_id):
        """Delete a note"""
        try:
            note = Note.query.get_or_404(note_id)
            from models import db
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'Note deleted', 'id': note_id}), 200

        except Exception as e:
            from models import db
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # ==================== TASKS ENDPOINTS (Future) ====================

    @api_bp.route('/tasks', methods=['GET'])
    def list_tasks():
        """Get all tasks"""
        try:
            tasks = Task.query.order_by(Task.created_at.desc()).all()
            return jsonify([task.to_dict() for task in tasks])
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @api_bp.route('/tasks', methods=['POST'])
    def create_task():
        """Create a new task"""
        try:
            data = request.get_json()
            if not data or 'title' not in data:
                return jsonify({'error': 'Task title is required'}), 400

            task = Task(
                title=data['title'].strip(),
                description=data.get('description', '').strip()
            )
            from models import db
            db.session.add(task)
            db.session.commit()

            return jsonify(task.to_dict()), 201

        except Exception as e:
            from models import db
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    # Register blueprint
    app.register_blueprint(api_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

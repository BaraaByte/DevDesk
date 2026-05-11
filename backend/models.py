"""Database models for DevDesk"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Note(db.Model):
    """Notes model for storing user notes"""
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f'<Note {self.id}: {self.text[:20]}...>'


class Task(db.Model):
    """Enhanced tasks model for modern task management"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False, index=True)
    priority = db.Column(db.String(20), default='medium', index=True)  # low, medium, high, urgent
    category = db.Column(db.String(50), default='general', index=True)  # work, personal, etc.
    due_date = db.Column(db.DateTime)
    tags = db.Column(db.Text)  # JSON string of tags
    order = db.Column(db.Integer, default=0)  # For drag-and-drop ordering
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags.split(',') if self.tags else [],
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
        

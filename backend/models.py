"""Database models for DevDesk"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SystemStats(db.Model):
    """System statistics model"""
    __tablename__ = 'system_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    cpu_percent = db.Column(db.Float, nullable=False, default=0.0)
    ram_percent = db.Column(db.Float, nullable=False, default=0.0)
    ram_used_mb = db.Column(db.Float, nullable=False, default=0.0)
    ram_total_mb = db.Column(db.Float, nullable=False, default=0.0)
    disk_percent = db.Column(db.Float, nullable=False, default=0.0)
    disk_used_gb = db.Column(db.Float, nullable=False, default=0.0)
    disk_total_gb = db.Column(db.Float, nullable=False, default=0.0)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'cpu': self.cpu_percent,
            'ram': round(self.ram_used_mb / 1024, 1),  # Convert to GB
            'ram_total': round(self.ram_total_mb / 1024, 1),
            'ram_percent': self.ram_percent,
            'disk': self.disk_percent,
            'disk_used': round(self.disk_used_gb, 1),
            'disk_total': round(self.disk_total_gb, 1),
            'timestamp': self.timestamp.isoformat(),
        }
    
    def __repr__(self):
        return f'<SystemStats {self.timestamp} - CPU: {self.cpu_percent}% RAM: {self.ram_percent}%>'

class SystemLog(db.Model):
    """System event log"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # 'high_cpu', 'high_ram', etc.
    message = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default='info')  # info, warning, critical
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'event_type': self.event_type,
            'message': self.message,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat(),
        }
    
    def __repr__(self):
        return f'<SystemLog {self.severity.upper()} - {self.event_type}>'

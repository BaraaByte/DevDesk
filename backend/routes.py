"""API routes for DevDesk"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import psutil
from models import db, SystemStats, SystemLog

api_bp = Blueprint('api', __name__, url_prefix='/api')

def get_system_stats():
    """Gather current system statistics"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory
        memory = psutil.virtual_memory()
        ram_percent = memory.percent
        ram_used_mb = memory.used / (1024 * 1024)
        ram_total_mb = memory.total / (1024 * 1024)
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024 ** 3)
        disk_total_gb = disk.total / (1024 ** 3)
        
        return {
            'cpu_percent': cpu_percent,
            'ram_percent': ram_percent,
            'ram_used_mb': ram_used_mb,
            'ram_total_mb': ram_total_mb,
            'disk_percent': disk_percent,
            'disk_used_gb': disk_used_gb,
            'disk_total_gb': disk_total_gb,
        }
    except Exception as e:
        print(f"Error gathering system stats: {e}")
        return None

@api_bp.route('/stats/current', methods=['GET'])
def get_current_stats():
    """Get current system statistics"""
    stats = get_system_stats()
    
    if not stats:
        return jsonify({'error': 'Failed to gather system stats'}), 500
    
    # Save to database
    try:
        stat_entry = SystemStats(
            cpu_percent=stats['cpu_percent'],
            ram_percent=stats['ram_percent'],
            ram_used_mb=stats['ram_used_mb'],
            ram_total_mb=stats['ram_total_mb'],
            disk_percent=stats['disk_percent'],
            disk_used_gb=stats['disk_used_gb'],
            disk_total_gb=stats['disk_total_gb'],
        )
        db.session.add(stat_entry)
        db.session.commit()
    except Exception as e:
        print(f"Error saving stats to database: {e}")
        db.session.rollback()
    
    # Return formatted response
    return jsonify({
        'cpu': stats['cpu_percent'],
        'ram': round(stats['ram_used_mb'] / 1024, 1),
        'ram_total': round(stats['ram_total_mb'] / 1024, 1),
        'ram_percent': stats['ram_percent'],
        'disk': stats['disk_percent'],
        'disk_used': round(stats['disk_used_gb'], 1),
        'disk_total': round(stats['disk_total_gb'], 1),
        'timestamp': datetime.utcnow().isoformat(),
    })

@api_bp.route('/stats/history', methods=['GET'])
def get_stats_history():
    """Get historical system statistics"""
    limit = request.args.get('limit', 100, type=int)
    
    try:
        stats = SystemStats.query.order_by(SystemStats.timestamp.desc()).limit(limit).all()
        return jsonify([stat.to_dict() for stat in reversed(stats)])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats/summary', methods=['GET'])
def get_stats_summary():
    """Get summary statistics for the last hour"""
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    
    try:
        stats = SystemStats.query.filter(
            SystemStats.timestamp >= one_hour_ago
        ).all()
        
        if not stats:
            return jsonify({
                'avg_cpu': 0,
                'avg_ram': 0,
                'peak_cpu': 0,
                'peak_ram': 0,
                'sample_count': 0,
            })
        
        cpu_values = [s.cpu_percent for s in stats]
        ram_values = [s.ram_percent for s in stats]
        
        return jsonify({
            'avg_cpu': round(sum(cpu_values) / len(cpu_values), 1),
            'avg_ram': round(sum(ram_values) / len(ram_values), 1),
            'peak_cpu': round(max(cpu_values), 1),
            'peak_ram': round(max(ram_values), 1),
            'sample_count': len(stats),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/logs', methods=['GET'])
def get_logs():
    """Get system event logs"""
    limit = request.args.get('limit', 50, type=int)
    severity = request.args.get('severity')  # optional filter
    
    try:
        query = SystemLog.query.order_by(SystemLog.timestamp.desc())
        if severity:
            query = query.filter_by(severity=severity)
        logs = query.limit(limit).all()
        
        return jsonify([log.to_dict() for log in reversed(logs)])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/logs', methods=['POST'])
def create_log():
    """Create a system event log"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['event_type', 'message', 'severity']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        log = SystemLog(
            event_type=data['event_type'],
            message=data['message'],
            severity=data['severity'],
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(log.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
    })

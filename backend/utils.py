"""Utility functions for DevDesk Backend"""
import psutil
from typing import Dict, Any


def get_system_stats() -> Dict[str, Any]:
    """
    Collect current system statistics
    
    Returns:
        Dictionary with CPU, RAM, and Disk information in flat structure
    """
    try:
        # CPU usage (%)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # CPU count
        cpu_count = psutil.cpu_count(logical=True)
        
        # Memory usage
        memory = psutil.virtual_memory()
        ram_used = round(memory.used / (1024**3), 1)  # GB
        ram_total = round(memory.total / (1024**3), 1)  # GB
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_used = round(disk.used / (1024**3), 1)  # GB
        disk_total = round(disk.total / (1024**3), 1)  # GB
        
        return {
            'cpu': cpu_percent,
            'ram': ram_used,
            'ram_total': ram_total,
            'disk': disk.percent,
            'disk_used': disk_used,
            'disk_total': disk_total,
        }
    except Exception as e:
        return {'error': str(e)}


def get_cpu_stats() -> Dict[str, Any]:
    """Get detailed CPU statistics"""
    try:
        return {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(logical=True),
            'freq': psutil.cpu_freq().current,
        }
    except Exception as e:
        return {'error': str(e)}


def get_memory_stats() -> Dict[str, Any]:
    """Get detailed memory statistics"""
    try:
        memory = psutil.virtual_memory()
        return {
            'used': round(memory.used / (1024**3), 1),
            'total': round(memory.total / (1024**3), 1),
            'available': round(memory.available / (1024**3), 1),
            'percent': memory.percent,
            'free': round(memory.free / (1024**3), 1),
        }
    except Exception as e:
        return {'error': str(e)}


def get_disk_stats() -> Dict[str, Any]:
    """Get detailed disk statistics"""
    try:
        disk = psutil.disk_usage('/')
        return {
            'used': round(disk.used / (1024**3), 1),
            'total': round(disk.total / (1024**3), 1),
            'free': round(disk.free / (1024**3), 1),
            'percent': disk.percent,
        }
    except Exception as e:
        return {'error': str(e)}


def get_process_stats() -> Dict[str, Any]:
    """Get process statistics"""
    try:
        return {
            'total': len(psutil.pids()),
            'running': len([p for p in psutil.process_iter(['status']) if p.info['status'] == 'running']),
        }
    except Exception as e:
        return {'error': str(e)}

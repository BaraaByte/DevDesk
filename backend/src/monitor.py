"""
System monitoring module using psutil
Collects CPU, RAM, and other system metrics
"""

import psutil
from datetime import datetime
from typing import Dict, Any


class SystemMonitor:
    """Monitor system resources like CPU and memory"""
    
    def __init__(self):
        """Initialize the system monitor"""
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get current system statistics
        
        Returns:
            dict: Contains cpu (%), ram (GB), ram_total (GB), timestamp
        """
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        ram_gb = memory.used / (1024 ** 3)
        ram_total_gb = memory.total / (1024 ** 3)
        
        return {
            "cpu": float(cpu_percent),
            "ram": float(ram_gb),
            "ram_total": float(ram_total_gb),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get static system information
        
        Returns:
            dict: System info (OS, CPU count, etc.)
        """
        return {
            "os": f"{psutil.system()}: {psutil.release()}",
            "cpu_count": psutil.cpu_count(),
            "boot_time": self.boot_time.isoformat(),
            "ram_total_gb": psutil.virtual_memory().total / (1024 ** 3),
        }
    
    def get_cpu_per_core(self) -> Dict[str, Any]:
        """
        Get CPU usage per core
        
        Returns:
            dict: Per-core CPU percentages
        """
        per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        return {
            f"core_{i}": float(usage) 
            for i, usage in enumerate(per_core)
        }
    
    def get_process_info(self, pid: int) -> Dict[str, Any]:
        """
        Get information about a specific process
        
        Args:
            pid: Process ID
            
        Returns:
            dict: Process information (name, memory, CPU usage)
        """
        try:
            process = psutil.Process(pid)
            return {
                "pid": pid,
                "name": process.name(),
                "cpu_percent": float(process.cpu_percent(interval=0.1)),
                "memory_mb": float(process.memory_info().rss / (1024 ** 2)),
            }
        except psutil.NoSuchProcess:
            return {"error": f"Process {pid} not found"}

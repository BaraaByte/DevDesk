"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StatsResponse(BaseModel):
    """System statistics response model"""
    cpu: float  # CPU usage percentage (0-100)
    ram: float  # RAM usage in GB
    ram_total: float  # Total RAM in GB
    timestamp: str  # ISO format timestamp
    
    class Config:
        json_schema_extra = {
            "example": {
                "cpu": 45.2,
                "ram": 8.5,
                "ram_total": 16.0,
                "timestamp": "2026-05-07T14:32:45.123456"
            }
        }


class SystemInfo(BaseModel):
    """Static system information"""
    os: str
    cpu_count: int
    boot_time: str
    ram_total_gb: float


class ProcessInfo(BaseModel):
    """Process information"""
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float

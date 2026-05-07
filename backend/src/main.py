"""
DevDesk Backend - FastAPI Server
Provides system monitoring and API endpoints for the frontend dashboard
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime

from src.monitor import SystemMonitor
from src.models import StatsResponse

# Initialize FastAPI app
app = FastAPI(
    title="DevDesk API",
    description="Backend API for DevDesk Dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize system monitor
monitor = SystemMonitor()


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/stats", response_model=StatsResponse, tags=["stats"])
async def get_stats():
    """
    Get current system statistics
    Returns: CPU usage (%), RAM usage (GB), RAM total (GB), timestamp
    """
    stats = monitor.get_stats()
    return StatsResponse(**stats)


@app.websocket("/ws/stats")
async def websocket_stats(websocket: WebSocket):
    """
    WebSocket endpoint for real-time system statistics streaming
    Sends updates every 500ms
    """
    await websocket.accept()
    try:
        while True:
            stats = monitor.get_stats()
            await websocket.send_json(stats)
            await asyncio.sleep(0.5)  # Update every 500ms
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


@app.get("/api/info", tags=["system"])
async def get_system_info():
    """Get static system information"""
    return monitor.get_system_info()


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    print("🚀 DevDesk API starting...")
    print("📊 System Monitor initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    print("🛑 DevDesk API shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

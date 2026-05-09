"""Performance monitoring middleware for DevDesk Backend"""
import time
import logging
from flask import request, g

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMiddleware:
    """Middleware to monitor API response times and log performance metrics"""
    
    def __init__(self, app):
        self.app = app
        self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Store request start time"""
        g.start_time = time.time()
    
    def after_request(self, response):
        """Log request duration and performance metrics"""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # Log slow requests (> 500ms)
            if duration > 0.5:
                logger.warning(
                    f"Slow request: {request.method} {request.path} "
                    f"took {duration:.3f}s - Status: {response.status_code}"
                )
            else:
                logger.info(
                    f"Request: {request.method} {request.path} "
                    f"took {duration:.3f}s - Status: {response.status_code}"
                )
        
        return response

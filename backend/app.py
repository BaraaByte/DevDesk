"""DevDesk Backend - Modern Flask API"""
import os
from flask import Flask
from flask_cors import CORS
from config import config, CONFIG_MAP
from models import db
from routes import register_routes


def create_app(config_name=None):
    """
    Application factory
    
    Args:
        config_name: Configuration name (development, production, testing)
                    If None, uses FLASK_ENV environment variable
    
    Returns:
        Flask app instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app_config = CONFIG_MAP.get(config_name, CONFIG_MAP['development'])
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(app_config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register routes
    register_routes(app)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8000, debug=app.config['DEBUG'])
    app.run(debug=True, host='127.0.0.1', port=8000)
"""
Flask Application Package

This package contains the Flask application and related modules.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from flask import Flask
import os
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'production')
    
    if config_name == 'development':
        app.config.from_object('config.development.DevelopmentConfig')
    elif config_name == 'staging':
        app.config.from_object('config.staging.StagingConfig')
    else:
        app.config.from_object('config.production.ProductionConfig')
    
    # Setup logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/flask_app.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask application startup')
    
    # Register blueprints (if using blueprints)
    # from .main import bp as main_bp
    # app.register_blueprint(main_bp)
    
    return app

"""
import os
from datetime import timedelta

class StagingConfig:
    \"\"\"Staging configuration.\"\"\"
    
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'staging-secret-key'
    DEBUG = False
    TESTING = False
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://user:pass@localhost/flask_app_staging'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 20
    }
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://redis:6379/1'
    
    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Session configuration
    SESSION_TYPE = 'redis'
    SESSION_REDIS = REDIS_URL
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_app_staging:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    
    # Security configuration (relaxed for staging)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # API configuration (more permissive for testing)
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "2000 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Logging configuration (more verbose)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    LOG_FILE = '/var/log/flask_app/staging.log'
    LOG_MAX_BYTES = 50 * 1024 * 1024  # 50MB
    LOG_BACKUP_COUNT = 5
    
    # Email configuration (using test email service)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.mailtrap.io')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 2525))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'staging@example.com')
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB (larger for testing)
    UPLOAD_FOLDER = '/tmp/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'json', 'xml'}
    
    # API external services (with mock endpoints)
    EXTERNAL_API_TIMEOUT = 10
    EXTERNAL_API_RETRIES = 2
    USE_MOCK_SERVICES = True
    
    # Monitoring and metrics
    PROMETHEUS_METRICS = True
    HEALTH_CHECK_TIMEOUT = 3
    
    # Performance settings (development-friendly)
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Testing features
    ENABLE_DEBUG_TOOLBAR = os.environ.get('ENABLE_DEBUG_TOOLBAR', 'false').lower() == 'true'
    TESTING_DATABASE_RESET = True
    MOCK_EXTERNAL_APIS = True
    
    # Backup configuration (disabled in staging)
    BACKUP_ENABLED = False
    
    # Error handling (show more details)
    PROPAGATE_EXCEPTIONS = True
    
    @staticmethod
    def init_app(app):
        \"\"\"Initialize application with staging-specific settings.\"\"\"
        
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Console handler for staging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s: %(message)s'
        ))
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
        
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Flask application startup - Development mode')
        
        # Enable debug toolbar
        if DevelopmentConfig.FLASK_DEBUG_TOOLBAR:
            try:
                from flask_debugtoolbar import DebugToolbarExtension
                app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
                toolbar = DebugToolbarExtension(app)
                app.logger.info('Debug toolbar enabled')
            except ImportError:
                app.logger.warning('Debug toolbar not installed')
        
        # Enable profiler if requested
        if DevelopmentConfig.ENABLE_PROFILER:
            try:
                from werkzeug.middleware.profiler import ProfilerMiddleware
                app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
                app.logger.info('Profiler enabled')
            except ImportError:
                app.logger.warning('Profiler requested but not available')
        
        # Create upload directory
        if not os.path.exists(DevelopmentConfig.UPLOAD_FOLDER):
            os.makedirs(DevelopmentConfig.UPLOAD_FOLDER)
            app.logger.info(f'Created upload directory: {DevelopmentConfig.UPLOAD_FOLDER}')
"""

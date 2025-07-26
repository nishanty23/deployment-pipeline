"""
import os
from datetime import timedelta

class DevelopmentConfig:
    \"\"\"Development configuration.\"\"\"
    
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = True
    TESTING = False
    
    # Database configuration (SQLite for simplicity)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///flask_app_dev.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Enabled for development
    SQLALCHEMY_ECHO = True  # Log SQL queries
    
    # Redis configuration (optional in development)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/2'
    
    # Cache configuration (simple cache for development)
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60
    
    # Session configuration (filesystem-based)
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_sessions'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_app_dev:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Security configuration (relaxed for development)
    WTF_CSRF_ENABLED = False  # Disabled for easier API testing
    WTF_CSRF_TIME_LIMIT = None
    
    # API configuration (very permissive)
    RATELIMIT_ENABLED = False
    RATELIMIT_STORAGE_URL = None
    
    # Logging configuration (console only)
    LOG_LEVEL = 'DEBUG'
    LOG_TO_STDOUT = True
    
    # Email configuration (console backend)
    MAIL_BACKEND = 'console'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025  # MailHog or similar
    MAIL_USE_TLS = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    ADMIN_EMAIL = 'dev@localhost'
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB for development
    UPLOAD_FOLDER = '/tmp/dev_uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'json', 'xml', 'zip'}
    
    # API external services (all mocked)
    EXTERNAL_API_TIMEOUT = 5
    EXTERNAL_API_RETRIES = 1
    USE_MOCK_SERVICES = True
    MOCK_ALL_EXTERNAL_CALLS = True
    
    # Development tools
    FLASK_DEBUG_TOOLBAR = True
    EXPLAIN_TEMPLATE_LOADING = True
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Hot reloading
    USE_RELOADER = True
    USE_DEBUGGER = True
    
    # Testing features
    TESTING_DATABASE_RESET = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
    # Performance (development-friendly)
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = False
    
    # Monitoring (minimal)
    PROMETHEUS_METRICS = False
    HEALTH_CHECK_TIMEOUT = 1
    
    # Development flags
    DEVELOPMENT_MODE = True
    SKIP_AUTH_FOR_TESTING = True
    ENABLE_PROFILER = os.environ.get('ENABLE_PROFILER', 'false').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        \"\"\"Initialize application with development-specific settings.\"\"\"
        
        import logging
        
        # Console logging for development
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s: %(message)s'
        ))
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
"""

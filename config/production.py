"""
import os
from datetime import timedelta

class ProductionConfig:
    \"\"\"Production configuration.\"\"\"
    
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prod-secret-key-change-this'
    DEBUG = False
    TESTING = False
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://user:pass@localhost/flask_app_prod'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30
    }
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://redis:6379/0'
    
    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Session configuration
    SESSION_TYPE = 'redis'
    SESSION_REDIS = REDIS_URL
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'flask_app:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Security configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # API configuration
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "1000 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = '/var/log/flask_app/app.log'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 10
    
    # Email configuration (for error reporting)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    
    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = '/var/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx'}
    
    # API external services
    EXTERNAL_API_TIMEOUT = 30
    EXTERNAL_API_RETRIES = 3
    
    # Monitoring and metrics
    PROMETHEUS_METRICS = True
    HEALTH_CHECK_TIMEOUT = 5
    
    # CDN and static files
    CDN_DOMAIN = os.environ.get('CDN_DOMAIN')
    STATIC_FOLDER = '/var/www/static'
    
    # Backup configuration
    BACKUP_ENABLED = True
    BACKUP_SCHEDULE = '0 2 * * *'  # 2 AM daily
    BACKUP_RETENTION_DAYS = 30
    
    # Performance settings
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=24)
    JSONIFY_PRETTYPRINT_REGULAR = False
    
    # Error handling
    PROPAGATE_EXCEPTIONS = False
    
    @staticmethod
    def init_app(app):
        \"\"\"Initialize application with production-specific settings.\"\"\"
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler, SMTPHandler, RotatingFileHandler
        
        # File handler
        if not os.path.exists(os.path.dirname(ProductionConfig.LOG_FILE)):
            os.makedirs(os.path.dirname(ProductionConfig.LOG_FILE))
            
        file_handler = RotatingFileHandler(
            ProductionConfig.LOG_FILE,
            maxBytes=ProductionConfig.LOG_MAX_BYTES,
            backupCount=ProductionConfig.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, ProductionConfig.LOG_LEVEL))
        app.logger.addHandler(file_handler)
        
        # Email handler for critical errors
        if ProductionConfig.MAIL_USERNAME:
            auth = (ProductionConfig.MAIL_USERNAME, ProductionConfig.MAIL_PASSWORD)
            mail_handler = SMTPHandler(
                mailhost=(ProductionConfig.MAIL_SERVER, ProductionConfig.MAIL_PORT),
                fromaddr=ProductionConfig.MAIL_USERNAME,
                toaddrs=[ProductionConfig.ADMIN_EMAIL],
                subject='Flask Application Error',
                credentials=auth,
                secure=() if ProductionConfig.MAIL_USE_TLS else None
            )
            mail_handler.setFormatter(logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
            '''))
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        
        app.logger.setLevel(getattr(logging, ProductionConfig.LOG_LEVEL))
        app.logger.info('Flask application startup - Production mode')
"""

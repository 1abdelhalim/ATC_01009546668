from .settings import *
import os
import dj_database_url

# Use environment variable for DATABASE_URL or fallback to SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Make sure the connection is persistent
if 'default' in DATABASES:
    DATABASES['default']['CONN_MAX_AGE'] = 60

# Set debug from environment
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Security settings (enable for production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True  
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Set a proper SECRET_KEY for production
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY) 
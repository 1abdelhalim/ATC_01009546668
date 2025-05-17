"""
Production-specific settings for event_booking project.
Inherits from settings_postgres.py but overrides critical settings for production.
"""

import os
from django.core.exceptions import ImproperlyConfigured
from .settings_postgres import *

# Force debug to be False in production
DEBUG = False

# Get SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY environment variable is required but not set")

# Force the correct static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Azure-specific settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Update ALLOWED_HOSTS to include Azure internal IPs
ALLOWED_HOSTS.extend(['169.254.131.1', '169.254.131.2', '169.254.131.3', '169.254.131.4', '169.254.131.5'])

# Production security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database configuration - Check for individual DB environment variables if DATABASE_URL is not set
if not os.environ.get('DATABASE_URL') and os.environ.get('DB_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require' if os.environ.get('DATABASE_USE_SSL', 'True').lower() == 'true' else 'prefer',
            },
            'CONN_MAX_AGE': 60,
            'CONN_HEALTH_CHECKS': True,
        }
    } 
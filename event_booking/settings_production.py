"""
Production-specific settings for event_booking project.
Inherits from settings_postgres.py but overrides critical settings for production.
"""

from .settings_postgres import *

# Force debug to be False in production
DEBUG = False

# Force the correct static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Azure-specific settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Production security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY' 
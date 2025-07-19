"""
Django settings for Northflank deployment.
"""

import os
from .settings import *  # noqa: F403

# Defina SECRET_KEY explicitamente para evitar F405
SECRET_KEY = globals().get('SECRET_KEY', 'django-insecure-northflank-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    '0.0.0.0',
    'localhost',
    '127.0.0.1',
    '.northflank.app',
    '.vercel.app',
]

# Database configuration for Northflank
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'diario_ciclos_db'),
        'USER': os.environ.get('DATABASE_USER', 'user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', 'db'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# CORS settings for Northflank
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://*.vercel.app",
    "https://*.northflank.app",
]

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # noqa: F405
STATIC_URL = '/static/'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

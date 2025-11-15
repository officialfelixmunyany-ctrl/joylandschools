import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Allow overriding via environment for safer local/CI use; fallback keeps previous value.
import os
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-please-change-me')

# For local development only
DEBUG = True

# ALLOWED_HOSTS configuration
# - For development (DEBUG=True) we keep the permissive ['*'] so the
#   dev server is reachable from LAN IPs (convenient for local testing).
# - For safer control, you can set the DJANGO_ALLOWED_HOSTS environment
#   variable to a comma-separated list of hosts (e.g. "localhost,127.0.0.1,192.168.1.6").
ALLOWED_HOSTS_ENV = os.getenv('DJANGO_ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    # allow a comma-separated env var to override
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_ENV.split(',') if h.strip()]
else:
    if DEBUG:
        # permissive during development only
        ALLOWED_HOSTS = ['*']
    else:
        # production-safe default; update via DJANGO_ALLOWED_HOSTS when needed
        ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'users',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.PresenceMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'joyland.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Provide a lightweight site status contract for templates
                'users.context_processors.site_status',
                'users.context_processors.presence_stats',
            ],
        },
    },
]

WSGI_APPLICATION = 'joyland.wsgi.application'

# Database - sqlite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'joyland.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'users': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ['bootstrap5']
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# === AUTHENTICATION SETTINGS (ADDED) ===
LOGIN_URL = 'teacher_login'
LOGOUT_REDIRECT_URL = 'landing'
# === END AUTHENTICATION SETTINGS ===

# Email (development: console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@joyland.local'

# OpenAI Integration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_DEFAULT_MODEL = os.getenv('OPENAI_DEFAULT_MODEL', 'gpt-4')
ENABLE_GPT5_MINI = os.getenv('ENABLE_GPT5_MINI', 'false').lower() in ('1', 'true', 'yes')

# === FEATURE FLAGS (AUTHENTICATION REFACTOR) ===
# Enable role-aware login flow (teacher/parent/student-specific entry points)
FEATURE_ROLE_AWARE_LOGIN = os.getenv('FEATURE_ROLE_AWARE_LOGIN', 'true').lower() in ('1', 'true', 'yes')

# Enable shared login template consolidation (reduces duplication)
FEATURE_SHARED_LOGIN_TEMPLATE = os.getenv('FEATURE_SHARED_LOGIN_TEMPLATE', 'true').lower() in ('1', 'true', 'yes')

# Hide generic registration selector (forces role-specific registration)
FEATURE_HIDE_GENERIC_REGISTRATION = os.getenv('FEATURE_HIDE_GENERIC_REGISTRATION', 'false').lower() in ('1', 'true', 'yes')
# === END FEATURE FLAGS ===

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DB_DIR = BASE_DIR / 'bd'
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / 'db.sqlite3'

DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

# In production, set the SECRET_KEY environment variable.
# Example: export SECRET_KEY="your-strong-random-key-here"
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-rule-based-ai-12345-change-in-production')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

INSTALLED_APPS = []
MIDDLEWARE = []
ROOT_URLCONF = 'app'

TEMPLATES_CONFIG = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [str(BASE_DIR / 'templates')],
    'APP_DIRS': True,
}

DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(DB_PATH),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [str(BASE_DIR / 'static')] if (BASE_DIR / 'static').exists() else []

AI_SYSTEM_INFO = {
    'name': 'Rule-Based Credit Decision System',
    'version': '1.0.0',
    'type': 'Symbolic AI (Expert System)',
    'rules_count': 5,
    'description': 'Demonstrates transparent, rule-based AI decision making',
}
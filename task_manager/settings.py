from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR / 'task_manager'
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,webserver,webserver:9000").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'task_manager.main',
    'task_manager.users',
    'task_manager.statuses',
    'task_manager.tasks',
    'task_manager.labels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
if ACCESS_TOKEN:
    ROLLBAR = {
        'access_token': ACCESS_TOKEN,
        'environment': 'development' if DEBUG else 'production',
        'code_version': '1.0',
        'root': str(BASE_DIR),
    }

ROOT_URLCONF = 'task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'task_manager/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv(
            'DATABASE_URL', 'postgresql://postgres:011235!@localhost:5432/database'
        )
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

LOCALE_PATHS = [PROJECT_DIR / 'locale']
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
HANDLER404 = 'core.views.get_404'

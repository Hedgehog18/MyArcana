import os
from dotenv import load_dotenv
from pathlib import Path
# Для відображення повідомлень Django
from django.contrib.messages import constants as messages

# Шлях до .env
env_path = Path(__file__).resolve().parent.parent / '.env'

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')




OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-temp-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'main',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'uk-ua'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/accounts/login/'

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Для виведення листів у консоль (поки тестуємо)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# У продакшн — замінити на:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your_app_password'
DEFAULT_FROM_EMAIL = 'noreply@myarcana.online'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from enum import StrEnum
from pathlib import Path
import os
from dotenv import load_dotenv


class Envs(StrEnum):
    PRODUCTION = 'production'
    DEVELOPMENT = 'development'


def get_secret(key: str, default: str = '') -> str:
    value = os.getenv(key, default)
    if os.path.isfile(value):
        with open(value) as f:
            return f.read()
    return value


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(f'{BASE_DIR}/development.env')

SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
DJANGO_PORT = os.getenv('DJANGO_PORT', '8000')

USE_POSTGRES = os.getenv('USE_POSTGRES', 'False') == 'True'
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = get_secret('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


if ENVIRONMENT == Envs.PRODUCTION:
    DEBUG = False
    ALLOWED_HOSTS = [SERVER_ADDRESS]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [f'https://{SERVER_ADDRESS}']
    CSRF_TRUSTED_ORIGINS = [f'https://{SERVER_ADDRESS}']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
elif ENVIRONMENT == Envs.DEVELOPMENT:
    DEBUG = True
    ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'corsheaders',
    'comment',
    'forum',
    'rest_framework',
    'rest_framework.authtoken',
    'user_profile'
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'core.wsgi.application'


if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTHENTICATION_BACKENDS = [
    'account.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend'
]


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
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = 'static/'
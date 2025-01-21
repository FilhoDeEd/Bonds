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
        try:
            with open(value) as f:
                return f.read().strip()
        except OSError as e:
            raise Exception(f"Error reading the secret file at {value}: {e}")
    return value


BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = os.getenv('ENVIRONMENT', Envs.DEVELOPMENT)

if ENVIRONMENT == Envs.DEVELOPMENT and not get_secret('DJANGO_SECRET_KEY'):
    if not load_dotenv(f'{BASE_DIR}/development.env'):
        raise Exception(
            f'Failed to load the development environment file at {BASE_DIR}/development.env. '
            'Ensure the file exists and contains the necessary environment variables.'
        )

SECRET_KEY = get_secret('DJANGO_SECRET_KEY')
DJANGO_PORT = os.getenv('DJANGO_PORT', '8000')

USE_POSTGRES = os.getenv('USE_POSTGRES', 'False') in ['True', 'true']
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = get_secret('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


if ENVIRONMENT == Envs.PRODUCTION:
    DOMAIN = os.getenv('DOMAIN')
    DEBUG = False
    ALLOWED_HOSTS = [f'api.{DOMAIN}']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [f'https://www.{DOMAIN}']
    CSRF_TRUSTED_ORIGINS = [f'https://www.{DOMAIN}']
elif ENVIRONMENT == Envs.DEVELOPMENT:
    NODE_PORT = os.getenv('NODE_PORT')
    DEBUG = True
    ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [f'http://localhost:{NODE_PORT}']
    CSRF_TRUSTED_ORIGINS = [f'http://localhost:{NODE_PORT}']
else:
    raise Exception(f"Invalid environment named '{ENVIRONMENT}'.")


if ENVIRONMENT == Envs.PRODUCTION:
    STATIC_URL = f'https://api.{DOMAIN}/static/' # Não funciona. Atencion
    MEDIA_URL = f'https://api.{DOMAIN}/media/'
    STATIC_ROOT = '/static/'
    MEDIA_ROOT = '/media/'
elif ENVIRONMENT == Envs.DEVELOPMENT:
    STATIC_URL = 'static/'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'media')


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

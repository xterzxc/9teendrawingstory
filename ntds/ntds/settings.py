import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv('/etc/secrets/.env')


SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'
DEBUG_TOOLBAR = os.getenv('DEBUG_TOOLBAR', 'False') == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'draw',
    'debug_toolbar',
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

if DEBUG_TOOLBAR:
    MIDDLEWARE.insert(
        MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware'),
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    )


ROOT_URLCONF = 'ntds.urls'

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

WSGI_APPLICATION = 'ntds.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': BASE_DIR / os.getenv('DB_NAME'),
    }
}



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}



INTERNAL_IPS = [
    '127.0.0.1', # real ip 
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'


STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = 'staticfiles/'




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CF_BUCKET = os.getenv('CF_BUCKET')
CF_ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID')
CF_UPLOAD_URL = f'https://{CF_ACCOUNT_ID}.r2.cloudflarestorage.com/{CF_BUCKET}/'
CF_GET_URL = os.getenv('CF_GET_URL')
CF_ACCESS_KEY = os.getenv('CF_ACCESS_KEY')
CF_SECRET_ACCESS_KEY = os.getenv('CF_SECRET_ACCESS_KEY')
CF_REGION = 'us-east-1'
CF_SERVICE = 's3'


LOGIN_REDIRECT_URL = "index" 
LOGOUT_REDIRECT_URL = "index"
AUTH_USER_MODEL = 'users.User'

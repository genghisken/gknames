"""
Django settings for nameserver project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATHPREFIX = os.environ.get('WSGI_PREFIX')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Set the prefix for the object id you want to return to the requester.
OBJECT_PREFIX = os.environ.get('DJANGO_OBJECT_PREFIX')
# Set the nameing scheme to use, default is where 1 = aab, 2 = aac, etc
# (alternative is 1 = a, 2 = b, etc).
OBJECT_NAMING_SCHEME = os.environ.get('DJANGO_OBJECT_NAMING_SCHEME', 'aab')

SITE_ID = 1
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Set cookie names for session authentication
CSRF_COOKIE_NAME = 'csrf_' + os.environ.get('DJANGO_MYSQL_DBNAME')
SESSION_COOKIE_NAME = 'session_' + os.environ.get('DJANGO_MYSQL_DBNAME')

# Uncomment the following line if used behind a proxy server.
#CSRF_TRUSTED_ORIGINS = ['https://the.proxy.server']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_tables2',
    'nameserver',
    'nameserverapi.apps.NameserverapiConfig',
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

# Added token authentication class
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

ROOT_URLCONF = 'nameserver.urls'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, 'nameserver/templates'),

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = 'nameserver.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DJANGO_MYSQL_DBNAME'),
        'USER': os.environ.get('DJANGO_MYSQL_DBUSER'),
        'PASSWORD': os.environ.get('DJANGO_MYSQL_DBPASS'),
        'HOST': os.environ.get('DJANGO_MYSQL_DBHOST'),
        'PORT': int(os.environ.get('DJANGO_MYSQL_DBPORT')),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = PATHPREFIX + '/static/'

# STATICFILES_DIRS tells collectstatic where MY static files are.
STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'staticfiles'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


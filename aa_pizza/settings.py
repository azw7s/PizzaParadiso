"""
Django settings for aa_pizza project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path


DEBUG = True
# DEBUG = os.getenv('DEBUG', 'False') == 'True'


ALLOWED_HOSTS = ['pizzaparadiso-87c4c4557382.herokuapp.com', '127.0.0.1', 'www.pizzaparadiso-kw.com']


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customer',
    'menu',
    'order',
    'rest_framework',
    'djstripe',
    'storages',
    'autoslug',
    'phonenumber_field',
    'livereload',
    'django_extensions',
    'ipware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aa_pizza.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'order.context_processors.get_cart_id',
                'order.context_processors.get_cart_item_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'aa_pizza.wsgi.application'

SECRET_KEY = 'django-insecure-$f=hyksp4m0%u%_2ldo2a&$3)rffg@hj6blt+g0&sbnrn---q('
# SECRET_KEY = os.getenv('SECRET_KEY')


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "pizza_paradiso",
        'USER': "root",
        'PASSWORD': "kwamirzw7samadi",
        'HOST': "127.0.0.1",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASS'),
#         'HOST': os.getenv('DB_HOST'),
#     }
# }

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# LOG REDIRECTS

LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/home/'


# AWS


AWS_ACCESS_KEY_ID = 'AKIA6ODU3C6KE75FYRFG'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'pizzaparadiso'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_FILE_OVERWRITE = os.environ.get('AWS_S3_FILE_OVERWRITE')
# AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL', None)
# DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'


# Stripe

STRIPE_WEBHOOK_SECRET = "whsec_Ra6exjACrpu6gOksXwfoldqqMs2UJxFm"
STRIPE_PUBLIC_KEY = \
    "pk_test_51OMqPMCdFC8wFAX1m6WBevbH8zAjHiVySXQ0qs3dT9CQbexTba9Z9AhbFD0xrwtbKSTQvlQID9O351ITpNthfYYk00Dggoadwk"
STRIPE_SECRET_KEY = \
    "sk_test_51OMqPMCdFC8wFAX1urg7tnrZBg1mktkl412sRohgfl6LDUUeR1Or7eIDV9T3QER6tAnWyQlxXSpazx12H1WuBiwh000PAVi4Xk"
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
# STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
# STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
# DJSTRIPE_FOREIGN_KEY_TO_FIELD = os.getenv('DJSTRIPE_FOREIGN_KEY_TO_FIELD', 'id')


# YOUR_DOMAIN = os.getenv('YOUR_DOMAIN')
YOUR_DOMAIN = 'pizzaparadiso-kw.com'

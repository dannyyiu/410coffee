"""
Django settings for chai_cloud project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sc6o6hq2he*$y5-k%y+&)m#y8reu(0!x4eydt*2ekixz#jo3t('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# GLOBALS
#WS_URL = "ws://localhost:1025/ws" # DEBUG
#HTTP_URL = "http://localhost:8000/" # DEBUG
#WS_URL = "ws://chaiapp.tk:1025/ws" # HTTP DEPLOY
HTTP_URL = "http://localhost/" # DEPLOY (HTTP is okay here since used locally)
WS_URL = "wss://chaiapp.tk:1025/ws" # SSL DEPLOY

# PAYPAL GLOBALS
PP_CURRENCY = "CAD"
PP_TOKEN_URL = "https://api-3t.sandbox.paypal.com/nvp"
PP_EMAIL = "chai-facilitator_api1.gmail.com"
PP_MERC_ID = "BZ8PCS9ZDYTTG"
PP_PSS = "TSHBEMMJVLWXBHHU" # note: this is not login password
PP_SIGNATURE = "AFcWxV21C7fd0v3bYYYRCpSSRl31AXEh9liEDPaCcNurPvdeesaTwyYs"
PP_TEST_EMAIL = "chai-buyer@gmail.com" # used to autofill checkout email (testing)
PP_STORE_NAME = "CHAI+Store"

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'django.contrib.admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



ROOT_URLCONF = 'chai_cloud.urls'

WSGI_APPLICATION = 'chai_cloud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# secure proxy SSL header and secure cookies
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# session expire at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# wsgi scheme
os.environ['wsgi.url_scheme'] = 'https'

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = '/var/www/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "static"),
    '/home/ubuntu/chai_cloud_deploy/static',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

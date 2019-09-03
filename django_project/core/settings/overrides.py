# Set GeoNode prefix url
import ast
import os
import importlib

from distutils.util import strtobool

from geonode_generic.settings import *  # noqa

from core.settings.utils import validate_url, absolute_path


def update_settings_from(settings_name):
    """This method will try to update settings.

    It works as follows.

    The way GeoNode made as platform will let us to cascade different
    settings for each django app that uses GeoNode as a platform.

    We just need to load each settings and updated current locals modules.

    Let's say, the sites root settings is located (and described) in
    DJANGO_SETTINGS_MODULE

    This is the current file 'core.settings'

    This file will dictate which settings will load first and which to
    override form.

    Usually, 'geonode.settings' needs to be loaded first to include some
    basic settings. Then we need to override some settings based on the app
    we used. So we do

    update_settings_from(settings_name, current_module)

    To override settings in this module.

    By the design of Django, all needed settings starts with capital letter
    all Uppercase. So we exclude any files prefixed by _ since it is only of
    local module's concern.

    :param settings_name: The settings name in the format of python modules
        e.g. core.settings
    :type settings_name: basestring

    :return: will return current module
    :rtype: module
    """
    app_settings = importlib.import_module(settings_name)
    return {
        k: getattr(app_settings, k)
        for k in dir(app_settings) if not k.startswith('_')
    }

# Prefix to GeoNode index page
# We used ast for this to handle regex literal
GEONODE_INDEX_PREFIX = ast.literal_eval(
    os.environ.get('GEONODE_INDEX_PREFIX', "r'^administration/?$'")
)
GEONODE_PREFIX = ast.literal_eval(
    os.environ.get('GEONODE_PREFIX', "''")
)

MEDIA_URL = '/' + GEONODE_PREFIX + 'uploaded/'
STATIC_URL = '/' + GEONODE_PREFIX + 'static/'

STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    absolute_path('core', 'base_static'),
] + STATICFILES_DIRS

SCANAGROEMPRESA_URL = os.environ.get('SCANAGROEMPRESA_URL', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

if os.getenv('DEFAULT_BACKEND_DATASTORE'):
    DATABASES[os.getenv('DEFAULT_BACKEND_DATASTORE')] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('GEONODE_GEODATABASE'),
        'USER': os.environ.get('GEONODE_GEODATABASE_USERNAME'),
        'PASSWORD': os.environ.get('GEONODE_GEODATABASE_PASSWORD'),
        'HOST': os.environ.get('GEONODE_GEODATABASE_HOST'),
        'PORT': 5432
    }

DEBUG = strtobool(os.environ.get('DEBUG', 'False'))

# Contrib settings
INSTALLED_APPS += (
    'core.config_hook',
    'core.custom_rest_api',
    'core.kobo',
    'core.transfer',
)

# Celery settings
CELERY_BROKER_URL = os.environ.get('BROKER_URL', BROKER_URL)

CELERY_RESULT_PERSISTENT = False
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json', 'pickle']

if DEBUG:
    # Default settings for Debug mode is always eager
    _CELERY_TASK_ALWAYS_EAGER = 'True'
else:
    # Default settings for prod mode is to use worker
    _CELERY_TASK_ALWAYS_EAGER = 'False'

# But still, allow overrides from environment variables
CELERY_TASK_ALWAYS_EAGER = strtobool(
        os.environ.get('CELERY_TASK_ALWAYS_EAGER', _CELERY_TASK_ALWAYS_EAGER))
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_IGNORE_RESULT = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_WORKER_SEND_TASK_EVENTS = True
# Use this settings to limit concurrency (for Debugging)
if DEBUG:
    CELERY_WORKER_CONCURRENCY = 1
    CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_POOL_RESTARTS = True

ASYNC_SIGNALS_GEONODE = ast.literal_eval(os.environ.get(
        'ASYNC_SIGNALS_GEONODE', 'False'))

if ASYNC_SIGNALS_GEONODE and USE_GEOSERVER:
    from .geonode_queue_settings import *  # noqa
    CELERY_TASK_QUEUES += GEONODE_QUEUES

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'clean-import-job-daily': {
        'task': 'core.transfer.tasks.clean_import_job',
        'schedule': crontab(hour=0, minute=0),
    }
}

# Celery log
if DEBUG:
    LOGGING['disable_existing_loggers'] = False
    LOGGING['loggers']['celery']['level'] = 'DEBUG'

# Email settings
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '25'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'docker')
EMAIL_USE_TLS = strtobool(os.environ.get('EMAIL_USE_TLS', 'False'))
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL', 'support@kartoza.com')
EMAIL_SUBJECT_PREFIX = os.environ.get(
    'EMAIL_SUBJECT_PREFIX', '[SCANAGROEMPRESA]')
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Perform URL validations
# SITEURL should not end with slash
SITEURL = validate_url(SITEURL)

# SCANAGROEMPRESA_URL should end with slash
SCANAGROEMPRESA_URL = validate_url(SCANAGROEMPRESA_URL, end_slash=True)

# GeoServer internal Location and public location should end with slash
GEOSERVER_LOCATION = validate_url(GEOSERVER_LOCATION, end_slash=True)
GEOSERVER_PUBLIC_LOCATION = validate_url(
    GEOSERVER_PUBLIC_LOCATION, end_slash=True)

OGC_SERVER['default']['LOCATION'] = GEOSERVER_LOCATION
OGC_SERVER['default']['PUBLIC_LOCATION'] = GEOSERVER_PUBLIC_LOCATION
OGC_SERVER['default']['DATASTORE'] = os.environ.get('DEFAULT_BACKEND_DATASTORE', '')
OGC_SERVER['default']['TIMEOUT'] = int(os.environ.get(
    'OGC_SERVER_TIMEOUT', '3600'))

# Custom theme settings
USE_GEONODE_THEME_APP = ast.literal_eval(
    os.environ.get('USE_GEONODE_THEME_APP', 'False'))

if USE_GEONODE_THEME_APP:

    # Import app settings
    GEONODE_THEME_APP_NAME = os.environ.get('GEONODE_THEME_APP_NAME', None)
    theme_settings = update_settings_from(
        '{app_name}.settings'.format(app_name=GEONODE_THEME_APP_NAME))
    locals().update(theme_settings)

# custom SAE context processor
TEMPLATES[0]['OPTIONS']['context_processors'].append('core.context_processors.sae.sae_context')

TEMPLATES[0]['DIRS'].insert(0, absolute_path('core', 'base_templates'))

# custom geonode csrftoken
CSRF_COOKIE_NAME = os.environ.get(
    'GEONODE_CSRF_COOKIE_NAME',
    'csrftoken_geonode')

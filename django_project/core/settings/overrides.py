# Set GeoNode prefix url
import ast
import os
import importlib

from geonode_generic.settings import *  # noqa

from core.settings.utils import validate_url

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

GEONODE_PREFIX = ast.literal_eval(
    os.environ.get('GEONODE_PREFIX', "''")
)

MEDIA_URL = '/' + GEONODE_PREFIX + 'uploaded/'
STATIC_URL = '/' + GEONODE_PREFIX + 'static/'

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

# Custom theme settings
USE_GEONODE_THEME_APP = ast.literal_eval(
    os.environ.get('USE_GEONODE_THEME_APP', 'False'))

if USE_GEONODE_THEME_APP:

    # Import app settings
    GEONODE_THEME_APP_NAME = os.environ.get('GEONODE_THEME_APP_NAME', None)
    theme_settings = update_settings_from(
        '{app_name}.settings'.format(app_name=GEONODE_THEME_APP_NAME))
    locals().update(theme_settings)

# Set GeoNode prefix url
import ast
import os

from geonode_generic.settings import *  # noqa

from core.settings.utils import validate_url

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

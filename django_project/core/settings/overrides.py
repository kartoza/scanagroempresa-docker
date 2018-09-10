# Set GeoNode prefix url
import ast
import os

from geonode_generic.settings import *  # noqa

GEONODE_PREFIX = ast.literal_eval(
    os.environ.get('GEONODE_PREFIX', "''")
)

MEDIA_URL = '/' + GEONODE_PREFIX + 'uploaded/'
STATIC_URL = '/' + GEONODE_PREFIX + 'static/'

SCANWEBGIS_URL = os.environ.get('SCANWEBGIS_URL', '')

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

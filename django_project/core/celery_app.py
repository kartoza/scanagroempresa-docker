# coding=utf-8

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.overrides")

app = Celery('geonode')

from django.conf import settings

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



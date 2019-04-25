# coding=utf-8
from celery.result import AsyncResult
from django.db import models
from django.utils import timezone

from geonode.layers.models import Layer
from geonode.people.models import Profile


class ImportJob(models.Model):

    task_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    filepath = models.FileField(
        blank=True,
        null=True
    )
    layer = models.ForeignKey(
        Layer,
        blank=True,
        null=True)
    designated_owner = models.ForeignKey(
        Profile,
        blank=True,
        null=True)
    is_finished = models.BooleanField(
        default=False)
    created = models.DateTimeField(
        default=timezone.now())
    errors = models.TextField(
        blank=True,
        null=True)
    output_logs = models.TextField(
        blank=True,
        null=True)
    output_err = models.TextField(
        blank=True,
        null=True)

    @property
    def task_result(self):
        return AsyncResult(self.task_id)

    @property
    def task_status(self):
        res = self.task_result
        if not res:
            return 'UNKNOWN'
        return res.state

    @property
    def is_failed(self):
        res = self.task_result
        if res:
            return res.failed()
        else:
            return bool(self.errors)

    def __unicode__(self):
        return '{0.filepath} {0.task_status}'.format(self)

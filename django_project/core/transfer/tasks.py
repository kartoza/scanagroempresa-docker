# coding=utf-8
import logging
from StringIO import StringIO

from celery import shared_task
from celery.task import Task
from django.utils import timezone
from geonode.layers.models import Layer
from geonode.layers.utils import upload
from geonode.people.utils import get_valid_user

from core.transfer.models import ImportJob

LOGGER = logging.getLogger('geonode')


class ImportJobTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        try:
            job = ImportJob.objects.get(task_id=task_id)
            job.errors = exc.message
            job.output_err = str(exc)
            job.status = 'FAILED'
            job.save()
        except BaseException as e:
            LOGGER.error(e)
            LOGGER.error(exc)

    def on_success(self, retval, task_id, args, kwargs):

        try:
            job = ImportJob.objects.get(task_id=task_id)

            job.status = 'SUCCESS'
            job.is_finished = True

            layer_name = retval[0]['name']
            layer = Layer.objects.get(name=layer_name)
            job.layer = layer
            job.save()
        except BaseException as e:
            LOGGER.error(e)


@shared_task(bind=True, base=ImportJobTask)
def add_import_job(
        self, filepath, user=None, overwrite=True, *args, **kwargs):

    profile = get_valid_user(user=user)

    job, _ = ImportJob.objects.get_or_create(
        filepath=filepath,
        designated_owner=profile)
    job.task_id = self.request.id
    job.status = 'PENDING'
    job.save()
    out = StringIO()

    output = upload(
        filepath,
        user=user,
        overwrite=overwrite,
        skip=not overwrite,
        console=out)
    job.output_logs = out.getvalue()
    job.save()
    # determine result
    if not output:
        # We have failed.
        # Collect traceback
        raise Exception(
            'Import layers have failed for {0}\n'
            'Check that layer extensions were supported.'.format(filepath))
    elif output and output[0]['status'] == 'failed':
        raise output[0]['error']
    return output


@shared_task
def clean_import_job():
    now = timezone.now()
    for i in ImportJob.objects.all():
        date_diff = now - i.created
        if date_diff.days > 1:
            i.filepath.delete()
            i.delete()

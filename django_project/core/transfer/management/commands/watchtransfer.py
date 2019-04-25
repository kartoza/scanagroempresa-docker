# coding=utf-8
import os
import tarfile
import zipfile

import pyinotify
import re
import logging
from django.core.management import BaseCommand

from core.transfer.tasks import add_import_job

LOGGER = logging.getLogger('geonode')


class ZipLayerWatchHandler(pyinotify.ProcessEvent):

    def __init__(self, working_dir, callback=None):
        self.working_dir = working_dir
        self.callback = callback

    def _extract_zip(self, input, output_dir):
        with zipfile.ZipFile(input) as zf:
            zf.extractall(path=output_dir)

    def _extract_tar_gz(self, input, output_dir):
        with tarfile.open(input, 'r:gz') as tf:
            tf.extractall(path=output_dir)

    def process_IN_CREATE(self, event):
        # Process file, only if it is a zip file/tar.gz
        pathname = event.pathname
        filename = os.path.basename(pathname)
        pattern = re.compile(r'(?P<basename>.*)\.(?P<ext>zip|tar\.gz)$')

        match = pattern.search(filename)
        if match:
            LOGGER.info('Got file: {}'.format(pathname))

            basename = match.group('basename')

            LOGGER.info('Basename: {}'.format(basename))

            ext = match.group('ext')

            extract_f = {
                'zip': self._extract_zip,
                'tar.gz': self._extract_zip
            }
            extract_dir = os.path.join(self.working_dir, filename)
            try:
                os.makedirs(extract_dir, exist_ok=True)
            except:
                pass

            try:
                LOGGER.info('Attempting to extract {}'.format(pathname))
                # We need to extract to make sure zipfile is valid
                # and exit early if fails (not running importlayers)
                extract_f[ext](pathname, extract_dir)
                LOGGER.info('Extract finished.')
                self.callback(extract_dir)
            except BaseException as e:
                LOGGER.info('Extract failed, incomplete file')
                LOGGER.exception(e)

        else:
            LOGGER.info('Got file (not processed): {}'.format(pathname))

    def process_IN_MOVED_TO(self, event):
        LOGGER.info('Moved event.')
        self.process_IN_CREATE(event)

    def process_IN_MODIFY(self, event):
        LOGGER.info('Modify event.')
        self.process_IN_CREATE(event)


class Command(BaseCommand):

    help = (
        "Watch a specified directory of transferred files and automatically"
        "import it as layers")

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'watch_dir',
            help='Directory to watch')

        # keyword args
        parser.add_argument(
            '-u',
            '--user',
            dest='user',
            default=None,
            help="Default admin user to perform importlayers")

    def handle(self, *args, **options):

        watch_dir = options.get('watch_dir')
        self.user = options.get('user', None)
        verbosity = int(options.get('verbosity'))

        if verbosity > 0:
            logging.getLogger('').setLevel(logging.DEBUG)

        LOGGER.info('Start watching dir: {}'.format(watch_dir))
        LOGGER.info('Press CTRL+C to stop.')

        wm = pyinotify.WatchManager()

        handler = ZipLayerWatchHandler(watch_dir, self.add_job_callback)
        notifier = pyinotify.Notifier(wm, handler)

        flags = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | \
                pyinotify.IN_MOVED_TO
        wm.add_watch(watch_dir, flags, rec=True, auto_add=True)

        notifier.loop()

    def add_job_callback(self, filepath):
        LOGGER.info('Add new Import Job.')
        LOGGER.info('Filepath: {}'.format(filepath))
        LOGGER.info('User: {}'.format(self.user))
        LOGGER.info('')
        res = add_import_job.delay(filepath, self.user)
        LOGGER.info('Task id {}'.format(res.task_id))

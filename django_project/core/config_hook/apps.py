# coding=utf-8
from django.apps.config import AppConfig
from core.config_hook.permissions import initialize_permissions


class CoreAppConfig(AppConfig):

    name = "core"
    label = "core"

    def ready(self):
        super(CoreAppConfig, self).ready()
        # check settings
        from django.conf import settings

        installed_apps = []

        # Fix python 3 compatibility
        try:
            basestring
        except NameError:
            basestring = str

        for app in settings.INSTALLED_APPS:
            if isinstance(app, basestring):
                installed_apps.append(app)

        settings.INSTALLED_APPS = installed_apps

        # Install custom permissions
        initialize_permissions()

        # Init admin overrides
        from core.config_hook import admin  # noqa

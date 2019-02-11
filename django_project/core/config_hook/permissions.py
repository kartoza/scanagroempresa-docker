# coding=utf-8
import logging
import yaml
from core.settings.utils import absolute_path

LOGGER = logging.getLogger(__name__)


def initialize_permissions():
    """Initialize extra custom permissions for SAE-GeoNode.

    :type app_config: geonode.base.BaseAppConfig
    """

    # from django.contrib.auth.models import Permission
    # from django.contrib.contenttypes.models import ContentType
    from django.apps import apps
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    menu_permissions_fixture_path = absolute_path(
        'core', 'fixtures', 'menu_permissions.yaml')

    with open(menu_permissions_fixture_path, 'r') as f:
        try:
            fixture = yaml.load(f)
        except yaml.YAMLError as e:
            LOGGER.exception(e)
            return

    permission_models = fixture['core']
    for model_name, perms_list in permission_models.iteritems():
        core_permissions_content_type, __ = ContentType.objects.get_or_create(
            app_label='core', model=model_name)
        for perm in perms_list:
            perm_object, created = Permission.objects.get_or_create(
                name=perm, codename=perm,
                content_type=core_permissions_content_type)
            if created:
                LOGGER.info(
                    'Creating new custom permissions: {}'.format(
                        str(perm_object)))

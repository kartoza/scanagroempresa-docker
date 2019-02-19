# coding=utf-8
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from geonode.geoserver.helpers import create_gs_thumbnail
from geonode.maps.models import Map

from core.config_hook.utils import prevent_recursion, get_bounds_from_center_and_zoom

logger = logging.getLogger("geonode.geoserver.signals")


@receiver(post_save, sender=Map)
@prevent_recursion
def geoserver_post_save_map(sender, instance=None, created=False, **kwargs):
    if instance.center_x and instance.center_y and instance.zoom:
        # fix map bbox
        result = get_bounds_from_center_and_zoom(instance.center_x, instance.center_y, instance.zoom)
        instance.bbox_x0 = result['bbox_x0']
        instance.bbox_x1 = result['bbox_x1']
        instance.bbox_y0 = result['bbox_y0']
        instance.bbox_y1 = result['bbox_y1']
        instance.srid = result['srid']

        instance.set_missing_info()
        logger.info("... Creating Thumbnail for Map [%s]" % (instance.title))
        create_gs_thumbnail(instance, overwrite=True)

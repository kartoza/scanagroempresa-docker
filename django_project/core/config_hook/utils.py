# coding=utf-8
import math
from functools import wraps

from pyproj import Proj, transform


def prevent_recursion(func):
    """Decorator to prevent recursion when saving the instance.

    Taken from https://stackoverflow.com/a/28369908.
    """
    @wraps(func)
    def no_recursion(sender, instance=None, **kwargs):

        if not instance:
            return
        if hasattr(instance, '_dirty'):
            return

        func(sender, instance=instance, **kwargs)

        try:
            instance._dirty = True
            instance.save()
        finally:
            del instance._dirty

    return no_recursion


def get_bounds_from_center_and_zoom(center_x, center_y, zoom):
    """Calculate zoom level and center coordinates in mercator."""
    center_x = center_x
    center_y = center_y
    zoom = zoom

    deg_len_equator = 40075160 / 360

    # covert center in lat lon
    def get_lon_lat():
        wgs84 = Proj(init='epsg:4326')
        mercator = Proj(init='epsg:3857')
        lon, lat = transform(mercator, wgs84, center_x, center_y)
        return lon, lat

    # calculate the degree length at this latitude
    def deg_len():
        lon, lat = get_lon_lat()
        return math.cos(lat) * deg_len_equator

    lon, lat = get_lon_lat()

    # taken from http://wiki.openstreetmap.org/wiki/Zoom_levels
    # it might be not precise but enough for the purpose
    distance_per_pixel = 40075160 * math.cos(lat) / 2**(zoom+8)

    # calculate the distance from the center of the map in degrees
    # we use the calculated degree length on the x axis and the
    # normal degree length on the y axis assumin that it does not change

    # Assuming a map of 1000 px of width and 700 px of height
    distance_x_degrees = abs(distance_per_pixel * 500 / deg_len())
    distance_y_degrees = abs(distance_per_pixel * 350 / deg_len_equator)

    bbox_x0 = lon - distance_x_degrees
    bbox_x1 = lon + distance_x_degrees
    bbox_y0 = lat - distance_y_degrees
    bbox_y1 = lat + distance_y_degrees
    srid = 'EPSG:4326'

    return {
        'bbox_x0': bbox_x0,
        'bbox_x1': bbox_x1,
        'bbox_y0': bbox_y0,
        'bbox_y1': bbox_y1,
        'srid': srid
    }

# coding=utf-8
from geonode.api.urls import api
from core.custom_rest_api.resources import PermissionResource

api.register(PermissionResource())

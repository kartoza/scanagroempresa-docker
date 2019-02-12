# coding=utf-8
from django.contrib.auth.models import Permission
from django.db.models.query_utils import Q
from geonode.api.authorization import GeonodeApiKeyAuthentication
from geonode.people.models import Profile
from tastypie import fields
from tastypie.authentication import MultiAuthentication, SessionAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class PermissionResource(ModelResource):
    """Permission query Resource

    This resource is used to query set of permissions for a given user/group.

    The rule is as follow.

    To query permissions that a user have, send request to :

    api/permissions/?user=<userid>
    api/permissions/?user__username=<username>

    where <userid> comes from the `id` of GeoNode Profile models.
    where <username> comes from the `username` of GeoNode Profile models.

    To query permissions that a group have, send request to :

    api/permissions/?group=<groupid>
    api/permissions/?group__name=<groupslug>

    where <groupid> comes from `id` of django auth Group models.
    however it is not always practical to have this `id`.
    so instead you can use <groupslug>.
    where <groupslug> comes from `slug` of GeoNode GroupProfile models.

    Last. To just get the permission of currently connected/authenticated
    user. Use:

    api/permissions/?current_user=1
    """

    app_label = fields.CharField(
        attribute='content_type__app_label')
    model_name = fields.CharField()
    model_class_name = fields.CharField(
        attribute='content_type__model')

    def build_filters(self, filters=None, **kwargs):
        """Apply custom filters.

        We should be able to filters based on users and/or groups, and fetch
        their permissions.
        """
        new_filters = super(PermissionResource, self).build_filters(
            filters=filters, **kwargs)

        # If filtered by current_user, perform automatic filtering.
        extra_filters_keys = [
            'current_user',
            'user',
            'user__id',
            'user__username',
            'group',
            'group__id',
            'group__name'
        ]
        for k in extra_filters_keys:
            if k in filters.iterkeys():
                new_filters[k] = filters[k]

        return new_filters

    def apply_filters(self, request, applicable_filters):
        """Perform selection of filters.

        :type request: django.http.request.HttpRequest
        :type applicable_filters: dict
        """

        # In case of current user permission query, get user from request
        user = None
        if 'current_user' in applicable_filters.iterkeys():
            user = request.user
        elif 'user' in applicable_filters.iterkeys():
            user = Profile.objects.get(id=applicable_filters['user'])
        elif 'user__id' in applicable_filters.iterkeys():
            user = Profile.objects.get(id=applicable_filters['user__id'])
        elif 'user__username' in applicable_filters.iterkeys():
            user = Profile.objects

        current_queryset = self.get_object_list(request)

        # Check user permissions
        if user:
            # We actually can query all available permission for this user
            # But we need to honor other filters, so we fetch it but
            # doesn't immediately return the result.
            # get_all_permissions doesn't return queryset
            # so we use a little hack to filter the queryset.
            # this make sure the filter chain works later.
            perm_queries = None
            for perm_code in user.get_all_permissions():
                app_label, codename = perm_code.split('.')
                if perm_queries:
                    perm_queries = perm_queries | Q(
                        content_type__app_label=app_label, codename=codename)
                else:
                    perm_queries = Q(
                        content_type__app_label=app_label, codename=codename)
            current_queryset = current_queryset.filter(perm_queries)

            # Remove all user related filters, because we convert it to above
            for key in list(applicable_filters.iterkeys()):
                if 'user' in key:
                    del applicable_filters[key]

        # Combine all filters
        return current_queryset.filter(**applicable_filters)

    def dehydrate_model_name(self, bundle):
        obj = bundle.obj
        """:type: Permission"""
        return obj.content_type.name

    class Meta:
        filtering = {
            'app_label': ALL,
            'model_name': ALL,
            'model_class_name': ALL,
            'content_type': ALL_WITH_RELATIONS,
            'codename': ALL,
            'name': ALL,
            'user': ALL,
            'user__id': ALL,
            'user__username': ALL,
            'group': ALL,
            'group__id': ALL,
            'group__name': ALL,
            'current_user': ALL
        }
        queryset = Permission.objects.distinct().order_by(
            'content_type__app_label', 'codename')
        resource_name = 'permissions'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = MultiAuthentication(
            SessionAuthentication(), GeonodeApiKeyAuthentication())

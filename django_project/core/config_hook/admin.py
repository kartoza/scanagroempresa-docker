# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import Permission


class PermissionAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'codename', 'content_type']
    list_filter = ['content_type']
    search_fields = ['name', 'codename',
                     'content_type__app_label', 'content_type__model']


admin.site.register(Permission, PermissionAdmin)

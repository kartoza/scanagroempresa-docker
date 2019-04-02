# coding=utf-8
from django.contrib import admin
from core.transfer.models import ImportJob


class ImportJobAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'filepath',
        'layer',
        'designated_owner',
        'is_finished',
        'is_failed',
        'created'
    ]
    list_filter = [
        'is_finished',
        'designated_owner',
    ]
    search_fields = [
        'designated_owner',
        'layer',
        'filepath',
    ]


admin.site.register(ImportJob, ImportJobAdmin)

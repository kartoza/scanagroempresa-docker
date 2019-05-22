from django.contrib import admin
from models import KoboForm


class KoboFormAdmin(admin.ModelAdmin):

    list_display = ['id', 'form_title', 'form_id']


admin.site.register(KoboForm, KoboFormAdmin)

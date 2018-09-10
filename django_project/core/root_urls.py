# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import LocaleRegexURLResolver
from django.conf import settings
from django.views.generic import RedirectView, TemplateView

from geonode_generic.urls import urlpatterns

# We need to remove i18n if we want to use prefixed url.
for pattern in urlpatterns:
    if not isinstance(pattern, LocaleRegexURLResolver):
        continue
    if 'admin' in pattern.app_dict:
        admin_pattern = pattern
        break

urlpatterns += [
    url(r'admin/', include(admin.site.urls))
]
urlpatterns.remove(admin_pattern)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=settings.SCANWEBGIS_URL)),
    url(r'^geonode/?$',
        TemplateView.as_view(template_name='site_index.html'),
        name='home'),
    url(settings.GEONODE_PREFIX, include(urlpatterns)),
]

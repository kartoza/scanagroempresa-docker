# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import LocaleRegexURLResolver
from django.conf import settings
from django.views.generic import RedirectView, TemplateView

from geonode_generic.urls import urlpatterns
from core.custom_rest_api.urls import api

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
    url(r'^$', RedirectView.as_view(url=settings.SCANAGROEMPRESA_URL)),
    url(settings.GEONODE_INDEX_PREFIX,
        login_required(
            TemplateView.as_view(template_name='site_index.html'),
            login_url=settings.SCANAGROEMPRESA_URL),
        name='home'),
    url(settings.GEONODE_PREFIX, include(api.urls)),
    url(settings.GEONODE_PREFIX, include(urlpatterns)),
]

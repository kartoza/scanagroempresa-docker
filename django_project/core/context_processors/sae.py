from django.conf import settings


def sae_context(request):
    defaults = dict(
        SCANAGROEMPRESA_URL=settings.SCANAGROEMPRESA_URL,
        GEOSERVER_PUBLIC_LOCATION=settings.GEOSERVER_PUBLIC_LOCATION,
        CSRF_COOKIE_NAME=settings.CSRF_COOKIE_NAME
    )

    return defaults

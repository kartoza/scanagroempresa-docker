from django.conf import settings


def sae_context(request):
    defaults = dict(
        SCANAGROEMPRESA_URL=settings.SCANAGROEMPRESA_URL
    )
    
    return defaults
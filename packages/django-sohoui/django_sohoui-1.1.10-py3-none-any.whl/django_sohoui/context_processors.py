from django.conf import settings    


def custom_context(request):
    return {
        'LOGIN_BG_IMAGE': settings.SOHO_LOGIN_BG_IMAGE,
        'site_header': settings.SOHO_SITE_HEADER,
        'site_title': settings.SOHO_SITE_TITLE,
        'index_title': settings.SOHO_INDEX_TITLE,
    }

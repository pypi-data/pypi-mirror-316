from django.conf import settings    


def custom_context(request):
    return {
        ## 可能没有设置，添加默认值             
        'LOGIN_BG_IMAGE': getattr(settings, 'SOHO_LOGIN_BG_IMAGE', '/static/django_sohoui/images/logo_bg.jpg'),
    }

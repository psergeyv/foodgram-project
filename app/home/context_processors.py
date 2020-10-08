from django.conf import settings
import datetime as dt

from home.models import Setting

def setting_site(request):
    setting_list = {}

    setting = Setting.objects.filter(site = settings.SITE_ID).first()
    if setting:
        setting_list = setting
    return {'setting_site':setting_list}                   

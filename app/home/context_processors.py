from django.conf import settings
import datetime as dt

from home.models import Setting
from recipes.models import Tags


def setting_site(request):
    setting_list = {}

    setting = Setting.objects.filter(site=settings.SITE_ID).first()
    if setting:
        setting_list = setting
    return {'setting_site': setting_list}


def get_tags(request):
    list_tags = Tags.objects.order_by('title').all()
    tags = {}
    for tag in list_tags:
        tags[tag.slug] = {'title': tag.title, 'style': tag.style}
        temp_tags = []
        if request.GET.get('f'):
            temp_tags = request.GET.get('f').split(',')
        if tag.slug in temp_tags:
            tags[tag.slug]['view'] = True
            temp_tags.remove(tag.slug)
        else:
            tags[tag.slug]['view'] = False
            temp_tags.append(tag.slug)
        if len(temp_tags) > 0:
            tags[tag.slug]['url'] = '?f='+','.join(temp_tags)
        else:
            tags[tag.slug]['url'] = ''

    return {'tags': tags}

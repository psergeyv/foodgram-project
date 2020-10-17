from django.conf import settings
import datetime as dt

from home.models import Setting


def setting_site(request):
    setting_list = {}

    setting = Setting.objects.filter(site=settings.SITE_ID).first()
    if setting:
        setting_list = setting
    return {'setting_site': setting_list}


def get_tags(request):
    bdTags = Tags.objects.order_by("title").all()
    tags = {}
    tags_filters = []
    for tag in bdTags:
        tags[tag.slug] = {'title': tag.title, 'style': tag.style}
        tempTags = []
        if request.GET.get('f'):
            tempTags = request.GET.get('f').split(',')
        if tag.slug in tempTags:
            tags_filters.append(tag.id)
            tags[tag.slug]['view'] = True
            tempTags.remove(tag.slug)
        else:
            tags[tag.slug]['view'] = False
            tempTags.append(tag.slug)
        if len(tempTags) > 0:
            tags[tag.slug]['url'] = '?f='+','.join(tempTags)
        else:
            tags[tag.slug]['url'] = '/recipes/'+str(user_id)

    return tags

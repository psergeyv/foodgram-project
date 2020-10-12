from django import template
from home.models import Textblock


register = template.Library()


@register.filter(name='html_block')
def get_filter_values(request, codeblock):
    hrmlBlock = Textblock.objects.filter(codeblock=codeblock).first()
    hrmlBl = ''
    if hrmlBlock:
        hrmlBl = hrmlBlock.description
    return  hrmlBl   



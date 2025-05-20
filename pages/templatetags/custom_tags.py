from django import template
from django.utils.translation import get_language
import pprint

register = template.Library()

@register.filter
def pprint_filter(value):
    return pprint.pformat(value)


#@register.simple_tag
#def translated_page_title(page):
#    language_code = get_language()
#    translation = page.translations.filter(language=language_code).first()
#    return translation.title if translation and translation.title else page.title

@register.simple_tag
def translated_page_content(page, get_content=False): #nuevo argumento para manejar el content
    language_code = get_language()
    translation = page.translations.filter(language=language_code).first()

    if get_content:
        return translation.content if translation and translation.content else page.content
    else:
        return translation.title if translation and translation.title else page.title

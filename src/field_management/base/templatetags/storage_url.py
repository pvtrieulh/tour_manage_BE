from django import template
from django.core.files.storage import default_storage

register = template.Library()


@register.filter
def storage_url(url_link):
    if not url_link:
        return None
    return default_storage.url(url_link)

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.db.models import F

from base.utils import get_lang

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CacheMixin(object):
    cache_timeout = CACHE_TTL
    router = 'default'
    key_prefix = ''

    def get_cache_timeout(self):
        return self.cache_timeout

    def get_key_prefix(self):
        if not self.key_prefix:
            try:
                if self.serializer_class:
                    self.key_prefix = self.serializer_class.Meta.model.key_prefix
            except:
                pass
        try:
            model = self.queryset.model
            if model and self.kwargs['pk'] and hasattr(model, 'view_quantity'):
                model.objects.filter(id=self.kwargs['pk']).update(view_quantity=F('view_quantity') + 1)
        except Exception as e:
            pass
        return self.key_prefix

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout(), cache=self.router, key_prefix=self.get_key_prefix())(
            super(CacheMixin, self).dispatch)(
            *args, **kwargs)

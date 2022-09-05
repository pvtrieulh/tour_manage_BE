import requests
import json
from django.conf import settings
from django.db.models import F
from django.db.models.fields.files import FileField

from base.api.exceptions import ValidationException
from base.api.messages import FIELD_FORMAT_INT, BODY_MISS_FIELDS
from base.utils import write_error
from celery import shared_task


class BaseApi:
    def get_api_key(self):
        return 'abcxyz'

    def get_api_url(self):
        return 'https://abc.xyz'

    def get_url_endpoint(self, endpoint=None):
        if not endpoint:
            return "{host}?key={key}".format(host=self.get_api_url(), key=self.get_api_key())
        return "{host}/{endpoint}?key={key}".format(host=self.get_api_url(), key=self.get_api_key(), endpoint=endpoint)

    def request_headers(self):
        return {
            "Content-Type": 'application/json; charset=utf-8',
        }

    def json_dumps(self, data):
        """Standardized json.dumps function with separators and sorted keys set."""
        return json.dumps(data, separators=(',', ':'), sort_keys=True).encode('utf8')

    def request_post_api(self, payload, timeout=30):
        return requests.post(
            self.get_url_endpoint(),
            headers=self.request_headers(),
            data=self.json_dumps(payload),
            timeout=timeout
        )


class WeMapApi(BaseApi):
    def get_api_key(self):
        return settings.API_KEY_WEMAP

    def get_api_url(self):
        return settings.BASE_URL_WEMAP

    def request_headers(self):
        return {
            "Content-Type": 'application/json; charset=utf-8',
            "Accept-Language": "vi",
        }

    def request_get_features(self, endpoint=None, payload=None, timeout=30):
        try:
            response = requests.get(
                self.get_url_endpoint(endpoint),
                headers=self.request_headers(),
                params=payload,
                timeout=timeout
            )
        except:
            return None
        result = response.json()
        if not result:
            return None
        return result.get('features')


class FileModelStorageHelper:
    def __init__(self, model=None, ids=None, obj=None):
        self.model = model
        self.ids = ids
        self.fields = []
        self.field_paths = []
        self.obj = obj
        if self.obj:
            self.model = obj
        self.get_fields_file()
        self.get_paths()

    def get_paths(self):
        if not self.fields:
            return True
        if not self.obj:
            items = self.model.objects.filter(id__in=self.ids)
        else:
            items = [self.obj]
        self.field_paths = []
        for item in items:
            for field in self.fields:
                val = getattr(item, field)
                if val:
                    self.field_paths.append(val)

    def get_fields_file(self):
        self.fields = []
        fields = self.model._meta.get_fields()
        for field in fields:
            if isinstance(field, FileField):
                self.fields.append(field.name)

    def delete(self):
        if not self.field_paths:
            return None
        try:
            for item in self.field_paths:
                item.delete(save=False)
        except Exception as e:
            write_error(e)


def get_list_int_from_request(request, param_name, method='get'):
    if method == 'get':
        ids = request.GET.get(param_name)
    else:
        ids = request.data.get(param_name)
    if not ids:
        return []
    ids = ids.split(',')
    try:
        return list(map(int, ids))
    except:
        return []


def get_ids_from_request(request):
    '''
    get ids int from request - action multi
    :param request:
    :return:
    '''
    ids = request.data.get('ids')
    if not ids:
        raise ValidationException(BODY_MISS_FIELDS[1] % ('ids', ))
    ids = ids.split(',')
    try:
        return list(map(int, ids))
    except:
        raise ValidationException(FIELD_FORMAT_INT[1] % ('ids',))


def sort_dir_from_request(request, queryset, default_sort='created_at', allow_sort=[], sort_key_replace={}):
    sort = request.GET.get('sort')
    sort_dir = request.GET.get('dir')
    default_str = '-{s}'.format(s=default_sort)
    if not sort or sort not in allow_sort:
        return queryset.order_by(default_str)

    str_sort = ''
    if sort_dir != 'asc':
        str_sort = '-'
    if sort_key_replace.get(sort):
        sort = sort_key_replace.get(sort)
    str_sort = str_sort + sort
    if sort != default_sort:
        return queryset.order_by(str_sort)
    return queryset.order_by(str_sort)


def full_module_object_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__


def get_class_from_str(str_class_name):
    parts = str_class_name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def domed_float(value):
    if value is not None:
        return int(value + 0.5)

@shared_task()
def save_react_after_get_detail(user_id, obj_type, obj_id):
    from st_utility.models import UserReact
    from st_utility.models import ItemRecommend
    from st_utility.tasks import get_key_word
    user_react = UserReact.objects.filter(user=user_id, item__item_type=obj_type, item__item_id=obj_id).first()

    if user_react is None:
        item = ItemRecommend.objects.filter(item_type=obj_type, item_id=obj_id).first()
        if item is None:
            keyword = get_key_word(obj_type, obj_id)
            item = ItemRecommend.objects.create(item_id=obj_id, item_type=obj_type, keyword=keyword)
        user_react = UserReact.objects.create(item=item, user=user_id, count=0)
    user_react.count = F('count') + 1
    user_react.save()
    item_exists = UserReact.objects.filter(user=user_id).values_list('item')
    item_ids = ItemRecommend.objects.exclude(id__in=item_exists)
    for item in item_ids:
        UserReact.objects.create(item=item, user=user_id, count=0)

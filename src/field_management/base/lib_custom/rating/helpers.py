from django.apps import apps
from django.db.models import Q, Avg
from django.core.cache import cache

from base.choices import ENABLE, DISABLE
from .choices import LIKE_STATUS_LIKE
from base.permissions import request_to_auth_info
from base.utils import write_error, get_random_time_string
from st_auth.constant import MODE_PERSONAL_KEY
from word.helpers import is_valid_rule_word


def get_gallery_model(rate_model):
    return apps.get_model(app_label=rate_model._meta.app_label, model_name=rate_model.foreign_key.get('galley'))


def get_like_model(rate_model):
    return apps.get_model(app_label=rate_model._meta.app_label, model_name=rate_model.foreign_key.get('like'))


def get_reply_model(rate_model):
    return apps.get_model(app_label=rate_model._meta.app_label, model_name=rate_model.foreign_key.get('reply'))


def get_main_model(rate_model):
    return rate_model._meta.get_field('obj_main').remote_field.model


def get_model_from_app(class_view, obj_name):
    module = class_view.__module__
    module = module[0:module.find('.')]
    return apps.get_model(app_label=module, model_name=obj_name)


def create_from_validated_data(model_object, validated_data):
    obj = model_object()
    for item in validated_data:
        setattr(obj, item, validated_data.get(item))
    obj.save()
    return obj


class RateListToElement:
    rate_list = None
    rate_ids = []
    reply_ids = []
    user_data = {}
    request = None

    def __init__(self, request):
        self.request = request
        self.user_data = {}
        self.rate_ids = []
        self.reply_ids = []

    def set_rate_list(self, rate_list):
        self.rate_list = rate_list
        self.__get_rate_ids()

    def __get_rate_ids(self):
        for i in self.rate_list:
            self.rate_ids.append(i.id)

    def set_rate_reply(self, reply_list, rate_list):
        self.rate_list = rate_list
        for i in reply_list:
            self.reply_ids.append(i.id)

    def exec_all_data(self, reply=True, gallery=True, is_like=True):
        return {
            'reply': self.get_reply() if reply else None,
            'gallery': self.get_gallery() if gallery else None,
            'is_like': self.get_like(self.request) if is_like else None,
        }

    def get_reply(self):
        if not len(self.rate_ids):
            return None
        reply_model = get_reply_model(self.rate_list[0])
        queryset_union = None
        for rate_id in self.rate_ids:
            queryset = reply_model.objects.filter(rate_id=rate_id, status=ENABLE, approve=ENABLE) \
                .order_by('-created_at')[0:3]
            if queryset_union is None:
                queryset_union = queryset
            else:
                queryset_union = queryset_union.union(queryset)
        result = {}

        for reply_item in queryset_union:
            if reply_item.user_mod not in self.user_data:
                self.user_data[reply_item.user_mod] = []
            self.user_data[reply_item.user_mod].append(reply_item.user_id)
            if reply_item.rate_id not in result:
                result[reply_item.rate_id] = []
            result[reply_item.rate_id].append(reply_item)
            self.reply_ids.append(reply_item.id)
        return result

    def get_gallery(self):
        if not len(self.rate_ids) and not len(self.reply_ids):
            return None
        gallery_collection = get_gallery_model(self.rate_list[0]).objects\
            .filter(Q(rate_id__in=self.rate_ids) | Q(reply_id__in=self.reply_ids))\
            .only('file', 'rate_id', 'reply_id')

        result = {
            'rate': {},
            'reply': {},
        }
        for i in gallery_collection:
            if i.rate_id:
                key = 'rate'
                id = i.rate_id
            elif i.reply_id:
                key = 'reply'
                id = i.reply_id

            if id not in result[key]:
                result[key][id] = []
            result[key][id].append({
                'id': i.id,
                'file': i.file
            })
        return result

    def get_like(self, request):
        if not len(self.rate_ids):
            return None
        request_auth = request_to_auth_info(request=request)
        if not request_auth:
            return None
        like_collection = get_like_model(self.rate_list[0]).objects\
            .filter(rate_id__in=self.rate_ids, status=LIKE_STATUS_LIKE,
                    user_id=request_auth.get('user_id'), user_mod=request_auth.get('user_type')) \
            .only('rate_id')
        result = {}
        for i in like_collection:
            result[i.rate_id] = [i.id]
        return result


def rate_obj_after_save(rate_obj):
    '''recount rate and calculator rate avg of obj main'''
    main_obj = rate_obj.obj_main
    rate_model = type(rate_obj)
    update_fields_model = ['rate_count']
    rate_count = rate_model.objects.filter(obj_main_id=rate_obj.obj_main_id, status=ENABLE, approve=ENABLE).count()
    main_obj.rate_count = rate_count
    if hasattr(main_obj, 'rate_avg'):
        rate_avg = rate_model.objects.filter(obj_main_id=rate_obj.obj_main_id, status=ENABLE, approve=ENABLE) \
            .aggregate(Avg('rate'))
        if rate_avg.get('rate__avg'):
            main_obj.rate_avg = round(rate_avg.get('rate__avg'), 1)
            update_fields_model.append('rate_avg')
    main_obj.save(update_fields=update_fields_model)


def rate_obj_list_after_save(rate_list_obj):
    '''recount rate and calculator rate avg of obj main'''
    obj_main_dict = {}
    for item in rate_list_obj:
        obj_main_dict[item.obj_main_id] = item
    try:
        for id, item in obj_main_dict.items():
            rate_obj_after_save(item)
    except Exception as e:
        write_error(e)


def rate_reply_after_save(reply_obj, created=False, deleted=False):
    '''recount reply of rate obj'''
    reply_model = type(reply_obj)
    count_reply = reply_model.objects.filter(rate_id=reply_obj.rate_id, status=ENABLE, approve=ENABLE).count()
    rate_obj = reply_obj.rate
    rate_obj.reply_count = count_reply
    fields_update_rate_obj = ['reply_count']
    if not deleted:
        if reply_obj.approve == DISABLE:
            rate_obj.is_approve_child = False
        else:
            rate_obj.is_approve_child = True
    fields_update_rate_obj.append('is_approve_child')
    if created:  # check is reply by user
        rate_obj.is_reply = reply_obj.user_mod != MODE_PERSONAL_KEY
        fields_update_rate_obj.append('is_reply')
    rate_obj.save(is_cal_count=False, update_fields=fields_update_rate_obj)


def rate_reply_list_after_save(rate_reply_list, created=False, deleted=False):
    '''recount rate and calculator rate avg of obj main'''
    obj_main_dict = {}
    for item in rate_reply_list:
        obj_main_dict[item.rate_id] = item
    try:
        for id, item in obj_main_dict.items():
            rate_reply_after_save(item, created, deleted)
    except Exception as e:
        write_error(e)


def rate_check_valid_word_before_save(comment):
    valid_word = is_valid_rule_word(comment)
    if valid_word is True:
        return True
    key = get_random_time_string(10)
    cache.set(key, {
        'comment': comment,
        'word': valid_word
    }, 120)
    return {
        "key": key,
        'word': valid_word
    }


def rate_pass_invalid_rule_with_key(comment, key=None):
    if not key:
        return None
    rate_word = cache.get(key)
    if not rate_word:
        return None
    if rate_word.get('comment') != comment:
        return None
    return rate_word.get('word')

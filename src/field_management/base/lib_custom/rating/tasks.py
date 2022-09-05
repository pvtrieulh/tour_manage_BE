from celery import shared_task

from base.choices import ENABLE, DISABLE
from base.helpers import get_class_from_str
from word.helpers import is_valid_rule_word


@shared_task
def rate_check_valid_word(obj_id, obj_type_str):
    obj_model = get_class_from_str(obj_type_str)
    obj = obj_model.objects.filter(id=obj_id).first()
    if not obj:
        return False
    valid_word = is_valid_rule_word(obj.comment)
    if valid_word is True:
        obj.approve = ENABLE
        obj.save()
        return True
    obj.approve = DISABLE
    obj.save()
    return valid_word

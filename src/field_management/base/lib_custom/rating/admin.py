from base.admin import BaseModelAdmin


class ObjectRateBaseAdmin(BaseModelAdmin):
    list_display = ['id', 'rate', 'obj_main', 'user_id', 'user_mod', 'status', 'approve']


class ObjectRateGalleryBaseAdmin(BaseModelAdmin):
    list_display = ['id', 'rate_id', 'reply_id', 'file']


class ObjectRateLikeBaseAdmin(BaseModelAdmin):
    list_display = ['id', 'rate_id', 'user_id', 'user_mod', 'status']


class ObjectRateReplyBaseAdmin(BaseModelAdmin):
    list_display = ['id', 'rate_id', 'user_id', 'user_mod', 'status', 'approve']


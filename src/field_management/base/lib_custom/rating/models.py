from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.transaction import on_commit

from base.choices import ENABLE
from base.validators import validate_file_size_image, validate_file_extension_image
from base.models import BaseModelStatusApprove, BaseModelTime, base_upload
from base.user_base import UserInfoTypeAbstract
from base.helpers import full_module_object_name
from .helpers import rate_obj_after_save, rate_reply_after_save
from .choices import LIKE_STATUS_CHOICE, LIKE_STATUS_LIKE
from .tasks import rate_check_valid_word


def upload_image_rate(instance, filename):
    return base_upload(filename, "upload/{}/rate".format(instance._meta.app_label))


class RateObjmainBaseModel(models.Model):
    rate_avg = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Trung bình điểm đánh giá",
        validators=[MinValueValidator(0), MaxValueValidator(5)], )
    rate_count = models.PositiveIntegerField(default=0, verbose_name='Tổng số rate')

    class Meta:
        abstract = True


class RateBaseModel(UserInfoTypeAbstract, BaseModelTime, BaseModelStatusApprove):
    '''attr overwrite by class inheritance
    obj_main = models.ForeignKey(on_delete=models.CASCADE, verbose_name="Name of obj", to="object_main_to_rate")
    '''

    rate = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                    verbose_name="Giá trị rate", null=True, blank=True)
    comment = models.TextField(null=True, blank=True, verbose_name="Bình luận rate")
    like_count = models.PositiveIntegerField(default=0, verbose_name="Tổng số lượng like")
    reply_count = models.PositiveIntegerField(default=0, verbose_name="Tổng số lượng reply")
    is_reply = models.BooleanField(default=False, verbose_name="Reply chưa?")
    is_approve_child = models.BooleanField(default=True, verbose_name="Approve con chưa?")
    reason_un = models.TextField(null=True, blank=True, verbose_name="Lý do không duyệt")
    foreign_key = {
        'reply': 'ObjectRateReply',
        'galley': 'ObjectRateGallery',
        'like': 'ObjectRateLike'
    }

    class Meta:
        # db_table = 'st_tour_rate'
        abstract = True
        indexes = [
            models.Index(fields=['user_id', 'user_mod', ]),
        ]

    def save(self, is_cal_count=True, *args, **kwargs):
        created = True if not self.pk else False
        result = super().save(*args, **kwargs)
        if created and (self.status != ENABLE or self.approve != ENABLE):
            return result
        if is_cal_count:
            rate_obj_after_save(self)
        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        rate_obj_after_save(self)
        return result


class RateReplyBaseModel(UserInfoTypeAbstract, BaseModelTime, BaseModelStatusApprove):
    rate = models.ForeignKey(on_delete=models.CASCADE, verbose_name="Khóa ngoại rate", related_name="+",
                             to="ObjectRate")
    comment = models.TextField(verbose_name="Reply rate comment")
    reason_un = models.TextField(null=True, blank=True, verbose_name="Lý do không duyệt")

    class Meta:
        # db_table = 'st_tour_rate_reply'
        abstract = True
        indexes = [
            models.Index(fields=['user_id', 'user_mod', ]),
        ]

    def save(self, *args, **kwargs):
        created = True if not self.pk else False
        result = super().save(*args, **kwargs)
        if created and (self.status != ENABLE or self.approve != ENABLE):
            return result
        rate_reply_after_save(reply_obj=self, created=created)
        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        rate_reply_after_save(self, deleted=True)
        return result


class RateGalleryBase(BaseModelTime):
    rate = models.ForeignKey(on_delete=models.CASCADE, verbose_name="Khóa ngoại rate", related_name="+",
                             to="ObjectRate", null=True, blank=True)
    reply = models.ForeignKey(on_delete=models.CASCADE, verbose_name="Khóa ngoại rate reply", related_name="+",
                              to="ObjectRateReply", null=True, blank=True)
    file = models.ImageField(upload_to=upload_image_rate, verbose_name="Upload ảnh gallery",
                             validators=[validate_file_size_image, validate_file_extension_image],
                             help_text="File upload phải có dung lượng nhỏ hơn 2MB"
                             )

    class Meta:
        # db_table = 'st_tour_rate_gallery'
        abstract = True


class RateLikeBase(UserInfoTypeAbstract, BaseModelTime):
    rate = models.ForeignKey(on_delete=models.CASCADE, verbose_name="Khóa ngoại rate", related_name="+",
                             to="ObjectRate")
    status = models.SmallIntegerField(default=0, verbose_name="Trạng thái like", choices=LIKE_STATUS_CHOICE)

    class Meta:
        # db_table = 'st_tour_rate_like'
        abstract = True
        indexes = [
            models.Index(fields=['user_id', 'user_mod', ]),
        ]

    def save(self, rate_obj=None, *args, **kwargs):
        result = super().save(*args, **kwargs)
        # recount like of rate obj
        like_model = type(self)
        count_like = like_model.objects.filter(rate_id=self.rate_id, status=LIKE_STATUS_LIKE).count()
        if rate_obj is None:
            rate_obj = self.rate
        rate_obj.like_count = count_like
        rate_obj.save(is_cal_count=False, update_fields=["like_count"])
        return result

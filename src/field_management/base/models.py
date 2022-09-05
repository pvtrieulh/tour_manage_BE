import time
from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from base.utils import get_filename_ext, clean_cache_by_prefix
from .choices import ENABLE, WAITING_APPROVAL_KEY, STATUS_APPROVAL, APPROVE_SELECT_CHOICE, STATUS_SELECT


def base_upload(filename, path="default/file"):
    new_filename = time.time()
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "{path}/{final_filename}".format(
        path=path,
        final_filename=final_filename
    )


def upload_image(instance, filename):
    return base_upload(filename, "{}{}".format('upload/', instance._meta.app_label))


def base_filter(model):
    return model.objects.filter(
        Q(status=ENABLE)
    )


def adv_filter(model):
    return model.objects.filter(deleted_at=None)


class BaseModel(models.Model):
    class Meta:
        abstract = True


class BaseCacheModel(BaseModel):
    key_prefix = None
    key_cache_clean = []

    class Meta:
        abstract = True

    def clean_cache(self):
        if self.key_prefix:
            clean_cache_by_prefix(self.key_prefix)
        if self.key_cache_clean:
            for i in self.key_cache_clean:
                clean_cache_by_prefix(i)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.clean_cache()
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def delete(self, using=None, keep_parents=False):
        self.clean_cache()
        return super().delete(using=using, keep_parents=keep_parents)


class BaseModelTime(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Thời gian tạo')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Thời gian chỉnh sửa')

    class Meta:
        abstract = True


class BaseModelStatus(BaseModel):
    status = models.BooleanField(
        default=ENABLE,
        verbose_name="Enable"
    )

    class Meta:
        abstract = True


class BaseModelStatusApprove(BaseModel):
    status = models.SmallIntegerField(
        default=ENABLE,
        verbose_name="Trạng thái (user manage)",
        choices=STATUS_SELECT
    )
    approve = models.SmallIntegerField(
        choices=APPROVE_SELECT_CHOICE,
        default=ENABLE,
        verbose_name="Kiểm duyệt (admin manage)",
    )

    class Meta:
        abstract = True


class BaseModelTimeStatus(BaseModelTime, BaseModelStatus):
    class Meta:
        abstract = True


class AppTracking(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    remote_ip = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        null=True,
        verbose_name="Vĩ độ / latitude"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        null=True,
        verbose_name="Kinh độ / longitude"
    )

    class Meta:
        db_table = 'd_app_tracking'
        verbose_name = "Lượng tải về"
        verbose_name_plural = "Lượng tải về"


class StatusApproval(models.Model):
    status_approval = models.SmallIntegerField(default=WAITING_APPROVAL_KEY, 
        choices=STATUS_APPROVAL, null=True, blank=True, verbose_name='Trạng thái phê duyệt')

    class Meta:
        abstract = True


class TableAbstract(models.Model):
    '''Table template use write raw query, not migrate'''
    class Meta:
        db_table = 'd_table_tmp'

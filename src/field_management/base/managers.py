from django.db.models import Manager
from base.choices import ENABLE


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class PublishedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ENABLE)


class PublishedKeyManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ENABLE)

from django.core.management.base import BaseCommand
from article.models import Article
from base.hashgeo import to_hash_fields
from django_bulk_update.helper import bulk_update
from datetime import datetime
from django.conf import settings

batch_size = settings.HASH_FIELD_BATCH_SIZE


class Command(BaseCommand):
    help = 'Gen hash field'
    shebang_line = '#!/usr/bin/env bash'

    def handle(self, *args, **options):
        print(datetime.now())
        articles = Article.objects.all()
        for obj in articles:
            if obj.longitude and obj.latitude:
                fields = to_hash_fields(lon=obj.longitude, lat=obj.latitude)
                for attr, value in fields.items():
                    setattr(obj, attr, value)
        bulk_update(articles, batch_size=batch_size)
        print(datetime.now())
        self.stdout.write(self.style.SUCCESS('Successfully to hash field !!'))

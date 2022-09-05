from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from base.utils import clean_html
from culture.models import Culture


class Command(BaseCommand):
    help = 'Gen content'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                print(datetime.now())
                cultures = Culture.objects.all()
                for culture in cultures:
                    culture.content_exclude_html = clean_html(culture.content)
                    culture.save()
                print(datetime.now())

            self.stdout.write(self.style.SUCCESS('Successfully gen content !!'))
        except Exception as e:
            raise CommandError('Fail clear !\nReason: {}'.format(e))

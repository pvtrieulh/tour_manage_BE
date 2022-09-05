from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Cache clear'

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write('Cache clear success\n')

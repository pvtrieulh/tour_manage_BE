from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from base.models import Option


class Command(BaseCommand):
    help = 'Gen user'
    shebang_line = '#!/usr/bin/env bash'

    def handle(self, *args, **options):

        try:
            admin = User.objects.get(username='admin')
            if not Option.objects.filter(user_id=admin.user.id):
                Option.objects.create(
                    user=admin,
                    option='superuser',
                )

            self.stdout.write(self.style.SUCCESS('Successfully add option to admin !!'))

        except User.DoesNotExist:
            raise CommandError('username admin does not exist')

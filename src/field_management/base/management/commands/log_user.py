from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

import pandas as pd

LOG_PATH = 'logs/wp_check.log'
LOG_TMP = 'LAST LOGIN: {:>30} | PW CHANGED: {} | INFO: {}'


class Command(BaseCommand):
    help = 'log user'
    shebang_line = '#!/usr/bin/env bash'

    def log(self, msg):
        with open(LOG_TMP, 'w+') as f:
            f.write(msg)
        self.stdout.write(msg)

    def desc_user(self, data):
        return '{:>25}-{:>5} [{:>30}]'.format(data['Họ và tên'], data['Ban'], data['User'])

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        file = options.get('file')
        users = pd.read_excel(file)

        valid_users = []
        invalid_users = []
        not_founds = []

        for idx, data in users.iterrows():

            uid = data['User']
            desc = self.desc_user(data)
            self.log('scanning: {}'.format(uid))

            try:
                user = User.objects.get(username=uid)
                pw = data['Pass']
                pw_changed = not user.check_password(pw)

                msg = LOG_TMP.format(
                    # user.username,
                    # user.is_active,
                    str(user.last_login),
                    pw_changed,
                    desc
                )
                # self.log(msg)
                if pw_changed:
                    valid_users.append(msg)
                else:
                    invalid_users.append(msg)

            except Exception as e:
                msg = 'NOT FOUND idx: {:>5} - {:>5} | {}'.format(idx, uid, desc)
                not_founds.append(msg)
                # self.log('idx: {} - {} not found'.format(idx, uid))

        self.log('VALID: \n')
        for msg in valid_users:
            self.log(msg)
        self.log('\n\n')

        self.log('INVALID: \n')
        for msg in invalid_users:
            self.log(msg)
        self.log('\n\n')

        self.log('NOT FOUND: \n')
        for msg in not_founds:
            self.log(msg)
        self.log('\n\n')

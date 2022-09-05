from django.core.management.base import BaseCommand
import pandas
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Gen user'
    shebang_line = '#!/usr/bin/env bash'

    def handle(self, *args, **options):

        df = pandas.read_csv('data/master/tk_aic.csv')
        with open('scripts/gen_supereditor.sh', 'w') as output_file:
            output_file.write(self.shebang_line)
            output_file.write('\n')
            for i in range(df['User'].count()):
                if User.objects.filter(username=df['User'][i]).exists():
                    continue

                per = df['vaitro'][i]
                per = per.split('/')[1].strip()
                if per == 'Admin':
                    permission = 'createsupereditor'
                    str = 'python manage.py ' + permission + ' --username ' + df['User'][i] \
                          + ' --password ' + df['Pass'][i] + ' --noinput --email ' + df['Pass'][i] + '.com'
                    output_file.write(str)
                    output_file.write('\n')

        with open('scripts/gen_editor.sh', 'w') as output_file:
            output_file.write(self.shebang_line)
            output_file.write('\n')
            for i in range(df['User'].count()):
                if User.objects.filter(username=df['User'][i]).exists():
                    continue

                per = df['vaitro'][i]
                per = per.split('/')[1].strip()
                if per == 'Editor':
                    permission = 'createeditor'
                    str = 'python manage.py ' + permission + ' --username ' + df['User'][i] \
                          + ' --password ' + df['Pass'][i] + ' --noinput --email ' + df['Pass'][i] + '.com'
                    output_file.write(str)
                    output_file.write('\n')

        output_file.close()

        self.stdout.write(self.style.SUCCESS('Successfully gen user !!'))

import logging, requests
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.conf import settings
from pathlib import Path


class Command(BaseCommand):
    help = 'Dump db with init data, option: --action=dump|load'
    folder_data = None

    def add_arguments(self, parser):
        parser.add_argument('-d', '--action', type=str, nargs='?')

    def handle(self, *args, **options):
        self.get_folder_data()
        if options['action'] == 'load':
            return self.load_data()
        if options['action'] == 'dump':
            return self.dump_data()
        print('argument action require: --action=dump|load')
        return None

    def get_folder_data(self):
        self.folder_data = os.path.join(settings.ROOT_PROJ_DIR, 'data', 'init_json')
        Path(self.folder_data).mkdir(parents=True, exist_ok=True)

    def load_data(self):
        path_data = Path(self.folder_data)
        if not path_data.exists():
            print('Not found folder data/init_json')
            return None
        print('Load begin...')
        for file in os.listdir(path_data):
            call_command('loaddata', os.path.join(path_data, file))
        print('Load end...')

    def dump_data(self):
        print('dump begin...')
        datas = [
            'organization.organization',
            'syndication.categoryprocesslearning',
            'dao_tao.language',
            'location.country',
            'app_image.appimage',
            'pages.appstatus',
            'pages.applanguage',
            'cron_job.crontask',
        ]
        for i in datas:
            self.write_file_data(i)
        print('dump sucess')

    def write_file_data(self, app_data):
        with open('{folder}/{app}.json'.format(folder=self.folder_data, app=app_data), 'w+') as f:
            call_command('dumpdata', app_data, '--indent=2', stdout=f)
            print('----: {app}'.format(app=app_data))
        f.closed

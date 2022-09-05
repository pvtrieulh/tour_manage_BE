from django.core.management.base import BaseCommand, CommandError

import os
import requests
from urllib.parse import urlparse
from django.core.files import File

def vb_url_to_s3(o, redownload=False):
    if not o.url:
        return
    if o.s3_url and not redownload:
        return

    print('downloading ', o.url)
    r = requests.get(o.url)
    filename = os.path.basename(urlparse(o.url).path)

    with open('tmp/{}'.format(filename), 'wb') as tf:
        tf.write(r.content)

    with open('tmp/{}'.format(filename), 'rb') as tf:
        o.s3_url.save(filename, File(tf), save=True)

    os.remove('tmp/{}'.format(filename))
    print(o.url, 'done')


class Command(BaseCommand):
    help = 'download vbe audio to s3'

    def handle(self, *args, **options):
        from culture.models import Voice as CultureVoice
        from story_book.models import Voice as StoryVoice

        print('processing {} - Culture Voice '.format(CultureVoice.objects.count()))
        for voice in CultureVoice.objects.all():
            vb_url_to_s3(voice, False)

        print('processing {} - Story Voice '.format(StoryVoice.objects.count()))
        for voice in StoryVoice.objects.all():
            vb_url_to_s3(voice, False)






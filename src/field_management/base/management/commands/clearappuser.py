from django.core.management.base import BaseCommand, CommandError
from fcm_django.models import FCMDevice
from django.db import transaction

from feedback.models import Feedback
from personal.models import Personal, MyTimeline, PersonalTimeline, PersonalBookmark, PersonalFcmDevice, \
    BlacklistToken, PushNotification

from notification.models import Notification
from photo_contest.models import PhotoContest


class Command(BaseCommand):
    help = 'Clear App User'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                Feedback.objects.all().delete()
                MyTimeline.objects.all().delete()
                PersonalBookmark.objects.all().delete()
                PersonalFcmDevice.objects.all().delete()
                FCMDevice.objects.all().delete()
                BlacklistToken.objects.all().delete()
                Notification.objects.all().delete()
                PhotoContest.objects.all().delete()
                Personal.objects.all().delete()
                PersonalTimeline.objects.all().delete()
                PushNotification.objects.all().delete()

            self.stdout.write(self.style.SUCCESS('Successfully clear app user !!'))
        except Exception as e:
            raise CommandError('Fail clear !\nReason: {}'.format(e))

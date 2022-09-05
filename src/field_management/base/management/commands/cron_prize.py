from itertools import islice

from django.core.management.base import BaseCommand, CommandError

from base.models import base_filter
from prize.choices import CARD2, CARD5, CARD4, CARD3, UNTAKEN, TAKEN
from prize.models import PrizeTurn, PrizeToday, PhoneCard


class Command(BaseCommand):
    help = 'Cron prize'
    shebang_line = '#!/usr/bin/env bash'

    def handle(self, *args, **options):

        try:
            PrizeTurn.objects.all().delete()  # không có cũng k sao, có cho bớt nặng db
            phone_card = base_filter(PhoneCard).filter(card_status=UNTAKEN)
            phone_card_50 = phone_card.filter(card_value=CARD2)[:540]
            phone_card_100 = phone_card.filter(card_value=CARD3)[:115]
            phone_card_200 = phone_card.filter(card_value=CARD4)[:75]
            phone_card_500 = phone_card.filter(card_value=CARD5)[:40]

            arr_phone_card = list(phone_card_50) + list(phone_card_100) + list(phone_card_200) + list(phone_card_500)

            # batch_size = 500
            #
            # objs = (PrizeToday(card_value=ele.card_value,
            #                    card_type=ele.card_type,
            #                    card_serial=ele.card_serial,
            #                    card_code=ele.card_code, ) for ele in arr_phone_card)
            # while True:
            #     batch = list(islice(objs, batch_size))
            #     if not batch:
            #         break
            #     PrizeToday.objects.bulk_create(batch, batch_size)

            for ele in arr_phone_card:
                ele.card_status = TAKEN
                ele.save()
                PrizeToday.objects.create(
                    card_value=ele.card_value,
                    card_type=ele.card_type,
                    card_serial=ele.card_serial,
                    card_code=ele.card_code,
                )

            self.stdout.write(self.style.SUCCESS('Successfully cron prize !!'))

        except Exception as e:
            raise CommandError('Fail cron prize !\nReason: {}'.format(e))

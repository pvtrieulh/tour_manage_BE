from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission, Group
from article.models import Category
from pages.models import AppStatus, REVIEWING

from base.choices import AR_CT_1, AR_CT_9, AR_CT_8, AR_CT_7, AR_CT_6, AR_CT_5, AR_CT_4, AR_CT_3, AR_CT_2, \
    AR_CT_10, AR_CT_11, AR_CT_12, AR_CT_13, AR_CT_14, AR_CT_15, AR_CT_16, AR_CT_17, AR_CT_18, AR_CT_19, AR_CT_20, \
    AR_CT_1_OLD, AR_CT_9_OLD, AR_CT_8_OLD, AR_CT_7_OLD, AR_CT_6_OLD, AR_CT_5_OLD, AR_CT_4_OLD, AR_CT_3_OLD, AR_CT_2_OLD, \
    AR_CT_21


class Command(BaseCommand):
    help = 'Make init data'

    def handle(self, *args, **options):

        try:
            Category.objects.filter(name=AR_CT_1_OLD).update(name=AR_CT_1)
            Category.objects.filter(name=AR_CT_2_OLD).update(name=AR_CT_2)
            Category.objects.filter(name=AR_CT_3_OLD).update(name=AR_CT_3)
            Category.objects.filter(name=AR_CT_4_OLD).update(name=AR_CT_4)
            Category.objects.filter(name=AR_CT_5_OLD).update(name=AR_CT_5)
            Category.objects.filter(name=AR_CT_6_OLD).update(name=AR_CT_6)
            Category.objects.filter(name=AR_CT_7_OLD).update(name=AR_CT_7)
            Category.objects.filter(name=AR_CT_8_OLD).update(name=AR_CT_8)
            Category.objects.filter(name=AR_CT_9_OLD).update(name=AR_CT_9)
        except Exception:
            raise CommandError('rename fail')

        try:
            Category.objects.get(name=AR_CT_1)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_1
            )
        try:
            Category.objects.get(name=AR_CT_2)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_2
            )
        try:
            Category.objects.get(name=AR_CT_3)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_3
            )
        try:
            Category.objects.get(name=AR_CT_4)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_4
            )
        try:
            Category.objects.get(name=AR_CT_5)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_5
            )
        try:
            Category.objects.get(name=AR_CT_6)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_6
            )
        try:
            Category.objects.get(name=AR_CT_7)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_7
            )
        try:
            Category.objects.get(name=AR_CT_8)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_8
            )
        try:
            Category.objects.get(name=AR_CT_9)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_9
            )
        try:
            Category.objects.get(name=AR_CT_10)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_10
            )
        try:
            Category.objects.get(name=AR_CT_11)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_11
            )
        try:
            Category.objects.get(name=AR_CT_12)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_12
            )
        try:
            Category.objects.get(name=AR_CT_13)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_13
            )
        try:
            Category.objects.get(name=AR_CT_14)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_14
            )
        try:
            Category.objects.get(name=AR_CT_15)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_15
            )
        try:
            Category.objects.get(name=AR_CT_16)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_16
            )
        try:
            Category.objects.get(name=AR_CT_17)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_17
            )
        try:
            Category.objects.get(name=AR_CT_18)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_18
            )
        try:
            Category.objects.get(name=AR_CT_19)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_19
            )

        try:
            Category.objects.get(name=AR_CT_20)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_20
            )

        try:
            Category.objects.get(name=AR_CT_21)
        except Category.DoesNotExist:
            Category.objects.create(
                name=AR_CT_21
            )

        # group super_editor
        try:
            group_super_editor = Group.objects.get(name='super_editor')
        except Group.DoesNotExist:
            Group.objects.create(
                name='super_editor'
            )
            group_super_editor = Group.objects.get(name='super_editor')

        permissions = Permission.objects.filter(codename__contains='add_prize')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='change_prize')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='view_prize')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='delete_prize')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='add_homesetting')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='change_homesetting')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='view_homesetting')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='delete_homesetting')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='view_phonecard')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='view_prizehistory')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='view_prizetoday')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename='add_subcategory')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename='change_subcategory')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename='view_subcategory')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename='delete_subcategory')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='add_audio')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='change_audio')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='view_audio')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='delete_audio')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='add_voice')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='change_voice')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='view_voice')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='delete_voice')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename='add_category')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename='change_category')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename='view_category')
        for ele in permissions:
            group_super_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename='delete_category')
        for ele in permissions:
            group_super_editor.permissions.add(ele)

        permission = Permission.objects.get(codename='add_article')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_article')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_article')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_article')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_articlemetafield')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_articlemetafield')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_articlemetafield')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_articlemetafield')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_articleimage')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_articleimage')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_articleimage')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_articleimage')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_culture')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_culture')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_culture')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_culture')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.filter(codename='add_dateyinyang')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='change_dateyinyang')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='view_dateyinyang')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='delete_dateyinyang')
        for per in permission:
            group_super_editor.permissions.add(per)

        permission = Permission.objects.get(codename='add_greeting')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_greeting')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_greeting')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_greeting')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_tuvi')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_tuvi')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_tuvi')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_tuvi')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_youtube')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_youtube')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_youtube')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_youtube')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.filter(codename='add_ageintothehouse')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='change_ageintothehouse')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='view_ageintothehouse')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='delete_ageintothehouse')
        for per in permission:
            group_super_editor.permissions.add(per)

        permission = Permission.objects.get(codename='add_pushnotification')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_pushnotification')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_pushnotification')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_pushnotification')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_storybook')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_storybook')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_storybook')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_storybook')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_chapter')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_chapter')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_chapter')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_chapter')
        group_super_editor.permissions.add(permission)

        permission = Permission.objects.filter(codename='add_xuathanh')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='change_xuathanh')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='view_xuathanh')
        for per in permission:
            group_super_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='delete_xuathanh')
        for per in permission:
            group_super_editor.permissions.add(per)

        permission = Permission.objects.get(codename='add_dailymsg')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_dailymsg')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_dailymsg')
        group_super_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_dailymsg')
        group_super_editor.permissions.add(permission)

        # group editor
        try:
            group_editor = Group.objects.get(name='editor')
        except Group.DoesNotExist:
            Group.objects.create(
                name='editor'
            )
            group_editor = Group.objects.get(name='editor')

        permissions = Permission.objects.filter(codename__contains='add_audio')
        for ele in permissions:
            group_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='change_audio')
        for ele in permissions:
            group_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='view_audio')
        for ele in permissions:
            group_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='delete_audio')
        for ele in permissions:
            group_editor.permissions.add(ele)

        permissions = Permission.objects.filter(codename__contains='add_voice')
        for ele in permissions:
            group_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='change_voice')
        for ele in permissions:
            group_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='view_voice')
        for ele in permissions:
            group_editor.permissions.add(ele)
        permissions = Permission.objects.filter(codename__contains='delete_voice')
        for ele in permissions:
            group_editor.permissions.add(ele)

        permission = Permission.objects.get(codename='add_article')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_article')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_article')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_article')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_articlemetafield')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_articlemetafield')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_articlemetafield')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_articlemetafield')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_articleimage')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_articleimage')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_articleimage')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_articleimage')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_culture')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_culture')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_culture')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_culture')
        group_editor.permissions.add(permission)

        permission = Permission.objects.filter(codename='add_dateyinyang')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='change_dateyinyang')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='view_dateyinyang')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='delete_dateyinyang')
        for per in permission:
            group_editor.permissions.add(per)

        permission = Permission.objects.get(codename='add_greeting')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_greeting')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_greeting')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_greeting')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_tuvi')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_tuvi')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_tuvi')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_tuvi')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_youtube')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_youtube')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_youtube')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_youtube')
        group_editor.permissions.add(permission)

        permission = Permission.objects.filter(codename='add_ageintothehouse')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='change_ageintothehouse')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='view_ageintothehouse')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='delete_ageintothehouse')
        for per in permission:
            group_editor.permissions.add(per)

        permission = Permission.objects.get(codename='add_pushnotification')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_pushnotification')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_pushnotification')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_pushnotification')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_storybook')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_storybook')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_storybook')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_storybook')
        group_editor.permissions.add(permission)

        permission = Permission.objects.get(codename='add_chapter')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_chapter')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_chapter')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_chapter')
        group_editor.permissions.add(permission)

        permission = Permission.objects.filter(codename='add_xuathanh')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='change_xuathanh')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='view_xuathanh')
        for per in permission:
            group_editor.permissions.add(per)
        permission = Permission.objects.filter(codename='delete_xuathanh')
        for per in permission:
            group_editor.permissions.add(per)

        permission = Permission.objects.get(codename='add_dailymsg')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='change_dailymsg')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='view_dailymsg')
        group_editor.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_dailymsg')
        group_editor.permissions.add(permission)

        AppStatus.objects.create(app_status=REVIEWING)

        self.stdout.write(self.style.SUCCESS('Successfully create init data !!'))

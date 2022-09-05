# import re
from django.contrib import admin
# from django.utils.safestring import mark_safe
# from .models import HomeSetting, SyncScore, CareerOrderRequest
# from .forms import *
# import datetime
# from django.contrib.auth.models import User
# # Register your models here.
#
#
# class BaseModelAdmin(admin.ModelAdmin):
#     exclude = ['created_by', 'updated_by', 'published_by', 'published_at']
#     form = BaseForm
#
#     def has_delete_permission(self, request, obj=None):
#         if request.user:
#             if request.user.is_superuser:
#                 return True
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         if obj:
#             try:
#                 op = Option.objects.get(user_id=request.user.id)
#                 if op.option == EDITOR and obj.status == PUBLISHED:
#                     return False
#             except Option.DoesNotExist:
#                 pass
#         return True
#
#     def save_model(self, request, obj, form, change):
#         obj.deleted = False
#
#         if obj.status == PUBLISHED:
#             obj.published_by = request.user.id
#             obj.published_at = str(datetime.datetime.now())
#
#         if not change:
#             obj.created_by = request.user.id
#         else:
#             obj.updated_by = request.user.id
#
#         obj.save()
#
#     def get_queryset(self, request):
#         qs = super(BaseModelAdmin, self).get_queryset(request)
#         try:
#             op = Option.objects.get(user_id=request.user.id)
#             if op.option == EDITOR:
#                 return qs.filter(created_by=request.user.id)
#         except Option.DoesNotExist:
#             pass
#         return qs
#
#     def get_form(self, request, obj=None, **kwargs):
#         has_change_permission = self.has_change_permission(request, obj)
#         if not has_change_permission and obj:
#             try:
#                 obj.content = re.sub(r">\s*<", "><", obj.content)
#                 obj.content = mark_safe(obj.content)
#             except AttributeError:
#                 pass
#
#             try:
#                 obj.interpretation = re.sub(r">\s*<", "><", obj.interpretation)
#                 obj.interpretation = mark_safe(obj.interpretation)
#             except AttributeError:
#                 pass
#
#             try:
#                 obj.content_html = re.sub(r">\s*<", "><", obj.content_html)
#                 obj.content_html = mark_safe(obj.content_html)
#             except AttributeError:
#                 pass
#
#         base_form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
#
#         class BaseAdminFormWithRequest(base_form):
#             def __new__(cls, *args, **kwargs):
#                 kwargs['request'] = request
#                 return base_form(*args, **kwargs)
#
#         return BaseAdminFormWithRequest
#
#     def published_user(self, obj):
#         if not obj.published_by:
#             return None
#         try:
#             user = User.objects.get(id=obj.published_by)
#         except User.DoesNotExist:
#             return "-"
#
#         return str(user.username)
#
#     def updated_user(self, obj):
#         if not obj.updated_by:
#             return None
#         try:
#             user = User.objects.get(id=obj.updated_by)
#         except User.DoesNotExist:
#             return "-"
#
#         return str(user.username)
#
#     def author(self, obj):
#         if not obj.created_by:
#             return None
#         try:
#             user = User.objects.get(id=obj.created_by)
#         except User.DoesNotExist:
#             return "-"
#
#         return str(user.username)
#
#     updated_user.short_description = 'Người cập nhập'
#     published_user.short_description = 'Người đăng tải'
#     author.short_description = 'Người tạo'
#     author.allow_tags = False
#
#
# class SyncScoreAdmin(admin.ModelAdmin):
#     list_display = ['id', 'minscore', 'maxscore', 'module_name', 'method']
#     list_filter = ['module_name']
#
#
# admin.site.register(SyncScore, SyncScoreAdmin)
# admin.site.register(CareerOrderRequest)


class BaseModelAdmin(admin.ModelAdmin):
    actions = ['make_published', 'make_unpublished']

    def created_at_format(self, obj):
        return obj.created_at.strftime("%H:%M %d/%m/%Y") if obj.created_at else '-'

    def updated_at_format(self, obj):
        return obj.updated_at.strftime("%H:%M %d/%m/%Y") if obj.updated_at else '-'

    def make_published(self, request, queryset):
        rows_published = queryset.update(status=True)
        self.message_user(request, "%s được phát hành thành công." % rows_published)
    make_published.short_description = "Phát hành các khóa đào tạo đã chọn"

    def make_unpublished(self, request, queryset):
        rows_published = queryset.update(status=False)
        self.message_user(request, "%s đã được bỏ phát hành thành công." % rows_published)
    make_unpublished.short_description = "Bỏ phát phát hành các khóa đào tạo đã chọn"

    class Meta:
       abstract = True

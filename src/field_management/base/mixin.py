from django.contrib.auth.models import User
from rest_framework import viewsets



class BaseMixin(object):
    def published_user(self, obj):
        if not obj.published_by:
            return None
        try:
            user = User.objects.get(id=obj.published_by)
        except User.DoesNotExist:
            return "-"

        return str(user.username)

    def updated_user(self, obj):
        if not obj.updated_by:
            return None
        try:
            user = User.objects.get(id=obj.updated_by)
        except User.DoesNotExist:
            return "-"

        return str(user.username)

    def author(self, obj):
        if not obj.created_by:
            return None
        try:
            user = User.objects.get(id=obj.created_by)
        except User.DoesNotExist:
            return "-"

        return str(user.username)

    updated_user.short_description = 'Người cập nhập'
    published_user.short_description = 'Người đăng tải'
    author.short_description = 'Người tạo'
    author.allow_tags = False


class MixedPermissionModelViewSet(viewsets.ModelViewSet):
   '''
   Mixed permission base model allowing for action level
   permission control. Subclasses may define their permissions
   by creating a 'permission_classes_by_action' variable.

   Example:
   permission_classes_by_action = {'list': [AllowAny],
                                   'create': [IsAdminUser]}
   '''

   permission_classes_by_action = {}

   def get_permissions(self):
      try:
        # return permission_classes depending on `action`
        return [permission() for permission in self.permission_classes_by_action[self.action]]
      except KeyError:
        # action is not set return default permission_classes
        return [permission() for permission in self.permission_classes]
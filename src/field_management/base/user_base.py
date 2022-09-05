from django.db import models
from rest_framework import serializers

from base.models import BaseModel
from st_admin.models import AdminModel
from st_business.models import BusinessModel
from st_personal.models import PersonalModel
from st_auth.constant import MODE_AUTH_CHOICE


class AuthAvatarBaseSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return obj.get_avatar()

    class Meta:
        model = PersonalModel
        fields = [
            'avatar',
        ]


class PersonalSerializer(AuthAvatarBaseSerializer):
    class Meta:
        model = PersonalModel
        fields = [
            'id',
            'name',
            'avatar'
        ]


class AdminSerializer(AuthAvatarBaseSerializer):
    class Meta:
        model = AdminModel
        fields = [
            'id',
            'name',
            'avatar'
        ]


class BusinessSerializer(AuthAvatarBaseSerializer):
    class Meta:
        model = BusinessModel
        fields = [
            'id',
            'name',
            'avatar'
        ]


class RelatedUser(models.Model):
    admin = models.ForeignKey(AdminModel,on_delete= models.CASCADE,  null=True, related_name="+")
    personal = models.ForeignKey(PersonalModel, on_delete = models.CASCADE , null=True, related_name="+")
    business = models.ForeignKey(BusinessModel,on_delete=models.CASCADE, null=True, related_name="+")

    class Meta:
        abstract = True


def relation_user(instance):
    try:
        if instance.personal:
            return PersonalSerializer(instance.personal).data
        if instance.business:
            return BusinessSerializer(instance.business).data
        if instance.admin:
            return AdminSerializer(instance.admin).data
        return None
    except:
        return None


def check_model_auth(request):
    try: 
        user = request.user
        if isinstance(user, BusinessModel):
            return {'business': user.id}
        elif isinstance(user, AdminModel):
            return {'admin': user.id}
        else:
            return {'personal': user.id}
        return None
    except:
        return None


class UserInfoTypeAbstract(BaseModel):
    user_id = models.PositiveIntegerField(verbose_name="Người dùng")
    user_mod = models.SmallIntegerField(verbose_name="Loại người dùng", choices=MODE_AUTH_CHOICE)

    class Meta:
        abstract = True

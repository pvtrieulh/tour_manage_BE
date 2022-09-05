from rest_framework import serializers

from base.utils import format_datetime
from base.validators import validate_file_size_image, validate_file_extension_image
from st_auth.helpers import json_auth_base_data
from .choices import RATE_MAX_FILE


class RateGallerySerializer(serializers.Serializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        return obj.get('file').url if obj.get('file') else None


class RateListBaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    comment = serializers.CharField()
    created_at = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return format_datetime(obj.created_at)

    def get_user(self, obj):
        return json_auth_base_data(authors=self.context.get('authors'), obj=obj)

    def get_gallery(self, obj):
        collection = self.context.get('gallery')
        if not collection:
            return None
        item = collection.get(obj.id)
        if not item:
            return None
        return RateGallerySerializer(item, many=True).data


class CommentListSerializer(RateListBaseSerializer):
    like_count = serializers.IntegerField()
    is_like = serializers.SerializerMethodField()
    reply_count = serializers.IntegerField()
    reply = serializers.SerializerMethodField()

    def get_is_like(self, obj):
        is_like = self.context.get('is_like')
        if not is_like:
            return False
        return True if is_like.get(obj.id) else False

    def get_reply(self, obj):
        collection = self.context.get('reply')
        if not collection:
            return None
        item = collection.get(obj.id)
        if not item:
            return None
        return RateListBaseSerializer(item, many=True,  context={
            'authors': self.context.get('authors'),
            'gallery': self.context.get('gallery_reply'),
        }).data


class RateListSerializer(CommentListSerializer):
    rate = serializers.IntegerField()


class RateCreateSerializer(serializers.Serializer):
    rate = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField()


class RateCreateResponseSerializer(RateListSerializer):
    approve = serializers.IntegerField()
    word_rule = serializers.SerializerMethodField()

    def get_word_rule(self, obj):
        return self.context.get('word_rule')


class RateReplyCreateSerializer(serializers.Serializer):
    comment = serializers.CharField()


class RateReplyCreateResponseSerializer(RateListBaseSerializer):
    approve = serializers.IntegerField()
    word_rule = serializers.SerializerMethodField()

    def get_word_rule(self, obj):
        return self.context.get('word_rule')


class RateReplyListStatusSerializer(RateListBaseSerializer):
    status = serializers.IntegerField()
    approve = serializers.IntegerField()
    reason_un = serializers.CharField()


class RateGalleryCreateSerializer(serializers.Serializer):
    image = serializers.ListField(child=serializers.FileField(
        allow_empty_file=False,
        use_url=False,
        validators=[validate_file_size_image, validate_file_extension_image]
    ), max_length=RATE_MAX_FILE)
    rate_id = serializers.IntegerField(allow_null=True, required=False)
    reply_id = serializers.IntegerField(allow_null=True, required=False)

    def bulk_create(self, model_gallery):
        validated_data = self.validated_data
        image = validated_data.pop('image')
        objs = []
        for img in image:
            file = model_gallery(file=img, rate_id=validated_data.get('rate_id'), reply_id=validated_data.get('reply_id'))
            objs.append(file)
        return model_gallery.objects.bulk_create(objs)


class RateSingleItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rate = serializers.IntegerField()
    comment = serializers.CharField()
    created_at = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
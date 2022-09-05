import re
from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr
from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.db.models import Avg
from rest_framework import serializers

from base.map_url import MAP_URL_API_WEB, SCHEMA_HOST_WEB
from base.validators import validate_file_extension_image, validate_file_size_image, \
    validate_file_extension_attach_files, validate_file_size_v2, validate_file_extension_doc
from base.choices import *
from base.utils import format_datetime
from pages.models import AppVersion


class BaseSerializer(serializers.ModelSerializer):
    pass


class BaseTimeSerializer(BaseSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return format_datetime(obj.created_at)

    def get_updated_at(self, obj):
        return format_datetime(obj.updated_at)


class ImagesSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(validators=[validate_file_extension_image, validate_file_size_image])
    )

    def validate_images(self, data):
        max_images = settings.MAX_IMAGE_LENGTH
        if len(data) > max_images:
            raise serializers.ValidationError("Bạn chỉ được tải tối đa {} ảnh.".format(max_images))


class FilesAttachSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(validators=[validate_file_extension_attach_files, validate_file_size_v2])
    )


class FilesSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(validators=[validate_file_extension_doc, validate_file_size_v2])
    )


class HomeSearchSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    view_quantity = serializers.SerializerMethodField()
    published_at = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    category_text = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'id',
            'title',
            'link',
            'cover_url',
            'view_quantity',
            'published_at',
            'content_type',
            'category_text',
            'category',
        ]

    def get_id(self, obj):
        return obj.id

    def get_link(self, obj):
        request = self.context['request']
        base_url = request.build_absolute_uri().replace(request.get_full_path(), '')
        full_path = reverse('api-culture:culture-detail',
                            args=[obj.id]) if obj.table_name == HOME_SEARCH_TABLE_CULTURE else reverse(
            'api-article:article-detail-v2', args=[obj.id]
        )
        return '{}{}'.format(base_url, full_path)

    def get_cover_url(self, obj):
        return obj.cover_url.url if obj.cover_url else None

    def get_title(self, obj):
        return obj.title

    def get_view_quantity(self, obj):
        return obj.view_quantity

    def get_published_at(self, obj):
        return obj.published_at.strftime("%H:%M %d/%m/%Y") if obj.published_at else None

    def get_category(self, obj):
        return obj.category_name

    def get_category_text(self, obj):
        return TEXT_TYPE_HOME_SEARCH[obj.table_name]

    def get_content_type(self, obj):
        return obj.table_name


class AppVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppVersion
        fields = (
            'app_status',
            'version',
            'os',
            'last_version',
        )


class PrimaryKeyRelatedListField(serializers.ListField):
    def __init__(self, queryset=None, **kwargs):
        assert queryset is not None, 'queryset must be specified for PrimaryKeyRelatedListField'
        self.child = serializers.PrimaryKeyRelatedField(queryset=queryset)
        super().__init__(**kwargs)

    def get_value(self, dictionary):
        dictionary = dictionary.copy()

        keys = []
        for k, _ in dictionary.items():
            if k.startswith(f'{self.field_name}['):
                keys.append(k)
        for k in keys:
            dictionary.appendlist(self.field_name, dictionary.getlist(k)[0])

        return super().get_value(dictionary)

    def to_representation(self, data):
        return super().to_representation(data.all())


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """
    validators = [validate_file_size_image, validate_file_extension_image]

    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except Exception:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ShareUrlSerializer(serializers.ModelSerializer):
    share_url = serializers.SerializerMethodField()

    class Meta:
        fields = ['share_url']

    def get_share_url(self, obj):
        from base.middleware import get_request
        request = get_request()
        path = None
        for pattern, value in MAP_URL_API_WEB:
            if re.search(pattern, request.path):
                path = value
                if obj and hasattr(obj, 'id'):
                    path = path.replace('?', str(obj.id), 1)
        if request and path:
            slug = request.GET.get('slug') if request.GET.get('slug') else ""
            return SCHEMA_HOST_WEB + path + slug
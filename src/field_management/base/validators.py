import datetime
import json
import os
import facebook
import re
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from rest_framework import status
from validate_email import validate_email
from zalo.sdk.app import ZaloAppInfo, Zalo3rdAppClient
from google.oauth2 import id_token
from google.auth.transport import requests

from base.api.exceptions import BadRequestException, NotFoundException
from .choices import EXTENSIONS_LIST, PROVIDER_FACEBOOK, PROVIDER_GOOGLE, PROVIDER_ZALO, PROVIDER_APPLE


def int_checker(val):
    try:
        int(val)
        return True
    except Exception:
        return False


def float_checker(val):
    try:
        float(val)
        return True
    except Exception:
        return False


def str_checker(val):
    return isinstance(val, str)


def is_list_int(data):
    try:
        return [int(item) for item in data]
    except Exception:
        return False


def image_size_checker(val, limit_size=1028):
    import sys

    valid = isinstance(val, InMemoryUploadedFile)
    if not valid:
        return False

    data_size = sys.getsizeof(val)
    return data_size <= limit_size


def latitude_checker(val):
    if val > 90 or val < -90:
        return False
    return True


def longitude_checker(val):
    if val > 180 or val < -180:
        return False
    return True


def is_valid(required_fields, data):
    for field in required_fields:
        field_name = field[0]
        field_checker = field[1]

        if field_name not in data or not data.get(field_name):
            raise BadRequestException('field: {} is required'.format(field_name))
        if field_checker and not field_checker(data[field_name]):
            raise BadRequestException('field: {} is invalid type'.format(field_name))


def dob_checker(data):
    if 'date_of_birth' in data:
        try:
            date_of_birth = data['date_of_birth']
            datetime.datetime.strptime(date_of_birth, '%Y-%m-%d')
        except Exception:
            raise BadRequestException('date_of_birth : incorrect data format, should be YYYY-MM-DD')


def lat_checker(data):
    if 'latitude' in data:
        is_float = float_checker(data['latitude'])
        if not is_float:
            raise BadRequestException('latitude must be a number')
        latitude = float(data['latitude'])
        valid_latitude = latitude_checker(latitude)
        if not is_float:
            raise BadRequestException('latitude must be a number')
        if not valid_latitude:
            raise BadRequestException('latitude must be a number and in range [-90.0, 90.0]')


def email_checker(data):
    if 'email' in data:
        if not validate_email(data['email']):
            raise NotFoundException(message="Invalid email!", status_code=status.HTTP_406_NOT_ACCEPTABLE)


def lon_checker(data):
    if 'longitude' in data:
        is_float = float_checker(data['longitude'])
        if not is_float:
            raise BadRequestException('longitude must be a number')
        longitude = float(data['longitude'])
        valid_longitude = longitude_checker(longitude)
        if not valid_longitude:
            raise BadRequestException('longitude must be a number and in range [-180.0, 180.0]')


def extra_info_checker(data):
    if 'extra_info' in data:
        try:
            extra_info = data['extra_info']
            json.loads(extra_info)
        except Exception:
            raise BadRequestException('extra_info : incorrect data format, should be a json format')


def content_type_checker(data, types):
    if 'content_type' in data:
        content_type = data['content_type']
        if content_type not in types:
            raise BadRequestException('content_type must be in {}'.format(types))


def content_type_existed(val, types):
    if val not in types:
        raise BadRequestException('content_type must be in {}'.format(types))


def content_id_checker(data):
    if 'content_id' in data:
        content_id = data['content_id']
        if not int_checker(content_id):
            raise BadRequestException('content_id must be int number')


def location_checker(data, fields, is_lat):
    for field in fields:
        if field in data:
            is_float = float_checker(data[field])
            if not is_float:
                raise BadRequestException('{} must be a number'.format(field))
            value = float(data[field])
            if not is_float:
                raise BadRequestException(' {} must be a number'.format(field))
            if is_lat and not latitude_checker(value):
                raise BadRequestException('{} must be a number and in range [-90.0, 90.0]'.format(field))
            elif not longitude_checker(value):
                raise BadRequestException('{} must be a number and in range [-180.0, 180.0]'.format(field))
        else:
            raise BadRequestException('field: {} is required'.format(field))


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File upload phải có định dạng là mp3')


def validate_file_extension_audio(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3', '.wma', '.wav', '.flac', '.aac']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File upload phải có định dạng là mp3')


def validate_file_size(value):
    filesize = value.file.size
    max_file_size = settings.MAX_FILE_SIZE
    if filesize > max_file_size * 1024 * 1024:
        raise ValidationError("Dung lượng file upload không được quá %sMB" % str(max_file_size))


def validate_file_size_v2(value):
    file_size = value.size
    max_file_size = settings.MAX_FILE_SIZE
    if file_size > max_file_size * 1024 * 1024:
        raise ValidationError("Dung lượng file upload không được quá %sMB" % str(max_file_size))


def verify_user_id(data):
    message_err = 'Thông tin người dùng không hợp lệ.'
    access_token = data.get('access_token')
    provider = data.get('provider')
    provider_id = data.get('provider_id')
    email = data.get('email')
    if provider == PROVIDER_FACEBOOK:
        verify = validate_access_token_facebook(access_token, provider_id, email)
    elif provider == PROVIDER_ZALO:
        verify = validate_access_token_zalo(access_token, provider_id)
    elif provider == PROVIDER_GOOGLE:
        verify = validate_access_token_google(access_token, provider_id, email)
    elif provider == PROVIDER_APPLE:
        verify = True
    else:
        verify = False
    if not verify:
        raise BadRequestException(message_err)


def validate_access_token_facebook(access_token, uid, email):
    verify_token = False
    try:
        graph = facebook.GraphAPI(access_token=access_token)
        args = {'fields': 'id, email, name', }
        profile = graph.get_object('me', **args)
        verify_token = profile['id'] == uid and (profile.get('email') == email or email is None)
    except Exception as _:
        pass
    return verify_token


def validate_access_token_zalo(access_token, uid):
    # TODO test zalo not return access token
    return True
    verify_token = False
    try:
        zalo_info = ZaloAppInfo(app_id=settings.ZALO_APP_ID, secret_key=settings.ZALO_APP_SECRET, callback_url="")
        zalo_3rd_app_client = Zalo3rdAppClient(zalo_info)
        profile = zalo_3rd_app_client.get('/me', access_token, {'fields': 'id'})
        verify_token = profile['id'] == uid
    except Exception as _:
        pass
    return verify_token


def validate_access_token_google(access_token, uid, email):
    verify_token = False
    try:
        idinfo = id_token.verify_oauth2_token(access_token, requests.Request())
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return False

        verify_token = idinfo['sub'] == uid and (email is None or email == idinfo.get('email'))
    except Exception as e:
        pass
    return verify_token


def validate_file_extension_doc(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.doc', '.docx', '.pdf', '.xls', '.xlsx']
    ext = re.sub("[^a-z0-9.]", "", ext.lower())
    if not ext in valid_extensions:
        raise ValidationError('File upload phải có định dạng là doc, docx hoặc pdf, xls, xlsx')


def validate_file_extension_pdf(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File upload phải có định dạng là pdf')


def validate_rate(value):
    try:
        rate = int(value)
        if not 0 < rate < 6:
            raise ValidationError('Rate must be in [1, 5]')
    except ValueError:
        raise ValidationError('Rate must be an integer')


def validate_email_field(value):
    if not validate_email(value):
        raise ValidationError('Email invalid')


def validate_upload_file(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.flv', '.mp4', '.m3u8', '.ts', '.3gp', '.mov', '.avi', '.wmv', '.png', '.jpeg', '.jpg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File upload phải có định dạng video hoặc ảnh')


def validate_file_size_image(value):
    file_size = value.size
    max_file_size = settings.MAX_IMAGE_SIZE
    if file_size > max_file_size * 1024 * 1024:
        raise ValidationError("Dung lượng file upload không được quá %sMB" % str(max_file_size))


def validate_file_extension_image(value):
    valid_extensions = ('.png', '.jpg', '.jpeg')
    if not value.name.lower().endswith(valid_extensions):
        raise ValidationError('File tải lên phải có định dạng là jpg, png hoặc jpeg')


def validate_file_extension_attach_files(value):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.doc', '.docx', '.pdf')
    if not value.name.lower().endswith(valid_extensions):
        raise ValidationError('File tải lên phải có định dạng là jpg, doc, pdf, png hoặc jpeg')


def validate_file_extension_office(value):
    valid_extensions = None

    for x in EXTENSIONS_LIST:
        if value.name.lower().endswith(x[1]):
            valid_extensions = x[0]
            break

    if valid_extensions:
        return valid_extensions

    raise ValidationError('File tải lên không đúng định dạng hoặc đã bị hư hỏng')


def validate_img_extension_hcdt(value):
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
    if not value.name.lower().endswith(valid_extensions):
        raise ValidationError('File tải lên phải có định dạng là jpg, png, jpeg, gif, tiff, bmp')


def validate_file_extension_hcdt(value):
    valid_extensions = ('.pdf', '.csv', '.txt', '.doc', '.dot', '.wbk', '.docx', '.docm', '.dotx', '.dotm', '.docb')
    if not value.name.lower().endswith(valid_extensions):
        raise ValidationError('File tải lên phải có định dạng là MS Word, pdf, csv, txt')


def validate_upload_file_video(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.flv', '.mp4', '.m3u8', '.ts', '.3gp', '.mov', '.avi', '.wmv', 'm4v']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File upload phải có định dạng video')


def validate_file_and_image(value):
    file_valid_extensions = ('.pdf', '.csv', '.txt', '.doc', '.dot', '.wbk', '.docx', '.docm', '.dotx', '.dotm', '.docb')
    image_valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
    sum_valid_extensions = file_valid_extensions + image_valid_extensions
    if not value.name.lower().endswith(sum_valid_extensions):
        raise ValidationError('File tải lên phải là văn bản hoặc hình ảnh')


def validate_audio_and_image(value):
    audio_valid_extensions = ('.mp3', '.wma', '.wav', '.flac', '.aac')
    image_valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
    sum_valid_extensions = audio_valid_extensions + image_valid_extensions
    if not value.name.lower().endswith(sum_valid_extensions):
        raise ValidationError('File tải lên phải là âm thanh hoặc hình ảnh')


def validate_file_and_image_v2(value):
    file_valid_extensions = ('.doc', '.docx', '.pdf', '.xls', '.xlsx')
    image_valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
    sum_valid_extensions = file_valid_extensions + image_valid_extensions
    if not value.name.lower().endswith(sum_valid_extensions):
        raise ValidationError('File tải lên phải là văn bản hoặc hình ảnh')


def validate_upload_video_mp4(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File upload phải có định dạng video mp4')

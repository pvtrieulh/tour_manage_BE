from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = ''
    file_overwrite = False


class MediaStorage(S3Boto3Storage):
    location = ''
    file_overwrite = False

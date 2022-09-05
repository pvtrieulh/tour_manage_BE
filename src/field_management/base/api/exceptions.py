from __future__ import unicode_literals

from rest_framework import status, exceptions
from rest_framework.response import Response
from django.conf import settings
from base.api.response import ErrorResponse
from base.utils import write_error


def my_error_handler(exc, *args):
    """
    Returns the response that should be used for any given exception.
    By default we handle the REST framework `APIException`, and some new exception we created...
    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['X-Throttle-Wait-Seconds'] = '%d' % exc.wait
        try:
            code = str(exc.detail.get('code'))
            if type(code) is str and code.isdigit():
                code = int(code)
            message = exc.detail.get('message')
        except:
            code = exc.status_code
            message = exc.detail
        return ErrorResponse(
            message=message,
            status=exc.status_code,
            code=code
        )

    if isinstance(exc, NotFoundException) or \
            isinstance(exc, PermissionDeniedException) or \
            isinstance(exc, ValidationException):

        return ErrorResponse(
            message=NotFoundException.get_message(exc),
            status=NotFoundException.get_status_code(exc),
            data=NotFoundException.get_data(exc),
        )

    if settings.DEBUG:
        # show full error trackback in api tool
        return None

    write_error(exc)
    bad_request = BadRequestException()
    return ErrorResponse(
        message=bad_request.get_message(),
        status=bad_request.get_status_code()
    )


class CustomAPIException(Exception):

    def __init__(self, message='Exception', status_code=status.HTTP_400_BAD_REQUEST, data=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.data = data

    def get_message(self):
        return self.message

    def get_status_code(self):
        return self.status_code

    def get_data(self):
        return self.data


class NotFoundException(CustomAPIException):
    message = 'Not found data.'
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message=message, status_code=status_code):
        super(NotFoundException, self).__init__(message=message, status_code=status_code)


class BadRequestException(CustomAPIException):
    message = 'Bad Request.'
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=message, status_code=status_code):
        super(BadRequestException, self).__init__(message=message, status_code=status_code)


class PermissionDeniedException(CustomAPIException):
    message = 'Permission Denied'
    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, message=message, status_code=status_code):
        super(PermissionDeniedException, self).__init__(message=message, status_code=status_code)


class ValidationException(CustomAPIException):
    message = 'validation error'
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    def __init__(self, message=message, status_code=status_code, data=None):
        super(ValidationException, self).__init__(message=message, status_code=status_code, data=data)

from rest_framework.response import Response
from rest_framework import status as rest_status


class SuccessResponse(Response):
    def __init__(self, status=rest_status.HTTP_200_OK, message='succeed', data={}, extra={}, headers=None, code=200):
        results = {"results": {
            "code": code,
            "message": message,
            'data': data
        }}
        # add extra data
        if extra:
            results["results"].update(extra)
        # add headers for response
        if headers:
            for name, value in headers.items():
                self[name] = value

        super(SuccessResponse, self).__init__(data=results, status=status)


class ErrorResponse(Response):
    def __init__(self, status=rest_status.HTTP_404_NOT_FOUND, message='error', data={}, code=None):
        if not code:
            code = status
        results = {"error": {
            "code": code,
            "message": message
        }}
        if data:
            results['error']['data'] = data

        super(ErrorResponse, self).__init__(data=results, status=status)


class ValidationErrorResponse(ErrorResponse):
    def __init__(self, status=rest_status.HTTP_422_UNPROCESSABLE_ENTITY, message='validation error', data={}, code=422):
        super(ValidationErrorResponse, self).__init__(status=status, message=message, data=data, code=code)

from django.db import connection
from rest_framework.response import Response
from django.conf import settings
from django.db import connection
import threading


class ResponseMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, Response):
            response.data['api_version'] = settings.API_VERSION
            # response._is_rendered = False
            # response.render()
        return response


class QueryCountDebugMiddleware(object):
    """Debug query count - use for DEBUG only."""
    """
    This middleware will log the number of queries run
    and the total time taken for each request (with a
    status code of 200). It does not currently support
    multi-db setups.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        total_time = 0

        for query in connection.queries:
            query_time = query.get('time')

            if query_time is None:
                query_time = query.get('duration', 0) / 1000
            total_time += float(query_time)
            print(query)

        print('%s queries run, total %s seconds' % (len(connection.queries), total_time))

        return response


class CustomCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"

        # Code to be executed for each request/response after
        # the view is called.

        return response


class GlobalRequestMiddleware(object):
    '''
        Get request from any where
    '''
    GLOBAL_REQUEST_STORAGE = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.GLOBAL_REQUEST_STORAGE.request = request
        try:
            return self.get_response(request)
        finally:
            del self.GLOBAL_REQUEST_STORAGE.request


def get_request():
    try:
        return GlobalRequestMiddleware.GLOBAL_REQUEST_STORAGE.request
    except Exception:
        return None

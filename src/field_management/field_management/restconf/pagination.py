from rest_framework import pagination
from rest_framework.response import Response

from base.api.exceptions import NotFoundException


class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    offset_query_param = 'offset'
    limit_query_param = 'limit'

    def get_paginated_response(self, data):

        return Response({
            'results': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'total_items': int(self.count),
                'item_per_page': int(self.limit),
                "data": data,
            }
        })


class CustomRankPagination(pagination.LimitOffsetPagination):
    default_limit = 5
    max_limit = 5

    def dataResult(self, data):
        return data

    def get_paginated_response(self, data):
        if data.__len__() == 0:
            raise NotFoundException

        return Response({
            'results': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'total_items': int(self.count),
                'item_per_page': int(self.limit),
                "data": self.dataResult(data),
            }
        })


class CustomProvincePagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000
    offset_query_param = 'offset'
    limit_query_param = 'limit'

    def get_paginated_response(self, data):

        return Response({
            'results': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'total_items': int(self.count),
                'item_per_page': int(self.limit),
                "data": data,
            }
        })


class MapPagination(CustomPagination):
    default_limit = 50
    max_limit = 100

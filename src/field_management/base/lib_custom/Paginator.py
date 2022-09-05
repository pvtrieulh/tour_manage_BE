from rest_framework.utils.urls import replace_query_param, remove_query_param
from rest_framework.response import Response
from django.db import connection

from base.models import TableAbstract


class PaginatorRaw:
    default_limit = 10
    max_limit = 100
    offset_query_param = 'offset'
    limit_query_param = 'limit'
    sort_query_param = 'sort'
    dir_query_param = 'dir'

    def __init__(self, query=None, query_binding=None, request=None, default_limit=None, max_limit=None,
                 order_default=None, order_avai=None):
        self.query = query
        self.request = request
        self.query_binding = query_binding
        self.order_default = order_default
        self.order_avai = order_avai
        self.order_by = ''
        if default_limit:
            self.default_limit = default_limit
        if max_limit:
            self.max_limit = max_limit
        self.offset = 0
        self.limit = self.default_limit
        self.total = 0
        self.data = None

    def exec(self):
        if not self.query:
            return self
        self.exec_order_by()
        self.exec_offset()
        self.exec_limit()
        self.exec_query()
        return self

    def exec_offset(self):
        self.offset = self.positive_int(self.request.GET.get(self.offset_query_param), default=0)

    def exec_limit(self):
        self.limit = self.positive_int(
            self.request.GET.get(self.limit_query_param),
            max_val=self.max_limit,
            default=self.default_limit
        )

    def exec_order_by(self):
        self.order_by = ''
        order_by_param = ''
        order_by_default = ''
        if self.order_avai:
            order_by_param = self.order_by_params_query()
        if self.order_default:
            order_by_default = self.order_by_default()
        if order_by_param:
            self.order_by = order_by_param
        if order_by_default:
            if self.order_by:
                self.order_by = self.order_by + ','
            self.order_by = self.order_by + ' ' + order_by_default
        if self.order_by:
            self.order_by = ' ORDER BY ' + self.order_by
        return self.order_by

    def order_by_params_query(self):
        sort = self.request.GET.get('sort')
        sort_dir = self.request.GET.get('dir')
        if not sort or sort not in self.order_avai:
            return ''
        if sort_dir != 'asc' or not sort_dir:
            return sort + ' desc'
        return sort + ' asc'

    def order_by_default(self):
        order_by = ''
        for i, v in self.order_default.items():
            if order_by:
                order_by = order_by + ', '
            order_by = '{order_by}{sort} {dir}'.format(order_by=order_by, sort=i, dir=v)
        return order_by

    def positive_int(self, val, max_val=None, default=0):
        if not val:
            return default
        val = int(val)
        if val < 0:
            return default
        if max_val:
            return min(val, max_val)
        return val

    def exec_query(self):
        self.exec_total()
        if type(self.query) is list:
            query_exec = ' union '.join(self.query)
        else:
            query_exec = self.query
        query_exec = query_exec + self.order_by \
             + ' LIMIT {limit} OFFSET {offset}'.format(limit=self.limit, offset=self.offset)
        self.data = TableAbstract.objects.raw(query_exec, self.query_binding)

    def exec_total(self):
        if type(self.query) is list:
            query_exec_count = []
            for item_query in self.query:
                query_exec_count.append(self.__split_select_count(item_query))

            query_exec_count = 'SELECT sum(count) as count FROM (' + ' union '.join(query_exec_count) + ') as tbl_count'
        else:
            query_exec_count = self.__split_select_count(self.query)
        with connection.cursor() as cursor:
            cursor.execute(query_exec_count, self.query_binding)
            count = cursor.fetchone()
            self.total = int(count[0])
            cursor.close()

    def __split_select_count(self, query):
        select_pos = query.find('SELECT')
        from_post = query.find('FROM')
        return query[0:select_pos] + 'SELECT count(*) as count ' + query[from_post:]

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()]

    def response(self, data):
        return Response({
            'results': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'total_items': self.total,
                'item_per_page': self.limit,
                "data": data,
            }
        })

    def get_next_link(self):
        if self.offset + self.limit >= self.total:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        if self.offset <= 0:
            return None

        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)

        if self.offset - self.limit <= 0:
            return remove_query_param(url, self.offset_query_param)

        offset = self.offset - self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_operator(dict_vals):
        operator = {}
        for k, v in dict_vals.items():
            if v is None:
                operator[f'o_{k}'] = 'is'
                dict_vals[k] = 'NULL'
            else:
                operator[f'o_{k}'] = '='
        return operator

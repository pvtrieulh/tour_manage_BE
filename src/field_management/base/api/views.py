from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import AppTracking
from base.validators import is_valid, lat_checker, lon_checker
from base.permissions import AuthRequired, IsAppVerified

from base.api.exceptions import BadRequestException, NotFoundException
from base.api.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin


class AppTrackingCreateView(APIView):
    permission_classes = (IsAppVerified,)

    def post(self, request, format=None):
        data = request.data
        validator(data)
        remote_ip = request.META['REMOTE_ADDR']
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            remote_ip = request.META['HTTP_X_FORWARDED_FOR']
        try:
            AppTracking.objects.create(remote_ip=remote_ip,
                                       latitude=data['latitude'],
                                       longitude=data['longitude'],
                                       )

            return Response({"result": {"code": 201, "message": "succeed"}}, status=201)
        except Exception:
            return BadRequestException


def validator(data):
    required_fields = (
        ('latitude', None),
        ('longitude', None),
    )
    is_valid(required_fields, data)

    lat_checker(data)
    lon_checker(data)


class DetailSlugView(RetrieveModelMixin, generics.RetrieveAPIView):

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        id = self.request.GET.get('id')
        slug = self.request.GET.get('slug')
        if id:
            queryset = queryset.filter(id=id)
        if slug:
            queryset = queryset.filter(slug=slug)
        obj = queryset.first()
        if not obj:
            raise NotFoundException
        self.check_object_permissions(self.request, obj)

        return obj

from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from django.shortcuts import _get_queryset

from base.utils import clean_cache_by_prefix
from base.api.exceptions import NotFoundException
from base.api.messages import MSG_SUCCESS, MSG_CREATE_SUCCESS, MSG_DESTROY_SUCCESS
from base.api.response import SuccessResponse, ErrorResponse, ValidationErrorResponse


def get_object_or_404(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise NotFoundException


class RetrieveModelMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    success_response = MSG_SUCCESS

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
        }

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {'pk': self.kwargs['pk']} if 'pk' in self.kwargs else {}

        try:
            obj = get_object_or_404(queryset, **filter)  # Lookup the object
            self.check_object_permissions(self.request, obj)
        except NotFoundException as ex:
            raise NotFoundException

        return obj

    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        success_response = self.success_response
        instance = self.get_object()
        data = self.get_serializer(instance, context={'request': request}).data
        return SuccessResponse(data=data, code=success_response[0], message=success_response[1])


class MultipleFieldLookupMixin(object):
    lookup_fields = ('pk',)

    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)


class ListModelMixin(object):
    success_response = MSG_SUCCESS

    def list(self, request, *args, **kwargs):
        """
        List a queryset.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True, context={'request': request})
            result = self.get_success_response(serializer)
        return result

    def get_success_response(self, serializer):
        success_response = self.success_response
        return SuccessResponse(data=serializer.data, code=success_response[0], message=success_response[1])


class ListModelByFieldMixin(ListModelMixin):
    lookup_field = 'id'

    def get_queryset(self):
        params = {self.lookup_field: self.kwargs.get(self.lookup_field)}
        return self.queryset.filter(**params)


class ClearCacheMixin(object):
    key_prefix = None

    def get_key_prefix(self, prefix_id=None):
        if not prefix_id and 'pk' not in self.kwargs:
            return self.key_prefix

        prefix_id = prefix_id if prefix_id else self.kwargs["pk"]
        return self.key_prefix.format(pk=prefix_id) if self.key_prefix else None

    def clear_cache(self, prefix_id=None):
        key_prefix = self.get_key_prefix(prefix_id)

        if not key_prefix:
            return
        return clean_cache_by_prefix(key_prefix)


class CreateModelMixin(ClearCacheMixin):
    """
    Create a model instance.
    """
    status_code = status.HTTP_201_CREATED
    success_response = MSG_CREATE_SUCCESS
    serializer_response = None

    def create(self, request, *args, **kwargs):

        credentials = self.get_credentials(request)
        serializer = self.get_serializer(data=credentials, context={'request': request})

        if not serializer.is_valid():
            # write log error response
            return ValidationErrorResponse(data=serializer.errors)
        instance = self.perform_create(serializer)
        if not self.serializer_response:
            serializer_response = serializer
        else:
            serializer_response = self.serializer_response(instance=instance)
        return self.get_success_response(serializer_response)

    def get_credentials(self, request):
        return request.data

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def get_success_response(self, serializer):
        # clean cache
        self.clear_cache()
        return SuccessResponse(
            data=serializer.data,
            status=self.status_code,
            headers=self.get_success_headers(serializer.data),
            code=self.success_response[0],
            message=self.success_response[1]
        )


class UpdateModelMixin(ClearCacheMixin):
    """
    Update a model instance.
    """
    status_code = status.HTTP_200_OK
    success_response = MSG_SUCCESS
    serializer_response = None

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        credentials = self.get_credentials(request)

        serializer = self.get_serializer(instance, data=credentials, context={'request': request}, partial=partial)
        if not serializer.is_valid():
            # write log error response
            return ValidationErrorResponse(data=serializer.errors)

        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if not self.serializer_response:
            serializer_response = serializer
        else:
            serializer_response = self.serializer_response(instance=instance)
        return self.get_success_response(serializer_response)

    def get_credentials(self, request):
        return request.data

    def perform_update(self, serializer):
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_success_response(self, serializer):
        # clean cache
        self.clear_cache()
        return SuccessResponse(
            data=serializer.data,
            status=self.status_code,
            code=self.success_response[0],
            message=self.success_response[1]
        )


class DestroyModelMixin(ClearCacheMixin):
    """
    Destroy a model instance.
    """
    status_code = status.HTTP_200_OK
    success_response = MSG_DESTROY_SUCCESS

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)
        return self.get_success_response(instance)

    def perform_destroy(self, instance):
        return instance.delete()

    def get_success_response(self, instance=None):
        # clean cache
        self.clear_cache(instance.id)
        success_response = self.success_response
        return SuccessResponse(status=self.status_code, code=success_response[0], message=success_response[1])


class CreateManyMixin(CreateModelMixin):
    status_code = status.HTTP_200_OK

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(CreateManyMixin, self).get_serializer(*args, **kwargs)


class UpdateStatusManyMixin(APIView):
    status_code = status.HTTP_200_OK
    success_response = MSG_SUCCESS

    def get_list_object(self):
        try:
            ids = self.request.data.get('ids')
            return super().get_queryset().filter(pk__in=ids)
        except:
            raise NotFoundException

    def update(self, request, *args, **kwargs):
        data = request.data
        enabled = data.get('enabled')

        list_instance = self.get_list_object()
        status = 1 if enabled else 0
        list_instance.update(status=status)

        serializer = self.get_serializer(list_instance, many=True)
        return self.get_success_response(serializer, list_instance)

    def get_success_response(self, serializer, list_instance):
        # clean cache
        list_instance.first().clean_cache() if list_instance else None
        return SuccessResponse(
            data=serializer.data,
            status=self.status_code,
            code=self.success_response[0],
            message=self.success_response[1]
        )


class DestroySelectModelMixin(APIView):
    """
    Destroy select model instance.
    rest_pk is list pk delete
    """
    status_code = status.HTTP_200_OK
    success_response = MSG_DESTROY_SUCCESS

    def delete(self, request):
        list_pk = self.request.GET.getlist('rest_pk')
        instance = super().get_queryset().filter(pk__in=list_pk)
        self.perform_destroy(instance)
        return self.get_success_response(instance)
        
    def perform_destroy(self, instance):
        instance.first().clean_cache() if instance else None
        return instance.delete()

    def get_success_response(self, instance=None):
        success_response = self.success_response
        return SuccessResponse(status=self.status_code, code=success_response[0], message=success_response[1])

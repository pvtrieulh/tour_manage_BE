from rest_framework import status as rest_status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Count

from notification.tasks import send_notification_when_create_comment, send_notification_when_reply_comment
from notification.helpers import get_object_type
from base.api.messages import MSG_AUTH_NOT_ALLOWED, LIKE_MSG_UNLIKE, LIKE_MSG_LIKE, WORD_RULE_CMT_INVALID, \
    WORD_RULE_INVALID_REASON_UN
from base.api.mixins import CreateModelMixin
from base.api.exceptions import NotFoundException
from base.api.response import ValidationErrorResponse, SuccessResponse, ErrorResponse
from base.helpers import sort_dir_from_request
from base.permissions import AuthRequired, GeneralAuthRequired
from base.choices import ENABLE, DISABLE
from st_auth.helpers import get_author_of_list_obj
from .serializers import RateListSerializer, RateListBaseSerializer, RateCreateSerializer, \
    RateGalleryCreateSerializer, RateReplyCreateSerializer, CommentListSerializer, RateCreateResponseSerializer, \
    RateReplyCreateResponseSerializer
from .helpers import RateListToElement, get_main_model, get_reply_model, create_from_validated_data, get_gallery_model, \
    get_like_model, get_model_from_app, rate_check_valid_word_before_save, rate_pass_invalid_rule_with_key
from .choices import LIKE_STATUS_LIKE, LIKE_STATUS_NONE


class RateViewBase:
    rate_model = 'ObjectRate'

    def get_main_object(self):
        obj = get_main_model(self.get_rate_model()).objects.filter(id=self.kwargs['pk']).first()
        if not obj:
            raise NotFoundException
        return obj

    def get_rate_object(self):
        obj = self.get_rate_model().objects.filter(id=self.kwargs['pk'], status=ENABLE, approve=ENABLE).first()
        if not obj:
            raise NotFoundException
        return obj

    def get_rate_model(self):
        if type(self.rate_model) is not str:
            return self.rate_model
        self.rate_model = get_model_from_app(self, self.rate_model)
        return self.rate_model


class RateListBase(RateViewBase, ListAPIView):
    serializer_class = RateListSerializer

    def get_queryset(self):
        obj = self.get_main_object()
        queryset = self.get_rate_model().objects.filter(obj_main_id=obj.id, status=ENABLE, approve=ENABLE)

        queryset = sort_dir_from_request(
            request=self.request,
            queryset=queryset,
            default_sort='created_at',
            allow_sort=['created_at', 'rate', 'reply_count', 'like_count']
        )
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        List a queryset.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        rate_exec = RateListToElement(request=request)
        rate_exec.set_rate_list(rate_list=page)
        element_result_rate = rate_exec.exec_all_data()
        authors = get_author_of_list_obj(obj_list=page, extends={
            'user_more': rate_exec.user_data
        })
        serializer = self.serializer_class(page, many=True, context={
            'authors': authors,
            'gallery': element_result_rate.get('gallery').get('rate') if element_result_rate.get('gallery') else None,
            'gallery_reply': element_result_rate.get('gallery').get('reply') if element_result_rate.get('gallery') else None,
            'is_like': element_result_rate.get('is_like'),
            'reply': element_result_rate.get('reply')
        })
        return self.get_paginated_response(serializer.data)


class RateReplyListBase(RateViewBase, ListAPIView):
    serializer_class = RateListBaseSerializer

    def get_queryset(self, rate_obj):
        return get_reply_model(self.get_rate_model()).objects.filter(rate_id=rate_obj.id, status=ENABLE, approve=ENABLE)\
            .order_by('-created_at')

    def list(self, request, *args, **kwargs):
        obj = self.get_rate_object()
        queryset = self.get_queryset(obj)
        page = self.paginate_queryset(queryset)
        rate_exec = RateListToElement(request=request)
        rate_exec.set_rate_reply(reply_list=page, rate_list=[obj])

        authors = get_author_of_list_obj(obj_list=page)
        gallery = rate_exec.get_gallery()
        serializer = self.serializer_class(page, many=True, context={
            'authors': authors,
            'gallery': gallery.get('reply') if gallery else None,
        })
        return self.get_paginated_response(serializer.data)


class RateCreateBase(RateViewBase, CreateModelMixin, CreateAPIView):
    serializer_class = RateCreateSerializer
    serializer_response = RateCreateResponseSerializer
    permission_classes = (AuthRequired, )

    def create(self, request, *args, **kwargs):
        obj_main = self.get_main_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ValidationErrorResponse(data=serializer.errors)
        image_gallery = request.data.getlist('image[]')
        image_gallery = list(filter(None, image_gallery))
        gallery_serializer = None
        if len(image_gallery) > 0:
            gallery_serializer = RateGalleryCreateSerializer(data={
                'image': image_gallery
            })
            if not gallery_serializer.is_valid():
                return ValidationErrorResponse(data=gallery_serializer.errors)

        # check rule before save
        rate_word_rule = rate_pass_invalid_rule_with_key(
            serializer.validated_data['comment'],
            request.data.get('key')
        )
        if not rate_word_rule:
            rate_word_valid_key = rate_check_valid_word_before_save(serializer.validated_data['comment'])
            if rate_word_valid_key is not True:
                return ValidationErrorResponse(
                    message=WORD_RULE_CMT_INVALID[1],
                    code=WORD_RULE_CMT_INVALID[0],
                    data=rate_word_valid_key
                )
            serializer.validated_data['approve'] = ENABLE
        else:
            serializer.validated_data['approve'] = DISABLE
            serializer.validated_data['reason_un'] = WORD_RULE_INVALID_REASON_UN[1] + ', '.join(rate_word_rule)

        serializer.validated_data['obj_main_id'] = obj_main.id
        serializer.validated_data['user_id'] = request.user_id
        serializer.validated_data['user_mod'] = request.user_type

        with transaction.atomic():
            rate_obj = create_from_validated_data(self.get_rate_model(), serializer.validated_data)
            if gallery_serializer:
                gallery_serializer.validated_data['rate_id'] = rate_obj.id
                gallery_serializer.bulk_create(get_gallery_model(self.get_rate_model()))
        if serializer.validated_data['approve'] == ENABLE:
            send_notification_when_create_comment.delay(get_object_type(obj_main), obj_main.id, rate_obj.id)
        # response data for new rate
        rate_exec = RateListToElement(request=request)
        rate_exec.set_rate_list(rate_list=[rate_obj])
        element_result_rate = rate_exec.exec_all_data(reply=False, is_like=False)
        authors = get_author_of_list_obj(obj_list=[rate_obj], extends={
            'user_more': rate_exec.user_data
        })
        serializer = self.serializer_response(instance=rate_obj, context={
            'authors': authors,
            'gallery': element_result_rate.get('gallery').get('rate') if element_result_rate.get('gallery') else None,
            'word_rule': rate_word_rule
        })
        return SuccessResponse(
            data=serializer.data,
            status=self.status_code,
            code=self.success_response[0],
            message=self.success_response[1]
        )


class RateReplyCreateBase(RateViewBase, CreateModelMixin, CreateAPIView):
    serializer_class = RateReplyCreateSerializer
    serializer_response = RateReplyCreateResponseSerializer
    permission_classes = (AuthRequired, )

    def is_allow_reply(self, rate_obj):
        # check is owner and it reply by business
        if rate_obj.user_id == self.request.user_id and rate_obj.user_mod == self.request.user_type:
            return True
        return False

    def create(self, request, *args, **kwargs):
        rate_obj = self.get_rate_object()
        if not self.is_allow_reply(rate_obj=rate_obj):
            return ErrorResponse(
                status=rest_status.HTTP_400_BAD_REQUEST,
                code=MSG_AUTH_NOT_ALLOWED[0],
                message=MSG_AUTH_NOT_ALLOWED[1]
            )
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ValidationErrorResponse(data=serializer.errors)
        image_gallery = request.data.getlist('image[]')
        image_gallery = list(filter(None, image_gallery))
        gallery_serializer = None
        if len(image_gallery) > 0:
            gallery_serializer = RateGalleryCreateSerializer(data={
                'image': image_gallery
            })
            if not gallery_serializer.is_valid():
                return ValidationErrorResponse(data=gallery_serializer.errors)

        # check rule before save
        rate_word_rule = rate_pass_invalid_rule_with_key(
            serializer.validated_data['comment'],
            request.data.get('key')
        )
        if not rate_word_rule:
            rate_word_valid_key = rate_check_valid_word_before_save(serializer.validated_data['comment'])
            if rate_word_valid_key is not True:
                return ValidationErrorResponse(
                    message=WORD_RULE_CMT_INVALID[1],
                    code=WORD_RULE_CMT_INVALID[0],
                    data=rate_word_valid_key
                )
            serializer.validated_data['approve'] = ENABLE
        else:
            serializer.validated_data['approve'] = DISABLE
            serializer.validated_data['reason_un'] = WORD_RULE_INVALID_REASON_UN[1] + ', '.join(rate_word_rule)

        serializer.validated_data['rate_id'] = rate_obj.id
        serializer.validated_data['user_id'] = request.user_id
        serializer.validated_data['user_mod'] = request.user_type

        with transaction.atomic():
            reply_obj = create_from_validated_data(get_reply_model(self.get_rate_model()), serializer.validated_data)
            if gallery_serializer:
                gallery_serializer.validated_data['reply_id'] = reply_obj.id
                gallery_serializer.bulk_create(get_gallery_model(self.get_rate_model()))

        if serializer.validated_data['approve'] == ENABLE:
            send_notification_when_reply_comment.delay(get_object_type(rate_obj.obj_main), rate_obj.obj_main.id, reply_obj.id)
        # response data for new rate
        rate_exec = RateListToElement(request=request)
        rate_exec.set_rate_reply(reply_list=[reply_obj], rate_list=[rate_obj])
        element_result_rate = rate_exec.exec_all_data(reply=False, is_like=False)
        authors = get_author_of_list_obj(obj_list=[reply_obj], extends={
            'user_more': rate_exec.user_data
        })
        serializer = self.serializer_response(instance=reply_obj, context={
            'authors': authors,
            'gallery': element_result_rate.get('gallery').get('reply') if element_result_rate.get('gallery') else None,
            'word_rule': rate_word_rule
        })
        return SuccessResponse(
            data=serializer.data,
            status=self.status_code,
            code=self.success_response[0],
            message=self.success_response[1]
        )


class RateLikeBase(RateViewBase, CreateAPIView):
    permission_classes = (GeneralAuthRequired, )

    def create(self, request, *args, **kwargs):
        rate_obj = self.get_rate_object()
        like_model = get_like_model(self.get_rate_model())
        is_like = like_model.objects.filter(rate_id=rate_obj.id, user_id=request.user_id, user_mod=request.user_type)\
            .first()
        # create like
        if not is_like:
            is_like = like_model(
                rate_id=rate_obj.id,
                user_id=request.user_id,
                user_mod=request.user_type,
                status=LIKE_STATUS_NONE
            )
        if is_like.status == LIKE_STATUS_NONE:
            is_like.status = LIKE_STATUS_LIKE
            code = LIKE_MSG_LIKE[0]
            message = LIKE_MSG_LIKE[1]
        else:  # unlike
            is_like.status = LIKE_STATUS_NONE
            code = LIKE_MSG_UNLIKE[0]
            message = LIKE_MSG_UNLIKE[1]
        is_like.save(rate_obj=rate_obj)
        return SuccessResponse(message=message, code=code, data={
            'like_count': rate_obj.like_count
        })


class RateStatisticalBase(RateViewBase, APIView):

    def get(self, request, pk):
        main_obj = self.get_main_object()
        data = [{'rate': i, 'id': 0} for i in range(1, 6)]
        rate_statistic = self.get_rate_model().objects.filter(obj_main_id=main_obj.id, status=ENABLE, approve=ENABLE)\
            .values('rate').annotate(id=Count('id')).values('rate', 'id')
        rate_statistic = data + list(rate_statistic)
        result_statistic = {item.get('rate'): item.get('id') for item in rate_statistic}
        return SuccessResponse(data={
            'rate_avg': round(main_obj.rate_avg, 1) if main_obj.rate_avg else None,
            'rate_count': main_obj.rate_count,
            'rate_value': result_statistic
        })


class CommentListBase(RateListBase):
    serializer_class = CommentListSerializer


class CommentCreateBase(RateCreateBase):
    serializer_class = RateReplyCreateSerializer


class CommentReplyCreateBase(RateReplyCreateBase):
    def is_allow_reply(self, rate_obj):
        return True

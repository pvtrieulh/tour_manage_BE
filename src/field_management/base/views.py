from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from location.models import District
from pages.models import AppStatus, ANDROID, IOS, AppVersion, FLUTTER
from .utils import check_vietnam_ip

from base.api.serializers import AppVersionSerializer
from base.api.response import SuccessResponse


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.

@cache_page(timeout=CACHE_TTL)
def count(request):
    """
    count from 0 to times
    use for test caching setting
    """
    times = request.GET.get('t')
    try:
        total = 0
        times = int(times)
        for i in range(0, times):
            total += i
    except Exception as e:
        return JsonResponse({
            'message': 'invalid time value {}'.format(times),
            'error': str(e)
        })

    return JsonResponse({
        'message': 'sum from 0 to times {} -> {}'.format(times, total),
        'total': total
    })


def status(request):
    """
    check api status
    """
    return JsonResponse({
        'status': 'ok',
        'status_code': 200,
        'message': 'alive'
    })


def choose_province(request):
    province = request.GET.get('p')
    province = int(province)
    districts = District.objects.filter(province=province)
    qs_json = serializers.serialize('json', districts)
    return HttpResponse(qs_json, content_type='application/json')


def policy(request):
    return render(request, 'app/policy.html')


def app_status(request):
    """
    check app status
    """
    remote_ip = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # load balancer
        remote_ip = request.META['HTTP_X_FORWARDED_FOR']
    is_vietnam_ip, country_code = check_vietnam_ip(remote_ip)

    type_app = request.GET.get('type')
    app_version = request.GET.get('version')
    language_code = request.GET.get('lang')
    if type_app is None or type_app not in [ANDROID, IOS, FLUTTER]:
        return JsonResponse(
            {'status': 'false', 'message': " Not found any app status matching type {}".format(type_app)}, status=404)

    app = AppStatus.objects.select_related('language').filter(os=type_app)
    if language_code:
        app = app.filter(language__code=language_code)

    _status = 'published' if is_vietnam_ip else 'reviewing'

    app = app.filter(app_status=_status)
    last_version = app.filter(last_version=True).first().version if app.filter(
        last_version=True).exists() else None

    if app_version:
        app = app.filter(version=app_version)

    app = app.order_by('-version').first()
    data = gen_data(app, is_vietnam_ip, country_code)

    return JsonResponse(
        {
            'app_status': _status,
            'results': {
                'last_version': last_version,
                'data': data,
            }
        }
    )


def gen_data(app, is_vietnam_ip, country_code):
    if not is_vietnam_ip:
        status = 'reviewing'
    elif app:
        status = app.app_status
    else:
        status = None

    return {
        'app_status': status,
        'country_code': country_code,
        'app_version': app.version if app else None,
        'settings': app.setting if app else None,
    }


def app_status_v2(request):
    """
    check app status
    """
    remote_ip = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # load balancer
        remote_ip = request.META['HTTP_X_FORWARDED_FOR']
    is_vietnam_ip, country_code = check_vietnam_ip(remote_ip)

    type_app = request.GET.get('type')
    app_version = request.GET.get('version')

    if type_app is None or type_app not in [ANDROID, IOS]:
        return JsonResponse(
            {'status': 'false', 'message': " Not found any app status matching type {}".format(type_app)}, status=404)

    app = AppStatus.objects.filter(os=type_app)
    last_version = app.filter(last_version=True).first().version if app.filter(
        last_version=True).exists() else None

    if app_version and app.filter(version=app_version):
        app = app.filter(version=app_version)

    app = app.order_by('-version').first()

    data = gen_data_v2(app, is_vietnam_ip, country_code)

    return JsonResponse(
        {
            'app_status': 'published' if is_vietnam_ip else 'reviewing',
            'results': {
                'last_version': last_version,
                'data': data,
            }
        }
    )


class VersionApp(APIView):

    def get(self, request):
        type_app = request.GET.get('type')
        version = AppVersion.objects.filter(os=type_app).order_by('-last_version', '-version').first()
        return SuccessResponse(data=AppVersionSerializer(version).data)


def gen_data_v2(app, is_vietnam_ip, country_code):
    if not is_vietnam_ip:
        status = 'reviewing'
    else:
        status = app.app_status

    results = list(app.setting.values())

    for item in results:
        recursive_convert_dict_to_list(item)

    return {
        'app_status': status,
        'country_code': country_code,
        'app_version': app.version,
        'settings': results
    }


def recursive_convert_dict_to_list(item):
    for k, v in item.items():
        if isinstance(v, dict):
            item[k] = list(v.values())
            recursive_convert_dict_to_list(v)

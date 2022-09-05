from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS
from django.conf import settings

from base.middleware import GlobalRequestMiddleware, get_request
from permission.helpers import full_route_name_to_permission, check_permission, check_permission_business
from .choices import VERIFY_CLIENT_API_KEY, HTTP_APP_VERSION, VERIFY_SERVER_API_KEY
from .utils import get_access_token, get_remote_ip, get_lang
from .api.exceptions import NotFoundException

from st_auth.models import AuthModel
from st_admin.models import AdminModel
from st_business.models import BusinessModel
from st_personal.models import PersonalModel
from st_auth.constant import MODE_ADMINISTRATOR_KEY, MODE_PERSONAL_KEY, MODE_BUSINESS_KEY, \
    MODE_PERSONAL, MODE_BUSSINESS, MODE_ADMINISTRATOR


def get_model_by_name(model_name):
    if model_name == AdminModel.__name__:
        return AdminModel
    elif model_name == BusinessModel.__name__:
        return BusinessModel
    return PersonalModel


def check_client_key(request, class_auth=None):
    if request.META.get(VERIFY_CLIENT_API_KEY) == settings.CLIENT_API_KEY:
        return True
    if class_auth:
        class_auth.message = {"code": 403, "message": "You don't have permission to access api"}
    return False


def request_to_auth_info(request=None, cls_auth=None):
    try:
        if not request:
            request = get_request()
        if hasattr(request, 'user_id') and hasattr(request, 'user_type') and request.user_id and request.user_type:
            return {
                'user_id': request.user_id,
                'user': request.user,
                'st_authmodel': request.st_authmodel,
                'user_type': request.user_type,
                'user_folder': request.user_folder,
                'remote_ip': request.remote_ip,
                'personal_id': request.personal_id,
                'admin_id': request.admin_id,
                'business_id': request.business_id
            }

        if not cls_auth:
            payload = AuthModel.decode_access_token(get_access_token(request))
        else:
            payload = cls_auth.decode_auth_token(get_access_token(request))
        result = {
            'user_id': None,
            'user': None,
            'st_authmodel': None,
            'user_type': None,
            'user_folder': None,
            'remote_ip': None,
            'personal_id': None,
            'admin_id': None,
            'business_id': None
        }
        result['user_id'] = payload['sub']
        result['st_authmodel'] = get_model_by_name(payload['model'])
        result['user'] = result['st_authmodel'].objects.all().get(pk=payload['sub'])
        if isinstance(result['user'], AdminModel):
            result['user_type'] = MODE_ADMINISTRATOR_KEY
            result['user_folder'] = MODE_ADMINISTRATOR
            result['admin_id'] = payload['sub']
        elif isinstance(result['user'], BusinessModel):
            result['user_type'] = MODE_BUSINESS_KEY
            result['user_folder'] = MODE_BUSSINESS
            result['business_id'] = payload['sub']
        else:
            result['user_type'] = MODE_PERSONAL_KEY
            result['user_folder'] = MODE_PERSONAL
            result['personal_id'] = payload['sub']
        result['remote_ip'] = get_remote_ip(request)

        # set other value for request
        request.user_id = result['user_id']
        request.user = result['user']
        request.st_authmodel = result['st_authmodel']
        request.user_type = result['user_type']
        request.user_folder = result['user_folder']
        request.remote_ip = result['remote_ip']
        request.admin_id = result['admin_id']
        request.business_id = result['business_id']
        request.personal_id = result['personal_id']
        request.lang = get_lang(request)

        # set request with new value
        GlobalRequestMiddleware.GLOBAL_REQUEST_STORAGE.request = request
        return result
    except:
        return None


class IsAppVerified(AllowAny):
    """
    verify client api key
    """
    message = {"code": 403, "message": "You don't have permission to access api"}

    def has_permission(self, request, view):
        return check_client_key(request)


class GeneralAuthRequired(BasePermission):
    """
    Allows access only to authenticated users.
    """
    message = {"code": 401, "message": "Invalid token. Please log in again."}
    cls_auth = None

    def has_permission(self, request, view):
        if not check_client_key(request, class_auth=self):
            return False
        request_auth = request_to_auth_info(request=request, cls_auth=self.cls_auth)
        if not request_auth:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return True


class AuthRequired(GeneralAuthRequired):
    """
    Allows access only to authenticated users.
    """
    message = {"code": 401, "message": "Invalid token. Please log in again."}
    cls_auth = PersonalModel

class AuthRequiredOrNot(GeneralAuthRequired):
    """
    Allows access only to authenticated users.
    """
    message = {"code": 401, "message": "Invalid token. Please log in again."}
    cls_auth = PersonalModel

    def has_permission(self, request, view):
        check_client_key(request, class_auth=self)
        request_to_auth_info(request=request, cls_auth=self.cls_auth)
        return True


class BusinessAuthRequired(GeneralAuthRequired):
    """
    Allows access only to authenticated users.
    """
    message = {"code": 401, "message": "Invalid token. Please log in again."}
    cls_auth = BusinessModel

    def has_permission(self, request, view):
        if not check_client_key(request, class_auth=self):
            return False
        request_auth = request_to_auth_info(request=request, cls_auth=BusinessModel)
        if not request_auth:
            return False
        self.message = {"code": 403, "message": "Need permission"}
        return check_permission_business(request, view)


class AdminAuthRequired(GeneralAuthRequired):
    """
    Allows access only to authenticated users.
    """
    message = {"code": 401, "message": "Invalid token. Please log in again."}
    cls_auth = AdminModel

    def has_permission(self, request, view):
        if not check_client_key(request, class_auth=self):
            return False
        request_auth = request_to_auth_info(request=request, cls_auth=AdminModel)
        if not request_auth:
            return False
        self.message = {"code": 403, "message": "Need permission"}
        return check_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = {"code": 403, "message": "You do not have permission to perform this action."}

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        owner_id = None
        user = request.user
        if isinstance(user, AdminModel) and hasattr(obj, 'admin_id'):
            owner_id = getattr(obj, 'admin_id')
        elif isinstance(user, BusinessModel) and hasattr(obj, 'business_id'):
            owner_id = getattr(obj, 'business_id')
        elif hasattr(obj, 'personal_id'):
            owner_id = getattr(obj, 'personal_id')
        elif hasattr(obj, 'user_id'):
            owner_id = getattr(obj, 'user_id')

        return owner_id == request.user_id

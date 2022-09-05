from django.utils.translation import gettext_lazy as __
MSG_SUCCESS = (200, __('Succeed'))
MSG_CREATE_SUCCESS = (201, __('Create success'))
MSG_DESTROY_SUCCESS = (201, __('Destroy success'))
MSG_AUTH_TOKEN_INVALID = (400, __('Invalid token. Please log in again.'))
MSG_AUTH_TOKEN_EXPIRED = (401, __('Signature expired. Please log in again.'))
MSG_AUTH_TOKEN_BLACKLISTED = (402, __('Token blacklisted. Please log in again.'))
MSG_AUTH_NOT_ALLOWED = (403, __('You do not have permission to perform this action.'))

# general message
LIKE_MSG_LIKE = (10001, __('Like success'))
LIKE_MSG_UNLIKE = (10002, __('Unlike success'))
BODY_MISS_FIELDS = (10003, __('Field %s is missing'))
FIELD_REQUIRED = (10004, __('This field is required.'))
FIELD_FORMAT_INT = (10005, __('Field %s must be an (list) integer'))

# app auth permission
MSG_AUTH_LOGIN = (20000, __('Login success'))
MSG_AUTH_LOGOUT = (20001, __('Logout success'))
MSG_AUTH_INFO = (20002, __('User info'))
MSG_AUTH_REFRESHTOKEN = (20003, __('Refresh token success'))
MSG_AUTH_REGISTER = (20004, __('Register new user success'))
MSG_PROFILE_ACCOUNT = (20005, __('Profile account'))
MSG_CHANGE_PASSWORD = (20006, __('Your password has been updated successfully'))
MSG_FORGOT_PASSWORD = (20007, __('Create OTP forgot password success'))
MSG_CONFIRM_OTP = (20008, __('Token valid'))
MSG_RESET_PASSWORD = (20009, __('Reset password success'))
MSG_FORGOT_PASSWORD_SUBJECT = __('Yêu cầu lấy lại mật khẩu')
MSG_ACCOUNT_BLOCKED = (20010, __('Account is blocked'))

# media manage
MSG_UPLOAD_FILE = (21001, __('Upload file media success'))
VALID_FILE_SIZE = (21101, __('Please keep filesize under %s. Current filesize %s'))
VALID_FILE_TYPE = (21102, __('File type is supported: %s'))

# app news
NEWS_SLIDE_MAX_FILE_UPLOAD = (22001, __('Max number file in slide is %s'))

# app fcm device
MSG_FCM_DEVICE_CREATE = (30000, __('Register device token success'))
MSG_FCM_DEVICE_ADD_USER = (30001, __('Register device token for account success'))

# app hotel
MSG_RATE_ALREADY_EXIST =  (30001, __('Rate already exist.'))
MSG_CREATE_RATE_FAILS =  (30002, __('Create rate fails.'))

# social feature
MSG_CREATE_FEEDBACK = (40001, __('Create feedback success'))
MSG_CREATE_FEEDBACK_COMMENT = (40002, __('Create feeback comment success'))
MSG_DELETE_FEEDBACK = (40003, __('Delete feeback  success'))

# favourite
MSG_DELETE_FAVOUTITE = (50001, __('Delete favourite success'))

# schedule
MSG_SCHEDULE_SERVICE_DELETE = (60001, __('Delete schedule service success'))

#ship_tickets
MSG_CREATE_SHIP_TICKET = (70001, __('Create ship ticket success.'))
MSG_CREATE_SHIP_TICKET_FAILS = (70002, __('Create ship ticket fails.'))
MSG_DELETE_FEEDBACK = (70003, __('Delete ship ticket success.'))

# tour
MSG_TOUR_NOT_FOUND = (80001, __('Not found data'))
MSG_ID_NOT_EXITS = (80002, __('Invalid value type'))

# word
WORD_RULE_CMT_INVALID = (90001, __('Comments violating words'))
WORD_RULE_INVALID_REASON_UN = (90002, __('Từ bị vi phạm: '))

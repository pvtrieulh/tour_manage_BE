import time

ENABLE = 1
DISABLE = 0
PENDING = 2
UN_APPROVE = 2
APPROVED = 3
HIDDEN = 4

STATUS_SELECT = (
    (ENABLE, 'Enable'),
    (DISABLE, 'Disable'),
)
LIST_STATUS = (DISABLE, ENABLE)

STATUS_APPROVE_CHOICE = (
    (ENABLE, 'Đã duyệt'),
    (DISABLE, 'Chưa duyệt'),
    (UN_APPROVE, 'Không duyệt'),
    (HIDDEN, 'Ẩn'),
)

TYPE_VIDEO = 1
TYPE_IMAGE = 2

APPROVE_SELECT_CHOICE = (
    (ENABLE, 'Đã duyệt'),
    (DISABLE, 'Chưa duyệt'),
    (UN_APPROVE, 'Không duyệt'),
)


# GENDER SELECT
GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_OTHER = 3

GENDER_SELECT = (
    (GENDER_MALE, 'Nam'),
    (GENDER_FEMALE, 'Nữ'),
    (GENDER_OTHER, 'Khác'),
)

HTTP_AUTHORIZATION = 'HTTP_AUTHORIZATION'
VERIFY_CLIENT_API_KEY = 'HTTP_CLIENTAPIKEY'
VERIFY_SERVER_API_KEY = 'HTTP_SERVERAPIKEY'
HTTP_APP_VERSION = 'HTTP_APPVERSION'
CLIENT_LANG_KEY = 'HTTP_ACCEPT_LANGUAGE'

app_version = '1.1.0'

PROVINCE = []
DISTRICT = []

TBB = "Tây Bắc bộ"
DBB = "Đông Bắc bộ"
DBSH = "Đồng bằng sông Hồng"
BTB = "Bắc Trung Bộ"
DHNTB = "Duyên hải Nam Trung Bộ"
TN = "Tây Nguyên"
DNB = "Đông Nam Bộ"
TNB = "Tây Nam Bộ"
CANUOC = "Cả nước"
MIENBAC = "Miền Bắc"
MIENTRUNG = "Miền Trung"
MIENNAM = "Miền Nam"

REGIONS = (
    (TBB, TBB),
    (DBB, DBB),
    (DBSH, DBSH),
    (BTB, BTB),
    (DHNTB, DHNTB),
    (TN, TN),
    (DNB, DNB),
    (TNB, TNB),
    (CANUOC, CANUOC),
)

REGIONS_COUNTRY = (
    (MIENBAC, MIENBAC),
    (MIENTRUNG, MIENTRUNG),
    (MIENNAM, MIENNAM),
    (CANUOC, CANUOC)
)

TAYBACBO = ['Lào Cai', 'Yên Bái', 'Lai Châu', 'Điện Biên', 'Sơn La', 'Hòa Bình']
DONGBACBO = ['Hà Giang', 'Tuyên Quang', 'Phú Thọ', 'Thái Nguyên', 'Bắc Cạn', 'Cao Bằng', 'Lạng Sơn', 'Bắc Giang',
             'Quảng Ninh']
DONGBANGSONGHONG = ['Hà Nội', 'Vĩnh Phúc', 'Bắc Ninh', 'Hưng Yên', 'Hải Dương', 'Hải Phòng', 'Thái Bình', 'Nam Định',
                    'Ninh Bình', 'Hà Nam']
BACTRUNGBO = ['Thanh Hóa', 'Nghệ An', 'Hà Tĩnh', 'Quảng Bình', 'Quảng Trị', 'Thừa Thiên Huế']
DUYHAINAMTRUNGBO = ['Đà Nẵng', 'Quảng Nam', 'Quảng Ngãi', 'Bình Định', 'Phú Yên', 'Khánh Hòa', 'Ninh Thuận',
                    'Bình Thuận']
TAYNGUYEN = ['Kon Tum', 'Gia Lai', 'Đắk Lắk', 'Đắk Nông', 'Lâm Đồng']
DONGNAMBO = ['Hồ Chí Minh', 'Đồng Nai', 'Bà Rịa Vũng Tàu', 'Vũng Tàu', 'Bình Dương', 'Bình Phước', 'Tây Ninh']
TAYNAMBO = ['Long An', 'Tiền Giang', 'Bến Tre', 'Vĩnh Long', 'Trà Vinh', 'Đồng Tháp', 'An Giang', 'Kiên Giang',
            'Cần Thơ', 'Hậu Giang', 'Sóc Trăng', 'Bạc Liêu', 'Cà Mau']

CACHE_ORGANIZATION_PREFIX = 'CACHE_ORGANIZATION_PREFIX'
CACHE_ARTICLE_PREFIX = 'CACHE_ARTICLE_PREFIX'
CACHE_TOURIST_ATTRACTION_PREFIX = 'CACHE_TOURIST_ATTRACTION_PREFIX'
CACHE_WORKER_PREFIX = 'CACHE_WORKER_PREFIX'
CACHE_CULTURE_PREFIX = 'CACHE_CULTURE_PREFIX'
CACHE_HOMETOP_PREFIX = 'CACHE_HOMETOP_PREFIX'
CACHE_HOMESEARCH_PREFIX = 'CACHE_HOMESEARCH_PREFIX'
CACHE_HOROSCOPE_PREFIX = 'CACHE_HOROSCOPE_PREFIX'
CACHE_XUATHANH_PREFIX = 'CACHE_XUATHANH_PREFIX'
CACHE_LABOR_EXPORT_PREFIX = 'CACHE_LABOR_EXPORT_PREFIX'
CACHE_LOICHUC_PREFIX = 'CACHE_LOICHUC_PREFIX'
CACHE_VIDEO_PREFIX = 'CACHE_VIDEO_PREFIX'
CACHE_ENGLISH_PREFIX = 'CACHE_ENGLISH_PREFIX'
CACHE_TRUYEN_PREFIX = 'CACHE_TRUYEN_PREFIX'
CACHE_QUANGNINH_PREFIX = 'CACHE_QUANGNINH_PREFIX'
CACHE_LESSION_PREFIX = 'CACHE_LESSION_PREFIX'
CACHE_EMERGENCY_PREFIX = 'CACHE_EMERGENCY_PREFIX'
CACHE_AGENCY_PREFIX = 'CACHE_AGENCY_PREFIX'
CACHE_TRAVEL_PREFIX = 'CACHE_TRAVEL_PREFIX'
CACHE_MY_PROVINCE_PREFIX = 'CACHE_MY_PROVINCE_PREFIX'
CACHE_LOCATION_PREFIX = 'CACHE_LOCATION_PREFIX'
CACHE_OPINION_PREFIX = 'CACHE_OPINION_PREFIX'
CACHE_PROPOSAL_PREFIX = 'CACHE_PROPOSAL_PREFIX'
CACHE_LAW_PREFIX = 'CACHE_LAW_PREFIX'
CACHE_ECONOMY_PREFIX = 'CACHE_ECONOMY_PREFIX'
CACHE_TRANSLATION_PREFIX = 'CACHE_TRANSLATION_PREFIX'
CACHE_BUSINESS_SOFTWARE_PREFIX = 'CACHE_BUSINESS_SOFTWARE_PREFIX'
CACHE_HOSPITAL_PREFIX = 'CACHE_HOSPITAL_PREFIX'
CACHE_WEAKPEOPLE_FORUM_PREFIX = 'CACHE_WEAKPEOPLE_FORUM_PREFIX'
CACHE_HOTDEAL_CATEGORY_PREFIX = 'CACHE_HOTDEAL_CATEGORY_PREFIX'
CACHE_HOTDEAL_STORE_PREFIX = 'CACHE_HOTDEAL_STORE_PREFIX'
CACHE_HOTDEAL_LIST_PREFIX = 'CACHE_HOTDEAL_LIST_PREFIX'
CACHE_HOTDEAL_SUBCATEGORY_PREFIX = 'CACHE_HOTDEAL_SUBCATEGORY_PREFIX'
CACHE_CHARITY_ORGANIZATION_PREFIX = 'CACHE_CHARITY_ORGANIZATION_PREFIX'
CACHE_CHARITY_PHILANTHROPIST_PREFIX = 'CACHE_CHARITY_PHILANTHROPIST_PREFIX'
CACHE_CHARITY_PREFIX = 'CACHE_CHARITY_PREFIX'
CACHE_GOVERNMENT_PREFIX = 'CACHE_GOVERNMENT_PREFIX'
CACHE_PUBLIC_ADMINISTRATION_PREFIX = 'CACHE_PUBLIC_ADMINISTRATION_PREFIX'
CACHE_PUBLIC_ADMINISTRATION_REGISTER_PREFIX = 'CACHE_PUBLIC_ADMINISTRATION_REGISTER_PREFIX'
CACHE_CHARITY_PROGRAM_PREFIX = 'CACHE_CHARITY_PROGRAM_PREFIX'
CACHE_TICKET_PREFIX = 'CACHE_TICKET_PREFIX'
CACHE_TAXI_PREFIX = 'CACHE_TAXI_PREFIX'
CACHE_WEBGAME_PREFIX = 'CACHE_WEBGAME_PREFIX'
CACHE_MEDICAL_PREFIX = 'CACHE_MEDICAL_PREFIX'
CACHE_MUSIC_PREFIX = 'CACHE_MUSIC_PREFIX'
CACHE_CLINIC_PREFIX = 'CACHE_CLINIC_PREFIX'
CACHE_PUBLIC_ADMINISTRATION_MB_PREFIX = 'CACHE_PUBLIC_ADMINISTRATION_MB_PREFIX'
CACHE_APPRENTICE_PREFIX = 'CACHE_APPRENTICE_PREFIX'
CACHE_EDUCATION_VIDEO_PREFIX = 'CACHE_EDUCATION_VIDEO_PREFIX'
CACHE_COMMUNITY_PREFIX = 'CACHE_COMMUNITY_PREFIX'
CACHE_LEGAL_REG_PREFIX = 'CACHE_LEGAL_REG_PREFIX'
CACHE_KNOWLEDGE_XKLD_PREFIX = 'CACHE_KNOWLEDGE_XKLD_PREFIX'
CACHE_PREPARING_EXAM_PREFIX = 'CACHE_PREPARING_EXAM_PREFIX'
CACHE_GREETING_CARD_PREFIX = 'CACHE_GREETING_CARD_PREFIX'
CACHE_HOTEL_PREFIX = 'CACHE_HOTEL_PREFIX'

AC1 = 'Giọng nam Miền Bắc'
AC2 = 'Giọng nữ Miền Bắc 1'
AC3 = 'Giọng nữ Miền Bắc 2'
AC4 = 'Giọng nam Miền Nam'
AC5 = 'Giọng nữ Miền Nam'

ACCENT = (
    ('hn_male_xuantin_vdts_48k-hsmm', AC1),
    ('hn_female_xuanthu_news_48k-hsmm', AC2),
    ('hn_female_thutrang_phrase_48k-hsmm', AC3),
    ('sg_male_xuankien_vdts_48k-hsmm', AC4),
    ('sg_female_xuanhong_vdts_48k-hsmm', AC5),
)

HOME_SEARCH_CULTURE = 'bài viết'
HOME_SEARCH_ARTICLE = 'địa điểm'
HOME_SEARCH_TABLE_CULTURE = 'culture'
HOME_SEARCH_TABLE_ARTICLE = 'article'
TEXT_TYPE_HOME_SEARCH = {
    HOME_SEARCH_TABLE_ARTICLE: 'Địa điểm',
    HOME_SEARCH_TABLE_CULTURE: "Bài viết"
}

MONTH = (
    ('', '-----'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)

QUARTER = (
    ('', '-----'),
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV'),
)

RADIO = 'Radio'
TEXT = 'Text'
TYPE = (
    (TEXT, TEXT),
    (RADIO, RADIO),
)

MAX_RECORD_HOME_SEARCH = 20

DESC = 'desc'
ASC = 'asc'
INVESTMENT_CURRENCY_INIT = 'tỷ'
RECRUITMENT_CURRENCY_INIT = 'triệu'
STORAGE_MEMORY = 'kb'

OTHER_EXTENSIONS = ('.pdf', '.csv', '.txt')
WORD_EXTENSIONS = ('.doc', '.dot', '.wbk', '.docx', '.docm', '.dotx', '.dotm', '.docb')
EXCEL_EXTENSIONS = (
    '.xls', '.xlt', '.xlm', '.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', '.xla', '.xlam', '.xll', '.xlw')
POWERPOINT_EXTENSIONS = ('.ppt', '.pot', '.pps', '.pptx', '.pptm', '.potx', '.potm', \
                         '.ppam', '.ppsx', '.ppsm', '.sldx', '.sldm')

WORD = 'Word'
EXCEL = 'Excel'
POWERPOINT = 'Powerpoint'
OTHER = 'Khác'

EXTENSIONS_TYPE = [WORD, EXCEL, POWERPOINT, OTHER]
EXTENSIONS_LIST = [(WORD, WORD_EXTENSIONS), (EXCEL, EXCEL_EXTENSIONS), (POWERPOINT, POWERPOINT_EXTENSIONS),
                   (OTHER, OTHER_EXTENSIONS)]

TYPE_IOS = 'ios'
TYPE_ANDROID = 'android'
DIVICES = 'all'

IMAGE_EXTENSION = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp')
FILE_EXTENSION = ('.pdf', '.csv', '.txt', '.doc', '.dot', '.wbk', '.docx', '.docm', '.dotx', '.dotm', '.docb')

REACTION_NONE_TEXT = "Không cảm xúc"
REACTION_LIKE_TEXT = 'Thích'
REACTION_LOVE_TEXT = "Yêu"
REACTION_WOW_TEXT = "Ngạc nhiên"
REACTION_HAHA_TEXT = "Cười"
REACTION_SAD_TEXT = "Buồn"
REACTION_ANGRY_TEXT = "Phản đối"

REACTION_NONE = 0
REACTION_LIKE = 1
REACTION_LOVE = 2
REACTION_WOW = 3
REACTION_HAHA = 4
REACTION_SAD = 5
REACTION_ANGRY = 6

REACTION = (
    (REACTION_NONE, REACTION_NONE_TEXT),
    (REACTION_LIKE, REACTION_LIKE_TEXT),
    (REACTION_LOVE, REACTION_LOVE_TEXT),
    (REACTION_WOW, REACTION_WOW_TEXT),
    (REACTION_HAHA, REACTION_HAHA_TEXT),
    (REACTION_SAD, REACTION_SAD_TEXT),
    (REACTION_ANGRY, REACTION_ANGRY_TEXT),
)

AC1 = 'Giọng nam Miền Bắc'
AC2 = 'Giọng nữ Miền Bắc 1'
AC3 = 'Giọng nữ Miền Bắc 2'
AC4 = 'Giọng nam Miền Nam'
AC5 = 'Giọng nữ Miền Nam'

GOOGLE_ACCENT_A = "Giọng nữ Bắc 1 - Google"
GOOGLE_ACCENT_B = "Giọng nam Bắc 1 - Google"
GOOGLE_ACCENT_C = "Giọng nữ Bắc 2 - Google"
GOOGLE_ACCENT_D = "Giọng nam Bắc 2 - Google"

ACCENT = (
    ("vi-VN-Wavenet-A", GOOGLE_ACCENT_A),
    ("vi-VN-Wavenet-B", GOOGLE_ACCENT_B),
    ("vi-VN-Wavenet-C", GOOGLE_ACCENT_C),
    ("vi-VN-Wavenet-D", GOOGLE_ACCENT_D),
    ('hn_male_xuantin_vdts_48k-hsmm', AC1),
    ('hn_female_xuanthu_news_48k-hsmm', AC2),
    ('hn_female_thutrang_phrase_48k-hsmm', AC3),
    ('sg_male_xuankien_vdts_48k-hsmm', AC4),
    ('sg_female_xuanhong_vdts_48k-hsmm', AC5),
)

LIST_ACCENT = {
    'hn_male_xuantin_vdts_48k-hsmm': AC1,
    'hn_female_xuanthu_news_48k-hsmm': AC2,
    'hn_female_thutrang_phrase_48k-hsmm': AC3,
    'sg_male_xuankien_vdts_48k-hsmm': AC4,
    'sg_female_xuanhong_vdts_48k-hsmm': AC5,
}

GOOGLE_ACCENT_KEYS = [
    "vi-VN-Wavenet-A",
    "vi-VN-Wavenet-B",
    "vi-VN-Wavenet-C",
    "vi-VN-Wavenet-D",
]

GOOGLE_ACCENT = (
    ("vi-VN-Wavenet-A", GOOGLE_ACCENT_A),
    ("vi-VN-Wavenet-B", GOOGLE_ACCENT_B),
    ("vi-VN-Wavenet-C", GOOGLE_ACCENT_C),
    ("vi-VN-Wavenet-D", GOOGLE_ACCENT_D),
)

OLD_ACCENT = ['hn_male_xuantin_vdts_48k-hsmm', 'hn_female_xuanthu_news_48k-hsmm', 'hn_female_thutrang_phrase_48k-hsmm',
              'sg_male_xuankien_vdts_48k-hsmm', 'sg_female_xuanhong_vdts_48k-hsmm']

API_HOST_ENDPOINT = 'https://serviceqn.hcdt.vn'
SERVICE_QN_API_UPLOAD = 'https://cdnqn.hcdt.vn/{id}'
SERVICE_QN_API_ASSIGN = 'https://cdnqn.hcdt.vn/dir/assign?count=1'

GROUP_ID = '351912440383137'
COMPANY_ID = '141493402617530'
GOVERNMENT_ID = '70506183153870'
OFFLINE_ID = 'b79078c5-e3cd-40c5-9bfb-0be17198d621'
OFFLINE_ID_COMMENT = 'b932e93a-190a-4bcc-978b-b121dca078a1'
APP_ID = "942UTPH8i0VO2FCxvVjPcW0liAExVdpR"
PASSWORD = "eyJ0eXBlIjoiand0IiwiYWxnIjoiUlM1MTIiLCJraWQiOiIwIn0.eyJzdWIiOiIxNDE0OTM0MDI2MTc1MzAiLCJhdWQiOiIxMjM0LTU2NzgtOTEwIiwibmJmIjoxNTY4Mjg4MTUzLCJpc3MiOiJzc28uc253LmNvbSIsImlkIjoiMTQxNDkzNDAyNjE3NTMwIiwiZXhwIjoxNTk5ODI0MTUzLCJpYXQiOjB9.AYzVTFzw0nN73BWLRc2OVBj3XGdbwqbsaS1KnFCWnV76hRyLmKxO4uPzFPz_eabsR0_3gpZwyP7QgItECJprpfQWoQ8XkVzRlf4F2IXCFUf-dAJbdm8ooYPCmxTbhW0oBwBRA0wd64ZP9S4yzV2Bkb93Gxv5NbCp5Dyc38d7alP4TspMYKmOyixCmwMdm3B7LQneP6bxZ-2YOtlQjGwALA1dED4nJ704pt_V0TZ9jSN1q4tn2Jr_d2DyHaYG2RGkf-V3tt3P8fTg7wg-CObZyK1wviCF3EoiF3Pz46lMF3DsMYKnz5bouz4JE7pyfRKGF2rhB4uZhBow0x1kHh1QHw"
EMAIL_DEFAULT = 'congdan@quangninh.gov.vn'

SERVICE_QN_API_TAG = '{}/tags?maxscore=0&minscore=0'.format(GROUP_ID)
SERVICE_QN_API_OPINION_ENTRIES = '{}/entries'.format(GROUP_ID)
SERVICE_QN_API_GET_ENTRIES = '{}/entries'
SERVICE_QN_API_GET_REJECTED_ENTRIES = '{}/rejected_entries'
SERVICE_QN_API_USER_LOGIN = 'user/login'
SERVICE_QN_API_LIST_COMMENT = '{id}/comments'
SERVICE_QN_API_LIST_REACTION = '{id}/reactions'
SERVICE_QN_API_USER_INFO = 'user/{id}'
SERVICE_QN_API_ADD_COMMENT = '{id}/comments'
SERVICE_QN_API_EDIT_COMMENT = 'comments/{id}'
SERVICE_QN_API_GET_ENTRIES_UNAPPROVAL = 'public/qn/un_approval'

GOVERNMENT_DATA_ID = '211174952026809'
EMERGENCY_SITUATION_DATA_ID = '281543696204481'
CONTENT_TYPE_FORM_DATA = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarytAI6NAJglQEO4FPK"}
CONTENT_TYPE_FORM_JSON = "application/json"
HEADER_FORM_JSON = {"Content-Type": CONTENT_TYPE_FORM_JSON, "company-id": COMPANY_ID}
IMAGE = 'image'
FILE = 'file'
TOTAL_FILE_AMOUNT = 10
LINH_VUC_KHAC = "LĨNH VỰC KHÁC"
MAX_SCORE = int(round(time.time() * 1000))
EXTRA_TIME_CHECK_EXP = 60 * 60 * 1000
TIME_CHECK_EXP = MAX_SCORE + EXTRA_TIME_CHECK_EXP
LIMIT_RECORD = 2000
MAX_STRING = 200
MINE = "image/png"
PUT = 'putting'
POST = 'posting'
VERSION_CREATE = 1
VERSION_UPDATE = 2
DEFAULT_API_HOST = 'https://serviceqn.hcdt.vn/'
INFORMATION = 'Information'
EMERGENCY = 'EmergencySituation'
OPINION = 'Opinion'
TIME_DELAY_UPLOAD_FILE = 5
SERVICE_QN_API_ADD_REACTION = 'reactions'
SERVICE_QN_API_DETAIL_ENTRY = 'entries/{id}/detail'
SERVICE_QN_API_DELETE_ENTRY = 'entries/{id}'
METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_PUT = 'put'
METHOD_DELETE = 'delete'
BAD_GATEWAY = 'Bad Gateway'
MODULE = (
    (OPINION, OPINION),
    (EMERGENCY, EMERGENCY),
    (INFORMATION, INFORMATION),
)
SYNC_DATA = 'Sync data'
SYNC_REJECTED_DATA = 'Sync rejected data'
SYNC_UNAPPROVAL_DATA = 'Sync unapproval data'
SYNC_COMMENT = 'Sync comment'
SYNC_REACTION = 'Sync reaction'
POST_DATA = 'Post data'
POST_COMMENT = 'Post comment'
POST_REACTION = 'Post reaction'
METHOD = (
    (SYNC_DATA, SYNC_DATA),
    (SYNC_REJECTED_DATA, SYNC_REJECTED_DATA),
    (SYNC_UNAPPROVAL_DATA, SYNC_UNAPPROVAL_DATA),
    (SYNC_COMMENT, SYNC_COMMENT),
    (SYNC_REACTION, SYNC_REACTION),
    (POST_DATA, POST_DATA),
    (POST_COMMENT, POST_COMMENT),
    (POST_REACTION, POST_REACTION),
)

# ADD O TO AVOID DUPLICATE KEY
O_PENDING = 'Đang chờ phê duyệt'
O_REJECTED = 'Từ chối'
O_PROCESSING = 'Đang xử lý'
O_DONE = 'Đã xử lý'
O_DRAFT = 'Lưu nháp'
STATUS_OPINION = (
    (O_PENDING, O_PENDING),
    (O_REJECTED, O_REJECTED),
    (O_PROCESSING, O_PROCESSING),
    (O_DONE, O_DONE),
    (O_DRAFT, O_DRAFT)
)

WAITING_APPROVAL_KEY = 1
NOT_APPROVED_KEY = 2
APPROVED_KEY = 3

STATUS_APPROVAL = (
    (APPROVED_KEY, 'Đã duyệt'),
    (NOT_APPROVED_KEY, 'Không phế duyệt'),
    (WAITING_APPROVAL_KEY, 'Đang kiểm duyệt'),
)

# CURRENCY_CHOICES
DOLLAR = 'dollar'
YEN = 'yen'
VND = 'vnd'
CURRENCY_CHOICES = (
    (DOLLAR, 'Dollar ($)'),
    (YEN, 'Yen (¥)'),
    (VND, 'VNĐ (₫)')
)

PROVIDER_FACEBOOK = 'facebook'
PROVIDER_GOOGLE = 'google'
PROVIDER_ZALO = 'zalo'
PROVIDER_APPLE = 'apple'

# type model service
TYPE_HOTELS = 1
TYPE_DRIVING_CAR = 2
TYPE_GUIDELINES = 3
TYPE_TICKET_VISIT = 4
TYPE_SHIP_TICKET = 5
TYPE_RESTAURANT = 6
TYPE_NEWS = 7
TYPE_SPECIAL = 8
TYPE_TOUR = 9
TYPE_FLIGHT = 10
TYPE_SCHEDULE = 11
TYPE_HASHED_GEO = 12
TYPE_TRANSPORT = 13
TYPE_PROMOTION = 14
TYPE_EVENT = 15
TYPE_SURVEY = 16
TYPE_SYSTEM = 17
TYPE_DRINK = 18

TYPE_APPROVE_NEWS = 1001
TYPE_APPROVE_GEO = 1002
TYPE_APPROVE_PROMOTION = 1003


TYPE_ACTION_COMMENT = 1004
TYPE_ACTION_REPLY = 1005
TYPE_UPDATE_PROFILE = 1006
TYPE_APPROVE_PROFILE = 1007

TYPE_APPROVE_TICKET_VISIT = 1008

LIST_CATE_HASHED_GEO = ['khu_vui_choi', 'rung_quoc_gia', 'lang_nghe', 'bao_tang', 'bai_bien', 'danh-lam-thang-canh']

MAP_TYPE_STRING = {
    TYPE_HOTELS: "Khách sạn, Hotel",
    TYPE_DRIVING_CAR: "Thuê xe tự lái, Car, driving",
    TYPE_GUIDELINES: "Hướng dẫn viên, guideline",
    TYPE_TICKET_VISIT: "Vé tham quan, ticket visit",
    TYPE_SHIP_TICKET: "Vé tàu, Ship",
    TYPE_RESTAURANT: "Nhà hàng, đồ ăn, restaurant, food",
    TYPE_NEWS: "Tin tức, news",
    TYPE_SPECIAL: "Đặc sản địa phương, local special",
    TYPE_TOUR: "Chuyến du lịch, tour",
    TYPE_FLIGHT: "Chuyến bay, máy bay, flight",
    TYPE_SCHEDULE: "Kế hoạch du lịch, lịch trình, schedule",
    TYPE_HASHED_GEO: "Vị trí địa lí, geography, map",
    TYPE_TRANSPORT: "Phương tiện, tìm đường, transport, map",
    TYPE_PROMOTION: "Tin tức giảm giá, promotion, news",
    TYPE_DRINK: "Đồ uống, drink, coffee",
}



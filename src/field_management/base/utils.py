import base64, os, json, maxminddb, requests, time, boto3, botocore, logging, re, uuid
import random
import string
import six

from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from datetime import datetime, date
# from google.cloud import texttospeech
from django.core.files.storage import default_storage
from django.core.files.temp import NamedTemporaryFile
from google.oauth2 import service_account
from numpy.core.umath import lcm
from threading import Thread
from urllib.parse import urlparse

from django.core.files import File
from django.conf import settings
from django.core.cache import caches

from base.middleware import get_request
from base.choices import CLIENT_LANG_KEY, HTTP_AUTHORIZATION

MAX_PROBLEM_LIST = 100

logger = logging.getLogger(__name__)
cache = caches['default']

WEEKDAYS = {'Sunday': 'Chủ nhật', 'Monday': 'Thứ hai', 'Tuesday': 'Thứ ba', 'Wednesday': 'Thứ tư',
            'Thursday': 'Thứ năm', 'Friday': 'Thứ sáu', 'Saturday': 'Thứ bảy'}

GOOGLE_APPLICATION_CREDENTIALS = "./data/master/tienichnguoidan-demo-1ba371ed2be2.json"
END_CHAR = [" ", ".", ","]
MAX_LENGTH = 5000


def clean_html(html, length=False):
    """
    clean html code, return text
    1. remove all script and style elements
    2. break into lines and remove leading and trailing space on each
    3. break multi-headlines into a line each
    4. drop blank lines
    """
    if not html:
        return None
    html = html.replace('><', '> <')
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(['script', 'style']):
        script.decompose()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # return cleaned text
    return text[:length] if text and length else text


def can_chi_year(year):
    start_year = 1984
    arr_can = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
    arr_chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    j = arr_can.__len__()
    k = arr_chi.__len__()
    bcnn = lcm(j, k)

    result = []
    j = 0
    k = 0
    for i in range(bcnn):
        if j > arr_can.__len__() - 1:
            j = 0
        if k > arr_chi.__len__() - 1:
            k = 0
        out = arr_can[j] + ' ' + arr_chi[k]
        j += 1
        k += 1
        result.append((start_year, out))
        start_year += 1

    arr_can_chi = {k: v for k, v in result}
    try:
        can_chi = arr_can_chi[year]
    except Exception as e:
        while year < result[0][0]:
            year += bcnn
        while year > result[bcnn - 1][0]:
            year -= bcnn
        can_chi = arr_can_chi[year]

    return can_chi


def can_chi():
    start_year = 1984
    arr_can = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
    arr_chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    j = arr_can.__len__()
    k = arr_chi.__len__()
    bcnn = lcm(j, k)

    result = []
    j = 0
    k = 0
    for i in range(bcnn):
        if j > arr_can.__len__() - 1:
            j = 0
        if k > arr_chi.__len__() - 1:
            k = 0
        out = arr_can[j] + ' ' + arr_chi[k]
        j += 1
        k += 1
        result.append((str(start_year), out))
        start_year += 1

    return tuple(result)


def get_filename(filename):
    return filename.upper()


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def get_html_xuat_hanh(xuat_hanh):
    import calendar
    xh = xuat_hanh
    eng_day_name = calendar.day_name[xh.ngay_duong.weekday()]
    vn_day_name = WEEKDAYS[eng_day_name]
    with open('templates/app/xuathanh.html', 'r') as file:
        html = file.read()
        print(html)
        return html.format(vn_day_name, xh.ngay_duong, xh.ngay_am, xh.ten_ngay, xh.ten_thang, xh.la_ngay, xh.tai_than,
                           xh.hy_than, xh.hac_than, xh.gio_hoang_dao, xh.gio_hac_dao, xh.tuoi_khac_ngay,
                           xh.tuoi_khac_thang, xh.nen, xh.khong_nen)


if __name__ == '__main__':
    test_html = """"""

    text = clean_html(test_html)

    # print('cleaned html: \n')
    print(text)


def encrypt(string):
    try:
        # convert integer etc to string first
        string = str(string)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(string.encode('UTF-8'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("UTF-8")
        return encrypted_text
    except Exception as e:
        return None


def decrypt(string):
    try:
        # base64 decode
        string = base64.urlsafe_b64decode(string)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(string).decode("UTF-8")
        return decoded_text
    except Exception as e:
        return None


def get_link_voice(voice, content):
    try:
        config_voice = settings.CONFIG_VOICE
        content = content.lower()
        payload = {
            "app_id": config_voice["app_id"],
            "key": config_voice["key"],
            "voice": voice,
            "user_id": config_voice["user_id"],
            "service_type": config_voice["service_type"],
            "bit_rate": config_voice["bit_rate"],
            "sample_rate": config_voice["sample_rate"],
            "type_output": config_voice["type_output"],
            "audio_type": config_voice["audio_type"],
            "input_text": clean_html(str(content))
        }
        url = config_voice["url"]
        api_response = requests.post(url, data=payload)

        # hotfix-debug: show status code and response text form vb
        print('vbee response status code: ', api_response.status_code)
        print('vbee response status text: ', api_response.text)

        api_response = api_response.json()
        link_audio = api_response['link']
        return link_audio
    except Exception:
        raise Exception


def vb_url_to_s3(model):
    if not hasattr(model, 's3_url'):
        return
    if not hasattr(model, 'url'):
        return

    try:
        r = requests.get(model.url)
        filename = os.path.basename(urlparse(model.url).path)

        with open('tmp/{}'.format(filename), 'wb') as tf:
            tf.write(r.content)

        with open('tmp/{}'.format(filename), 'rb') as tf:
            model.s3_url.save(filename, File(tf), save=True)

        os.remove('tmp/{}'.format(filename))
    except Exception as e:
        print('cannot convert url from vbee to s3', e)


def create_voice(voice, content, model):
    link = get_link_voice(voice=voice, content=content)
    model.url = link

    # download vbee audio and upload to s3
    vb_url_to_s3(model)

    model.created_at = datetime.now()
    model.save()


class VoiceCreater(Thread):
    def __init__(self, voice, content, model):
        super(VoiceCreater, self).__init__()
        self.voice = voice
        self.content = content
        self.model = model

    def run(self):
        create_voice(self.voice, self.content, self.model)


# Start Google Cloud text-to-Speech

def find_end_index(content, start_index, text_length=MAX_LENGTH):
    # finding and return end index of a text

    if start_index + text_length > len(content):
        max_index = len(content)
    else:
        max_index = start_index + text_length

    for i in range(max_index - 1, start_index - 1, -1):
        if content[i] in END_CHAR or i == len(content) - 1:
            return i + 1


def get_audio_path(file_data, base_name):
    # push audio file to s3 and return file name

    file_name = '{}/audio/{}.mp3'.format(base_name, time.time())
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

    bucket.put_object(Key=file_name, Body=file_data, ContentType='audio/mp3', CacheControl="max-age=86400")
    return file_name


# def write_audio(voice, content, base_name):
#     # convert text to speech
#
#     content = clean_html(content)
#     credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
#     client = texttospeech.TextToSpeechClient(credentials=credentials)
#     voice = texttospeech.types.VoiceSelectionParams(
#         language_code='vi-VN',
#         name=voice)
#
#     audio_config = texttospeech.types.AudioConfig(
#         audio_encoding=texttospeech.enums.AudioEncoding.MP3)
#
#     synthesis_input = texttospeech.types.SynthesisInput(text="")
#     response = client.synthesize_speech(synthesis_input, voice, audio_config)
#     start_index = 0
#     end_index = 0
#     while end_index < len(content) - 1:
#         end_index = find_end_index(content, start_index)
#         synthesis_input = texttospeech.types.SynthesisInput(text=content[start_index:end_index])
#         response.audio_content += client.synthesize_speech(synthesis_input, voice, audio_config).audio_content
#         start_index = end_index
#
#     return get_audio_path(response.audio_content, base_name)


def google_create_voice(voice, content, model, base_name):
    if not hasattr(model, 'created_at'):
        return
    if hasattr(model, 's3_url'):
        model.s3_url = write_audio(voice, content, base_name)
    elif hasattr(model, 'url'):
        model.url = write_audio(voice, content, base_name)
    else:
        return
    model.created_at = datetime.now()
    model.save()


class GoogleVoiceCreater(Thread):
    def __init__(self, voice, content, model, base_name):
        super(GoogleVoiceCreater, self).__init__()
        self.voice = voice
        self.content = content
        self.model = model
        self.base_name = base_name

    def run(self):
        # End Google Cloud text-to-Speech
        google_create_voice(self.voice, self.content, self.model, self.base_name)


def to_country_code(res):
    try:
        return res['country']['iso_code']
    except:
        raise ValueError


def check_vietnam_ip(ip):
    try:
        db = './data/master/GeoLite2-Country.mmdb'
        reader = maxminddb.open_database(db)
        res = reader.get(ip)
        if res is None:
            return False, 'Unknow'
        country_code = to_country_code(res)
        if country_code in settings.ALLOWED_COUNTRYS:
            return True, country_code
        return False, country_code
    except Exception as _:
        return False, 'Unknow'


def encrypt_rsa(public_key_loc, message):
    '''
    param: public_key_loc Path to public key
    param: message String to be encrypted
    return base64 encoded encrypted string
    '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    key = open(public_key_loc, "rb").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(bytes(message, 'utf-8'))
    return base64.b64encode(encrypted).decode()


def generate_rsa(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA
    private_key = RSA.generate(bits)
    public_key = private_key.publickey()
    with open("private.pem", "wb") as prv_file:
        prv_file.write(private_key.exportKey("PEM"))

    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key.exportKey("PEM"))
    return private_key, public_key


def decrypt_rsa(private_key_loc, package):
    '''
        param: public_key_loc Path to your private key
        param: package String to be decrypted
        return decrypted string
        '''
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    from base64 import b64decode
    key = open(private_key_loc, "rb").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    decrypted = rsakey.decrypt(b64decode(package))
    return decrypted


def get_region_by_ip(ip):
    try:
        db = '../data/master/GeoLite2-City.mmdb'
        reader = maxminddb.open_database(db)
        res = reader.get(ip)
        return to_city(res), to_region(res), to_country_code(res)
    except Exception as _:
        return 'Unknow', 'Unknow', 'Unknow'


def to_region(res):
    try:
        return res['subdivisions'][0]['names']['en']
    except:
        raise ValueError


def to_city(res):
    try:
        return res['city']['names']['en']
    except:
        raise ValueError


def get_object_client_s3():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )


def get_bucket_s3():
    s3 = boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    return s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)


def put_file_to_boto_s3_from_url(url_file, directory, extension, content_type):
    """
    function put file to boto-s3 from url
    :param url_file:
    :param directory:
    :param extension:
    :param content_type:
    :return: file_name or None
    """
    r = requests.get(url_file)
    if not r.ok:
        return None

    file = requests.get(url_file).content
    time_now = time.time()
    file_name = directory + '/{}.{}'.format(time_now, extension)
    bucket = get_bucket_s3()

    try:
        bucket.put_object(Key=file_name, Body=file, ContentType=content_type, CacheControl="max-age=86400")
        # file_url = 'https://{}/{}'.format(settings.AWS_S3_CUSTOM_DOMAIN, file_name)
        return file_name
    except Exception as e:
        logger.error('Failed to put image to S3: ' + str(e))
        return None


def put_file_to_boto_s3(file, directory, extension, content_type):
    """
    function put file to boto-s3
    :param file:
    :param directory:
    :param extension:
    :param content_type:
    :return: file_name or None
    """
    time_now = time.time()
    file_name = directory + '/{}.{}'.format(time_now, extension)
    bucket = get_bucket_s3()

    try:
        bucket.put_object(Key=file_name, Body=file, ContentType=content_type, CacheControl="max-age=86400")
        return file_name
    except Exception as e:
        logger.error('Failed to put file to S3: ' + str(e))
        return None


def clean_cache_by_prefix(prefix):
    """clean cache when model saved - ignore if any exception raised"""
    try:
        if settings.CACHES['default']['BACKEND'] == 'django_redis.cache.RedisCache':
            keys = cache.keys("*{}*".format(prefix))
            if keys:
                cache.delete_many(keys)
    except Exception as _:
        pass


def dowload_files_from_s3(files, images):
    files_dict = []
    for item in images:
        image = item.__dict__
        file_url = image['image']
        file_name = file_url[file_url.rfind('/') + 1:]
        image.update({'file': file_url, 'file_name': file_name, 'instance': item})
        files_dict.append(image)

    for item in files:
        file = item.__dict__
        file.update({'instance': item})
        files_dict.append(file)

    for item in files_dict:
        """ get file url and create file path """
        file_url = str(item['file'])
        file_path = str('logs/tmp/{}'.format(str(item['file_name'])))
        try:
            s3 = get_object_client_s3()
            s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, file_url, file_path)
            item.update({'tmp_path': file_path})
        except botocore.exceptions.ClientError as e:
            logger.log('Download file {} failed. Error: {}'.format(file_url, str(e)))
            continue
    return files_dict


def export_entities_to_tags(detailMd):
    tags = {}
    entities = detailMd.get("entities") if detailMd.get("entities") else []

    for item in entities:
        offset = int(item.get("offset"))
        data = item.get("data")
        type = item.get("type")

        """Get data image"""
        image_url = data.get("url") if data.get("url") else data.get("src")
        file_name = item.get("data").get("fileName")

        """Update tags"""
        if type == "IMAGE":
            tag = '<img src="{}" alt="{}" height="auto" width="100%">'.format(image_url, file_name)
            tags.update({offset: {'tags': [tag], 'type': 'image'}})
    return tags


def insert_to_tags(tags, tag, offset):
    if offset not in tags:
        tags.update({offset: {'tags': [tag]}})
    else:
        tags_data = tags[offset]
        tags_data['tags'].append(tag)
        tags[offset].update(tags_data)
    return tags


if __name__ == '__main__':
    region = get_region_by_ip('171.254.139.43')
    print(region)


def handle_page_params(page, limit):
    paginator = {}
    if page is None or page.isdigit() == False:
        page = 1
    page = int(page)
    if page < 1:
        page = 1
    paginator['page'] = page
    if limit is None or limit.isdigit() == False:
        limit = MAX_PROBLEM_LIST
    limit = int(limit)
    paginator['limit'] = limit
    paginator['min'] = (page - 1) * limit
    paginator['max'] = paginator['min'] + limit
    return paginator


asciiChars = {
    '0': ['°', '₀', '۰', '０'],
    '1': ['¹', '₁', '۱', '１'],
    '2': ['²', '₂', '۲', '２'],
    '3': ['³', '₃', '۳', '３'],
    '4': ['⁴', '₄', '۴', '٤', '４'],
    '5': ['⁵', '₅', '۵', '٥', '５'],
    '6': ['⁶', '₆', '۶', '٦', '６'],
    '7': ['⁷', '₇', '۷', '７'],
    '8': ['⁸', '₈', '۸', '８'],
    '9': ['⁹', '₉', '۹', '９'],
    'a': ['à', 'á', 'ả', 'ã', 'ạ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ', 'ā', 'ą', 'å', 'α', 'ά',
          'ἀ', 'ἁ', 'ἂ', 'ἃ', 'ἄ', 'ἅ', 'ἆ', 'ἇ', 'ᾀ', 'ᾁ', 'ᾂ', 'ᾃ', 'ᾄ', 'ᾅ', 'ᾆ', 'ᾇ', 'ὰ', 'ά', 'ᾰ', 'ᾱ', 'ᾲ', 'ᾳ',
          'ᾴ', 'ᾶ', 'ᾷ', 'а', 'أ', 'အ', 'ာ', 'ါ', 'ǻ', 'ǎ', 'ª', 'ა', 'अ', 'ا', 'ａ', 'ä'],
    'b': ['б', 'β', 'ب', 'ဗ', 'ბ', 'ｂ'],
    'c': ['ç', 'ć', 'č', 'ĉ', 'ċ', 'ｃ'],
    'd': ['ď', 'ð', 'đ', 'ƌ', 'ȡ', 'ɖ', 'ɗ', 'ᵭ', 'ᶁ', 'ᶑ', 'д', 'δ', 'د', 'ض', 'ဍ', 'ဒ', 'დ', 'ｄ'],
    'e': ['é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'ë', 'ē', 'ę', 'ě', 'ĕ', 'ė', 'ε', 'έ', 'ἐ', 'ἑ', 'ἒ',
          'ἓ', 'ἔ', 'ἕ', 'ὲ', 'έ', 'е', 'ё', 'э', 'є', 'ə', 'ဧ', 'ေ', 'ဲ', 'ე', 'ए', 'إ', 'ئ', 'ｅ'],
    'f': ['ф', 'φ', 'ف', 'ƒ', 'ფ', 'ｆ'],
    'g': ['ĝ', 'ğ', 'ġ', 'ģ', 'г', 'ґ', 'γ', 'ဂ', 'გ', 'گ', 'ｇ'],
    'h': ['ĥ', 'ħ', 'η', 'ή', 'ح', 'ه', 'ဟ', 'ှ', 'ჰ', 'ｈ'],
    'i': ['í', 'ì', 'ỉ', 'ĩ', 'ị', 'î', 'ï', 'ī', 'ĭ', 'į', 'ı', 'ι', 'ί', 'ϊ', 'ΐ', 'ἰ', 'ἱ', 'ἲ', 'ἳ', 'ἴ', 'ἵ', 'ἶ',
          'ἷ', 'ὶ', 'ί', 'ῐ', 'ῑ', 'ῒ', 'ΐ', 'ῖ', 'ῗ', 'і', 'ї', 'и', 'ဣ', 'ိ', 'ီ', 'ည်', 'ǐ', 'ი', 'इ', 'ی', 'ｉ'],
    'j': ['ĵ', 'ј', 'Ј', 'ჯ', 'ج', 'ｊ'],
    'k': ['ķ', 'ĸ', 'к', 'κ', 'Ķ', 'ق', 'ك', 'က', 'კ', 'ქ', 'ک', 'ｋ'],
    'l': ['ł', 'ľ', 'ĺ', 'ļ', 'ŀ', 'л', 'λ', 'ل', 'လ', 'ლ', 'ｌ'],
    'm': ['м', 'μ', 'م', 'မ', 'მ', 'ｍ'],
    'n': ['ñ', 'ń', 'ň', 'ņ', 'ŉ', 'ŋ', 'ν', 'н', 'ن', 'န', 'ნ', 'ｎ'],
    'o': ['ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'ø', 'ō', 'ő', 'ŏ', 'ο',
          'ὀ', 'ὁ', 'ὂ', 'ὃ', 'ὄ', 'ὅ', 'ὸ', 'ό', 'о', 'و', 'θ', 'ို', 'ǒ', 'ǿ', 'º', 'ო', 'ओ', 'ｏ', 'ö'],
    'p': ['п', 'π', 'ပ', 'პ', 'پ', 'ｐ'],
    'q': ['ყ', 'ｑ'],
    'r': ['ŕ', 'ř', 'ŗ', 'р', 'ρ', 'ر', 'რ', 'ｒ'],
    's': ['ś', 'š', 'ş', 'с', 'σ', 'ș', 'ς', 'س', 'ص', 'စ', 'ſ', 'ს', 'ｓ'],
    't': ['ť', 'ţ', 'т', 'τ', 'ț', 'ت', 'ط', 'ဋ', 'တ', 'ŧ', 'თ', 'ტ', 'ｔ'],
    'u': ['ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự', 'û', 'ū', 'ů', 'ű', 'ŭ', 'ų', 'µ', 'у', 'ဉ', 'ု', 'ူ',
          'ǔ', 'ǖ', 'ǘ', 'ǚ', 'ǜ', 'უ', 'उ', 'ｕ', 'ў', 'ü'],
    'v': ['в', 'ვ', 'ϐ', 'ｖ'],
    'w': ['ŵ', 'ω', 'ώ', 'ဝ', 'ွ', 'ｗ'],
    'x': ['χ', 'ξ', 'ｘ'],
    'y': ['ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ', 'ÿ', 'ŷ', 'й', 'ы', 'υ', 'ϋ', 'ύ', 'ΰ', 'ي', 'ယ', 'ｙ'],
    'z': ['ź', 'ž', 'ż', 'з', 'ζ', 'ز', 'ဇ', 'ზ', 'ｚ'],
    'aa': ['ع', 'आ', 'آ'],
    'ae': ['æ', 'ǽ'],
    'ai': ['ऐ'],
    'ch': ['ч', 'ჩ', 'ჭ', 'چ'],
    'dj': ['ђ', 'đ'],
    'dz': ['џ', 'ძ'],
    'ei': ['ऍ'],
    'gh': ['غ', 'ღ'],
    'ii': ['ई'],
    'ij': ['ĳ'],
    'kh': ['х', 'خ', 'ხ'],
    'lj': ['љ'],
    'nj': ['њ'],
    'oe': ['ö', 'œ', 'ؤ'],
    'oi': ['ऑ'],
    'oii': ['ऒ'],
    'ps': ['ψ'],
    'sh': ['ш', 'შ', 'ش'],
    'shch': ['щ'],
    'ss': ['ß'],
    'sx': ['ŝ'],
    'th': ['þ', 'ϑ', 'ث', 'ذ', 'ظ'],
    'ts': ['ц', 'ც', 'წ'],
    'ue': ['ü'],
    'uu': ['ऊ'],
    'ya': ['я'],
    'yu': ['ю'],
    'zh': ['ж', 'ჟ', 'ژ'],
    '(c)': ['©'],
    'A': ['Á', 'À', 'Ả', 'Ã', 'Ạ', 'Ă', 'Ắ', 'Ằ', 'Ẳ', 'Ẵ', 'Ặ', 'Â', 'Ấ', 'Ầ', 'Ẩ', 'Ẫ', 'Ậ', 'Å', 'Ā', 'Ą', 'Α', 'Ά',
          'Ἀ', 'Ἁ', 'Ἂ', 'Ἃ', 'Ἄ', 'Ἅ', 'Ἆ', 'Ἇ', 'ᾈ', 'ᾉ', 'ᾊ', 'ᾋ', 'ᾌ', 'ᾍ', 'ᾎ', 'ᾏ', 'Ᾰ', 'Ᾱ', 'Ὰ', 'Ά', 'ᾼ', 'А',
          'Ǻ', 'Ǎ', 'Ａ', 'Ä'],
    'B': ['Б', 'Β', 'ब', 'Ｂ'],
    'C': ['Ç', 'Ć', 'Č', 'Ĉ', 'Ċ', 'Ｃ'],
    'D': ['Ď', 'Ð', 'Đ', 'Ɖ', 'Ɗ', 'Ƌ', 'ᴅ', 'ᴆ', 'Д', 'Δ', 'Ｄ'],
    'E': ['É', 'È', 'Ẻ', 'Ẽ', 'Ẹ', 'Ê', 'Ế', 'Ề', 'Ể', 'Ễ', 'Ệ', 'Ë', 'Ē', 'Ę', 'Ě', 'Ĕ', 'Ė', 'Ε', 'Έ', 'Ἐ', 'Ἑ', 'Ἒ',
          'Ἓ', 'Ἔ', 'Ἕ', 'Έ', 'Ὲ', 'Е', 'Ё', 'Э', 'Є', 'Ə', 'Ｅ'],
    'F': ['Ф', 'Φ', 'Ｆ'],
    'G': ['Ğ', 'Ġ', 'Ģ', 'Г', 'Ґ', 'Γ', 'Ｇ'],
    'H': ['Η', 'Ή', 'Ħ', 'Ｈ'],
    'I': ['Í', 'Ì', 'Ỉ', 'Ĩ', 'Ị', 'Î', 'Ï', 'Ī', 'Ĭ', 'Į', 'İ', 'Ι', 'Ί', 'Ϊ', 'Ἰ', 'Ἱ', 'Ἳ', 'Ἴ', 'Ἵ', 'Ἶ', 'Ἷ', 'Ῐ',
          'Ῑ', 'Ὶ', 'Ί', 'И', 'І', 'Ї', 'Ǐ', 'ϒ', 'Ｉ'],
    'J': ['Ｊ'],
    'K': ['К', 'Κ', 'Ｋ'],
    'L': ['Ĺ', 'Ł', 'Л', 'Λ', 'Ļ', 'Ľ', 'Ŀ', 'ल', 'Ｌ'],
    'M': ['М', 'Μ', 'Ｍ'],
    'N': ['Ń', 'Ñ', 'Ň', 'Ņ', 'Ŋ', 'Н', 'Ν', 'Ｎ'],
    'O': ['Ó', 'Ò', 'Ỏ', 'Õ', 'Ọ', 'Ô', 'Ố', 'Ồ', 'Ổ', 'Ỗ', 'Ộ', 'Ơ', 'Ớ', 'Ờ', 'Ở', 'Ỡ', 'Ợ', 'Ø', 'Ō', 'Ő', 'Ŏ', 'Ο',
          'Ό', 'Ὀ', 'Ὁ', 'Ὂ', 'Ὃ', 'Ὄ', 'Ὅ', 'Ὸ', 'Ό', 'О', 'Θ', 'Ө', 'Ǒ', 'Ǿ', 'Ｏ', 'Ö'],
    'P': ['П', 'Π', 'Ｐ'],
    'Q': ['Ｑ'],
    'R': ['Ř', 'Ŕ', 'Р', 'Ρ', 'Ŗ', 'Ｒ'],
    'S': ['Ş', 'Ŝ', 'Ș', 'Š', 'Ś', 'С', 'Σ', 'Ｓ'],
    'T': ['Ť', 'Ţ', 'Ŧ', 'Ț', 'Т', 'Τ', 'Ｔ'],
    'U': ['Ú', 'Ù', 'Ủ', 'Ũ', 'Ụ', 'Ư', 'Ứ', 'Ừ', 'Ử', 'Ữ', 'Ự', 'Û', 'Ū', 'Ů', 'Ű', 'Ŭ', 'Ų', 'У', 'Ǔ', 'Ǖ', 'Ǘ', 'Ǚ',
          'Ǜ', 'Ｕ', 'Ў', 'Ü'],
    'V': ['В', 'Ｖ'],
    'W': ['Ω', 'Ώ', 'Ŵ', 'Ｗ'],
    'X': ['Χ', 'Ξ', 'Ｘ'],
    'Y': ['Ý', 'Ỳ', 'Ỷ', 'Ỹ', 'Ỵ', 'Ÿ', 'Ῠ', 'Ῡ', 'Ὺ', 'Ύ', 'Ы', 'Й', 'Υ', 'Ϋ', 'Ŷ', 'Ｙ'],
    'Z': ['Ź', 'Ž', 'Ż', 'З', 'Ζ', 'Ｚ'],
    'AE': ['Æ', 'Ǽ'],
    'Ch': ['Ч'],
    'Dj': ['Ђ'],
    'Dz': ['Џ'],
    'Gx': ['Ĝ'],
    'Hx': ['Ĥ'],
    'Ij': ['Ĳ'],
    'Jx': ['Ĵ'],
    'Kh': ['Х'],
    'Lj': ['Љ'],
    'Nj': ['Њ'],
    'Oe': ['Œ'],
    'Ps': ['Ψ'],
    'Sh': ['Ш'],
    'Shch': ['Щ'],
    'Ss': ['ẞ'],
    'Th': ['Þ'],
    'Ts': ['Ц'],
    'Ya': ['Я'],
    'Yu': ['Ю'],
    'Zh': ['Ж'],
    ' ': ["\xC2\xA0", "\xE2\x80\x80", "\xE2\x80\x81", "\xE2\x80\x82", "\xE2\x80\x83", "\xE2\x80\x84", "\xE2\x80\x85",
          "\xE2\x80\x86", "\xE2\x80\x87", "\xE2\x80\x88", "\xE2\x80\x89", "\xE2\x80\x8A", "\xE2\x80\xAF",
          "\xE2\x81\x9F", "\xE3\x80\x80", "\xEF\xBE\xA0"],
}


def name_to_slug(str, slugSplit="-"):
    str = re.sub(r'^\s+|\s+$', '', str)
    for keySlug in asciiChars:
        arrSymbol = asciiChars[keySlug]
        for itemSymbol in arrSymbol:
            str = re.sub(r'' + itemSymbol, keySlug, str)

    str = str.lower();
    str = re.sub(r'[^a-z0-9 -]', '', str)
    str = re.sub(r'\s+', slugSplit, str)
    return re.sub(r'\-+', slugSplit, str)


def name_to_slug_unique(str, slugSplit="-"):
    slug = name_to_slug(str, slugSplit)
    return '{slug}-{millis}-{time}'.format(slug=slug, millis=get_random_string(16), time=datetime.now().timestamp())


def get_random_string(length=32):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def get_random_time_string(length=32):
    return "{t}{s}".format(t=datetime.now().timestamp(), s=get_random_string(length=length))


def write_error(e):
    print('--------------------------------------- Error: ')
    print(e)
    logger.exception(e)


def get_langs_avai_array():
    langs = []
    for item in settings.LANGUAGES:
        langs.append(item[0])
    return langs


def get_lang(request=None):
    try:
        if not request:
            request = get_request()
        lang = request.META.get(CLIENT_LANG_KEY)
        if lang in get_langs_avai_array():
            return lang
        return 'vi'
    except Exception:
        return 'vi'


def setattr_for_instance(instance, dict_attr_value):
    """
    set multi attr of instance object
    :param instance: model
    :param dict_attr_value: dict format: attr column -> value
    :return:
    """
    for attr, val in dict_attr_value.items():
        setattr(instance, attr, val)
    return instance


def get_age(date_of_birth):
    if hasattr(date_of_birth, 'year'):
        age = date.today().year - date_of_birth.year
        return age if age > 0 else 0


def format_date(date):
    return date.strftime("%Y-%m-%d") if date else None


def format_datetime(datetime):
    return datetime.strftime("%Y-%m-%d %H:%M:%S") if datetime else None


def is_worker_profile_full(required_fields):
    for field in required_fields:
        if not field:
           return False
    return True


def get_access_token(request):
    from base.api.exceptions import BadRequestException
    from base.api.messages import MSG_AUTH_TOKEN_INVALID
    try:
        return request.META.get(HTTP_AUTHORIZATION).split(" ")[1]
    except (AttributeError, IndexError):
        raise BadRequestException(message=MSG_AUTH_TOKEN_INVALID[1])


def get_remote_ip(request):
    remote_ip = request.META['REMOTE_ADDR']
    return request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else remote_ip


def datetime_to_milisecond(datetime):
    return int(datetime.timestamp() * 1000)


def gen_md5_hash_uuid(string):
    if not string:
        return
    return str(uuid.uuid3(uuid.NAMESPACE_URL, string))


def get_full_url_path(path):
    if not path:
        return None
    if re.match('^http(s)?://', path) is None:
        return default_storage.url(path)
    return path


def isBase64(data):
    if isinstance(data, six.string_types):
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

    # Try to decode the file. Return validation error if it fails.
    try:
        base64.b64decode(data)
        return True
    except Exception:
        return False


def detach_url_and_base64(gallerys):
    collect_base64 = []
    collect_url = []
    for gallery in gallerys:
        if 'image' not in gallery:
            continue
        if isBase64(gallery['image']):
            collect_base64.append(gallery)
        else:
            collect_url.append(gallery)
    return collect_base64, collect_url


def json_collection_to_obj_data(collection, obj, col_response=[], col_id='id'):
    if not collection:
        return None
    item = collection.get(getattr(obj, col_id))
    if not item:
        return None
    result = {}
    for i in col_response:
        result[i] = getattr(item, i)
    return result


def check_dict_exists_values(dict):
    for key, value in dict.items():
        if value:
            return True
        if type(value) is str and value.strip():
            return True
    return False


def check_slug_from_title(obj_model, title, obj=None):
    slug = name_to_slug(title)
    object_search = obj_model.objects.filter(slug=slug)
    if obj:
        object_search = object_search.exclude(id=obj.id)
    object_search = object_search.first()
    if not object_search:
        return slug
    return name_to_slug_unique(slug)

def format_time_hour_minute(time):
    return time.strftime("%H:%M") if time else None


def get_image_from_url(url):
    if not url:
        return None
    else:
        url = str(url).replace(" ", "%20")
        response = requests.get(url)
        filename, file_extension = os.path.splitext(url)
        if response.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            return File(img_temp, name='image{}'.format(file_extension))

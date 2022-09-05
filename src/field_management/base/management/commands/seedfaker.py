from django.core.management.base import BaseCommand, CommandError
import random
from faker import Faker
from article.models import Article, Category as CategoryArticale, ArticleImage
from entertain.models import Entertain
from culture.models import Culture, Category
from greeting.models import Greeting, Category as CategoryGreeting
from personal.models import Game
from story_book.models import StoryBook, Chapter
import logging
from datetime import datetime, timedelta
from itertools import islice
from base.utils import can_chi
from tuvi.choices import TUOI_CON
from tuvi.models import AgeIntoTheHouse, Tuvi, XuatHanh
from youtube.models import Youtube
from base.choices import SCREENS, TARGET, REGIONS
from django.conf import settings

from base.hashgeo import to_hash_fields

logger = logging.getLogger(__name__)

target = [row[0] for row in TARGET]

regions = [row[0] for row in REGIONS]

CANCHI = can_chi()
canchi = [row[0] for row in CANCHI]
screen_code = [row[0] for row in SCREENS]

TAG = ["Bánh chưng", "Tết", "Thịt lợn", "Cây đào", "Pháo hoa", "Bánh đậu xanh", "Bái đính", "Du xuân", "Sự kiện"]

list_model = ["all", "Article", "Culture", "StoryBook", "Entertain", "Game", "Greeting", "Youtube", "AgeIntoTheHouse",
              "Tuvi", 'XuatHanh']

fake = Faker('en_US')
batch_size = settings.SEED_FAKER_BATCH_SIZE
image_url = [
    'photo_contest/image/1547093690.3678176.jpg',
    'youtube/image/1545707509.8891351.jpg',
    'photo_contest/image/1547093684.0623834.jpg'
]


# create data category culture
def create_data_category():
    objs = (Category(name=fake.text(max_nb_chars=10, ext_word_list=None),
                     screens=random.sample(set(screen_code), random.randint(1, 4))
                     ) for _ in range(10))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Category.objects.bulk_create(batch, batch_size)


# create data culture
def create_data_culture(category, total_record):
    objs = (Culture(category_id=int(random.choice(category)),
                    pickup=random.choice([True, False]),
                    cover_url=random.choice(image_url),
                    tags="|".join(random.sample(set(TAG), random.randint(1, 4))),
                    targets=random.sample(set(target), random.randint(1, 4)),
                    title=fake.text(max_nb_chars=100, ext_word_list=None),
                    content=fake.text(),
                    source=fake.text(max_nb_chars=100, ext_word_list=None),
                    extra_info=fake.text(),
                    address_detail=fake.street_address(),
                    screens=random.sample(set(screen_code), random.randint(1, 4)),
                    status="phát hành",
                    published_at=datetime.now()) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Culture.objects.bulk_create(batch, batch_size)


def gen_article(category):
    latitude = random.uniform(10, 25)
    longitude = random.uniform(100, 110)

    obj = Article(category_id=int(random.choice(category)),
                  pickup=random.choice([True, False]),
                  cover_url=random.choice(image_url),
                  tags="|".join(random.sample(set(TAG), random.randint(1, 4))),
                  targets=random.sample(set(target), random.randint(1, 4)),
                  title=fake.text(max_nb_chars=100, ext_word_list=None),
                  content=fake.text(),
                  source=fake.text(max_nb_chars=100, ext_word_list=None),
                  extra_info=fake.text(),
                  phone_contact=fake.phone_number(),
                  website=fake.url(schemes=None),
                  place_name=fake.text(max_nb_chars=100, ext_word_list=None),
                  address_detail=fake.street_address(),
                  region=random.choice(regions),
                  latitude=latitude,
                  longitude=longitude,
                  date_start=fake.date_time_between(start_date="now", end_date="+20d", tzinfo=None),
                  date_end=fake.date_time_between(start_date="+20d", end_date="+30d", tzinfo=None),
                  time_start=fake.time(pattern="%H:%M:%S", end_datetime=None),
                  time_end=fake.time(pattern="%H:%M:%S", end_datetime=None),
                  status="phát hành",
                  published_at=datetime.now()
                  )

    fields = to_hash_fields(lon=obj.longitude, lat=obj.latitude)
    for attr, value in fields.items():
        setattr(obj, attr, value)

    # do somting with obj
    return obj


# create data article
def create_data_article(category, total_record):
    objs = (gen_article(category) for _ in range(total_record))

    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Article.objects.bulk_create(batch, batch_size)


def create_data_article_image(article, total_record):
    objs = (
        ArticleImage(article_id=int(random.choice(article)),
                     image=random.choice(image_url),
                     ) for _ in range(total_record * 2))

    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        ArticleImage.objects.bulk_create(batch, batch_size)


# create data story book
def create_data_story_book(total_record):
    objs = (
        StoryBook(name=fake.text(max_nb_chars=100, ext_word_list=None),
                  cover_url=random.choice(image_url),
                  status="phát hành",
                  published_at=datetime.now()
                  ) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        StoryBook.objects.bulk_create(batch, batch_size)


# create data chapter
def create_data_chapter(story_book, total_record):
    objs = (
        Chapter(story_book_id=int(random.choice(story_book)),
                title=fake.text(max_nb_chars=100, ext_word_list=None),
                content=fake.text(),
                status="phát hành",
                published_at=datetime.now()
                ) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Chapter.objects.bulk_create(batch, batch_size)


# create data entertain
def create_data_entertain(total_record):
    objs = (
        Entertain(title=fake.text(max_nb_chars=100, ext_word_list=None),
                  content=fake.text(),
                  status="phát hành",
                  published_at=datetime.now()
                  ) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Entertain.objects.bulk_create(batch, batch_size)


# create data game
def create_data_game(total_record):
    objs = (
        Game(name=fake.text(max_nb_chars=100, ext_word_list=None),
             summary=fake.text(max_nb_chars=100, ext_word_list=None),
             content=fake.text(),
             url=fake.url(schemes=None),
             status="phát hành",
             published_at=datetime.now()
             ) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Game.objects.bulk_create(batch, batch_size)


# create data category greeting
def create_data_category_greeting():
    objs = (CategoryGreeting(name=fake.text(max_nb_chars=10, ext_word_list=None)) for _ in range(10))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        CategoryGreeting.objects.bulk_create(batch, batch_size)


# create data greeting
def create_data_greeting(category, total_record):
    objs = (Greeting(category_id=int(random.choice(category)),
                     cover_url="youtube/image/1545707509.8891351.jpg",
                     title=fake.text(max_nb_chars=100, ext_word_list=None),
                     content=fake.text(),
                     status="phát hành",
                     published_at=datetime.now()) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Greeting.objects.bulk_create(batch, batch_size)


# create data youtube
def create_data_youtube(total_record):
    objs = (Youtube(cover_url="youtube/image/1545707509.8891351.jpg",
                    title=fake.text(max_nb_chars=100, ext_word_list=None),
                    link="https://www.youtube.com/watch?v=OQyrcwDbnnI",
                    status="phát hành",
                    published_at=datetime.now()) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Youtube.objects.bulk_create(batch, batch_size)


# create data AgeIntoTheHouse
def create_data_age_into_the_house(total_record):
    objs = (AgeIntoTheHouse(can_chi=random.choice(canchi),
                            age_match=random.choice(canchi),
                            interpretation=fake.text(),
                            status="phát hành",
                            published_at=datetime.now()) for _ in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        AgeIntoTheHouse.objects.bulk_create(batch, batch_size)


# create data DateYinYang
def create_data_xuathanh():
    objs = (XuatHanh(tuoi_con=row[0],
                     content=fake.text(),
                     extra_info=fake.text(),
                     status="phát hành",
                     published_at=datetime.now()
                     ) for row in TUOI_CON)
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        XuatHanh.objects.bulk_create(batch, batch_size)


def gen_tuvi(i, gender, total_record):
    date_start = datetime(year=1950, month=1, day=1)

    x = int(604440 / total_record)
    if x < 24:
        x = 24
    birthday_from = date_start + timedelta(hours=+i * x + 1)
    birthday_to = date_start + timedelta(hours=+i * x + x),

    obj = Tuvi(gender=gender,
               birthday_from=birthday_from,
               birthday_to=birthday_to[0].date(),
               summary=fake.text(max_nb_chars=100, ext_word_list=None),
               content_html=fake.text(),
               status="phát hành",
               published_at=datetime.now())
    return obj


# create data Tuvi
def create_data_tu_vi_male(total_record):
    objs = (gen_tuvi(i, 'Male', total_record) for i in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Tuvi.objects.bulk_create(batch, batch_size)


def create_data_tu_vi_female(total_record):
    objs = (gen_tuvi(i, 'Female', total_record) for i in range(total_record))
    while True:
        batch = list(islice(objs, batch_size))
        if not batch:
            break
        Tuvi.objects.bulk_create(batch, batch_size)


class Command(BaseCommand):
    help = 'Seeder data'

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Model in list {}'.format(list_model))
        parser.add_argument('total_record', type=int, help='Indicates the number of record to be created')

    def handle(self, *args, **options):
        print(datetime.now())
        model = options['model']
        total_record = options['total_record']

        if model not in list_model:
            raise CommandError('Model in list {}'.format(list_model))

        if model == "Culture" or model == "all":
            Culture.objects.all().delete()
            Category.objects.all().delete()
            create_data_category()
            category = Category.objects.values_list('id', flat=True)
            create_data_culture(category, total_record)

        if model == "Article" or model == "all":
            ArticleImage.objects.all().delete()
            Article.objects.all().delete()
            category_article = CategoryArticale.objects.values_list('id', flat=True)
            create_data_article(category_article, total_record)
            articles = Article.objects.values_list('id', flat=True)
            create_data_article_image(articles, total_record)

        if model == "StoryBook" or model == "all":
            StoryBook.objects.all().delete()
            create_data_story_book(total_record)
            story_book = StoryBook.objects.values_list('id', flat=True)
            create_data_chapter(story_book, total_record)

        if model == "Entertain" or model == "all":
            Entertain.objects.all().delete()
            create_data_entertain(total_record)

        if model == "Game" or model == "all":
            Game.objects.all().delete()
            create_data_game(total_record)

        if model == "Greeting" or model == "all":
            Greeting.objects.all().delete()
            CategoryGreeting.objects.all().delete()
            create_data_category_greeting()
            category = CategoryGreeting.objects.values_list('id', flat=True)
            create_data_greeting(category, total_record)

        if model == "Youtube" or model == "all":
            Youtube.objects.all().delete()
            create_data_youtube(total_record)

        if model == "AgeIntoTheHouse" or model == "all":
            AgeIntoTheHouse.objects.all().delete()
            create_data_age_into_the_house(total_record)

        if model == "XuatHanh" or model == "all":
            XuatHanh.objects.all().delete()
            create_data_xuathanh()

        if model == "Tuvi" or model == "all":
            Tuvi.objects.all().delete()
            create_data_tu_vi_female(total_record)
            create_data_tu_vi_male(total_record)

        print(datetime.now())

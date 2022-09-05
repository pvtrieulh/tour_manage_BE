# snippets/urls.py
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.urls import path

urlpatterns = [
    path('', AppTrackingCreateView().as_view(), name='create-new-download'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

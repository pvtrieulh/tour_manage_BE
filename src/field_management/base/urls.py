from .views import choose_province
from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('', views.status, name='status'),
    path('change_city', choose_province),
    # url(r'^post-autocomplete/$', views.PostAutocomplete.as_view(), name='post-autocomplete',),
]

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('get_link', GetLinks.as_view(), name='get_link'),
    path('test', Test.as_view(), name='test'),
]

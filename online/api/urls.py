from django.urls import path
from .views import *

urlpatterns = [
    path('get_token/<str:code>', get_access_token, name='get_access_token'),
]